from flask import Blueprint
routes = Blueprint('routes', __name__)

from routes.polling_routes import *