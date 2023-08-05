# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def create_activate_deactivate_object(model_class, action, **kwargs):
    if action == 'create':
        model_class.objects.create(**kwargs)
    else:
        obj = model_class.objects.get(**kwargs)
        if action == 'deac':
            if obj.is_active:
                obj.is_active = False
        elif action == 'act':
            if not obj.is_active:
                obj.is_active = True
        obj.save()

    return {'message': 'Success!'}