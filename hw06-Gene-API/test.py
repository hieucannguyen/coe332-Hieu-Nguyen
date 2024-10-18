import requests
import json

#response = requests.get(url='https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')

response = requests.get(url='https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
data = json.loads(response.content)['response']['docs']


for gene in data:
    print(gene['hgnc_id'], type(json.dumps(gene)))