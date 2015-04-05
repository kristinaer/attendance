# -*- coding: utf-8 -*-
from django.db.models import Q
from django.contrib import admin
from django.forms import ModelForm, HiddenInput
from users.models import User
from django.contrib.auth.admin import UserAdmin as AdminUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import Group, Permission


class UserAdminForm(ModelForm):
    password = ReadOnlyPasswordHashField(widget = HiddenInput(), label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"password/\">this form</a>."))

class PermissionListFilter(admin.SimpleListFilter):
    title = ('Права пользователя')
    parameter_name = 'permission'

    def lookups(self, request, model_admin):
        permissions = Permission.objects.all()
        return [(permission.id, str(permission)) for permission in permissions]

    def queryset(self, request, queryset):
        return queryset.filter(Q(user_permissions__id=self.value()) | Q(groups__permissions__id=self.value()))


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['id', 'f', 'i', 'o', 'get_groups']
    list_filter = ('groups', PermissionListFilter)
    search_fields = ('f', 'i', 'o')
    ordering = ['id']
    list_per_page = 20

    @sensitive_post_parameters()
    def user_change_password(self, request, id):
        return AdminUser(self.model, self.admin_site).user_change_password(request, id)

admin.site.register(User, UserAdmin)

class PermissionAdmin(admin.ModelAdmin): pass
admin.site.register(Permission, PermissionAdmin)
