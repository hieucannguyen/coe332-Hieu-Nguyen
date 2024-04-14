from jobs import get_job_by_id, update_job_status, q, rd, rdb
import json
from datetime import datetime

@q.worker
def do_work(jobid):
    update_job_status(jobid, 'in progress')
    job = get_job_by_id(jobid)
    genes = get_genes_by_groups(job['gene_group'])
    date_freq = {}
    for gene in genes:
        date_object = datetime.strptime(gene['date_approved_reserved'], '%m-%d-%Y').date()
        date_freq[date_object] = date_freq.get(date_object, 0) + 1
    rdb.set(jobid, json.dumps(date_freq))
    update_job_status(jobid, 'complete')

def get_genes_by_groups(group):
    result = []
    for key in rd.keys():
        gene = json.loads(rd.get(key))
        if gene['gene_group'] == group:
            result.append(gene)
    return result

do_work()

