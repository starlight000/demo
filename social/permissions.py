from common import errors


def has_perm(perm_name):
    '''
    @has_perm('superlike')
    :param perm_name:
    :return:
    '''
    def decorator(view_func):
        def wapper(request,*args,**kwargs):
            user=request.user
            if user.vip.has_perm(perm_name):
                return view_func(request,*args,**kwargs)
            else:
                raise errors.ViPPerMError
        return wapper
    return decorator
