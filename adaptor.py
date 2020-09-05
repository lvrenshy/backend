import jwt
import datetime
from datetime import datetime, timedelta
from django.http import JsonResponse,HttpResponse

# import time
import hashlib
import psycopg2
from .user import models

import json
from django.db import connection
import random

SECRET_KEY = '123456'
cur = psycopg2.connect(database='blog', user='blog', password='blog123', host='127.0.0.1', port='5432')
cursor = cur.cursor()


def create_a_token(account_number):
    time_out = datetime.utcnow() + timedelta(days=0, seconds=8000)
    option = {
        'iss': 'shy_home.com',  # token的签发者
        'exp': time_out,
        'iat': datetime.utcnow(),
        'aud': 'webkit',  # token的接收者，这里指定为浏览器
        'account_number': account_number  # 放入用户信息，唯一标识，解析后可以使用该信息
    }
    # 加盐

    # 将token加密再从字节码转化成字符串
    token = jwt.encode(option, SECRET_KEY, 'HS256').decode()
    response = JsonResponse({"code": account_number}, status=200, content_type='application/json',
                            charset='utf-8')
    # 把token放入headers中
    response["token"] = token
    response["account_number"] = account_number
    # 给token权限，不加这行无法发送token
    response["Access-Control-Expose-Headers"] = "token"
    return response


def decode_of_token(request):
    get_token = request.META.get('HTTP_TOKEN')
    # 将headers中的token进行解密
    token = jwt.decode(get_token, SECRET_KEY, audience='webkit', algorithms=['HS256'])
    account_number = token['account_number']
    print("account_number",account_number[0]['account_number'])
    return account_number[0]['account_number']


def hash_password(password):
    """
    使用sha1加密算法，返回str加密后的字符串
   """
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    sha1_password = sha1.hexdigest()
    return sha1_password

# def comment()
# # 验证身份
# def check_identity(request):
#     phone = decode_of_token(request)
#     code = models.Users.objects.get(telephone_num=phone).power
#     if code == 1:
#         # 还不是司机
#         return 'passenger'
#     elif code == 2:
#         return 'driver'