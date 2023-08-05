import datetime

from flask import g, request, render_template, jsonify
from flask_cors import cross_origin
from uuid import uuid4

from alerta.app import app, db
from alerta.app.switch import Switch
from alerta.app.auth import permission, is_in_scope
from alerta.app.utils import absolute_url, jsonp, parse_fields, process_alert, process_status, add_remote_ip
from alerta.app.metrics import Timer
from alerta.app.alert import Alert
from alerta.app.exceptions import RejectException, RateLimit, BlackoutPeriod
from alerta.app.heartbeat import Heartbeat
from alerta.plugins import Plugins

LOG = app.logger

plugins = Plugins()

# Set-up metrics
gets_timer = Timer('alerts', 'queries', 'Alert queries', 'Total time to process number of alert queries')
receive_timer = Timer('alerts', 'received', 'Received alerts', 'Total time to process number of received alerts')
delete_timer = Timer('alerts', 'deleted', 'Deleted alerts', 'Total time to process number of deleted alerts')
status_timer = Timer('alerts', 'status', 'Alert status change', 'Total time and number of alerts with status changed')
tag_timer = Timer('alerts', 'tagged', 'Tagging alerts', 'Total time to tag number of alerts')
attrs_timer = Timer('alerts', 'attributes', 'Alert attributes change', 'Total time and number of alerts with attributes changed')
untag_timer = Timer('alerts', 'untagged', 'Removing tags from alerts', 'Total time to un-tag number of alerts')


@app.route('/_', methods=['OPTIONS', 'PUT', 'POST', 'DELETE', 'GET'])
@cross_origin()
@jsonp
def test():

    return jsonify(
        status="ok",
        method=request.method,
        json=request.json,
        data=request.data.decode('utf-8'),
        args=request.args,
        app_root=app.root_path,
    )


@app.route('/')
def index():

    rules = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint not in ['test', 'static']:
            rules.append(rule)
    return render_template('index.html', base_url=absolute_url(), rules=rules)


@app.route('/alerts', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_alerts():

    gets_started = gets_timer.start_timer()
    try:
        query, fields, sort, _, page, limit, query_time = parse_fields(request.args)
    except Exception as e:
        gets_timer.stop_timer(gets_started)
        return jsonify(status="error", message=str(e)), 400

    try:
        severity_count = db.get_counts(query=query, fields={"severity": 1}, group="severity")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    try:
        status_count = db.get_counts(query=query, fields={"status": 1}, group="status")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if limit < 1:
        return jsonify(status="error", message="page 'limit' of %s is not valid" % limit), 416

    total = sum(severity_count.values())
    pages = ((total - 1) // limit) + 1

    if total and page > pages or page < 0:
        return jsonify(status="error", message="page out of range: 1-%s" % pages), 416

    if 'history' not in fields:
        fields['history'] = {'$slice': app.config['HISTORY_LIMIT']}

    try:
        alerts = db.get_alerts(query=query, fields=fields, sort=sort, page=page, limit=limit)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    alert_response = list()
    if len(alerts) > 0:

        last_time = None

        for alert in alerts:
            body = alert.get_body()
            body['href'] = absolute_url('/alert/' + alert.id)

            if not last_time:
                last_time = body['lastReceiveTime']
            elif body['lastReceiveTime'] > last_time:
                last_time = body['lastReceiveTime']

            alert_response.append(body)

        gets_timer.stop_timer(gets_started)
        return jsonify(
            status="ok",
            total=total,
            page=page,
            pageSize=limit,
            pages=pages,
            more=page < pages,
            alerts=alert_response,
            severityCounts=severity_count,
            statusCounts=status_count,
            lastTime=last_time,
            autoRefresh=Switch.get('auto-refresh-allow').is_on(),
        )
    else:
        gets_timer.stop_timer(gets_started)
        return jsonify(
            status="ok",
            message="not found",
            total=total,
            page=page,
            pageSize=limit,
            pages=pages,
            more=False,
            alerts=[],
            severityCounts=severity_count,
            statusCounts=status_count,
            lastTime=query_time,
            autoRefresh=Switch.get('auto-refresh-allow').is_on()
        )


@app.route('/alerts/history', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_history():

    try:
        query, _, _, _, _, limit, query_time = parse_fields(request.args)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400

    try:
        history = db.get_history(query=query, limit=limit)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    for alert in history:
        alert['href'] = absolute_url('/alert/' + alert['id'])

    if len(history) > 0:
        return jsonify(
            status="ok",
            history=history,
            lastTime=history[-1]['updateTime']
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            history=[],
            lastTIme=query_time
        )


@app.route('/alert', methods=['OPTIONS', 'POST'])
@cross_origin()
@permission('write:alerts')
@jsonp
def receive_alert():

    if not Switch.get('sender-api-allow').is_on():
        return jsonify(status="error", message="API not accepting alerts. Try again later."), 503

    recv_started = receive_timer.start_timer()
    try:
        incomingAlert = Alert.parse_alert(request.data)
    except ValueError as e:
        receive_timer.stop_timer(recv_started)
        return jsonify(status="error", message=str(e)), 400

    if g.get('customer', None):
        incomingAlert.customer = g.get('customer')

    add_remote_ip(request, incomingAlert)

    try:
        alert = process_alert(incomingAlert)
    except RejectException as e:
        receive_timer.stop_timer(recv_started)
        return jsonify(status="error", message=str(e)), 403
    except RateLimit as e:
        receive_timer.stop_timer(recv_started)
        return jsonify(status="error", id=incomingAlert.id, message=str(e)), 429
    except BlackoutPeriod as e:
        receive_timer.stop_timer(recv_started)
        return jsonify(status="ok", id=incomingAlert.id, message=str(e)), 202
    except Exception as e:
        receive_timer.stop_timer(recv_started)
        return jsonify(status="error", message=str(e)), 500

    receive_timer.stop_timer(recv_started)

    if alert:
        body = alert.get_body()
        body['href'] = absolute_url('/alert/' + alert.id)
        return jsonify(status="ok", id=alert.id, alert=body), 201, {'Location': body['href']}
    else:
        return jsonify(status="error", message="insert or update of received alert failed"), 500


@app.route('/alert/<id>', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_alert(id):

    customer = g.get('customer', None)
    try:
        alert = db.get_alert(id=id, customer=customer)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if alert:
        body = alert.get_body()
        body['href'] = absolute_url('/alert/' + alert.id)
        return jsonify(status="ok", total=1, alert=body)
    else:
        return jsonify(status="error", message="not found", total=0, alert=None), 404


@app.route('/alert/<id>/status', methods=['OPTIONS', 'PUT', 'POST'])  # POST is deprecated
@cross_origin()
@permission('write:alerts')
@jsonp
def set_status(id):

    status_started = status_timer.start_timer()
    customer = g.get('customer', None)
    try:
        alert = db.get_alert(id=id, customer=customer)
    except Exception as e:
        status_timer.stop_timer(status_started)
        return jsonify(status="error", message=str(e)), 500

    if not alert:
        status_timer.stop_timer(status_started)
        return jsonify(status="error", message="not found", total=0, alert=None), 404

    status = request.json.get('status', None)
    text = request.json.get('text', None) or ''

    if not status:
        status_timer.stop_timer(status_started)
        return jsonify(status="error", message="must supply 'status' as parameter"), 400

    try:
        alert, status, text = process_status(alert, status, text)
    except RejectException as e:
        status_timer.stop_timer(status_started)
        return jsonify(status="error", message=str(e)), 403
    except Exception as e:
        status_timer.stop_timer(status_started)
        return jsonify(status="error", message=str(e)), 500

    try:
        success = db.set_status(id, status, text)
    except Exception as e:
        status_timer.stop_timer(status_started)
        return jsonify(status="error", message=str(e)), 500

    if success:
        status_timer.stop_timer(status_started)
        return jsonify(status="ok")
    else:
        status_timer.stop_timer(status_started)
        return jsonify(status="error", message="not found"), 404


@app.route('/alert/<id>/tag', methods=['OPTIONS', 'PUT', 'POST'])  # POST is deprecated
@cross_origin()
@permission('write:alerts')
@jsonp
def tag_alert(id):

    tag_started = tag_timer.start_timer()
    customer = g.get('customer', None)
    try:
        alert = db.get_alert(id=id, customer=customer)
    except Exception as e:
        tag_timer.stop_timer(tag_started)
        return jsonify(status="error", message=str(e)), 500

    if not alert:
        tag_timer.stop_timer(tag_started)
        return jsonify(status="error", message="not found", total=0, alert=None), 404

    data = request.json

    if data and 'tags' in data:
        try:
            response = db.tag_alert(id, data['tags'])
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500
    else:
        tag_timer.stop_timer(tag_started)
        return jsonify(status="error", message="must supply 'tags' as list parameter"), 400

    tag_timer.stop_timer(tag_started)
    if response:
        return jsonify(status="ok")
    else:
        return jsonify(status="error", message="not found"), 404


@app.route('/alert/<id>/untag', methods=['OPTIONS', 'PUT', 'POST'])  # POST is deprecated
@cross_origin()
@permission('write:alerts')
@jsonp
def untag_alert(id):

    untag_started = untag_timer.start_timer()
    customer = g.get('customer', None)
    try:
        alert = db.get_alert(id=id, customer=customer)
    except Exception as e:
        untag_timer.stop_timer(untag_started)
        return jsonify(status="error", message=str(e)), 500

    if not alert:
        untag_timer.stop_timer(untag_started)
        return jsonify(status="error", message="not found", total=0, alert=None), 404

    data = request.json

    if data and 'tags' in data:
        try:
            response = db.untag_alert(id, data['tags'])
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500
    else:
        untag_timer.stop_timer(untag_started)
        return jsonify(status="error", message="must supply 'tags' as list parameter"), 400

    untag_timer.stop_timer(untag_started)
    if response:
        return jsonify(status="ok")
    else:
        return jsonify(status="error", message="not found"), 404


@app.route('/alert/<id>/attributes', methods=['OPTIONS', 'PUT'])
@cross_origin()
@permission('write:alerts')
@jsonp
def update_attributes(id):

    attrs_started = attrs_timer.start_timer()
    customer = g.get('customer', None)
    try:
        alert = db.get_alert(id=id, customer=customer)
    except Exception as e:
        attrs_timer.stop_timer(attrs_started)
        return jsonify(status="error", message=str(e)), 500

    if not alert:
        attrs_timer.stop_timer(attrs_started)
        return jsonify(status="error", message="not found", total=0, alert=None), 404

    attributes = request.json.get('attributes', None)

    if not attributes:
        attrs_timer.stop_timer(attrs_started)
        return jsonify(status="error", message="must supply 'attributes' as parameter"), 400

    try:
        success = db.update_attributes(id, attributes)
    except Exception as e:
        attrs_timer.stop_timer(attrs_started)
        return jsonify(status="error", message=str(e)), 500

    if success:
        attrs_timer.stop_timer(attrs_started)
        return jsonify(status="ok")
    else:
        attrs_timer.stop_timer(attrs_started)
        return jsonify(status="error", message="not found"), 404


@app.route('/alert/<id>', methods=['OPTIONS', 'DELETE', 'POST'])
@cross_origin()
@permission('admin:alerts')
@jsonp
def delete_alert(id):

    if (request.method == 'DELETE' or
            (request.method == 'POST' and '_method' in request.json and request.json['_method'] == 'delete')):
        started = delete_timer.start_timer()
        try:
            response = db.delete_alert(id)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500
        delete_timer.stop_timer(started)

        if response:
            return jsonify(status="ok")
        else:
            return jsonify(status="error", message="not found"), 404


# Return severity and status counts
@app.route('/alerts/count', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_counts():

    try:
        query, _, _, _, _, _, _ = parse_fields(request.args)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400

    try:
        severity_count = db.get_counts(query=query, fields={"severity": 1}, group="severity")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    try:
        status_count = db.get_counts(query=query, fields={"status": 1}, group="status")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if sum(severity_count.values()):
        return jsonify(
            status="ok",
            total=sum(severity_count.values()),
            severityCounts=severity_count,
            statusCounts=status_count
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            severityCounts=severity_count,
            statusCounts=status_count
        )


@app.route('/alerts/top10', methods=['OPTIONS', 'GET'])
@app.route('/alerts/top10/count', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_top10_count():

    try:
        query, _, _, group, _, _, _ = parse_fields(request.args)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400

    try:
        top10 = db.get_topn_count(query=query, group=group, limit=10)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    for item in top10:
        for resource in item['resources']:
            resource['href'] = absolute_url('/alert/' + resource['id'])

    if top10:
        return jsonify(
            status="ok",
            total=len(top10),
            top10=top10
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            top10=[],
        )


@app.route('/alerts/top10/flapping', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_top10_flapping():

    try:
        query, _, _, group, _, _, _ = parse_fields(request.args)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400

    try:
        top10 = db.get_topn_flapping(query=query, group=group, limit=10)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    for item in top10:
        for resource in item['resources']:
            resource['href'] = absolute_url('/alert/' + resource['id'])

    if top10:
        return jsonify(
            status="ok",
            total=len(top10),
            top10=top10
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            top10=[],
        )


@app.route('/environments', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_environments():

    try:
        query, _, _, _, _, limit, _ = parse_fields(request.args)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400

    try:
        environments = db.get_environments(query=query, limit=limit)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if environments:
        return jsonify(
            status="ok",
            total=len(environments),
            environments=environments
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            environments=[],
        )


@app.route('/services', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:alerts')
@jsonp
def get_services():

    try:
        query, _, _, _, _, limit, _ = parse_fields(request.args)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400

    try:
        services = db.get_services(query=query, limit=limit)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if services:
        return jsonify(
            status="ok",
            total=len(services),
            services=services
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            services=[],
        )


@app.route('/blackouts', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:blackouts')
@jsonp
def get_blackouts():

    try:
        blackouts = db.get_blackouts()
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if len(blackouts):
        return jsonify(
            status="ok",
            total=len(blackouts),
            blackouts=blackouts,
            time=datetime.datetime.utcnow()
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            blackouts=[],
            time=datetime.datetime.utcnow()
        )


@app.route('/blackout', methods=['OPTIONS', 'POST'])
@cross_origin()
@permission('write:blackouts')
@jsonp
def create_blackout():

    environment = request.json.get('environment', None)
    if not environment:
        return jsonify(status="error", message="Must supply non-empty 'environment' for blackouts."), 400

    resource = request.json.get("resource", None)
    service = request.json.get("service", None)
    event = request.json.get("event", None)
    group = request.json.get("group", None)
    tags = request.json.get("tags", None)
    customer = request.json.get("customer", None)
    start_time = request.json.get("startTime", None)
    end_time = request.json.get("endTime", None)
    duration = request.json.get("duration", None)

    if start_time:
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    if end_time:
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')

    try:
        blackout = db.create_blackout(environment, resource, service, event, group, tags, customer, start_time, end_time, duration)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    return jsonify(status="ok", id=blackout['id'], blackout=blackout), 201, {'Location': absolute_url('/blackout/' + blackout['id'])}


@app.route('/blackout/<path:blackout>', methods=['OPTIONS', 'DELETE', 'POST'])
@cross_origin()
@permission('write:blackouts')
@jsonp
def delete_blackout(blackout):

    if request.method == 'DELETE' or (request.method == 'POST' and request.json['_method'] == 'delete'):
        try:
            response = db.delete_blackout(blackout)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

        if response:
            return jsonify(status="ok")
        else:
            return jsonify(status="error", message="not found"), 404


@app.route('/heartbeats', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:heartbeats')
@jsonp
def get_heartbeats():

    customer = g.get('customer', None)
    if customer:
        query = {'customer': customer}
    else:
        query = {}

    try:
        heartbeats = db.get_heartbeats(query)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    hb_list = list()
    for hb in heartbeats:
        body = hb.get_body()
        body['href'] = absolute_url('/heartbeat/' + hb.id)
        hb_list.append(body)

    if hb_list:
        return jsonify(
            status="ok",
            total=len(heartbeats),
            heartbeats=hb_list,
            time=datetime.datetime.utcnow()
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            heartbeats=hb_list,
            time=datetime.datetime.utcnow()
        )


@app.route('/heartbeat', methods=['OPTIONS', 'POST'])
@cross_origin()
@permission('write:heartbeats')
@jsonp
def create_heartbeat():

    try:
        heartbeat = Heartbeat.parse_heartbeat(request.data)
    except ValueError as e:
        return jsonify(status="error", message=str(e)), 400

    if g.get('customer', None):
        heartbeat.customer = g.get('customer')

    try:
        heartbeat = db.save_heartbeat(heartbeat)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    body = heartbeat.get_body()
    body['href'] = absolute_url('/heartbeat/' + heartbeat.id)
    return jsonify(status="ok", id=heartbeat.id, heartbeat=body), 201, {'Location': body['href']}


@app.route('/heartbeat/<id>', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:heartbeats')
@jsonp
def get_heartbeat(id):

    customer = g.get('customer', None)

    try:
        heartbeat = db.get_heartbeat(id=id, customer=customer)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if heartbeat:
        body = heartbeat.get_body()
        body['href'] = absolute_url('/hearbeat/' + heartbeat.id)
        return jsonify(status="ok", total=1, heartbeat=body)
    else:
        return jsonify(status="error", message="not found", total=0, heartbeat=None), 404


@app.route('/heartbeat/<id>', methods=['OPTIONS', 'DELETE', 'POST'])
@cross_origin()
@permission('admin:heartbeats')
@jsonp
def delete_heartbeat(id):

    if request.method == 'DELETE' or (request.method == 'POST' and request.json['_method'] == 'delete'):
        try:
            response = db.delete_heartbeat(id)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

        if response:
            return jsonify(status="ok")
        else:
            return jsonify(status="error", message="not found"), 404


@app.route('/users', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('admin:users')
@jsonp
def get_users():

    name = request.args.get("name")
    login = request.args.get("login")

    if name:
        query = {'name': name}
    elif login:
        query = {'login': login}
    else:
        query = {}

    try:
        users = db.get_users(query)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if len(users):
        return jsonify(
            status="ok",
            total=len(users),
            users=users,
            domains=app.config['ALLOWED_EMAIL_DOMAINS'],
            orgs=app.config['ALLOWED_GITHUB_ORGS'],
            groups=app.config['ALLOWED_GITLAB_GROUPS'],
            roles=app.config['ALLOWED_KEYCLOAK_ROLES'],
            time=datetime.datetime.utcnow()
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            users=[],
            domains=app.config['ALLOWED_EMAIL_DOMAINS'],
            orgs=app.config['ALLOWED_GITHUB_ORGS'],
            time=datetime.datetime.utcnow()
        )


@app.route('/user', methods=['OPTIONS', 'POST'])
@cross_origin()
@permission('admin:users')
@jsonp
def create_user():

    if request.json and 'name' in request.json:
        name = request.json["name"]
        login = request.json["login"]
        password = request.json["password"]
        provider = request.json.get("provider", "basic")
        role = request.json.get("role", "user")
        text = request.json.get("text", "")
        email_verified = request.json.get("email_verified", False)
    else:
        return jsonify(status="error", message="Must supply user 'name', 'login' and 'password' as parameters"), 400

    try:
        user = db.create_user(name, login, password, provider, role, text, email_verified)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if user:
        return jsonify(status="ok", id=user['id'], user=user), 201, {'Location': absolute_url('/user/' + user['id'])}
    else:
        return jsonify(status="error", message="User with login '%s' already exists" % login), 409


@app.route('/user/<user>', methods=['OPTIONS', 'PUT'])
@cross_origin()
@permission('admin:users')
@jsonp
def update_user(user):
   
    if request.json:
        name = request.json.get('name', None)
        login = request.json.get('login', None)
        password = request.json.get('password', None)
        provider = request.json.get('provider', None)
        role = request.json.get('role', None)
        text = request.json.get('text', None)
        email_verified = request.json.get('email_verified', None)
    else:
        return jsonify(status="error", message="Nothing to update, request was empty"), 400

    if password and provider!='basic':
        return jsonify(status="error", message="Can only change the password for Basic Auth users."), 400

    try:
        user = db.update_user(user, name, login, password, provider, role, text, email_verified)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500
    
    if user:
        return jsonify(status="ok")
    else:
        return jsonify(status="error", message="not found"), 404


@app.route('/user/<user>', methods=['OPTIONS', 'DELETE', 'POST'])
@cross_origin()
@permission('admin:users')
@jsonp
def delete_user(user):

    if request.method == 'DELETE' or (request.method == 'POST' and request.json['_method'] == 'delete'):
        try:
            response = db.delete_user(user)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

        if response:
            return jsonify(status="ok")
        else:
            return jsonify(status="error", message="not found"), 404


@app.route('/perms', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:perms')
@jsonp
def get_perms():

    try:
        perms = db.get_perms()
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if perms:
        return jsonify(
            status="ok",
            total=len(perms),
            permissions=perms,
            time=datetime.datetime.utcnow()
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            permissions=[],
            time=datetime.datetime.utcnow()
        )


@app.route('/perm', methods=['OPTIONS', 'POST'])
@cross_origin()
@permission('admin:perms')
@jsonp
def create_perm():

    if request.json and 'scopes' in request.json and 'match' in request.json:
        scopes = request.json["scopes"]
        match = request.json["match"]

        for s in scopes:
            if not is_in_scope(s):
                return jsonify(status="error", message="Requested scope %s is beyond existing scopes: %s." % (s, ','.join(g.scopes))), 403

        try:
            perm = db.create_perm(scopes, match)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500
    else:
        return jsonify(status="error", message="Must supply user 'scope' and 'match' as parameters"), 400

    if perm:
        return jsonify(status="ok", id=perm['id'], permission=perm), 201, {'Location': absolute_url('/scope/' + perm['id'])}
    else:
        return jsonify(status="error", message="Permissions lookup for this match already exists"), 409


@app.route('/perm/<perm>', methods=['OPTIONS', 'DELETE', 'POST'])
@cross_origin()
@permission('admin:perms')
@jsonp
def delete_perm(perm):

    if request.method == 'DELETE' or (request.method == 'POST' and request.json['_method'] == 'delete'):
        try:
            response = db.delete_perm(perm)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

        if response:
            return jsonify(status="ok")
        else:
            return jsonify(status="error", message="not found"), 404


@app.route('/customers', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('admin:customers')
@jsonp
def get_customers():

    try:
        customers = db.get_customers()
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    if len(customers):
        return jsonify(
            status="ok",
            total=len(customers),
            customers=customers,
            time=datetime.datetime.utcnow()
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            customers=[],
            time=datetime.datetime.utcnow()
        )


@app.route('/customer', methods=['OPTIONS', 'POST'])
@cross_origin()
@permission('admin:customers')
@jsonp
def create_customer():

    if request.json and 'customer' in request.json and 'match' in request.json:
        customer = request.json["customer"]
        match = request.json["match"]
        try:
            customer = db.create_customer(customer, match)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500
    else:
        return jsonify(status="error", message="Must supply user 'customer' and 'match' as parameters"), 400

    if customer:
        return jsonify(status="ok", id=customer['id'], customer=customer), 201, {'Location': absolute_url('/customer/' + customer['id'])}
    else:
        return jsonify(status="error", message="Customer lookup for this match already exists"), 409


@app.route('/customer/<customer>', methods=['OPTIONS', 'DELETE', 'POST'])
@cross_origin()
@permission('admin:customers')
@jsonp
def delete_customer(customer):

    if request.method == 'DELETE' or (request.method == 'POST' and request.json['_method'] == 'delete'):
        try:
            response = db.delete_customer(customer)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

        if response:
            return jsonify(status="ok")
        else:
            return jsonify(status="error", message="not found"), 404


@app.route('/keys', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:keys')
@jsonp
def get_keys():

    if 'admin' in g.scopes or 'admin:keys' in g.scopes:
        try:
            keys = db.get_keys()
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500
    else:
        user = g.get('user')
        try:
            keys = db.get_user_keys(user)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    if keys:
        return jsonify(
            status="ok",
            total=len(keys),
            keys=keys,
            time=datetime.datetime.utcnow()
        )
    else:
        return jsonify(
            status="ok",
            message="not found",
            total=0,
            keys=[],
            time=datetime.datetime.utcnow()
        )


@app.route('/key', methods=['OPTIONS', 'POST'])
@cross_origin()
@permission('write:keys')
@jsonp
def create_key():

    if 'admin' in g.scopes or 'admin:keys' in g.scopes:
        try:
            user = request.json.get('user', g.user)
            customer = request.json.get('customer', None)
        except AttributeError:
            return jsonify(status="error", message="Must supply 'user' as parameter"), 400
    else:
        try:
            user = g.user
            customer = g.get('customer', None)
        except AttributeError:
            return jsonify(status="error", message="Must supply API Key or Bearer Token when creating new API key"), 400

    scopes = request.json.get("scopes", [])
    for scope in scopes:
        if not is_in_scope(scope):
            return jsonify(status="error", message="Requested scope %s is beyond existing scopes: %s." % (scope, ','.join(g.scopes))), 403

    type = request.json.get("type", None)
    if type and type not in ['read-only', 'read-write']:
        return jsonify(status="error", message="API key 'type' must be 'read-only' or 'read-write'"), 400

    text = request.json.get("text", "API Key for %s" % user)
    try:
        key = db.create_key(user, scopes=scopes, type=type, customer=customer, text=text)
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    return jsonify(status="ok", key=key['key'], data=key), 201, {'Location': absolute_url('/key/' + key['key'])}


@app.route('/key/<path:key>', methods=['OPTIONS', 'DELETE', 'POST'])
@cross_origin()
@permission('admin:keys')
@jsonp
def delete_key(key):

    query = {"key": key}
    if not db.get_keys(query):
        return jsonify(status="error", message="not found"), 404

    if request.method == 'DELETE' or (request.method == 'POST' and request.json['_method'] == 'delete'):
        try:
            response = db.delete_key(key)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

        if response:
            return jsonify(status="ok")
        else:
            return jsonify(status="error", message="not found"), 404
