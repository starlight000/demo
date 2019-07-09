#业务返回码，错误码配置
#用于前后段分离返回json码

OK=0

# 用户系统
PHONE_NUM_ERR=1001      #手机号格式错误
SMS_SEND_ERR=1002       #发送验证码失败
VERIFY_CODE_ERR=1003    #验证码错误
LOGIN_REQUIRED=1004     #未登录
AVATAR_UPLOAD_ERR=1005  #avatar上传失败

# 社交系统
LIKE_ERR=2001   #喜欢失败
SID_ERR=2002    #被滑动者不存在




# API层可以通过错误码返回，logic和midels没那么容易返回
class LogicException(Exception):
    def __init__(self,code):
        self.code=code

class LogicError(Exception):
    code=None

def gen_logic_error(name,code):
    return type(name,(LogicError,),{'code':code})

AVatarUploadError=gen_logic_error('AVatarUploadError',1005)  #上传图像失败
SwipeError=gen_logic_error('SwipeError',2001)
SidError=gen_logic_error('SidError',SID_ERR)
RewindLimitError=gen_logic_error('RewindLimitError',2003)   #反悔次数超过每日上线

# vip系统
ViPPerMError=gen_logic_error('ViPPerMError',3001)   #权限错误
