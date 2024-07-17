#!/usr/bin/python3
"""Flask web application"""
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
import os
from models import storage


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprint after all routes are defined
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage on teardown"""
    storage.close()


def run_flask():
    """Method to run flask"""
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'),
            threaded=True)


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors that returns a JSON-formatted response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    run_flask()
