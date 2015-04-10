# -*- coding: utf-8 -*-
__author__ = 'Кристина'
import datetime
import pytils
from django.db.models import Q
from django import http
from django import forms
from django.template import loader, Context
from django.contrib import admin
from django.forms import ModelForm, HiddenInput
from users.models import User, Prepod, Student
from django.conf.urls import patterns
from django.utils.safestring import mark_safe
from core.views.generic import JsonView
from django.contrib.auth.admin import UserAdmin as AdminUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group, Permission


admin.site.disable_action('delete_selected')

def delete_users(modeladmin, request, queryset):
    queryset.update(is_active=False)
delete_users.short_description = u'Удалить выбранных пользователей'


class TemplateUserAdmin(admin.ModelAdmin):
    search_fields = ('log', 'f', 'i', 'o')
    ordering = ['f', 'i', 'o']
    list_per_page = 10
    actions = [delete_users]

    @method_decorator(sensitive_post_parameters())
    def user_change_password(self, request, id):
        return AdminUser(self.model, self.admin_site).user_change_password(request, id)

    def get_fullname(self, obj):
        return obj.get_full_name()
    get_fullname.admin_order_field = 'name'
    get_fullname.allow_tags = True
    get_fullname.short_description = 'ФИО'

    def get_urls(self):
        urls = super(TemplateUserAdmin, self).get_urls()
        extra_urls = patterns('',
                              (r'^(\d+)/password/$',
                               self.admin_site.admin_view(self.user_change_password))
                              )
        return extra_urls + urls


class UserAdminForm(ModelForm):
    password = ReadOnlyPasswordHashField(widget = HiddenInput(), label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"password/\">this form</a>."))

class UserAdmin(TemplateUserAdmin):
    form = UserAdminForm
    list_display = ['id', 'get_fullname','get_groups']
    list_filter = ['groups', 'is_active']

    def get_groups(self, obj):
        html = loader.get_template('users/backend/_list_groups_user.html').render(Context({
            'user_id': obj.id,
            'groups': obj.groups.all(),
        }))
        return mark_safe(html)
    get_groups.allow_tags = True
    get_groups.short_description = 'Группа'

admin.site.register(User, UserAdmin)


class PrepodAdminForm(ModelForm):
    class Meta:
        model = Prepod
        fields = ['f', 'i', 'o', 'is_active', 'log', 'password']


class PrepodAdmin(TemplateUserAdmin):
    list_display = ['id', 'get_fullname', 'log']
    form = PrepodAdminForm
    readonly_fields = ('log', 'password')
    list_filter = ['is_active']

    def get_queryset(self, request):
        qs = super(PrepodAdmin, self).get_queryset(request)
        return qs.filter(groups__name=u'Преподаватели')

admin.site.register(Prepod, PrepodAdmin)


class PermissionAdmin(admin.ModelAdmin): pass
admin.site.register(Permission, PermissionAdmin)
