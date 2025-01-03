from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import requests
import json
from vikalp_base_api import viaklp_bp
from clustering import cluster_statuses

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DOMAIN'] = "https://vikalp.social"

#fetch user account data
@app.get("/api/v1/accounts/<id>")
@cross_origin()

def get_profile(id):
    try:
        res1 = requests.get(f"https://{request.args['instance']}/api/v1/accounts/{id}")
        account = json.loads(res1.text)
        res2 = requests.get(f"https://{request.args['instance']}/api/v1/accounts/{id}/statuses")
        statuses = json.loads(res2.text)
    except requests.exceptions.ConnectionError as e:
        return {
                'error': "Can't Establish a connection to the server",
                'status': 502,
                'statusText': "Bad Gateway",
            }
    else:
        if res1.status_code >= 400:
            return ({
            'error': account['error'],
            'status': res1.status_code,
            'statusText': res1.reason,
        }, res1.status_code)
        elif res2.status_code >= 400:
            return ({
            'error': statuses['error'],
            'status': res2.status_code,
            'statusText': res2.reason,
        }, res2.status_code)
        else:
            data = {
                'account': account,
                'statuses': {
                    'cluster': cluster_statuses(statuses=statuses, url ="http://localhost:8080/service/cluster")
                }
            }
            return data
        
app.register_blueprint(viaklp_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
