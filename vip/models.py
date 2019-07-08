from django.db import models

# 会员
from lib.orm import ModelToDicMixin


class Vip(models.Model,ModelToDicMixin):
    name=models.CharField(max_length=32,unique=True)
    level=models.IntegerField(unique=True,default=0)
    price=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    # max_digits总位数（5） decimal_places 小数点后面的位数（2）999.00

    @property
    def perms(self):
        if not hasattr(self,'_perms'):
            vip_perms = VipPermission.objects.filter(vip_id=self.id).only('perm_id')
            perm_id_list = [p.perm_id for p in vip_perms]
            perms = Permission.objects.filter(id__in=perm_id_list).only('name')
            self._perms=perms

        return self.perms


    def has_perm(self,perm_name):
        '''
        检查当前vip等级是否拥有某种权限
        :param perm_name:
        :return:
        '''
        # 通过vip权限关系表获得vip对应的权限id

        perm_names=[p.name for p in self.perms]

        return perm_name in perm_names


    class Meta:
        db_table='vips'

# 权限
class Permission(models.Model,ModelToDicMixin):
    name=models.CharField(max_length=32,unique=True)
    description=models.TextField()

    class Meta:
        db_table='permissions'

#会员-权限
class VipPermission(models.Model):
    vip_id=models.IntegerField()
    perm_id=models.IntegerField()

    class Meta:
        db_table='vip_permissions'
