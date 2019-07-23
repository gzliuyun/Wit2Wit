from celery import Celery
from django.conf import settings
from django.template import loader
# 在celery_worker的代码文件中上以下几行代码，真正的代码中，wsgi已经帮我们初始化了，所以不需要加这几行----------------------
# 但是这两行import，如果在下面的任务函数中用到了，还是应该有的，不要搞错了
import os

import django
# 设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Wit2Wit.settings")
django.setup()
# 在celery_worker的代码文件中上以下几行代码----------------------


from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner

# 创建Celery类对象，第一个参数可以随便写，一般写路径
app = Celery('utils.celery_works.works', broker='redis://127.0.0.1:6379/2')


@app.task
def generate_static_index():
    '''用于生成静态的首页'''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 组织模板上下文
    context = {'types': types,  # 存放了商品的种类信息，其中还有分类下的首页展示商品信息
               'goods_banners': goods_banners,  # 存放了首页的轮播商品信息
               'promotion_banners': promotion_banners}  # 存放了促销活动的信息

    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')  # 这里需要绝对路径
    with open(save_path, 'w') as f:
        f.write(static_index_html)
