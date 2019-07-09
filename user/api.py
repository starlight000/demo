import time
from django.core.cache import cache
from common import utils, errors, config
from lib.http import render_json
from user import logic
from user.forms import ProfileForm
from user.models import User
from urllib.parse import urljoin


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



def get_profile(request):
    # uid=request.GET.get('uid')
    # user=User.objects.get(id=uid)
    # profile=request.objects.get(id=uid)

    user=request.user
    # 1.先从缓存中获取profile_data
    key=config.PROFILE_DATA_CACHE_PREFIX %user.id
    profile_data=cache.get(key)

    # 2.如果缓存中没有，则从数据库获取
    if profile_data is None:
        profile=user.profile
        profile_data=profile.to_dict(exclude=['vibtation','only_matche','auto_play'])
        # logger.debug('get from DB')

    # 3.将profile_data存储到缓存
        cache.set(key,profile_data)
    return render_json(data=profile_data)


def set_profile(request):
    user=request.user

    form=ProfileForm(request.POST,instance=user.profile)

    if form.is_valid():
        profile=form.save(commit=False)
        # 手动创建一对一关系
        profile.id=user.id
        profile.save()

        return render_json()
    else:
        return render_json(data=form.errors)


def upload_avatar(request):
    avatar=request.FILES.get('avatar')
    user=request.user



    # filename='avatar-%s-%d'%(user.id,int(time.time()))
    # filepath=os.path.join(settings.MEDIA_ROOT,filename)
    #
    # with open(filepath,'wb+')as output:
    #     # 切片上传
    #     for chunk in avatar.chunks():
    #         output.write(chunk)


    ret=logic.async_upload_avatar(user,avatar)
    if ret:
        return render_json()
    return render_json(code=errors.AVatarUploadError.code)
