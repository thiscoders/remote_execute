# -*- coding: utf-8 -*-

import os
import json
import subprocess
from flask import Flask, request

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/login', methods=['GET', 'POST'])
def login_app():
    return 'login...\r\n'


@app.route('/logout', methods=['GET', 'POST'])
def logout_app():
    return 'logout...\r\n'


def real_execute(func_name=False, func_param=False):
    base_dir = os.path.split(os.path.abspath(__file__))[0]
    shell_path = base_dir + '/shell/' + func_name + '.sh'
    is_file = os.path.isfile(shell_path)
    if not is_file:
        return 'Your intention does not exist!\r\n'
    is_exec = os.access(shell_path, os.X_OK)
    if not is_exec:
        return 'Your intention cannot be executed!\r\n'
    res = subprocess.run(args=[shell_path, func_param or ''], capture_output=True)
    return str(res.stdout, encoding='utf-8') + '\r\n'


@app.route('/execute', methods=['GET', 'POST'])
def remote_execute():
    req_method = request.method
    req_user_agent = request.user_agent.string
    # 'Mozilla/5.0 (Windows NT; Windows NT 10.0; zh-CN) WindowsPowerShell/5.1.19041.1'
    if 'curl' not in req_user_agent and 'PowerShell' not in req_user_agent:
        return "Use the curl command on the terminal.<br/><br/>curl 'http://127.0.0.1:5000/execute?func_name=hostname'"
    if req_method == 'POST':
        req_data = request.get_data()
        req_json = json.loads(req_data)
        func_name = req_json.get('func_name', False)
        if not func_name:
            return 'Please explain your intention!(by post)\r\n'
        func_param = req_json.get('func_param', False)
        return real_execute(func_name=func_name, func_param=func_param)
    elif req_method == 'GET':
        req_args = request.args
        func_name = req_args.get('func_name', False)
        if not func_name:
            return 'Please explain your intention!(by get)\r\n'
        func_param = req_args.get('func_param', False)
        return real_execute(func_name=func_name, func_param=func_param)
    else:
        return 'Unsupported access protocol!\r\n'


@app.route('/')
def hello():
    return 'hello\r\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
