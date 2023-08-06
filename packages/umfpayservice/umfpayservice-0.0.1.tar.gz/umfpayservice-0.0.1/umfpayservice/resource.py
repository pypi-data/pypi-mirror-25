# -*- coding: utf-8 -*-

import umfpayservice
from umfpayservice import api_requestor, util, error, regex_check, sign, common

class UmfPayObject(dict):
    def __init__(self, service=None):
        super(UmfPayObject, self).__init__()

        self.service = service

class APIResource(UmfPayObject):

    def __init__(self, service=None):
        super(APIResource, self).__init__(service)

        if service in common.service_keys:
            self.service = service
        else:
            raise error.ParamsError("[请求参数校验] "
                                            "service: 为空或该接口本SDK不支持，请联系联动运营人员！")
        self.request_params = {}
        self.resp = {}

    def request(self, params):
        self.request_params = params

        requestor = api_requestor.APIRequestor()
        response = requestor.request('post', params)
        self.resp = response
        return response

    def create(self, **params):
        params = self.add_common_params(params)
        if self.check_params(params):
            self.process_params(params)

            response = self.request(params)

            return response
        return None

    def add_common_params(self, params):
        '''
        添加公共参数
        :param params:
        :return:
        '''
        common_params = {
            'service': self.service,
            'sign_type': umfpayservice.umf_config.sign_type,
            'charset': umfpayservice.umf_config.charset,
            'res_format': umfpayservice.umf_config.res_format,
            'version': umfpayservice.umf_config.api_version
        }

        return dict(common_params, **params)

    def check_params(self, params):
        '''
        校验参数
        :param params:
        :return:
        '''
        required_keys = self.get_required_keys()
        util.logger.info("该接口的必传参数列表为：%r" % required_keys)
        if not (params.has_key(required_key) for required_key in required_keys):
            raise error.ParamsError("[请求参数校验]"
                                    "该接口缺少必传字段。必传字段列表为：%s" % required_keys)
        if (regex_check.RegexCheck.check(key, value) for key, value in params.iteritems()):
            return True
        return False

    @classmethod
    def process_params(cls, params):
        # 空参数过滤
        for key in params.keys():
            if params[key] is None or (params[key] == ''):
                del params[key]

        # 敏感字段加密
        cls.encrypt_fields(params)

        # 添加签名
        try:
            plain = sign.get_sorted_plain(params)
            sign_str = sign.sign(plain, params['mer_id'])
            params['sign'] = sign_str
        except:
            raise error.SignatureError("使用商户私钥生成签名失败。")

    @classmethod
    def encrypt_fields(cls, params):
        for key, value in params.iteritems():
            if (value is not None or '') and key in common.encrypt_fields:
                try:
                    value = value.decode('utf-8').encode('gbk')
                    params[key] = sign.encrypt_data(value)
                except:
                    raise error.SignatureError("%s: 敏感字段加密失败。(%s: %s)" % (key, key, value))

    @classmethod
    def get_required_keys(cls):
        raise TypeError('APIResource 是一个虚拟类，你需要在它的子类中实现get_required_keys方法')




