from django.urls.conf import path,re_path
from .views import *

urlpatterns=[
    path('',index),
    path('index/',index),
    re_path(r'^(\d+)/$',detail),
    re_path(r'^list(\d+)_(\d+)_(\d+)/$',list),
    # path('search/',MySearchView.as_view()),
    # url(r'^search/$',MySearchView()),
]
