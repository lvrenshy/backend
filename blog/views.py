from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
import json

from blog import models
from blog.models import Blog


def commit_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            content = data.get('content')
            if content is not None:
                blog_instance = Blog.objects.get(id=1)
                models.Comment.objects.create(content=data.get('content'),
                                              commentator=data.get('commentator'),
                                              serial_number=blog_instance,
                                              comment_time=datetime.now())
                return JsonResponse({'code': 200})
            else:
                return '请输入账号'
        except Exception as ex:
            return JsonResponse({'error': ex})
    else:
        return JsonResponse({'code': 403, 'error': '请用post请求'})


def get_blog(request):
    if request.method == 'GET':
        blog_instance = models.Blog.objects.get(id=request.GET.get('id'))
        the_blog_comments = models.Comment.objects.filter(serial_number=blog_instance)
        comments = list(the_blog_comments.values('commentator', 'content', 'comment_time', 'serial_number_id'))
        for comment in comments:
            comment['comment_time'] = comment['comment_time'].strftime('%y-%m-%d %H:%M:%S')
        return JsonResponse({'blog': model_to_dict(blog_instance),
                             'comments': comments
                             })
    else:
        return JsonResponse({'code': 403, 'error': '请用get请求'})
