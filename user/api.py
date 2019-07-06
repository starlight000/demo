from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from common import utils, errors, config
from lib.http import render_json
from user import logic
from user.models import User


def verify_phone(request):
    '''
    验证手机号并发送验证码接口
    :param request:
    :return:
    '''
    phone_num=request.POST.get('phone_num','')
    phone_num=phone_num.strip()

    # 验证手机号
    if utils.is_phone_num(phone_num.strip()):
        # 生成并发送随机验证码
        if logic.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SMS_SEND_ERR)
    return render_json(code=errors.PHONE_NUM_ERR)


def login(request):
    '''
    登录接口
    :param request:
    :return:
    '''
    phone_num=request.POST.get('phone_num','')
    code=request.POST.get('code','')

    phone_num=phone_num.strip()
    code=code.strip()

    # 1.检查验证码
    cached_code=cache.get(config.VERIFY_CODE_CACHE_PREFIX % phone_num)
    if cached_code !=code:
        return render_json(code=errors.VERIFY_CODE_ERR)

    # 2.登录或注册

    # 捕获错误（不能全盘吃掉错误，尽量捕获多的错误，解决它）
    # try:
    #     user=User.objects.get(phone=phone)
    # except User.DoesNotExist:
    #     user=User.objects.create(phone=phone)

    user,created=User.objects.get_or_create(phonenum=phone_num)
    request.session['uid']=user.id

    return render_json(data=user.to_dict())



# def get_profile(request):
    # uid=request.GET.get('uid')
    # user=User.objects.get(id=uid)
    #pid=request.objects.get(id=uid)
    # profile=request.user.profile
    # return render_json(data=profile.to_dict(exclude=[]))



# def det_profile(request):
#     user=request.user
#     form=ProfileForm(request.POST,instance=user.profile)
#
#     if form.is_valid():
#         form.save()


# def upload_avatar(rwquest):
#     avatar=request.FILES.get('avatar')
#
#     with open(filepath,'wb+')as output:
#         for chunk in avator.chunks():
#             output.write()
