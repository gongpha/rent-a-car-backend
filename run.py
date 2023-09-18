""" for running in the production server """
from waitress import serve
from app import init_app

app = init_app()
serve(app, host="0.0.0.0", port=80)
