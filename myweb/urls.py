#后台管理子路由文件
import imp
from myweb.views import index
from django.urls import path,include
from myweb.views import index

urlpatterns = [
    path('',index.index,name="myweb_index"),
    path('login',index.login,name="myweb_login"),
    path('dologin',index.dologin,name="myweb_dologin"),
    path('reg',index.reg,name="myweb_reg"),
    path('doreg',index.doreg,name="myweb_doreg"),

    path('booklist',index.booklist,name="myweb_booklist"),
    path('digitallist',index.digitallist,name="myweb_digitallist"),
    path('clothlist',index.clothlist,name="myweb_clothlist"),
    path('dailylist',index.dailylist,name="myweb_dailylist"),
    path('trafficlist',index.trafficlist,name="myweb_trafficlist"),
    path('otherlist',index.otherlist,name="myweb_otherlist"),
    path('goods_details/',index.goods_details,name="myweb_goodsdetails"),
    

    path('after_search/',index.after_search,name="myweb_aftersearch"),
    
    
    

    path("web/",include([
        #path('',index.webindex,name="myweb_webindex"),
        
        path('c_password',index.c_password,name="myweb_c_password"),
        path('do_c_password',index.do_c_password,name="myweb_do_c_password"),
        path('usercenter',index.usercenter,name="myweb_usercenter"),
        path('logout',index.logout,name="myweb_logout"),
        path('release',index.release,name="myweb_release"),
        path('release_goods',index.release_goods,name="myweb_releaseGoods"),
        path('release_records/<int:pIndex>',index.release_records,name="myweb_release_records"),
        path('cart/',index.docart,name="myweb_docart"),
        path('cart',index.cart,name="myweb_cart"),
        path('delcart/',index.delcart,name="myweb_delcart"),
        path('purchase',index.purchase,name="myweb_purchase"),
        path('uedit/',index.uedit,name="myweb_uedit"),
        path('douedit/',index.douedit,name="myweb_douedit"),
        path('delgood/',index.delgood,name="myweb_delgood"),
        path('purchase_records/<int:pIndex>',index.purchase_records,name="myweb_purchase_records"),
        
        
        
        
    ]))

    


]

