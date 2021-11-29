from flask import Flask
from flask_restplus import Api

from bttmbotmanager.api.app import api as ns_generic

authorizations = {
    "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"},
}

flask_app = Flask(__name__)
api = Api(
    app=flask_app,
    version="1.0",
    title="bttmbot manager",
    description="Manage bttmbot running at same time",
)

api.add_namespace(ns_generic)
