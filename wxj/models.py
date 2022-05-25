from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.db.models.signals import post_save

# Create your models here.
# 另一种方式 使用 Profile 模式拓展用户模型
# 在settings.py中设置要使用的UserProfile Model 信息，如：
# AUTH_PROFILE_MODULE = 'wxj.UserProfile'
# 在使用时，先得到user，然后通过user提供的get_profile()来得到profile对象，如：
# user.get_profile().nickname
# 需要注意的一点是，Profile对象不会和User一起自动创建，需要以某种方式自己搞定这件事情。
# 最合理的最Djangoist的方式就是注册一个handler到User的post_save signal了。

from django.contrib.auth.models import User
class Profile(models.Model):
    gender_choices = (
        ('M','男'),
        ('F','女')
    )
    nickname = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    depart  = models.CharField('部门',max_length=50, null=True,blank=True)
    chejian  = models.CharField('车间',max_length=50,null=True, blank=True)
    gangwei  = models.CharField('岗位',max_length=50, null=True,blank=True)
    birthday = models.DateField('生日',null=True,blank=True)
    gender = models.CharField('性别',max_length=10,choices=gender_choices,default='F')
    address = models.CharField('地址',max_length=100,default='', null=True,blank=True)
    mobile = models.CharField('手机号',max_length=11,null=True,blank=True)
    mima  = models.CharField('标记',max_length=50, null=True,blank=True)
    remark  = models.CharField('备注',max_length=200, null=True,blank=True)
    image = models.ImageField(upload_to='image/user/%Y',default='image/user/default.png',max_length=100)

def create_user_profile(sender, instance, created, **kwargs):
     if created:
         Profile.objects.create(user = instance)
 
post_save.connect(create_user_profile, sender = User)


# class User(AbstractUser):
#     """
#     Users within the Django authentication system are represented by this model.
#     Username, password and email are required. Other fields are optional.
#     """
#     gender_choices = (
#         ('M','男'),
#         ('F','女')
#     )
#     nickname = models.CharField('昵称',max_length=50, null=True,blank=True)
#     depart  = models.CharField('部门',max_length=50, null=True,blank=True)
#     chejian  = models.CharField('车间',max_length=50,null=True, blank=True)
#     gangwei  = models.CharField('岗位',max_length=50, null=True,blank=True)
#     birthday = models.DateField('生日',null=True,blank=True)
#     gender = models.CharField('性别',max_length=10,choices=gender_choices,default='F')
#     address = models.CharField('地址',max_length=100,default='', null=True,blank=True)
#     mobile = models.CharField('手机号',max_length=11,null=True,blank=True)
#     mima  = models.CharField('标记',max_length=50, null=True,blank=True)
#     remark  = models.CharField('备注',max_length=200, null=True,blank=True)
#     image = models.ImageField(upload_to='image/user/%Y',default='image/user/default.png',max_length=100)

#     class Meta(AbstractUser.Meta):
#         verbose_name = '用户信息'
#         verbose_name_plural = verbose_name

#     def __str__(self):
#         # AbstractUser这个类里面有 username这个属性
#         return self.username

class TodoItem(models.Model):
    """
    OA发送事项
    """
    LV_CHOICES = {
        1: '普通',
        2: '重要',
        3: '非常重要',
    }
    title = models.CharField('标题',max_length=200)
    initiator = models.ForeignKey(User, verbose_name='发起人',on_delete=models.CASCADE)
    contents = models.TextField('内容',null=True,blank=True)
    recipients = models.CharField('接收人列表',max_length=200,null=True,blank=True)
    selid = models.CharField('接收人id列表', max_length=200, null=True, blank=True)
    level = models.SmallIntegerField('等级',default=1, choices=LV_CHOICES.items(),null=True,blank=True)
    time_send = models.DateTimeField('发送时间')
    time_new = models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    time_edit = models.DateTimeField('修改时间',auto_now = True,null=True,blank=True)
    remark = models.CharField('备注',max_length=200,null=True,blank=True)
    status = models.SmallIntegerField('状态',default=1)
    deleted = models.SmallIntegerField('已删除',default=0)
    # upfile = models.FileField("附件",upload_to='oa/%Y/%m/%d/',null=True,blank=True)
    upfiles = models.ManyToManyField('OAfiles')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "wxj_oa"
        verbose_name = "OA事项"
        verbose_name_plural = verbose_name

class OAfiles(models.Model):
    title = models.CharField('标题', max_length=200)
    upfile = models.FileField("附件", upload_to='oa/%Y/%m/%d/', null=True, blank=True)
    
    class Meta:
        verbose_name = "OA附件"
        verbose_name_plural = verbose_name