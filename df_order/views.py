import datetime

from django.shortcuts import render
from df_user.user_decorator import login
from df_user.models import UserInfo
from df_goods.models import GoodsInfo
from df_cart.models import *
from django.db import transaction
from .models import *
from decimal import Decimal
from django.http import JsonResponse

@login
def order(request):
    uid=request.session.get('user_id')
    user=UserInfo.objects.get(pk=int(uid))

    # 获取订单对象
    order_id=request.GET.getlist('order_id')
    order_list=[]

    for id in order_id:
        order_list.append(CartInfo.objects.get(pk=int(id)))

    if user.uphone == '':
        uphone=''
    else:
        uphone=user.uphone[0:4]+'****'+user.uphone[-4:]

    # 构造上下文
    context={'title':'提交订单','uphone':uphone,'page_name':1,'user':user,'order_list':order_list}
    return render(request,'df_order/place_order.html',context)


'''
1.创建订单对象
2.判断商品库存
3.创建详单对象
4.修改库存
5.删除购物车
'''
@transaction.atomic()
@login
def order_handle(request):
    trans_id=transaction.savepoint()
    # 购物车编号
    try:
        post=request.POST
        order_list=post.getlist('id[]')
        print(order_list)
        total=post.get('total')
        address=post.get('address')
        print(address)

        order=OrderInfo()
        now=datetime.datetime.now()
        uid = request.session['user_id']
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        print(order.oid)
        order.user_id=uid
        order.odate=now
        order.ototal=Decimal(total)
        order.oaddress=address
        order.save()

        # 创建详单
        for order_id in order_list:
            print(order_id)
            cartinfo=CartInfo.objects.get(id=order_id)
            good=GoodsInfo.objects.get(id=cartinfo.goods_id)
            if int(good.gkucun) >= int(cartinfo.count):
                print("库存")
                # 库存够
                good.gkucun-=cartinfo.count
                good.save()

                goodinfo=GoodsInfo.objects.get(cartinfo__id=order_id)

                detailinfo=OrderDetailInfo()
                detailinfo.goods_id=int(goodinfo.id)
                detailinfo.order_id=int(order.oid)
                detailinfo.price=Decimal(int(goodinfo.gprice))
                detailinfo.count=int(cartinfo.count)
                detailinfo.save()

                cartinfo.delete()
            else:
                transaction.savepoint_rollback(trans_id)
                return JsonResponse({'status':2})
    except Exception as e:
        transaction.savepoint_rollback(trans_id)

    return JsonResponse({'status': 1})

def pay(request,oid):
    tran_id = transaction.savepoint()
    # try:
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = 1

    order.save()
    print('*' * 10)
    print(order.oid)
    context = {'oid': oid}
    return render(request, 'df_order/pay.html', context)