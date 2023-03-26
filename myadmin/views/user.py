
from  django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
#管理员信息管理的视图文件
from myadmin.models import User
from datetime import datetime

from myweb.models import CartInfo, GoodsInfo
def index(request,pIndex=1):
    '''浏览信息'''
    umod = User.objects
    ulist = umod.filter(status__lt=9)
    mywhere = []
    #获取并判断搜索条件
    kw=request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword='+kw)
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist,5)#5条分页
    maxpages = page.num_pages #获取最大页数
    #判断
    if pIndex > maxpages:
        pIndex  = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页码数
    plist = page.page_range #获取当前页码列表
    context = {"userlist":list2,'plist':plist,'pIndex':pIndex,"maxpages":maxpages,'mywhere':mywhere}
    return render(request,"myadmin/user/index.html",context)

def shop(request,pIndex=1):
    
    ulist = GoodsInfo.goods.filter(isDelete__contains=0)
    mywhere = []
    #获取并判断搜索条件
    kw=request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(title__contains=kw)
        mywhere.append('keyword='+kw)




    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist,5)#5条分页
    maxpages = page.num_pages #获取最大页数
    #判断
    if pIndex > maxpages:
        pIndex  = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页码数
    plist = page.page_range #获取当前页码列表
    context = {"userlist":list2,'plist':plist,'pIndex':pIndex,"maxpages":maxpages,'mywhere':mywhere}
    return render(request,"myadmin/user/shop.html",context)


def order(request,pIndex=1):
    ulist = CartInfo.objects.filter(status__contains=2)
    mywhere = []
    #获取并判断搜索条件
    kw=request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(title__contains=kw)
        mywhere.append('keyword='+kw)




    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist,5)#5条分页
    maxpages = page.num_pages #获取最大页数
    #判断
    if pIndex > maxpages:
        pIndex  = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页码数
    plist = page.page_range #获取当前页码列表
    context = {"userlist":list2,'plist':plist,'pIndex':pIndex,"maxpages":maxpages,'mywhere':mywhere}
    return render(request,"myadmin/user/order.html",context)




def add(request):
    '''加载添加页面'''
    return render(request,"myadmin/user/add.html")

def insert(request):
    '''执行信息添加'''
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        #获取密码并md5
        import hashlib,random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n)  #从表单获取密码并添加干扰值
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()  #获取md5值
        ob.password_salt = n

        ob.status = 6
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()  #写入到数据库
        context = {'info':"添加成功！"}
    except Exception as err:
        print(err)
        context = {'info':"添加失败！"}
    return render(request,"myadmin/info.html",context)

def delete(request,uid=0):
    '''执行信息删除'''
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}

    return render(request,"myadmin/info.html",context)




def edit(request,uid=0):
    '''加载信息编辑表单'''
    try:
        ob = User.objects.get(id=uid)
        context={"user":ob}
        return render(request,"myadmin/user/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,uid):
    '''执行信息编辑'''
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"myadmin/info.html",context)

