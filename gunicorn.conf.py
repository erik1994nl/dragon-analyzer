import os

use_loglevel = os.getenv("LOG_LEVEL", "info")
accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "300")
timeout_str = os.getenv("TIMEOUT", "300")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

# Gunicorn config variables
loglevel = use_loglevel
errorlog = use_errorlog
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)
workers = 1
wsgi_app = "dragon_analyzer.main:app"
bind = "0.0.0.0:6300"
worker_class = "uvicorn.workers.UvicornWorker"
