def check(func):
    def wapper(a):
        b=func(a)
        if b<0:
            return 0
        return b
    return wapper


