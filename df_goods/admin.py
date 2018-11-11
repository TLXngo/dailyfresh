from django.contrib import admin
from .models import *

@admin.register(TypeInfo)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle','isDelete']

@admin.register(GoodsInfo)
class GoodsAdmin(admin.ModelAdmin):
    list_display = [
        'id','gtype','isDelete',
    ]
