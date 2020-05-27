from django.contrib import admin
from account.models import User
from django import forms
from manageDomain.models import DomainModel
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin
# Register your models here.


# class UserAdmin(UserAdmin):
#     #需要显示的字段信息
#     list_display = ('username', 'id', 'is_superuser', 'email', 'user_domain')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#         (_('用户所属领域'), {'fields': ('user_domain',)})
#     )
#
#
#
# class userProfileForm(forms.ModelForm):
#     option = forms.ModelChoiceField(label=u'下拉框',queryset=DomainModel.objects.all())
#     # checkbox = forms.ModelMultipleChoiceField(label=u'多选框',queryset=DomainModel.objects.all(), widget=forms.CheckboxSelectMultiple())
#     class Meta:
#         model = User
#         fields = ['option']
#
#
# class profileInline(admin.StackedInline):
#     model = User
#     form = userProfileForm
#
#
# class testUserAdmin(UserAdmin):
#     inlines = [profileInline,]
#
# # admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


