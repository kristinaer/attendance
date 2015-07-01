# -*- coding: utf-8 -*-

from django.conf import settings

def common(request):
    u = request.user
    is_backend = request.path.startswith('/private/')
    params = {
        'current_user': u,
        'config' : {
            'local': settings.LOCAL,
        },
        'domain': settings.LOCAL.get('domain'),
        'current_url': 'http://%s%s' % (
            request.META.get('HTTP_HOST'),
            request.get_full_path()
        ),
    }
    return params
