from django.urls import include,path

app_label ='blog'

from blog import views

urlpatterns = [
    path('comment', views.commit_comment, name='comment'),
    path('detail',views.get_blog,name='detail')
]