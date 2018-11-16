from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from df_user.user_decorator import *

@login
def cart(request):
    uid = request.session['user_id']
    carts=CartInfo.objects.filter(user_id=uid)
    context = {'page_name':1,
               'carts':carts,
               'title':'购物车',}
    return render(request,'df_cart/cart.html',context)

@login
def add(request,gid,count):
    uid = request.session['user_id']
    gid=int(gid)
    count=int(count)
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    # 如果已经添加过了
    if len(carts)>0:
        cart=carts[0]
        cart.count=cart.count+count
    # 没添加过
    else:
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=count
        print(count)
        print(request.session.get('count'))
    cart.save()

    count = CartInfo.objects.filter(user_id=uid).count()
    request.session['count'] = count
    # 如果是ajax请求则返回json，否则转向购物车
    if request.is_ajax():
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')

@login
def edit(request,cart_id,count):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)

@login
def delete(request,cart_id):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)
