from flask import Flask, request, jsonify, render_template, abort
import subprocess
import os

from logging import basicConfig, getLogger, DEBUG
basicConfig(level=DEBUG)
logger = getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/me/api/post', methods=['POST'])
def api_post():
    me_id = os.environ['me_id']
    me_pass = os.environ['me_pass']

    if not request.headers['Content-Type'] == 'application/json':
        ret_data = {
            'status': 'FAIL',
            'reason': 'Content-Type is invalid.'
        }
        return jsonify(ret_data)
    
    post_data = request.json
    post_id = post_data['id']
    post_pass = post_data['pass']

    if post_id == me_id and post_pass == me_pass:
        pass
    else:
        ret_data = {
            'status': 'FAIL',
            'reason': 'Auth failed.'
        } 
        return jsonify(ret_data)

    try:
        subprocess.check_call(['python3.6', './twibot.py'])
        ret_data = {
            'status': 'SUCCESS'
        }
        return jsonify(ret_data)
    except subprocess.CalledProcessError as e:
        logger.debug('Error: ' + str(e.output))
        ret_data = {
            'status': 'FAIL',
            'reason': 'DB Error:' + str(e.output)
        }
        return jsonify(ret_data)
