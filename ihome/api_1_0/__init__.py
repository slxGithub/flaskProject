from flask import Blueprint

api = Blueprint("api", __name__)

# 导入蓝图的视图
from . import demo
from . import auth_code