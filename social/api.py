from django.shortcuts import render

from common import errors
from lib.http import render_json
from social import logic

#
def recommend(request):
    pass

    # recm_users=logic.recommend_users(request.user)
    # users=[u.to_dict() for u in recm_users]
    #
    #
    # return render_json(data=users)

#
def like(request):
    pass
    # sid=request.POST.get('sid')
    # user=request.user
    #
    # if logic.like_someone(user.id,sid):
    #     return render_json()
    # else:
    #     return render_json(errors.LIKE_ERR)
#
#
#
#
# def dislike(request):
#     return None
#
#
# def superlike(request):
#     sid=
#
#
# # 反悔操作:不需要从数据库获取操作
# def rewind(request):
#     logic.rewind()
#     return None
#
#
# def liked_me(request):
#     return None
#
#
# def friends(request):
#     return None