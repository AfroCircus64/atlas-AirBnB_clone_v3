#!/usr/bin/python3
"""Flask web application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown_db(exception):
    """Method for teardown"""
    storage.close()

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'), port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
