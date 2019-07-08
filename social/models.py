# from django.db import models
#
#
# # 划过的记录
# class Swiped(models.Model):
#
#     MARKS=(
#         ('like','喜欢'),
#         ('dislike','不喜欢'),
#         ('superlike','超级喜欢')
#     )
#
#     uid=models.IntegerField()
#     sid=models.IntegerField()
#     mark=models.CharField(max_length=16,choices=MARKS)
#     created_at=models.DateField(auto_now_add=True)
#
#     def is_liked(self):
#         def is_liked(cls,sid,uid):
#             return cls.objects.filter(uid=sid,sid=uid,
#                                       mark__in=['like','superlike'])
#
#     class Meta:
#         db_table='swiped'
#
#
# class Friend(models.Model):
#     '''
#     好友关系：双向关系
#
#     uid  fid
#     1     23
#     1     45
#     1     56
#     23     1
#     45     1
#     56     1
#     '''
#     uid1=models.IntegerField()
#     uid2=models.IntegerField()
#
#
#     @classmethod   #类方法
#     def make_friends(cls,uid1,uid2):
#         '''
#
#         :param uid1:
#         :param uid2:
#         :return:
#         '''
#         uid1,uid2=(uid1,uid2) if uid1<=uid2 else (uid2,uid1)
#
#         cls.objects.create(uid1=uid1,uid2=uid2)
#
#     @classmethod
#     def cancel_friends(cls,uid1,uid2):
#         uid1,uid2=
#
#     class Meta:
#         db_table='friends'
#
