# 和业务息息相关的东西，可以放在settings里面，我们在settings里面存放技术相关的东西

# 缓存key prefix：为工程业务增加前缀
VERIFY_CODE_CACHE_PREFIX='verify_code:%s'
REWIND_CACHE_PREFIX='rewind:%s'
PROFILE_DATA_CACHE_PREFIX='profile_data:%s'


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

# 七牛云配置
QN_ACCESS_KEY='W3Fxn5M_zrmCrPRW8ggZIOQqz-51P05rd_wtJkMc'
QN_SECERT_KRY='ZqTW8bi4IFz7pmgqYwcrotZB8_Z59SN_9O0a_uKa'
QN_BUCKET='demo'
QN_HOST='http://pu5fi2h1r.bkt.clouddn.com'

# 社交模块配置
REWIND_TIMES=3