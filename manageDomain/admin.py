from django.contrib import admin
from manageDomain.models import DomainModel,entityModel,relationModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import User
# Register your models here.


class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain_name']


class EntityAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'entity_label']


class RelationAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'relation_label']


# class UserAdmin(UserAdmin):
#     list_display = ('username', 'id',  'email')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(DomainModel, DomainAdmin)
admin.site.register(entityModel, EntityAdmin)
admin.site.register(relationModel, RelationAdmin)
admin.site.site_header = "专业知识图谱管理系统"
admin.site.site_title = "专业知识图谱管理系统"
