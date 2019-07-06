# 和业务息息相关的东西，可以放在settings里面，我们在settings里面存放技术相关的东西

# 云之讯短信平台配置
YZX_SMS_URL ='https://open.ucpaas.com/ol/sms/sendsms'

YZX_SMS_PARAMS  = {
	'sid':'ad273bf837671703a95733c111ece66b',
    'token':'82618de96e57f942c8f9442ff72b54c2',
	'appid':'4a2ccc493cc1481ca78d71beb0fe5195',
	'templateid':'481957',
	'param':None,
	'mobile':None
}

# 缓存key prefix：为工程业务增加前缀
VERIFY_CODE_CACHE_PREFIX='verify_code:%s'
REWIND_CACHE_PREFIX='rewind:%s'


# 社交模块配置
REWIND_TIMES=3