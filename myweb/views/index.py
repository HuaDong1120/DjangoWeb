from datetime import datetime
from logging.config import valid_ident
import time
import imp
import re
from xml.etree.ElementTree import PI
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator


# Create your views here.
from myweb.models import Member,GoodsInfo,CartInfo
from django.shortcuts import redirect
from django.urls import reverse
def index(request):  #首页
     books_list = GoodsInfo.goods.get_books()[0:3]
     digital_list = GoodsInfo.goods.get_digital()[0:3]
     cloth_list = GoodsInfo.goods.get_cloth()[0:3]
     daily_list = GoodsInfo.goods.get_daily()[0:3]
     traffic_list = GoodsInfo.goods.get_traffic()[0:3]
     other_list = GoodsInfo.goods.get_other()[0:3]
     context = {'books_list':books_list, 'digital_list':digital_list, 'cloth_list':cloth_list, 'daily_list':daily_list, 'traffic_list':traffic_list, 'other_list':other_list}
     return render(request,'myweb/goods/index.html',context)

     



def login(request):#登陆页面
     return render(request,'myweb/user/login.html')

def reg(request):  #注册页面
     return render(request,'myweb/user/reg.html')


def dologin(request): #登陆模块
     try:
          member = Member.objects.get(username=request.POST['number'])
        
          
          if member.status == 1:
               s = request.POST['password']
               if member.password == s:
                    print('登陆成功')
                    request.session['user'] = member.toDict()
                    request.session["key"] = member.id
                    
                    
                    return redirect(reverse('myweb_index'))
               else:
                    context = {"info":"登陆密码错误！"}           
          else:
               context = {"info":"无效的登陆账号！"}
     except Exception as err:
          print(err)
          context = {"info":"登陆账号不存在！"}
     return render(request,"myweb/user/login.html",context)

def doreg(request):  #注册模块
     try:
          ob = Member()
          ob.username = request.POST['number']
          ob.nickname = request.POST['username']
          ob.mobile = request.POST['mobile']
          ob.email = request.POST['register_email']
          ob.password = request.POST['password']
          ob.status = 1
          ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          ob.save()  #写入到数据库
          context = {'info':"注册成功！"}
     except Exception as err:
          print(err)
          context = {'info':"注册失败！"}
     return render(request,"myweb/info.html",context)

def usercenter(request):
     return render(request,'myweb/user/user_center.html')


def logout(request):  #退出
     request.session.flush()
     return redirect('/')

def release(request): #发布闲置
     post = request.POST
     title = post.get('title')
     type = post.get('type')
     price = post.get('price')
     address = post.get('address')
     # picture = post.get('picture')
     myfile = request.FILES.get("picture",None)
     
     cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
     destination = open("./static/myweb/goods/"+cover_pic,"wb+")
     for chunk in myfile.chunks():      # 分块写入文件  
          destination.write(chunk)  
     destination.close()
     #print("picture OK",fname)
     description = post.get('description')

     value = request.session.get('key')
     user_id = Member.objects.get(id=value)
     ob = GoodsInfo()
     status = 1
     create_at = datetime.now().strftime("%Y-%m-%d")
     ob = GoodsInfo.goods.create_good(title,type,cover_pic,price,address,description,user_id,create_at,status)
     ob.save()
     return redirect('/')

def release_goods(request):#发布闲置页面
     username = request.session.get('user')
     if username == None:
          context = {'error_msg': '请先登录'}
          return render(request, 'myweb/user/login.html', context)
     else:
          context = {}
          return render(request, 'myweb/goods/release_goods.html', context)



def booklist(request):  #书籍页面
     books_list = GoodsInfo.goods.get_books()
     context = {'books_list':books_list}
     return render(request,"myweb/goods/books_list.html",context)

def digitallist(request):  #数码页面
     digital_list = GoodsInfo.goods.get_digital()
     context = {'digital_list':digital_list}
     return render(request,"myweb/goods/digital_list.html",context)

def clothlist(request):  #衣物页面
     cloth_list = GoodsInfo.goods.get_cloth()
     context = {'cloth_list':cloth_list}
     return render(request,"myweb/goods/cloth_list.html",context)

def dailylist(request): #日常用品
     daily_list = GoodsInfo.goods.get_daily()
     context = {'daily_list': daily_list}
     return render(request,"myweb/goods/daily_list.html",context)

def trafficlist(request):  #交通
     traffic_list = GoodsInfo.goods.get_traffic()
     context = {'traffic_list': traffic_list}
     return render(request,"myweb/goods/traffic_list.html",context)

def otherlist(request):   #其他闲置
     other_list = GoodsInfo.goods.get_other()
     context = {'other_list':other_list}
     return render(request,"myweb/goods/other_list.html",context)


def goods_details(request):  #商品详情页
     id = request.GET['title']
     good = GoodsInfo.goods.get_uid(id)[0]
     # user = UserInfo.objects.filter(id=good.user.id)[0]
     # user = UserInfo.objects.get(id(UserInfo),good.user)[0]
     context = {'good':good}
     print(good.picture)
     return render(request, 'myweb/goods/goods_details.html', context)

def cart(request):  #购物车页面
     value = request.session.get('key')
     user = Member.objects.get(id=value)
     carts = CartInfo.objects.filter(buyer=user,status=1)
     total_price = 0
     total = 0
     for c in carts:
          total = total + 1
          total_price = total_price +c.price
     context = {'carts': carts, 'total_price':total_price, 'total':total}
     return render(request,'myweb/goods/cart.html',context)

def docart(request): #加入购物车
     
     username = request.session.get('user')
     if username == None:
          context = {'info': '请先登录'}
          return render(request,"myweb/user/login.html",context)
     else:
          title = request.GET['title']
          value = request.session.get('key')
          user = Member.objects.get(id=value)
          good1 = GoodsInfo.goods.get_uid(title)[0]
          if value == good1.user.id:
               context = {'info': '这是您自己发布的物品，无法购买！'}
               return render(request,"myweb/info.html",context)

          carts = CartInfo.objects.filter(buyer=user,good=good1)
          if carts.count() > 0:
               print(carts)
               context={'info':'商品已在购物车，请勿重复购买！'}
               return render(request,"myweb/info.html",context)
        
          #user = Member.objects.filter(username=username)[0]
          status = 1
          create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          
          cart = CartInfo.objects.create(title=good1.title,type=good1.type,picture=good1.picture,price=good1.price,buyer=user, good=good1,status=status,create_at=create_at,update_at=update_at)
          cart.save()

          return redirect(reverse('myweb_cart'))
          
     


def delcart(request):  #删除购物车商品
     title = request.GET['title']
     username = request.session.get('key')
     cart = CartInfo.objects.filter(good_id=title,buyer_id=username)[0]
     #print(cart)

     cart.delete()
     return redirect(reverse('myweb_cart'))
     

def after_search(request):    #查询商品
     search_title = request.GET['search_title']
     goods = GoodsInfo.goods.filter(title__contains=search_title)
     print(goods)
     count = GoodsInfo.goods.filter(title__contains=search_title).count()
     print(count)
     context = {'goods':goods, 'search_title':search_title, 'count':count}
     return render(request, 'myweb/goods/after_search.html', context)

def release_records(request,pIndex=1):   #发布的商品
     
     id = request.session.get('key')
     good = GoodsInfo.goods.get_id(id)

     #执行分页处理
     pIndex = int(pIndex)
     page = Paginator(good,2)
     maxpage = page.num_pages
     #判断
     if pIndex > maxpage:
          pIndex = maxpage
     if pIndex < 1:
          pIndex =1
     list2 = page.page(pIndex) #获取当前页数据
     #获取页码列表信息
     plist = page.page_range


     
     # user = UserInfo.objects.filter(id=good.user.id)[0]
     # user = UserInfo.objects.get(id(UserInfo),good.user)[0]
     context = {'good':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpage}
     return render(request,'myweb/user/release_record.html',context)


     
def c_password(request):   #修改密码页面
     return render(request,'myweb/user/c_password.html') 

def do_c_password(request):   #修改密码
     value = request.session.get('key')
     user = Member.objects.get(id=value)
     passw = request.POST['password']
     if user.password != passw:
          context = {'info': '请输入正确的旧密码！'}
          return render(request,"myweb/info.html",context)
     
     c_password= request.POST['new_password']
     c_passowrd_2 = request.POST['c_new_password']

     if c_password != c_passowrd_2:
          context = {'info': '两次输入的新密码不一致，请重新输入！'}
          return render(request,"myweb/info.html",context)
     
     user.password = c_password
     user.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     user.save()
     context={"info":"修改成功,请重新登陆！"}
     request.session.flush()
     return render(request,"myweb/info.html",context)


          
def purchase(request): #执行结算  
     value = request.session.get('key')
     user = Member.objects.get(id=value)
     carts = CartInfo.objects.filter(buyer=user,status=1)
     cart=[] #当前用户加入购物车中的商品又被加入到另外用户的购物车，需要删除的数组
     for c in carts:
          c.status = 2
          c.save()
          cart.append(c.good.id)
          uid = c.good.id
          good = GoodsInfo.goods.get_uid(uid)[0]
          good.status = 2
          good.save()
     for i in cart:     
          d_carts = CartInfo.objects.filter(good_id=i,status=1) #查询已经被购买的商品，但是在购物车表中的数据
          d_carts.delete()
     context={"info":"结算成功！"}
     return render(request,"myweb/info.html",context)     


def uedit(request):#用户修改发布的商品信息
     uid = request.GET['id']
     good = GoodsInfo.goods.get_uid(uid)[0]
     context={"good":good}
     return render(request,"myweb/goods/uedit.html",context)

def douedit(request):#执行修改操作
     uid = request.GET['id']
     good = GoodsInfo.goods.get_uid(uid)[0]
     good.title = request.POST['title']
     good.type = request.POST['type']
     good.price = request.POST['price']
     good.address = request.POST['address']
     good.description = request.POST['description']
     good.save()
     context={"info":"修改成功！"}
     return render(request,"myweb/info.html",context)

def delgood(request):#用户删除自己发布的物品
     id = request.GET['id']
     username = request.session.get('key')
     
     good = GoodsInfo.goods.get_good(id,username)[0]
     #print(cart)

     good.isDelete = 1
     good.save()
     
     return redirect(reverse('myweb_index'))

def purchase_records(request,pIndex=1): #用户的购买记录
     id = request.session.get('key')
     good = CartInfo.objects.filter(buyer_id=id,status=2)

     #执行分页处理
     pIndex = int(pIndex)
     page = Paginator(good,2)
     maxpage = page.num_pages
     #判断边界
     if pIndex > maxpage:
          pIndex = maxpage
     if pIndex < 1:
          pIndex =1
     list2 = page.page(pIndex) #获取当前页数据
     #获取页码列表信息
     plist = page.page_range


     
     # user = UserInfo.objects.filter(id=good.user.id)[0]
     # user = UserInfo.objects.get(id(UserInfo),good.user)[0]
     context = {'good':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpage}
     return render(request,'myweb/user/purchase_record.html',context)