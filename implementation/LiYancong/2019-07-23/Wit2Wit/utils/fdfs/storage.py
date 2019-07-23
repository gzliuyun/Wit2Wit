from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    '''fdfs自定义存储类'''

    def __init__(self, client_conf=None, base_url=None):
        '''Django必须能够不带任何参数来实例化存储类，这意味着任何设置都应该从django.conf.settings中获取'''
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    # 下面的方法代表了私有方法的一个公共接口，除非绝对的需要，这些方法不应该被子类覆盖
    def _open(self, name, mode='rb'):
        '''从存储中检索特定的文件，被Storage.open()调用，这是储存类用于打开文件的实际工具。它必须返回File对象'''
        return self._open(name, mode)

    # 被Storage.save()调用。name必须事先通过get、_valid_name()和get_available_name()过滤，并且content自己必须是一个File对象
    def _save(self, name, content):
        '''用给定的文件名保存给定的新内容，内容应该是一个合适的可以从头开始读取的File对象'''
        # 创建Fdfs_client对象
        client = Fdfs_client(self.client_conf)

        # 向fdfs上传文件
        res = client.upload_by_buffer(content.read())
        # 判断上传文件的状态是否成功
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('文件上传失败')

        # Remote file_id是字典里的返回值
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        '''如果提供的名称所引用的文件在文件系统中存在，则返回True，否则如果这个名称可用于新文件，返回False'''
        # 这里的文件名永远都是可用的
        return False

    def url(self, name):
        '''返回访问文件的url路径'''
        return self.base_url + name
