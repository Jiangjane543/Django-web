from django.contrib import admin
from learning.models import Topic,Entry
# Register your models here.
admin.site.register(Topic) #通过管理网站管理
admin.site.register(Entry)