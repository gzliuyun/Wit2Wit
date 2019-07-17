# 定义索引类
from haystack import indexes
# 导入你的模型类
from goods.models import GoodsSKU


# 指定对于某个类的某些数据建立索引
# 推荐的索引类名格式:模型类名+Index
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # document=True说明这是一个索引字段，use_template=True指定根据表中的哪些字段建立索引文件，索引说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    # 返回GoodsSKU模型类
    def get_model(self):
        return GoodsSKU

    # 对那些数据建立索引？这里是GoodsSKU表中的全部数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
