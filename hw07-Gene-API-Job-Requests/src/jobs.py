import json
import uuid
import redis
from hotqueue import HotQueue
import os

redis_host = os.environ.get('REDIS_HOST')
_redis_port='6379'

rd = redis.Redis(host=redis_host, port=_redis_port, db=0)
q = HotQueue("queue", host=redis_host, port=_redis_port, db=1)
jdb = redis.Redis(host=redis_host, port=_redis_port, db=2, decode_responses=True)

def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def _instantiate_job(jid, status, symbol, gene_family):
    """
    Create the job object description as a python dictionary. Requires the job id,
    status, sybmol and gene_family parameters.
    """
    return {'id': jid,
            'status': status,
            'symbol': symbol,
            'gene_family': gene_family }

def _save_job(jid, job_dict):
    """Save a job object in the Redis database."""
    jdb.set(jid, json.dumps(job_dict))
    return

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)
    return

def add_job(symbol, gene_family, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, symbol, gene_family)
    _save_job(jid, job_dict)
    _queue_job(jid)
    return job_dict

def get_job_by_id(jid):
    """Return job dictionary given jid"""
    return json.loads(jdb.get(jid))

def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job_dict = get_job_by_id(jid)
    if job_dict:
        job_dict['status'] = status
        _save_job(jid, job_dict)
    else:
        raise Exception()
