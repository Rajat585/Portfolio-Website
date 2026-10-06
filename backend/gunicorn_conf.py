"""Gunicorn config for VPS deployment. Run with:
    gunicorn -c gunicorn_conf.py portfolio_backend.wsgi:application
"""
bind = "127.0.0.1:8000"
workers = 3
timeout = 60
accesslog = "/var/log/portfolio/gunicorn-access.log"
errorlog = "/var/log/portfolio/gunicorn-error.log"
loglevel = "info"
