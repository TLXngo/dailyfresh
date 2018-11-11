from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from hashlib import sha1
from .models import *
import df_user.user_decorator
from df_goods.models import *

def register(request):
    context = {'title': '用户注册 天天生鲜'}
    return render(request, 'df_user/register.html', context)

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    if upwd != upwd2:
        return redirect('/user/register/')
    # 加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()
    # 创建对象保存
    user = UserInfo()
    user.upwd = upwd3
    user.uname = uname
    user.uemail = uemail
    user.save()
    # 进入登陆页面
    return redirect('/user/login/')

def register_exit(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    print(count)
    return JsonResponse({'count': count})

def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登陆 天天生鲜', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url','/')
            read = HttpResponseRedirect(url)
            if jizhu!=0:
                read.set_cookie('uname',uname)
            else:
                read.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name'] = users[0].uname
            return read

        else:
            context = {'title': '用户登陆 天天生鲜', 'error_name': 0, 'error_pwd': 1, 'uname': uname,}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登陆 天天生鲜', 'error_name': 1, 'error_pwd': 0, 'uname': uname,}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

@df_user.user_decorator.login
def info(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 最近浏览
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_ids1=goods_ids.split(',')
    # goods_list=GoodsInfo.objects.filter(id__in=goods_ids1)
    goods_list=[]
    if goods_ids!='':
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))


    context={'title':'天天生鲜-用户中心','user_name':request.session['user_name'],'user':user,'page_name':1,
             'goods_list':goods_list}
    return render(request, 'df_user/user_center_info.html',context)

@df_user.user_decorator.login
def order(request):
    context = {'title': '天天生鲜-我的订单','page_name':1}
    return render(request,'df_user/user_center_order.html',context)

@df_user.user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post = request.POST
        user.uphone=post.get('uphone')
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.save()
    context= {'title':'天天生鲜-我的信息','user':user,'page_name':1}
    return render(request,'df_user/user_center_site.html',context)
