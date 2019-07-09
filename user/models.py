import datetime

from django.db import models

# 存放身份信息
from django.utils.functional import cached_property


from lib.orm import ModelToDicMixin
from vip.models import Vip


class User(models.Model):
    phonenum=models.CharField(max_length=11,unique=True)
    nickname=models.CharField(max_length=32)
    sex=models.IntegerField(default=0)
    birth_year=models.IntegerField(default=2000)
    birth_month=models.IntegerField(default=1)
    birth_day=models.IntegerField(default=1)
    avatar=models.CharField(max_length=256)
    location=models.CharField(max_length=64)

    vip_id=models.IntegerField(default=1)

    # @property    #将方法变成属性
    @cached_property
    def age(self):
        today=datetime.date.today()
        birthday=datetime.date(self.birth_year,self.birth_month,self.birth_day)
        return (today-birthday).days//365

    @property
    def profile(self):
        '''
        user.profile.location
        :return:
        '''
        if not hasattr(self,'_profile'):
            self._profile,_=Profile.objects.get_or_create(id==self.id)

        return self._profile

    @property
    def vip(self):
        '''
        用户的vip信息
        :return:
        '''
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip


    def to_dict(self):
        return {
            'id':self.id,
            'phonenum':self.phonenum,
            'nickname':self.nickname,
            'sex':self.sex,
            'avatar':self.avatar,
            'location':self.location,
            'age':self.age
        }



    class Meta:
        db_table='users'

# 存放个人信息
class Profile(models.Model,ModelToDicMixin):
    '''
    ModelToDicMixin 功能单一的类，一个函数只做一件事，避免多继承带来的问题
    '''

    LOCATIONS={
        ('bj','北京'),
        ('sz','深圳'),
        ('sh','上海'),
        ('gz','广州'),
        ('cd','成都'),
        ('dl','大连')


    }
    SEXS=(
        (0,'全部'),
        (1,'男'),
        (2,'女')
    )

    location=models.CharField(max_length=64,choices=LOCATIONS)
    min_distance=models.IntegerField(default=1)
    max_distance=models.IntegerField(default=10)
    min_dating_age=models.IntegerField(default=18)
    max_dating_age=models.IntegerField(default=81)
    dating_sex=models.IntegerField(default=0,choices=SEXS)

    vibtation=models.BooleanField(default=True)   #开启震动
    only_matche=models.BooleanField(default=True)  #不让为匹配的人看我的相册
    auto_play=models.BooleanField(default=True)    #自动播放视频



    class Meta:
        db_table='profiles'