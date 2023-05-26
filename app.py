from flask import Flask, render_template, request
import requests
from requests.auth import HTTPDigestAuth

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ext_sip = request.form.get("ext_sip")
        ip_address = request.form.get('ip_address')
        cam_user = request.form.get('cam_user')
        cam_pass = request.form.get('cam_pass')
        caller_id = get_callerID(ip_address, cam_user, cam_pass, ext_sip)
        return render_template('result.html', caller_id=caller_id, ip_address=ip_address, cam_user=cam_user, cam_pass=cam_pass)
    return render_template('index.html')

@app.route('/terminate_call', methods=['POST'])
def terminate_call():
    ip_address = request.form.get('ip_address')
    cam_user = request.form.get('cam_user')
    cam_pass = request.form.get('cam_pass')
    call_id = request.form.get('call_id')
    term_call_server(ip_address, cam_user, cam_pass, call_id)
    return "Call terminated successfully!"

@app.route('/call_status', methods=['POST'])
def call_status():
    ip_address = request.form.get('ip_address')
    cam_user = request.form.get('cam_user')
    cam_pass = request.form.get('cam_pass')
    call_id = request.form.get('call_id')
    response = get_call_status(ip_address, cam_user, cam_pass, call_id)
    return response

def get_callerID(ip_address, cam_user, cam_pass, ext_sip):
    auth = HTTPDigestAuth(cam_user, cam_pass)
    url = f"http://{ip_address}/vapix/call"
    payload = {
        "axcall:Call": {
            "To": ext_sip,
            "SIPAccountId": "sip_account_1"
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, auth=auth, headers=headers, json=payload)
    response.raise_for_status()
    json_data = response.json()
    call_id = json_data["CallId"]
    return call_id

def term_call_server(ip_address, cam_user, cam_pass, call_id):
    auth = HTTPDigestAuth(cam_user, cam_pass)
    url = f"http://{ip_address}/vapix/call"
    payload = {
        "axcall:TerminateCall": {
            "CallId": call_id
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, auth=auth, headers=headers, json=payload)
    response.raise_for_status()

def get_call_status(ip_address, cam_user, cam_pass, call_id):
    auth = HTTPDigestAuth(cam_user, cam_pass)
    url = f"http://{ip_address}/vapix/call"
    payload = {
        "axcall:GetCallStatus": {
            "CallId": call_id
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, auth=auth, headers=headers, json=payload)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    app.run(host='0.0.0.0')
