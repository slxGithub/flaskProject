from flask import Flask, current_app, make_response,jsonify

from ihome.utils.captcha import captcha
from . import api
from ihome import redis_store, constants
from ihome.utils.response_codes import RET

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
        redis_store.setex(image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.loggerr(e)
        return jsonify(errcode = RET.DBERR,errmsg = "保存到redis失败")
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
    # 返回
