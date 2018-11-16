from django.urls.conf import path,include,re_path
from .views import *

urlpatterns=[
    path('register/', register),
    path('register_handle/',register_handle),
    path('register_exit/',register_exit),
    path('login/',login),
    path('login_handle/',login_handle),
    path('info/',info),
    path('order/',order),
    path('site/',site),
    path('logout/',logout),
    re_path(r'^user_center_order&(\d+)/$',user_center_order)

]