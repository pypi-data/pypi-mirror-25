
该demo展示了如何通过umfpayservice扩展包来更方便的调用联动服务，以及使用联动服务时的一些工具方法。

### demo使用指引

1. 创建虚拟环境 
```shell
sudo easy_install virtualenv
virtualenv venv
```

2. 切换到虚拟环境
```shell
source venv/bin/activate
```

3. 使用pip安装python包
```shell
pip install umfpayservice
```

4. 使用虚拟环境(venv)作为python解释器；设置方法(PyCharm为例)：Preferences->Project Interpreter->设置按钮，Add Local->选择venv下的python包

5. 使用时先导入扩展包
```shell
# 导入umfpayservice扩展包
import umfpayservice
```

4. 初始化umfpayservice包括设置日志路径、设置联动公钥、设置多个商户私钥，见代码示例。
```shell
# 设置打印log的路径
umfpayservice.umf_config.set_log_path('./logs')

# 添加商户号和私钥路径的映射，支持多商户号的场景
umfpayservice.umf_config.add_private_keys([('60000100', './cert/60000100_.key.pem'), ])

# 添加平台公钥路径
umfpayservice.public_key_path = './cert/cert_2d59_public.pem'
```

5. 初始化结束之后，可以按照各个接口代码示例调用平台服务。
```shell
# 调用平台服务
# 此处为了更清楚的显示每个接口调用的方式，将所有接口封装了测试方法(以test_开头的方法)，参考测试方法调用接口
umf_service_test.test_mobile_order()
```