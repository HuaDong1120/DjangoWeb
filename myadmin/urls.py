#后台管理子路由文件
import imp
from myadmin.views import index
from django.urls import path
from myadmin.views import user
urlpatterns = [
   path('',index.index,name="myadmin_index"),

   #管理员登陆,退出路由
   path('login',index.login,name="myadmin_login"),
   path('dologin', index.dologin, name="myadmin_dologin"),
   path('logout', index.logout, name="myadmin_logout"),
   path('verify', index.verify, name="myadmin_verify"),



   #管理员信息管理路由
   path('user/<int:pIndex>',user.index,name="myadmin_user_index"),
   path('shop/<int:pIndex>',user.shop,name="myadmin_user_shop"),
   path('order/<int:pIndex>',user.order,name="myadmin_user_order"),
   
   path('user/add', user.add, name="myadmin_user_add"),   
   path('user/insert',user.insert,name="myadmin_user_insert"),
   path('user/del/<int:uid>',user.delete,name="myadmin_user_delete"),
   path('user/edit/<int:uid>',user.edit,name="myadmin_user_edit"),
   path('user/update/<int:uid>',user.update,name="myadmin_user_update"),
]
