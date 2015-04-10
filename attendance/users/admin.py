# -*- coding: utf-8 -*-
__author__ = 'Кристина'
import datetime
import pytils
from django.db.models import Q
from django import http
from django import forms
from django.contrib.admin import SimpleListFilter
from django.template import loader, Context
from django.contrib import admin
from django.forms import ModelForm, HiddenInput
from users.models import User, Prepod, Student, Speciality, GroupSt, GroupStudents
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


class StudentAdminForm(ModelForm):
    class Meta:
        model = Student
        fields = ['f', 'i', 'o', 'is_active', 'log', 'password']

class StarostaListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Студенты')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'starosta'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', _('Старосты')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'yes':
            starosts = GroupSt.objects.filter(starosta__isnull=False).values_list('starosta', flat=True)
            return queryset.filter(id__in=starosts)

class StudentAdmin(TemplateUserAdmin):
    list_display = ['id', 'get_fullname',  'get_groupst', 'log']
    form = StudentAdminForm
    readonly_fields = ('log', 'password')
    list_filter = ['is_active', StarostaListFilter]
    def get_groupst(self, obj):
        html = loader.get_template('users/backend/_groupst_user.html').render(Context({
            'user_id': obj.id,
            'groupst': obj.groupsts.all(),
        }))
        return mark_safe(html)
    get_groupst.allow_tags = True
    get_groupst.short_description = 'Группа'

    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
        return qs.filter(groups__name=u'Студенты')

admin.site.register(Student, StudentAdmin)


class PermissionAdmin(admin.ModelAdmin): pass
admin.site.register(Permission, PermissionAdmin)


def delete_speciality(modeladmin, request, queryset):
    queryset.update(status='delete')
delete_speciality.short_description = u'Удалить выбранные специальности'

class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'qualification']
    list_filter = ['qualification', 'status']
    search_fields = ['name']
    ordering = ['name']
    actions = [delete_speciality]

admin.site.register(Speciality, SpecialityAdmin)


def delete_groupst(modeladmin, request, queryset):
    queryset.update(status='delete')
delete_groupst.short_description = u'Удалить выбранные группы'


class GroupStAdminForm(ModelForm):
    users = forms.ModelMultipleChoiceField(
        User.objects.all(),
        required=False
    )
    class Meta:
        model = GroupSt
        fields = ('name', 'speciality', 'date_end', 'starosta', 'status', 'users')

    def __init__(self, *args, **kwargs):
        specialities = Speciality.objects.order_by('name')
        users = User.objects.filter(groups__name="Студенты").order_by('f', 'i', 'o')

        super(GroupStAdminForm, self).__init__(*args, **kwargs)
        choices = [(s.pk, s.name,) for s in specialities]
        self.fields['speciality'].choices = choices
        choices = [(None, '---')] + [(u.pk, u.get_full_name(),) for u in users]
        self.fields['starosta'].choices = choices


class GroupStAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_speciality', 'get_starosta', 'date_end']
    list_filter = ['speciality', 'status']
    search_fields = ['name']
    ordering = ['date_end']
    form = GroupStAdminForm
    date_hierarchy = 'date_end'
    actions = [delete_groupst]
    def get_speciality(self, obj):
        html = loader.get_template('users/backend/_speciality_group.html').render(Context({
            'groupst_id': obj.id,
            'speciality': obj.speciality,
        }))
        return mark_safe(html)
    get_speciality.allow_tags = True
    get_speciality.short_description = 'Специальность'

    def get_starosta(self, obj):
        html = loader.get_template('users/backend/_starosta_group.html').render(Context({
            'groupst_id': obj.id,
            'starosta': obj.starosta,
        }))
        return mark_safe(html)
    get_starosta.allow_tags = True
    get_starosta.short_description = 'Староста'

admin.site.register(GroupSt, GroupStAdmin)
