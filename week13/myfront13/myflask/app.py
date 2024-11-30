from flask import Flask, Blueprint, render_template, request  # Flask 및 관련 모듈
import urllib.request  # HTTP 요청을 위해
import json  # JSON 데이터를 다루기 위해


endpoint = 'http://15.164.102.226:8080/pastebin/api'

app = Flask(__name__)
bp = Blueprint('mybp', __name__, 
               static_folder='static',
               static_url_path='/pastebin/static',
               template_folder='templates',
               url_prefix='/pastebin')

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
    with urllib.request.urlopen(req) as f:
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
    with urllib.request.urlopen(req) as f:
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
            headers = {'Accept': 'application/json'}
            method = 'POST'
            req = urllib.request.Request(url=url,
                                        data=data,
                                        headers=headers,
                                        method=method)
            urllib.request.urlopen(req)
        return render_template('createuser.html')

app.register_blueprint(bp)