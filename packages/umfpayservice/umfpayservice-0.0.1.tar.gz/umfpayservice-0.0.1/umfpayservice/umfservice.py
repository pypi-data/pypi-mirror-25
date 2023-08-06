# coding=utf-8

import datetime
import os
import urllib

import umfpayservice
from umfpayservice import api_requestor, util, error, sign
from resource import APIResource, UmfPayObject

class Order(APIResource):
    '''
    APP支付下单
    '''
    def __init__(self):
        super(Order, self).__init__('pay_req')

    @classmethod
    def get_required_keys(cls):
        return ["service" ,"charset", "mer_id", "sign_type", "version", "order_id", "mer_date", "amount", "amt_type"]

class ActiveScanCodeOrder(APIResource):
    '''
    收款-扫码支付
    主扫支付
    '''
    def __init__(self):
        super(ActiveScanCodeOrder, self).__init__('active_scancode_order')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "notify_url", "version", "goods_inf", "order_id", "mer_date", "amount", "amt_type", "scancode_type"]

class PassiveScanCodePay(APIResource):
    '''
    收款-扫码支付
    主扫支付
    '''
    def __init__(self):
        super(PassiveScanCodePay, self).__init__('passive_scancode_pay')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "notify_url", "version", "goods_inf", "order_id", "mer_date", "amount", "amt_type", "auth_code", "use_desc", "scancode_type"]

class ApplayPayShortcut(APIResource):
    '''
    收款-快捷支付
    下单
    '''
    def __init__(self):
        super(ApplayPayShortcut, self).__init__('apply_pay_shortcut')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "order_id", "notify_url", "order_id", "mer_date", "amount", "amt_type", "pay_type", "gate_id"]

class SmsReqShortcut(APIResource):
    '''
    收款-快捷支付
    获取短信
    '''
    def __init__(self):
        super(SmsReqShortcut, self).__init__('sms_req_shortcut')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "trade_no", "media_id", "media_type"]

class ConfirmPayShortcut(APIResource):
    '''
    收款-快捷支付
    确认支付
    '''
    def __init__(self):
        super(ConfirmPayShortcut, self).__init__('confirm_pay_shortcut')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "trade_no", "trade_no", "verify_code", "media_type", "media_id"]

class QueryMerBankShortcut(APIResource):
    '''
    收款-快捷支付
    获取银行列表
    '''
    def __init__(self):
        super(QueryMerBankShortcut, self).__init__('query_mer_bank_shortcut')

    @classmethod
    def get_required_keys(cls):
        return ["service", "sign_type", "charset", "mer_id", "version", "pay_type"]

class UnbindMercustProtocolShortcut(APIResource):
    '''
    收款-快捷支付
    解约接口
    '''
    def __init__(self):
        super(UnbindMercustProtocolShortcut, self).__init__('unbind_mercust_protocol_shortcut')

    @classmethod
    def get_required_keys(cls):
        return ["service", "sign_type", "charset", "mer_id", "version"]

class MerOrderInfoQuery(APIResource):
    '''
    订单查询
    查询历史订单信息
    '''
    def __init__(self):
        super(MerOrderInfoQuery, self).__init__('mer_order_info_query')

    @classmethod
    def get_required_keys(cls):
        return ["service", "sign_type", "charset", "mer_id", "version", "order_id", "mer_date"]

class QueryOrder(APIResource):
    '''
    订单查询
    查询当天订单状态
    '''
    def __init__(self):
        super(QueryOrder, self).__init__('query_order')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "sign_type", "mer_id", "version", "order_id", "mer_date"]

class MerCancel(APIResource):
    '''
    撤销
    '''
    def __init__(self):
        super(MerCancel, self).__init__('mer_cancel')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "sign_type", "mer_id", "version", "order_id", "mer_date", "amount"]


class MerRefund(APIResource):
    '''
    退款
    普通退费
    '''
    def __init__(self):
        super(MerRefund, self).__init__('mer_refund')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "sign_type", "mer_id", "version", "refund_no", "order_id", "mer_date", "org_amount"]

class SplitRefundReq(APIResource):
    '''
    退款
    批量转账退费
    '''
    def __init__(self):
        super(SplitRefundReq, self).__init__('split_refund_req')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "refund_no", "order_id", "mer_date", "refund_amount", "org_amount", "sub_mer_id", "sub_order_id"]

class MerRefundQuery(APIResource):
    '''
    退款
    退款状态查询方法
    '''
    def __init__(self):
        super(MerRefundQuery, self).__init__('mer_refund_query')

    @classmethod
    def get_required_keys(cls):
        return ["service", "sign_type", "charset", "mer_id", "version", "refund_no"]

class RefundInfoReplenish(APIResource):
    '''
    退款
    退费信息补录方法
    '''
    def __init__(self):
        super(RefundInfoReplenish, self).__init__('refund_info_replenish')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "refund_no", "card_holder", "card_id"]

#------------------------------------------------------------
# 付款
#------------------------------------------------------------
class TransferDirectReq(APIResource):
    '''
    付款
    下单
    '''
    def __init__(self):
        super(TransferDirectReq, self).__init__('transfer_direct_req')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "version", "sign_type", "order_id", "mer_date", "amount", "recv_account_type", "recv_bank_acc_pro", "recv_account", "recv_user_name", "recv_gate_id", "purpose", "prov_name", "city_name", "bank_brhname"]

class TransferQuery(APIResource):
    '''
    付款
    付款状态查询
    '''
    def __init__(self):
        super(TransferQuery, self).__init__('transfer_query')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "version", "sign_type", "order_id", "mer_date"]

class QueryAccountBalance(APIResource):
    '''
    付款
    余额查询
    '''
    def __init__(self):
        super(QueryAccountBalance, self).__init__('query_account_balance')

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "version", "sign_type"]

# ------------------------------------------------------------
# 鉴权
#------------------------------------------------------------
class CommAuth(APIResource):
    '''
    鉴权
    借记卡实名认证
    '''
    def __init__(self):
        super(CommAuth, self).__init__('comm_auth')

    def add_common_params(self, params):
        common_params = {
            'service': self.service,
            'sign_type': umfpayservice.umf_config.sign_type,
            'charset': umfpayservice.umf_config.charset,
            'res_format': umfpayservice.umf_config.res_format,
            'version': umfpayservice.umf_config.auth_version
        }
        return dict(common_params, **params)

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "auth_type", "order_id"]

class CreditCommAuth(APIResource):
    '''
    鉴权
    贷记卡实名认证
    '''
    def __init__(self):
        super(CreditCommAuth, self).__init__('comm_auth')

    def add_common_params(self, params):
        common_params = {
            'service': self.service,
            'sign_type': umfpayservice.umf_config.sign_type,
            'charset': umfpayservice.umf_config.charset,
            'res_format': umfpayservice.umf_config.res_format,
            'version': umfpayservice.umf_config.auth_version
        }
        return dict(common_params, **params)

    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "auth_type", "order_id"]

class IdentityAuth(APIResource):
    '''
    鉴权
    身份认证
    '''
    def __init__(self):
        super(IdentityAuth, self).__init__('comm_auth')

    def add_common_params(self, params):
        common_params = {
            'service': self.service,
            'sign_type': umfpayservice.umf_config.sign_type,
            'charset': umfpayservice.umf_config.charset,
            'res_format': umfpayservice.umf_config.res_format,
            'version': umfpayservice.umf_config.auth_version
        }
        return dict(common_params, **params)


    @classmethod
    def get_required_keys(cls):
        return ["service", "charset", "mer_id", "sign_type", "version", "auth_type", "order_id"]

# ---------------------------------------------------------------
# 对账
# ---------------------------------------------------------------
class DownloadSettleFile(APIResource):
    '''
    对账
    下载对账文件
    '''
    def __init__(self):
        super(DownloadSettleFile, self).__init__('download_settle_file')

    @classmethod
    def get_required_keys(cls):
        return ["service", "sign_type", "mer_id", "version", "settle_date"]

    def download(self, **params):
        self.add_common_params(params)
        if self.check_params(params):
            self.process_params(params)

            if params.has_key('settle_path'):
                file_path = params['settle_path']
                del params['settle_path']
            else:
                raise error.ParamsError("[请求参数校验] "
                                        "settle_path: 该字段不能为空。")
            file_name = "settle_file_%s.txt" % datetime.datetime.now().strftime("%Y%m%d")

            rbody, rcode = api_requestor.APIRequestor().download(file_path, file_name, 'post', params)

            if not (200 <= rcode < 300):
                raise error.APIError(
                    "接口返回的响应错误: %r (响应码为： %d)" % (rbody, rcode),
                    rbody, rcode)
            else:
                self.write_settle(file_path, file_name, rbody)
                return "下载对账文件成功，保存地址为：%s/%s" % (file_path, file_name)
        return None

    @classmethod
    def write_settle(self, file_path, file_name, content):
        if not os.path.isdir(file_path):
            os.mkdir(file_path)

        try:
            content = content.decode('gbk').encode('utf-8')
            with open("%s/%s" % (file_path, file_name), 'w') as f:
                f.write(content)
            util.logger.info("对账文件下载成功，文件路径为：%s/%s" % (file_path, file_name))
        except IOError as e:
            raise IOError("本地写文件失败，path= %s/%s" % (file_path, file_name))

# ------------------------------------------------------------
# 异步通知
# ------------------------------------------------------------

class AsynNotification(UmfPayObject):
    '''
    异步通知
    '''
    def __init__(self):
        super(AsynNotification, self).__init__()

    def notify_data_parser(self, notify_params_str):
        '''
        解析异步通知数据
        :param notify_params_str:
        :return:
        '''
        try:
            notify_params = {key: urllib.unquote(value) for key, value in
                            (split_param.split('=', 1) for split_param in notify_params_str.split('&'))}
            plain = sign.get_sorted_plain(notify_params)
            verify = sign.verify(plain, notify_params['sign'])
        except:
            raise error.SignatureError('异步通知验证签名异常')

        if verify:
            util.logger.info("平台通知数据验签成功")
            if notify_params.has_key('sign'): del notify_params['sign']
            if notify_params.has_key('sign_type'): del notify_params['sign_type']
            if notify_params.has_key('version'): del notify_params['version']

            return notify_params
        else:
            util.logger.info("平台通知数据验证签名发生异常")

    def response_umf_map(self, notify_params):
        '''
        拼接响应给平台的数据
        :param notify_params:
        :return:
        '''
        response_dict = {
            'mer_date': notify_params['mer_date'],
            'mer_id': notify_params['mer_id'],
            'order_id': notify_params['order_id'],
            'ret_code': '0000',
            'ret_msg': 'success',
            'version': '4.0',
            'sign_type': 'RSA'
        }

        mer_plain = sign.get_sorted_plain(response_dict)
        mer_sign = sign.sign(mer_plain, notify_params['mer_id'])
        response_dict['sign'] = mer_sign

        return util.convert_url_not_encode(response_dict)

class UmfServiceUtils(UmfPayObject):
    '''
    其他工具
    '''
    def __init__(self):
        super(UmfServiceUtils, self).__init__()

    @classmethod
    def generate_sign(cls, **params):
        params = params or {}

        requiredKeys = ['merId', 'orderId', 'orderDate', 'amount']
        for requiredKey in requiredKeys:
            if not params.has_key(requiredKey) or params[requiredKey] is None or params[requiredKey] == '':
                raise error.ParamsError('签名参数%s为空,请传入%s' % (requiredKey, requiredKey))

        plain = "%s%s%s%s" % (params['merId'], params['orderId'], params['amount'], params['orderDate'])
        sign_str = sign.sign(plain, params['merId'])
        util.logger.info("[generate_sign]签名后密文串:%s" % sign_str)
        return sign_str