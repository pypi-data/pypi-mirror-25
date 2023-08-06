# coding=utf-8
import umfpayservice
from umfpayservice import error, util

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import SHA

def encrypt_data(data):
    '''
    使用联动公钥加密数据
    '''
    key = get_public_key()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.encrypt(data)
    return base64.b64encode(text)

def sign(data, mer_id):
    '''
    使用商户私钥对数据签名
    '''
    gbk_data = data.decode('utf-8').encode('gbk')

    private_key = get_private_key(mer_id)
    key = RSA.importKey(private_key)
    h = SHA.new(gbk_data)
    signer = Signature_pkcs1_v1_5.new(key)
    signature = signer.sign(h)
    return base64.b64encode(signature)

def app_sign(data, mer_id):
    '''
    app的签名方法
    '''
    base64_sign = sign(data, mer_id)
    return base64.b64decode(base64_sign).encode('hex')

def verify(data, signature):
    '''
    使用联动公钥对数据验签
    '''
    public_key = get_public_key()
    key = RSA.importKey(public_key)
    digest = SHA.new()
    digest.update(data.decode('utf-8').encode('gbk'))
    verifier = Signature_pkcs1_v1_5.new(key)

    sig = base64.b64decode(signature)
    if verifier.verify(digest, sig):
        return True
    return False


def get_private_key(mer_id):
    '''
    获取商户私钥
    '''
    private_key_path = umfpayservice.umf_config.mer_private_keys[mer_id]
    if private_key_path is None:
        raise error.ConfigError("[配置错误] mer_id不在商户私钥配置列表中。(mer_id: %s)"
                                "商户私钥配置列表为：%s. " % (mer_id, umfpayservice.umf_config.mer_private_keys), "mer_id", mer_id)

    private_key = open(private_key_path, "r").read()
    return private_key.strip()

def get_public_key():
    '''
    获取联动公钥
    '''
    from umfpayservice import public_key_path, public_key
    if public_key is not None:
        return public_key.strip()
    if public_key_path is not None:
        umfpayservice.public_key = open(public_key_path, "r").read()
        return umfpayservice.public_key.strip()
    return None

def get_sorted_plain(params):
    params_copy = params.copy()
    # 删除不参与签名的字段
    if params_copy.has_key('sign_type'):
        del params_copy['sign_type']
    if params_copy.has_key('sign'):
        del params_copy['sign']

    params_copy = sorted(params_copy.items(), key=lambda d: d[0])
    plain = util.convert_url_not_encode(params_copy)

    util.logger.info("获取签名明文串：%s" % plain)
    return plain