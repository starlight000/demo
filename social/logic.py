# 将views里面重复的代码写到logic中

import datetime

from django.core.cache import cache

from common import config, errors
from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
    '''
    帅选符合user.profile条件的用户
    过滤掉 已经被划过的用户
    :param user:
    :return:
    '''
    today=datetime.date.today()

    # 年龄换算成出生年 18-20岁  18：2019-18=2001（最大年）  20：2019-20=1999（最小年）
    max_year=today.year-user.profile.min_dating_age
    min_year=today.year-user.profile.max_dating_age

    # 只取一个字段
    swiped_users=Swiped.objects.filter(uid=user.id).only('sid')
    swiped_sid_list=[s.sid for s in swiped_users]

    # 过滤掉滑过的人在swiped表中
    users=User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__gte=min_year,
        birth_year__lte=max_year
    ).exclude(id__in=swiped_sid_list)[:20]

    # 打印sql语句
    # print(user.query)

    return users
#
#
def like_someone(uid,sid):
    '''
    创建喜欢的人，如果对方
    :param uid:
    :param sid:
    :return:
    '''
    if not User.objects.filter(id=sid).exists():
        raise errors.SidError

    # 创建滑动记录
    # Swiped.objects.create(uid=uid,sid=sid,mark='like')
    ret=Swiped.swipe(uid=uid,sid=sid,mark='like')
    # 如果被滑动的人喜欢过我，则建立好友关系
    if ret and Swiped.is_liked(sid,uid):
        Friend.make_friends(uid,sid)

    return ret

#
def superlike_someone(uid,sid):
    if not User.objects.filter(id=sid).exists():
        return False

    # 创建滑动记录
    # Swiped.objects.create(uid=uid, sid=sid, mark='superlike')
    ret=Swiped.swipe(uid=uid,sid=sid,mark='superlike')

    # 只有正确滑动的记录
    # 如果被滑动的人喜欢过我，则建立好友关系
    if ret and Swiped.is_liked(sid, uid):
        # Friend.make_friends(uid, sid)
        Friend.objects.make_friends(uid,sid)
        #TODO：向
        return True

    return False
    #
#
def rewind(user):
    '''
    撤销当前登录用户的上一次滑动操作
    每天只能撤销操作三次
    :param user:
    :return:
    '''
    key=config.REWIND_CACHE_PREFIX %user.id

    rewind_times=cache.get(key,0)

    if rewind_times>=config.REWIND_TIMES:
        raise errors.RewindLimitError

    swipe=Swiped.objects.filter(uid=user.id).latest('created_at')

    if swipe.mark in ['like','superlike']:
        Friend.cancel_friends(user.id,swipe.sid)

    swipe.delete()

    now=datetime.datetime.now()
    timeout=86400-now.hour*3600-now.minute*60-now.second
    cache.set(key,rewind_times+1,timeout=timeout)


def liked_me(user):
    swipe_list=Swiped.objects.filter(sid=user.id,mark__in=['like','superlike'])
    # 过滤掉已经加为好友的用户
    # TODO:获得好友列表

    liked_me_uids=[s.uid for s in swipe_list]
    return liked_me_uids