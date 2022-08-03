import os
import multiprocessing

oeg = os.environ.get

bind = "0.0.0.0:8000"
reload = oeg("GUNICORN_RELOAD", "False").lower() == "true"
deamon = True
loglevel = oeg("GUNICORN_LOGLEVEL", "info")
errorlog = "-"
accesslog = "-"
timeout = int(oeg("GUNICORN_TIMEOUT", 300))
workers = multiprocessing.cpu_count() * 2 + 1
