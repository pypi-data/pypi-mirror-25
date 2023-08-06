# coding=utf-8
import logging
from util import logger

from regex_check import RegexCheck
import error
import datetime
import os

# 需要加密的敏感字段
encrypt_fields = ["card_id", "valid_date", "cvv2", "pass_wd", "identity_code",
                  "card_holder", "recv_account", "recv_user_name", "identity_holder",
                  "identityCode", "cardHolder", "mer_cust_name", "account_name", "bank_account", "endDate"]

# 联动提供的service列表
service_keys = ["pay_req", "pay_req_ivr_call", "pay_req_ivr_tcall", "query_order", "mer_cancel",
                    "mer_refund", "download_settle_file", "pay_req_split_front", "pay_req_split_back",
                    "pay_req_split_direct", "split_refund_req", "pay_result_notify", "split_req_result",
                    "split_refund_result", "credit_direct_pay", "debit_direct_pay", "pre_auth_direct_req",
                    "pre_auth_direct_pay", "pre_auth_direct_cancel", "pre_auth_direct_query",
                    "pre_auth_direct_refund", "pre_auth_direct_settle", "pay_transfer_register",
                    "pay_transfer_req", "pay_transfer_order_query", "pay_transfer_mer_refund", "card_auth",
                    "req_sms_verifycode", "pay_confirm", "pay_req_shortcut_front", "pay_req_shortcut",
                    "agreement_pay_confirm_shortcut", "query_mer_bank_shortcut", "unbind_mercust_protocol_shortcut",
                    "split_req",  "query_split_order",  "transfer_direct_req",  "transfer_query",
                    "mer_order_info_query",  "mer_refund_query",  "active_scancode_order", "passive_scancode_pay",
                    "query_account_balance", "comm_auth", "apply_pay_shortcut", "sms_req_shortcut",
                    "confirm_pay_shortcut", "get_mer_bank_shortcut", "unbind_mercust_protocol_shortcut",
                    "refund_info_replenish", "req_bind_verify_shortcut","req_bind_confirm_shortcut",
                    "bind_agreement_notify_shortcut","bind_req_shortcut_front"]

class Config(object):

    def __init__(self):
        # # log文件输出路径
        # self.log_path = "./logs"
        # 私钥对
        self.mer_private_keys = {}
        # 接口版本
        self.api_version = '4.0'
        self.auth_version = '1.0'
        # 默认签名加密方式
        self.sign_type = 'RSA'
        # 默认编码方式
        self.charset = 'UTF-8'
        # 默认响应格式
        self.res_format = 'HTML'

        self.set_logger(True, './logs', logging.INFO)

    # def __setattr__(self, key, value):
    #     if not hasattr(self, key):
    #         logger.warning("umfservice的umf_config配置不允许添加新的配置项。添加或修改配置失败。(%s: %s)", key, value)
    #     else:
    #         object.__setattr__(self, key, value)

    def add_private_keys(self, key_list=None):
        '''
        动态添加商户号和私钥路径对
        :param key_list:
        :return:
        '''
        if key_list is None:
            return

        if isinstance(key_list, list):
            for mer_id, private_key_path in key_list:
                if RegexCheck.check("mer_id", mer_id):
                    self.mer_private_keys[mer_id] = private_key_path
                else:
                    raise error.ConfigError("[配置错误] mer_id格式不匹配。(mer_id: %s)"
                                            "匹配规则为：%s" % (mer_id, RegexCheck.get_regexs()["mer_id"]))

    def set_logger(self, print_log, log_path, level):
        if print_log:
            if os.path.isdir(log_path):
                pass
            else:
                os.mkdir(log_path)
            log_file = "%s/umfservice_log_%s.log" % (log_path, datetime.datetime.now().strftime("%Y%m%d"))

            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [UMF SDK]%(message)s')
            fh.setFormatter(formatter)
            logger.setLevel(level)
            logger.addHandler(fh)
