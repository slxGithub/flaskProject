# from .CCPRestSDK import REST
from ihome.libs.yuntongxun.CCPRestSDK import REST
accountSid = '8a216da85d158d1b015d65525bf222fa'
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = '6b1891146bda4e93842bb8aef3f89c23'
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8a216da85d158d1b015d65525d5c2301'
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com'
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


class CCP:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:

            obj = super().__new__(cls)

            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls.instance = obj

        return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        """"""
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        # smsMessageSid:ff75e0f84f05445ba08efdd0787ad7d0
        # dateCreated:20171125124726
        # statusCode:000000
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送短信成功
            return 0
        else:
            # 发送失败
            return -1


if __name__ == "__main__":
    ccp = CCP()
    ret = ccp.send_template_sms("15910436301", ["12345", "5"], 1)

    print(ret)