from django.db import models


# 划过的记录
from common import errors
from common.errors import LogicException


class Swiped(models.Model):

    MARKS=(
        ('like','喜欢'),
        ('dislike','不喜欢'),
        ('superlike','超级喜欢')
    )

    uid=models.IntegerField()
    sid=models.IntegerField()
    mark=models.CharField(max_length=16,choices=MARKS)    #动作
    created_at=models.DateField(auto_now_add=True)  #记录动作是什么时候发生的

    @classmethod
    def is_liked(cls,sid,uid):
        return cls.objects.filter(uid=sid,sid=uid,
                                      mark__in=['like','superlike']).exists()

    @classmethod
    def swipe(cls,uid,sid,mark):
        '''
        :param uid:
        :param sid:
        :param mark:
        :return:
            如果滑动成功，返回True,否则返回False
        '''
        marks=[m for m,_ in cls.MARKS]
        if mark not in marks:
            raise LogicException(errors.SWIPE_ERR)
        if cls.objects.filter(uid=uid,sid=sid).exists():
            return False
        else:
            cls.objects.create(uid=uid,sid=sid,mark=mark)
            return True


    class Meta:
        db_table='swiped'


class FriendManager(models.Manager):
    """
    自定义 Manager，扩充 models.Manager 的默认行为，增加和业务相关的方法
    """

    def make_friends(self, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 <= uid2 else (uid2, uid1)
        # self.create(uid1=uid1, uid2=uid2)
        self.get_or_create(uid1=uid1, uid2=uid2)
#
class Friend(models.Model):
    '''
    好友关系：双向关系

    uid  fid
    1     23
    1     45
    1     56
    23     1
    45     1
    56     1
    '''
    objects=FriendManager()
    uid1=models.IntegerField()
    uid2=models.IntegerField()


    @classmethod   #类方法
    def make_friends(cls,uid1,uid2):
        '''

        :param uid1:
        :param uid2:
        :return:
        '''
        uid1,uid2=(uid1,uid2) if uid1 <= uid2 else (uid2,uid1)

        cls.objects.create(uid1=uid1,uid2=uid2)


    @classmethod
    def cancel_friends(cls,uid1,uid2):
        uid1,uid2=(uid1,uid2) if uid1 <= uid2 else (uid2,uid1)
        cls.objects.filter(uid1=uid1,uid2=uid2).delete()

    class Meta:
        db_table='friends'


