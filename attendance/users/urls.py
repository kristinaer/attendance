# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from users.views import (
    ListGroupView, GroupEditView, MainView, Logout
)

urlpatterns = patterns('',
    url(r'^groups/(?P<pk>[0-9]+)/$', GroupEditView.as_view(), name='group_edit'),
    url(r'^groups/$', ListGroupView.as_view(), name='group_list'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^$',  MainView.as_view(), name='users_f'),
)
