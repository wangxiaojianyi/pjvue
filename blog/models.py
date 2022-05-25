import datetime
from django.db import models
from django.utils import timezone


class Post (models.Model):
    author = models.ForeignKey('auth.User',related_name='作者', on_delete=models.CASCADE,default=1)
    title = models.CharField('标题',max_length=200)
    text = models.TextField('内容',)
    created_date = models.DateTimeField('创建时间',default=timezone.now)
    published_date = models.DateTimeField('发表时间',blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def was_published_recently(self):
        return timezone.now() >= self.published_date >=\
               timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'published_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.title
    # admin管理界面中显示中文model名称
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '[文章]'


class Comment (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,default=1)
    text = models.TextField('评论内容')

    def publish(self):
        self.save()

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '[评论]'



