from flask import Blueprint
'''
Регистрация макета API 
'''
api = Blueprint('api', __name__)

from . import auth, posts, errors