# -*- coding: utf-8 -*-

import upyun
import hashlib

# 需要填写自己的服务名，操作员名，密码
service = "image-ihome"
username = "hahahid"
password = "LkrV7QTFmjwLSKLjwuQdBeJ5ELDV6E2k"

import uuid

up = upyun.UpYun(service, username=username, password=password)


def storage(f):
    """
    rest文件上传
    """
    remote_file =str(uuid.uuid1())
    headers = { 'x-gmkerl-rotate': '180' }
    # ret = up.put(remote_file, file_data, headers=headers,form=True)
    res = up.put(remote_file, f, checksum=True, form=True)
    print(res)
    if res.get('code') == 200:
        return res.get("url")
    else:
        raise Exception("图片上传失败")

if __name__ == "__main__":
    with open("1.jpg",'rb') as f:
        storage(f)