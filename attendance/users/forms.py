# -*- coding: utf-8 -*-

from django import forms

from users.models import GroupSt


class GroupStForm(forms.ModelForm):
    class Meta:
        model = GroupSt
        fields = [
            'name',
            'speciality',
            'created_at',
        ]

