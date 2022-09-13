#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 9:34 PM
# @Author  : NeiL Liu
# @File    : config-template.py
# @Project ：xunacg_autosign
# @Software: PyCharm

config = {
    "accounts": [
        {  # 帳號1
            "email": "email@example.com",
            "password": "123456",
            "uid": "12345"
        },
        # {  # 帳號2
        #     "email": "example@example.com",
        #     "password": "123456",
        #     "uid": "12345"
        # }
    ],
    "push": True,
    "url": {
        "login_url": "https://www.xunacg.com/user-login.htm",
        "dailysign_url": "https://www.xunacg.com/sg_sign.htm",
        "freecoin_url": "https://www.xunacg.com/my-free.htm"
    }
}
