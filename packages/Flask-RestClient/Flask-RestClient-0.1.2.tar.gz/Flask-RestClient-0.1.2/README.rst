Flask插件for restful api client
===============================

Usage
-----


First init::

    from flask_rest_client import RestCient
    rest_client = RestClient()
    rest_client.init_app(app)

API
---

.. code-block::

    users_api = rest_client.get_api('users')
    j = users_api.get(1).json()  # 获取/users/1的数据
    j = users_api.get()  # 获取/users/的数据


配置项
------

====================    ================================================
配置项                  说明
====================    ================================================
REST_CIENT_BASE_URL     api的url_prefix
REST_CIENT_USERNAME     BaseAuth的username
REST_CIENT_PASSWORD     BaseAuth的password
REST_CIENT_VERIFY       requests的verfy配置，可以是自定义证书的路径
====================    ================================================
