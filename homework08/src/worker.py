from jobs import get_job_by_id, update_job_status, q, rd, rdb
import json
import logging
from datetime import datetime

@q.worker
def do_work(jobid):
    logging.debug('hello')
    update_job_status(jobid, 'in progress')
    job = get_job_by_id(jobid)
    genes = get_genes_by_groups(job['gene_group'])
    date_freq = {}
    for gene in genes:
        if gene.get('date_approved_reserved'):
            date_object = datetime.strptime(gene['date_approved_reserved'], '%Y-%m-%d').date()
            year = date_object.strftime('%Y')
            date_freq[year] = date_freq.get(year, 0) + 1
    rdb.set(jobid, json.dumps(date_freq))
    update_job_status(jobid, 'complete')

def get_genes_by_groups(group):
    result = []
    for key in rd.keys():
        gene = json.loads(rd.get(key))
        if gene.get('gene_group'):
            for g in gene.get('gene_group'):
                if g == group:
                    result.append(gene)
    return result

do_work()

