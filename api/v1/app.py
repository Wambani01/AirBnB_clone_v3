#!/usr/bin/python3

"""my flask file"""

from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def clean_up(exception=None):
    """eliminates current Session"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
