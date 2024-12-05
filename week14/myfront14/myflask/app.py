from flask import Flask, Blueprint, render_template, request
import urllib.request
import json
import ssl


endpoint = 'https://15.164.102.226:8443/pastebin/api'
# CERT = '/media/pastebinCA.crt'

app = Flask(__name__)
bp = Blueprint('mybp', __name__, 
               static_folder='static',
               static_url_path='/static',
               template_folder='templates',
               url_prefix='/pastebin')
# context = ssl.create_default_context()
# context.load_verify_locations(CERT)
context = ssl._create_unverified_context()

@bp.route(f'/', methods=['GET'])
@bp.route(f'/index.html', methods=['GET'])
def get_index():
    count_users = 0
    url = f'{endpoint}/users'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    
    with urllib.request.urlopen(req, context=context) as f:
        data = json.loads(f.read())
        count_users = len(data)

    count_pastes = 0
    url = f'{endpoint}/pastes'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    with urllib.request.urlopen(req, context=context) as f:
        data = json.loads(f.read())
        count_pastes = len(data)

    return render_template('index.html', 
                           count_users=count_users,
                           count_pastes=count_pastes)

@bp.route(f'/createuser', methods=['GET', 'POST'])
def create_user():
        if request.method == 'POST':
            url = f'{endpoint}/users'

            data = {'username': request.form['username'],
                    'password': request.form['password']}
            data = json.dumps(data).encode('utf-8')

            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            method = 'POST'
            req = urllib.request.Request(url=url,
                                        data=data,
                                        headers=headers,
                                        method=method)
            urllib.request.urlopen(req, context=context)
        return render_template('createuser.html')

@bp.route(f'/createpaste', methods=['GET', 'POST'])
def create_paste():
        if request.method == 'POST':
            url = f'{endpoint}/users/{request.form['username']}/pastes?password={request.form['password']}'

            data = {'title': request.form['title'],
                    'content': request.form['content']}
            data = json.dumps(data).encode('utf-8')

            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            method = 'POST'
            req = urllib.request.Request(url=url,
                                        data=data,
                                        headers=headers,
                                        method=method)
            urllib.request.urlopen(req, context=context)
        return render_template('createpaste.html')

@bp.route(f'/users/<user_name>/pastes', methods=['GET'])
def get_user_pastes(user_name):
    count_pastes = 0
    url = f'{endpoint}/users/{user_name}/pastes'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    with urllib.request.urlopen(req, context=context) as f:
        data = json.loads(f.read())
        count_pastes = len(data)

    return render_template('userpaste.html',
                           count_pastes=count_pastes,
                           user_name=user_name)

app.register_blueprint(bp)