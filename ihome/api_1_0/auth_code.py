from flask import Flask, current_app, make_response,jsonify,request
from ihome.utils.captcha import captcha
from . import api
from ihome import redis_store, constants
from ihome.utils.response_codes import RET
from ihome.models import User
from ihome import db
from ihome.libs.yuntongxun.SendSMS import CCP
import random
@api.route("/imagecodes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return:
    """
    # 获取参数
    # 参数验证
    # 逻辑处理
    name, text, image_data = captcha.captcha.generate_captcha()
    try:
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.loggerr(e)
        return jsonify(errcode = RET.DBERR,errmsg = "保存到redis失败")
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
    # 返回


@api.route("/smscodes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """

    :param mobile:
    :return:
    """
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    if not all([image_code_id,image_code]):
        return jsonify(errcode = RET.PARAMERR,errmsg = "参数不完整")
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.loggerr.error(e)
        return jsonify(errcode=RET.DBERR, errmsg="redis 数据库错误")
    if not real_image_code:
        return jsonify(errcode=RET.NODATA, errmsg="图片验证码过期")
        # 与用户填写的值进行对比
    if real_image_code.lower() != image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    sms_code = "%06d"%random.randint(0,999999)

    try:
        redis_store.setex("sms_code_%s"%mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # 发送短信
    try:
        ccp = CCP()
        result = ccp.send_template_sms("15910436301",[sms_code,int(constants.SEND_SMS_CODE_INTERVAL/60)],1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="短信发送异常")
    # 返回值
    if result == 0:
        # 发送成功
        return jsonify(errno=RET.OK, errmsg="发送成功")
    else:
        return jsonify(errno=RET.THIRDERR, errmsg="发送失败")
