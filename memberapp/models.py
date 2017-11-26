from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

# 商品类型


class GoodsType(models.Model):
    title = models.CharField('名称', max_length=30)
    desc = models.CharField('描述', max_length=200, default='商品描述')
    flag = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='static/image/good_type', default='normal.png')
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta():
        db_table = 'goods_Type'


# 商品字段
class Goods(models.Model):
    title = models.CharField('名称', max_length=50)
    price = models.DecimalField('商品价格', max_digits=8, decimal_places=2)
    desc = models.CharField('描述', max_length=1000, default='商品的描述信息')
    picture = models.ImageField('商品照片', upload_to='static/images/goods',default='normal.png')
    isDelete = models.BooleanField(default=False)
    type = models.ForeignKey(GoodsType)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/good/detail/?good={}/'.format(self.id)

    class Meta():
        db_table = 'goods'
        ordering = ['id']   # 默认按照id方式排序 否则会有无序列表警告


