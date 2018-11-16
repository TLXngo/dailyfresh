from django.urls.conf import re_path,path
from .views import *

urlpatterns = [
    path('',cart),
    re_path(r'^add(\d+)_(\d+)/$',add),
    re_path(r'^edit(\d+)_(\d+)/$',edit),
    re_path(r'^delete(\d+)/$',delete),

]
