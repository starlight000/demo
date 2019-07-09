from django.shortcuts import render

from common import errors
from lib.http import render_json
from social import logic

#
from social.models import Swiped
from social.permissions import has_perm
from user.models import User


def recommend(request):
    '''
    根据当前登录用户profile筛选符合条件的用户
    :param request:
    :return:
    '''

    recm_users=logic.recommend_users(request.user)
    users=[u.to_dict() for u in recm_users]
    print(users)

    return render_json(data=users)

#
def like(request):

    sid=int(request.POST.get('sid'))
    user=request.user

    matched=logic.like_someone(user.id,sid)

    return render_json(data={'matched':matched})

#
#
#
#
def dislike(request):
    sid = int(request.POST.get('sid'))
    user=request.user

    # Swiped.objects.create(uid=user.id,sid=sid,mark='dislike')
    Swiped.swipe(uid=user.id,sid=sid,mark='dislike')


    return render_json()
#
@has_perm('superlike')
def superlike(request):
    sid = int(request.POST.get('sid'))
    user = request.user

    matched = logic.superlike_someone(user.id, sid)

    return render_json(data={'matched': matched})
#
#
# 反悔操作:不需要从客户端获取操作
@has_perm('rewind')
def rewind(request):
    logic.rewind(request.user)
    return render_json()
#
#
@has_perm('liked_me')
def liked_me(request):

    liked_me_uid_list=logic.liked_me(request.user)
    print('----',request.user.id)
    users=User.objects.filter(id__in=liked_me_uid_list)
    user_list=[u.to_dict() for u in users]
    return render_json(data=user_list)


def friends(request):
    return None