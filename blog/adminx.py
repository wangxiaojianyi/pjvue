import xadmin
from xadmin.plugins.actions import BaseActionView
from .models import Post,Comment

# 自定义Action
class MyAction(BaseActionView):
     # 这里需要填写三个属性
     # 1. 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
     action_name = "my_action"
     # 2. 描述, 出现在 Action 菜单中,   
     description = (u'更改用户的激活状态')
     # 3. 该 Action 所需权限
     model_perm = 'change'

     # 而后实现 do_action 方法
     def do_action(self, queryset):
         # queryset 是包含了已经选择的数据的 queryset
         for obj in queryset:
         # 这里对每一个object对象的激活状态取反并保存到数据库，激活的改成未激活，# 未激活的变成激活状态
             obj.isdelete = not(obj.isdelete)
             obj.save()
         # 返回 HttpResponse
         return
# 定义好Action动作，添加到Admin的action属性中

# 自定义模型管理类
class PostAdmin(object):
    list_display = ("id","author", "title", "text", "created_date")
    # search_fields使用了外键，指定具体的字段，如author__username。
    search_fields=("author__username", "title")
    list_filter = ['created_date']     
    # 制定action
    actions = [MyAction, ]

# 注册模型类
xadmin.site.register(Post, PostAdmin)

class CommentAdmin(object):
    list_display = ("author", "post", "text")

# 注册模型类
xadmin.site.register(Comment, CommentAdmin)

