
该demo展示了如何通过umfpayservice扩展包来更方便的调用联动服务，以及使用联动服务时的一些工具方法。

### demo使用指引

1. 创建虚拟环境 

为了不造成环境的混乱，一般都会在工程下创建一个虚拟环境，该工程使用虚拟环境下的包和python解释器，不会与其他工程或全局环境冲突。
在项目路径下执行
```shell
// 此处是Mac环境安装、创建虚拟环境的命令，其他系统请自行搜索解决。

// 创建mac默认的python2.7的虚拟环境
sudo easy_install virtualenv
virtualenv venv

// 创建python3虚拟环境
python3 -m venv  venv3
```

2. 切换到虚拟环境
```shell
source venv/bin/activate
```

3. 使用pip安装python包
```shell
pip install umfpayservice
```

4. 使用虚拟环境(venv)作为python解释器；设置方法(PyCharm为例)：Preferences->Project Interpreter->设置按钮，Add Local->选择venv/bin/Python2.7执行文件

> 至此，完成了导入umfpayservice扩展包和配置python解释器的工作，demo工程就可以正常运行了。
> 以下是使用umfpayservice扩展包的步骤。

### 扩展包使用指引

1. 使用时先导入扩展包
```python
# -*- coding: utf-8 -*-
# 导入umfpayservice扩展包
import umfpayservice
```

2. 初始化umfpayservice包括设置日志路径、设置联动公钥、设置多个商户私钥，见代码示例。
```python
# -*- coding: utf-8 -*-
# 设置打印log的路径
umfpayservice.umf_config.set_log_path('./logs')

# 添加商户号和私钥路径的映射，支持多商户号的场景
umfpayservice.umf_config.add_private_keys([('60000100', './cert/60000100_.key.pem'), ])

# 添加平台公钥路径
umfpayservice.public_key_path = './cert/cert_2d59_public.pem'
```

3. 初始化结束之后，可以按照各个接口代码示例调用平台服务。
```python
# -*- coding: utf-8 -*-
# 调用平台服务
# 此处为了更清楚的显示每个接口调用的方式，将所有接口封装了测试方法(以test_开头的方法)，参考测试方法调用接口
umf_service_test.test_mobile_order()
```

### 扩展包详细配置

umfpayservice扩展包的所有配置在```umfpayservice.umf_config```中设置。
一般不需要配置，使用默认配置即可。
```python
# -*- coding: utf-8 -*-
# 设置是否打印log
umfpayservice.umf_config.is_log = False

#以及其他一些属性都可以直接通过'.'的调用方式设置
# 注意：以下设置非联动平台接口变更，不可进行更改，否则会导致接口调用失败

# 接口版本
umfpayservice.umf_config..api_version = '4.0'
umfpayservice.umf_config..auth_version = '1.0'
# 默认签名加密方式
umfpayservice.umf_config..sign_type = 'RSA'
# 默认编码方式
umfpayservice.umf_config..charset = 'UTF-8'
# 默认响应格式
umfpayservice.umf_config..res_format = 'HTML'
```