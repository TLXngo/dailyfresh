from django.urls.conf import re_path,path
from .views import *

urlpatterns = [
    path('',cart),
    re_path(r'^add(\d+)_(\d+)/$',add),

]
