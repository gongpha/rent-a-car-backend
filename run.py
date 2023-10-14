""" for running in the production server """
from waitress import serve
from app import init_app
from werkzeug.middleware.proxy_fix import ProxyFix

app = init_app()
serve(ProxyFix(app, x_for=1, x_host=1), host="0.0.0.0", port=80)