from flask import Blueprint

auth = Blueprint('authentication', __name__, template_folder='../templates', static_folder='../static')

from app.stocks import routes