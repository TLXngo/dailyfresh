from django.http import HttpResponseRedirect

# 如果未登录 转到登陆界面
def login(func):
    def login_func(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            print(request.get_full_path())
            red.set_cookie('url',request.get_full_path())
            return red
    return login_func
