__author__ = 'Кристина'
import datetime

from django.db.models import Q
from django import http
from django.template import loader, Context
from django.contrib import admin
from django.forms import ModelForm, HiddenInput
from users.models import User
from django.conf.urls import patterns
from django.utils.safestring import mark_safe
from core.views.generic import JsonView
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
    change_list_template = 'users/backend/change_list_template.html'
    list_display = ['id', 'get_fullname','get_groups']
    list_filter = ('groups', PermissionListFilter)
    search_fields = ('log', 'get_fullname')
    ordering = ['id']
    list_per_page = 10

    @sensitive_post_parameters()
    def user_change_password(self, request, id):
        return AdminUser(self.model, self.admin_site).user_change_password(request, id)

    def get_fullname(self, obj):
        return obj.get_full_name()
    get_fullname.admin_order_field = 'name'
    get_fullname.allow_tags = True
    get_fullname.short_description = 'ФИО'

    def get_groups(self, obj):
        html = loader.get_template('users/backend/_list_groups_user.html').render(Context({
            'user_id': obj.id,
            'groups': obj.groups.all(),
        }))
        return mark_safe(html)
    get_groups.allow_tags = True
    get_groups.short_description = 'Группа'

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        extra_urls = patterns('',
                              (r'^edit_groups_popup/$', self.EditGroupsPopup.as_view()),
                              (r'^save_groups/$', self.SaveGroups.as_view()),
                              (r'^(\d+)/password/$',
                               self.admin_site.admin_view(self.user_change_password))
                              )
        return extra_urls + urls

    class SavePopup(JsonView):
        def preprocess(self):
            if not self.request.is_ajax():
                raise http.Http404
            response = {
                'error': 0,
                'error_msg': '',
                'html': ''
            }
            user_id = self.request.GET.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    response['html'] = self.get_html(user)
                except User.DoesNotExist:
                    response['error'] = True
                    response['error_msg'] = 'Пользователь не найден'
            else:
                response['error'] = True
                response['error_msg'] = 'Информация о пользователе не передана'

            return response
        def get_html(self, user):
            for group in user.groups.all():
                user.groups.remove(group)
            groups = self.request.GET.getlist('groups')
            for group in Group.objects.filter(id__in=groups):
                user.groups.add(group)
            return loader.get_template('users/backend/_list_groups_user.html').render(Context({
                'user_id': user.id,
                'groups': user.groups.all(),
                }))

    class EditGroupsPopup(JsonView):
        def preprocess(self):
            if not self.request.is_ajax():
                raise http.Http404
            user_id = self.request.GET.get("user_id")
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise http.Http404
            groups = Group.objects.all()
            groups_array = []
            groups_user = user.groups.all()
            for group in groups:
                d = {}
                d['data'] = group
                d['checked'] = group in groups_user
                groups_array.append(d)
            return loader.get_template('users/backend/_edit_groups_popup.html').render(Context({
                'user_id': user_id,
                'groups': groups_array,
            }))

    class SaveGroups(SavePopup): pass

admin.site.register(User, UserAdmin)

class PermissionAdmin(admin.ModelAdmin): pass
admin.site.register(Permission, PermissionAdmin)