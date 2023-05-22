from flask import Blueprint

bp = Blueprint('stocks', __name__,  template_folder='../templates', static_folder='../static')

from app.authentication import authentication