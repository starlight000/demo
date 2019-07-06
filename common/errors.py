#业务返回码，错误码配置
#用于前后段分离返回json码

OK=0

# 用户系统
PHONE_NUM_ERR=1001      #手机号格式错误
SMS_SEND_ERR=1002       #发送验证码失败
VERIFY_CODE_ERR=1003    #验证码错误
LOGIN_REQUIRED=1004

# 社交系统
LIKE_ERR=2001   #喜欢失败
