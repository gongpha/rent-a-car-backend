""" run the app in development mode """
from app import init_app

app = init_app()
app.run(debug=True, host="0.0.0.0")
