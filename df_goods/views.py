from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.http import HttpResponse


def index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type02 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type03 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type04 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'title': '首页', 'guest_cart': 1,
               'type0': type0, 'type01': type01,
               'type1': type1, 'type02': type02,
               'type2': type2, 'type03': type03,
               'type3': type3, 'type04': type04, }
    return render(request, 'df_goods/index.html', context)


def detail(request, id):
    goods = GoodsInfo.objects.get(id=int(id))
    goods.gclick += 1
    goods.save()
    typeinfo = goods.gtype
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': goods.gtitle, 'guest_cart': 2, 'g': goods, 'news': news, 'id': id, 'typeinfo': typeinfo}
    response = render(request, 'df_goods/detail.html', context)

    # 记录最近浏览过的信息
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d' % goods.id
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) >= 1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id
    response.set_cookie('goods_ids', goods_ids)
    return response


def list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.filter(pk=int(tid))

    news = typeinfo[0].goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':  # 默认最新
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    if sort == '2':  # 价格
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    if sort == '3':  # 人气
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list, 2)
    page = paginator.page(int(pindex))
    context = {'title': '首页', 'guest_cart': 3,
               'page': page, 'news': news,
               'goods_list': goods_list,
               'sort': sort, 'typeinfo': typeinfo[0],
               'paginator': paginator,
               }
    return render(request, 'df_goods/list.html', context)

#
# from haystack.generic_views import SearchView
# from dailyfresh import settings
#
# class MySearchView(SearchView):
#     def build_page(self,*args, **kwargs):
#         #分页重写
#         context=super().extra_context(*args, **kwargs)   #继承自带的context
#         try:
#             page_no = int(self.request.GET.get('page', 1))
#         except Exception:
#             return HttpResponse("Not a valid number for page.")
#
#         if page_no < 1:
#             return HttpResponse("Pages should be 1 or greater.")
#         a =[]
#         for i in self.results:
#             a.append(i.object)
#         paginator = Paginator(a, 18)
#         # print("--------")
#         # print(page_no)
#         page = paginator.page(page_no)
#         return (paginator,page)
#
#     def extra_context(self,*args, **kwargs):
#         context = super().extra_context(*args, **kwargs)  # 继承自带的context
#         context['title']='搜索'
#         return context