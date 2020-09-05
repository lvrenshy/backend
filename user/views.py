from django.shortcuts import render
# Create your views here.
import json
import jwt
# import datetime
from datetime import datetime, timedelta
# import time
# Create your views here.
from django.http import HttpResponse, response, JsonResponse
from .models import models
from ..adaptor import *
import random



SECRET_KEY = '123456'


# 用户登录
def login(request):
    if request.method == 'POST':
        # try:
        data = json.loads(request.body.decode())
        account_number = data.get('account_number')
        if account_number is not None:
            # 获取输入的密码
            password = data.get('password')
            hash_pwd = hash_password(password)
            account_number = list(models.Users.objects.filter(account_number=account_number,password=hash_pwd).values())
            # 如果list(account_number)存在
            if len(list(account_number)) > 0:
                return create_a_token(account_number)
            else:
                return JsonResponse({"code": 403,'error':'请先注册'})
        else:
            return '请输入账号'
        # except Exception as ex:
        #     return JsonResponse({'error': ex})
    else:
        return JsonResponse({'code': 403,'error':'请用post请求'})


# 用户注册
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            print(data, 1111111111111111111111)
            account_number = data.get('account_number')
            password = data.get('password')
            password2 = data.get('password2')
            users = models.Users.objects.filter(account_number=account_number).count()
            if users == 0:
                if password == password2:
                    hash_pwd = hash_password(password)
                    user = {
                        "account_number": account_number,
                        "password": hash_pwd
                    }
                    # 创建用户
                    models.Users.objects.create(**user)
                    create_a_token(account_number)
                    return JsonResponse({'code':200})
                else:
                    return JsonResponse({"code":403,'error':'两次密码不一致'})
            else:
                return JsonResponse({"code": 403,'error':'该帐号已被注册'})
        except Exception as ex:
            return JsonResponse({'code':403,"error": ex})
    else:
        return JsonResponse({"code": 403,'error':'请用post请求'})

# request={'method':'post',
#          'account_number':'123456',
#          'password':123456,
#          'password2':123456
#          }
# register(request)