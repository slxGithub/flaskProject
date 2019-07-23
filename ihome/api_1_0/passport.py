from . import api
from flask import request, jsonify, current_app, session
from ihome.utils.response_codes import RET
from werkzeug.security import generate_password_hash, check_password_hash
from ihome import redis_store, db,constants
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

    user = User(name=mobile, mobile=mobile, password_hash=generate_password_hash(password))
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


@api.route("/sessions", methods=["POST"])
def login():
    """

    :return:
    """
    login_dict = request.get_json()
    mobile = login_dict.get("mobile")
    password = login_dict.get("password")

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： "access_nums_请求的ip_mobile": "次数"
    user_ip = request.remote_addr  # 用户的ip地址
    try:
        access_nums = redis_store.get("access_num_%s_%s" % (user_ip,mobile))
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    try:
        user = User.query.filter_by(name=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.OK, errmsg="数据库查询异常")

    if user is None or not check_password_hash(user.password_hash, password):
        # 如果验证失败，记录错误次数，返回信息
        try:
            # redis的incr可以对字符串类型的数字数据进行加一操作，如果数据一开始不存在，则会初始化为1
            redis_store.incr("access_num_%s_%s" % (user_ip,mobile))
            redis_store.expire("access_num_%s_%s" % (user_ip, mobile),constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.PWDERR, errmsg="账号或密码错误")

    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="登陆成功")


@api.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session",methods=["DELETE"])
def logout():
    """

    :return:
    """
    csrf_token = session.get("csrf_token")
    session.clear()
    session["csrf_token"]=csrf_token
    return jsonify(errno=RET.OK,errmsg="OK")
