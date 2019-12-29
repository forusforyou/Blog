from django.db import models

# Create your models here.


class User(models.Model):
    user = models.CharField("用户名", max_length=64)
    pwd = models.CharField("密码", max_length=128)

    def __str__(self):
        return self.user


class Comment(models.Model):
    create_time = models.DateField("创建时间")
    content = models.TextField('内容')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField("标题", max_length=64)
    content = models.TextField('内容')
    create_time = models.DateField('创建时间')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title