# 存放views里面重复的代码抽象到logic里面
import os
import time
from urllib.parse import urljoin

from django.core.cache import cache
from common import utils, config
from demo import settings
from lib import sms, qiniuyun
from worker import celery_app


def send_verify_code(phone_num):
    '''
    发送验证码
    :param phone_num:
    :return:
    '''

    # 生成验证码
    code=utils.gen_random_code(6)
    # 调用短信接口，发送验证码
    ret= sms.send(phone_num,code)

    if ret:
        cache.set(config.VERIFY_CODE_CACHE_PREFIX % phone_num,code,60*3)
    return ret


def upload_file(filename,f):

    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    with open(filepath, 'wb+')as output:
        # 切片上传
        for chunk in f.chunks():
            output.write(chunk)
    return filepath


def upload_qiniuyun(filename,filepath):

    ret,info=qiniuyun.upload(filename,filepath)

    if info.status_code==200:
        return True
    else:
        return False


# 异步上传七牛云
@celery_app.task
def async_upload_avatar(user,avatar):
    # 上传文件至本地服务器
    filename = 'avatar-%s-%d' % (user.id, int(time.time()))
    filepath = upload_file(filename, avatar)

    # 再将本地文件器文件上传至七牛云
    ret = upload_qiniuyun(filename, filepath)
    if ret:
        user.avatar=urljoin(config.QN_HOST,filename)
        user.save()

    return ret
