# 存放views里面重复的代码抽象到logic里面

from django.core.cache import cache
from common import utils, config
from lib import sms


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