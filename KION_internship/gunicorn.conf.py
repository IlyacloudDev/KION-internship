import multiprocessing


bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000


accesslog = "-"
errorlog = "-"
