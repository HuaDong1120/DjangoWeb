from django.db import models
from datetime import datetime
# Create your models here.
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)    #员工账号
    nickname = models.CharField(max_length=50)    #昵称
    password = models.CharField(max_length=128)#密码
    mobile = models.CharField(max_length=50)    #密码干扰值
    email = models.CharField(max_length=254)    #密码干扰值
    status = models.IntegerField(default=1)    #状态:1正常/2禁用/6管理员/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password':self.password,'mobile':self.mobile,'email':self.email,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "member"  # 更改表名


class GoodsInfoManager(models.Manager):
    def get_books(self):
        return super(GoodsInfoManager, self).get_queryset().filter(type='闲置书籍',isDelete=0,status=1)
    def get_digital(self):
        return super(GoodsInfoManager, self).get_queryset().filter(type='数码电子',isDelete=0,status=1)
    def get_cloth(self):
        return super(GoodsInfoManager, self).get_queryset().filter(type='鞋服佩饰',isDelete=0,status=1)
    def get_daily(self):
        return super(GoodsInfoManager, self).get_queryset().filter(type='日用物品',isDelete=0,status=1)
    def get_traffic(self):
        return super(GoodsInfoManager, self).get_queryset().filter(type='出行交通',isDelete=0,status=1)
    def get_other(self):
        return super(GoodsInfoManager, self).get_queryset().filter(type='其他闲置',isDelete=0,status=1)
    def get_title(self, title):
        return super(GoodsInfoManager, self).get_queryset().filter(title=title,isDelete=0,status=1)
    def get_id(self, uid):
        return super(GoodsInfoManager, self).get_queryset().filter(user_id=uid,isDelete=0,status=1)
    def get_uid(self, uid):
        return super(GoodsInfoManager, self).get_queryset().filter(id=uid,isDelete=0,status=1)
    def get_good(self, uid,uuid):
        return super(GoodsInfoManager, self).get_queryset().filter(id=uid,user_id=uuid,isDelete=0)

    def create_good(self, title, type, picture, price, address, description, user,create_at,status):
        book = self.create(title=title, type=type, picture=picture, price=price, address=address, description=description,user=user,create_at=create_at,status=status, isDelete=0)
        return book


# Create your models here.
class GoodsInfo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)  #名称
    type = models.CharField(max_length=20)  # 类型
    picture = models.ImageField(upload_to='goods')  #图片
    price = models.DecimalField(max_digits=10,decimal_places=2) #价格
    isDelete = models.BooleanField(default=False)  #删除
    address = models.CharField(max_length=100, default='', blank=True)  #交易地点
    description = models.CharField(max_length=300, default='', blank=True) #描述
    status = models.IntegerField(default=1)    #状态:1用户发布 2已被购买
    user = models.ForeignKey(Member,on_delete=models.CASCADE) #商家Id
    create_at = models.DateTimeField(default=datetime.now)  
    goods = GoodsInfoManager()
   
    class Meta:
        db_table = "goods_goodsinfo"
    def __str__(self):
        return self.title

class CartInfo(models.Model):
    title = models.CharField(max_length=20,default='')  #名称
    type = models.CharField(max_length=20,default='')  # 类型
    picture = models.ImageField(upload_to='goods',default='')  #图片
    number = models.CharField(max_length=20,default='1')  # 数量
    price = models.DecimalField(max_digits=10,decimal_places=2,default='') #价格
    status = models.IntegerField(default=1)    #状态:1加入购物车 2已经购买
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间
    buyer = models.ForeignKey(Member,on_delete=models.CASCADE) # 买家Id
    good = models.ForeignKey(GoodsInfo,on_delete=models.CASCADE)  # 商品Id
    
    class Meta:
        db_table = "cart_cartinfo"
