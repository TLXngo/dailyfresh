from django.urls.conf import path,re_path
from .views import *

urlpatterns=[
    path('',order),
    path('order_handle/',order_handle),
    re_path(r'^pay_(\d+)/$',pay),

]
