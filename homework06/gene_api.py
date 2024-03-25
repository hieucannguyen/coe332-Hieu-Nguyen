from flask import Flask, request, jsonify
import requests
import redis
import json

app = Flask(__name__)

def get_data():
    response = requests.get(url='https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
    return json.loads(response.content)['response']

def get_redis_client():
    return redis.Redis(host='redis-db', port=6379, db=0)

@app.route('/data', methods=['POST', 'GET', 'DELETE'])
def handle_data():
    rd = get_redis_client()
    if request.method == 'POST':
        data = get_data()['docs']
        for gene in data:
            rd.set(gene['hgnc_id'], json.dumps(gene))
        return jsonify({'message': 'Data added successfully'})
    if request.method == 'GET':
        result = []
        for key in rd.keys():
            result.append(json.loads(rd.get(key)))
        return jsonify(result)
    if request.method == 'DELETE':
        rd.flushdb()
        return jsonify({'message': 'Data deleted successfully'})

@app.route('/genes', methods=['GET'])
def get_genes():
    rd = get_redis_client()
    result = []
    for key in rd.keys():
        result.append(json.loads(rd.get(key)))
    return jsonify(result)

@app.route('/genes/<hgnc_id>', methods=['GET'])
def get_specific_gene(hgnc_id):
    rd = get_redis_client()
    if rd.exists(hgnc_id):
        return json.loads(rd.get(hgnc_id))
        
    return jsonify({'message': 'hgnc_id not found'})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
