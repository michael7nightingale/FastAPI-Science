"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count

bind = '0.0.0.0:9002'
# bind = "unix:/run/gunicorn.sock"
max_requests = 10000
timeout = 60
worker_class = 'uvicorn.workers.UvicornWorker'
workers = cpu_count() * 2 + 1
