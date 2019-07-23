from . import api
from flask import request, jsonify, current_app,session
from ihome.utils.response_codes import RET
from werkzeug.security import generate_password_hash, check_password_hash
from ihome import redis_store, db
import re
from ihome.models import User
from sqlalchemy import exc


@api.route("/users", methods=["POST"])
def register():
    """

    :return:
    """
    register_dict = request.get_json()
    mobile = register_dict.get("mobile")
    sms_code = register_dict.get("sms_code")
    password = register_dict.get("password")

    if not all([mobile, sms_code, password]):
        return jsonify(errcode=RET.PARAMERR, errmsg="参数不完整")

    if re.match('1[34578]/d{9}', mobile):
        return jsonify(errcode=RET.PARAMERR, errmsg="手机号格式错误")

    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR, errmsg="redis查询错误")

    if not real_sms_code:
        return jsonify(errcode=RET.DBERR, errmsg="手机验证码不存在")

    if real_sms_code != sms_code:
        return jsonify(errcode=RET.PARAMERR, errmsg="验证码不匹配")

    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    user = User(name=mobile, mobile=mobile,password_hash = generate_password_hash(password))
    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR, errmsg="手机号已被注册")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR, errmsg="数据库查询错误")

    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id

    return jsonify(errcode=RET.OK, errmsg="注册成功")
