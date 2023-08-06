# -*- coding: utf-8 -*-
# umfservice Python
# Configurations

public_key_path = None # 联动公钥文件地址
public_key = None # 联动公钥串

from umfpayservice.common import (
    encrypt_fields,
    Config
)
from umfpayservice.api_requestor import APIRequestor  # noqa

from umfpayservice.error import (  # 错误
    UmfPayError,
    ParamsError,
    SignatureError,
    APIError,
    RequestError)

from umfpayservice.util import logger, JSON  # 工具

from umfpayservice.umfservice import (  # 封装的请求接口类
    MobileOrder,
    ActiveScanPayment,
    PassiveScanPayment,
    QuickPayOrder,
    QuickGetMessage,
    QuickPayConfirm,
    QuickQuerybankSupport,
    QuickCancelSurrender,
    QueryhistoryOrder,
    QueryTodayOrder,
    CancelTrade,
    GeneralRefund,
    MassTransferRefund,
    QueryRefundState,
    RemedyRefundInformation,
    PaymentOrder,
    QueryPaymentStatus,
    QueryAccountBalance,
    DebitCardAuthentication,
    CreditCardAuthentication,
    IdentityAuthentication,
    ReconciliationDownload,
    AsynNotification,
    WebFrontPagePay,
    H5FrontPage,
    PublicPayment,
    UmfServiceUtils
    )

from umfpayservice.resource import (  # noqa
    UmfPayObject,
    APIResource,
    DownLoadAPIResource,
    ParamsGetAPIResource
)

umf_config = Config()

