from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    '''
    商品类别
    '''
    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    )

    name = models.CharField(max_length=30, default='', verbose_name='类别名', help_text='类别名')
    code = models.CharField(max_length=30, default='', verbose_name='类别code', help_text='类别code')
    desc = models.CharField(max_length=300, default='', verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别', help_text='类目级别')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父类别', help_text='父类别', related_name='sub_cat')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    '''
    品牌名
    '''
    category = models.ForeignKey(GoodsCategory, related_name='brands', on_delete=models.CASCADE, null=True, blank=True, verbose_name='类别', help_text='类别')
    name = models.CharField(max_length=30, default='', verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(max_length=200, default='', verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=200, upload_to='brands/')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'goods_category_brand'
        verbose_name = '品牌名'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class Goods(models.Model):
    '''
    商品
    '''
    category = models.ForeignKey('GoodsCategory', on_delete=models.CASCADE, null=True, blank=True, verbose_name='商品类目', help_text='商品类目')
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一货号')
    name = models.CharField(max_length=300, verbose_name='商品名')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='商品销售量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    goods_num = models.IntegerField(default=0, verbose_name='库存数量')
    market_price = models.FloatField(default=0, verbose_name='市场价')
    shop_price = models.FloatField(default=0, verbose_name='本店价格')
    goods_brief = models.TextField(max_length=500, verbose_name='商品简短描述')
    goods_desc = UEditorField(verbose_name='内容', imagePath='goods/images/', width=1000, height=300, filePath='goods/files/', default='')
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    goods_front_image = models.ImageField(upload_to='', null=True, blank=True, verbose_name='封面图')
    goods_front_image_url = models.CharField(max_length=300, default='', verbose_name='封面图URL')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, related_name='category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='商品类别')
    goods = models.ForeignKey(Goods, related_name='goods', on_delete=models.CASCADE)

    class Meta:
        db_table = 'index_ad'
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsImage(models.Model):
    '''
    商品轮播图
    '''
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, related_name='images', verbose_name='商品')
    image = models.ImageField(upload_to='', null=True, blank=False, verbose_name='图片')
    image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name='图片URL')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    '''
    轮播的图片
    '''
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='banner/', verbose_name='轮播图片')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.goods.name
