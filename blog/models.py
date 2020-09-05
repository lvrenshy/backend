from django.db import models

# Create your models here.
class Blog(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()


class Comment(models.Model):
    # 评论人
    commentator = models.CharField(max_length=100)
    # 关联文章表中的id,默认为关联对象的主键字段,级联删除
    serial_number = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    # 评论内容
    content = models.CharField(max_length=10000)

    comment_time = models.DateTimeField(null=True)