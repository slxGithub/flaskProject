from . import api
from ihome import db
from ihome import models

ytx = "6b1891146bda4e93842bb8aef3f89c23"

@api.route('/index')
def index():
    return "index page"
