# -*- coding: utf-8 -*-
import datetime
from django.views.generic import TemplateView, UpdateView, RedirectView
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout

from core.views.generic import LoginRequiredMixin
from core.utils.pager import Pager
from users.models import GroupSt
from users.forms import GroupStForm
from schedules.models import Schedule, ScheduleList


#===============================================================================
#
#===============================================================================
class Logout(RedirectView):
    permanent = False
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)

class MainView(LoginRequiredMixin, TemplateView):
    '''
    Общая реализация редактирования Редакционных материалов
    '''
    template_name = 'users/frontend/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        print (self.request.user.id)
        schedule = Schedule.objects.order_by('-id')[0]
        weekday=datetime.date.today().weekday()
        if weekday==6:
            weekday=0
        schedule_lists = ScheduleList.objects.filter(schedule=schedule, teacher=self.request.user.id, weekday=weekday)
        lists = [
            {'groups':[], 'time':'8:00-9:30'},
            {'groups':[], 'time':'9:40-11:10'},
            {'groups':[], 'time':'11:30-13:00'},
            {'groups':[], 'time':'13:30-15:00'},
            {'groups':[], 'time':'15:10-16:40'},
            {'groups':[], 'time':'17:00-18:30'},
            {'groups':[], 'time':'18:40-20:10'}
        ]
        for list in schedule_lists:
            lst = lists[list.number_pairs].get('groups', [])
            lst.append(list)
            lists[list.number_pairs]['groups'] = lst
        print lists

        context['schedule_lists'] = lists

        return context


class ListGroupView(LoginRequiredMixin, TemplateView):
    '''
    Общая реализация редактирования Редакционных материалов
    '''
    template_name = 'users/frontend/list_group.html'

    def get_context_data(self, **kwargs):
        context = super(ListGroupView, self).get_context_data(**kwargs)
        v = u'%s' % self.request.GET.get('by_text')
        qs = GroupSt.objects
        if v:
            qs = qs.filter(
                Q(name__icontains=v) |
                Q(starosta__f__icontains=v) |
                Q(speciality__name__icontains=v)
            )

        qs = qs.all().order_by('-id')
        context['paging'] = Pager('groups').get(qs, self.request.GET.get('page', 1))
        return context


class GroupEditView(LoginRequiredMixin, UpdateView):
    '''
    Редактирвоание события
    '''
    template_name = 'users/frontend/edit_group.html'
    model = GroupSt
    form_class = GroupStForm
    obj = False  # Ссылка на редактруемый объект
    success_url = ''  # Переопределяется в dispatch
    edit_view = 'users_frontend:group_edit'  # объект подходящий для передачи в reverse
    list_view = 'users_frontend:group_list'
    obj_type = u'События'
    js_module = 'BillboardBackend'

    def get_context_data(self, **kwargs):
        context = super(GroupEditView, self).get_context_data(**kwargs)
        context['seo_title'] = u'Редактирование %s' % self.obj_type
        #context['js_assets_ex'] = 'js_dt_back_ex'
        #if self.obj:
        #    context['tags'] = self.obj.tags.all()

        if self.js_module:
            context['js_module'] = self.js_module
        context['back_to'] = self.success_url

        if self.request.POST:
            context['form_seo_title'] = self.request.POST.get('form_seo_title', '')
        else:
            try:
                context['form_seo_title'] = self.obj.seo_data.title
            except AttributeError:
                pass
        return context

    def post(self, request, *args, **kwargs):
        ret = super(GroupEditView, self).post(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            seo = Seo()
            seo_data = {'title': self.request.POST.get('form_seo_title', '')}
            seo.assign_to_object(self.obj, seo_data)
        cache.delete_pattern('billboard:events:*')
        return ret

    def get_object(self, queryset=None):
        return self.obj

    def dispatch(self, request, *args, **kwargs):
        obj_id = int(kwargs.get('pk', '0'))
        if obj_id:
            self.obj = get_object_or_404(self.model, pk=obj_id)

        if not self.obj:
            new_obj = self.model()
            if hasattr(new_obj, 'user_id'):
                new_obj.user = self.request.user
            new_obj.save()
            return redirect(self.edit_view, pk=new_obj.pk)

        if not self.request.user.has_perm('billboard.change_event'):
            raise RedirectNeededException('error', u'У вас нет прав для редактирования этого объекта')

        self.success_url = reverse(self.list_view)
        return super(GroupEditView, self).dispatch(request, *args, **kwargs)