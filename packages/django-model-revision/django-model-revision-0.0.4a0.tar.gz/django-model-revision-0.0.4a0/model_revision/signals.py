# -*- coding: utf-8 -*-
from model_revision.models import Revision


def post_save_callback(sender, **kwargs):
    instance = kwargs['instance']
    raw = kwargs['raw']
    if not raw:
        Revision.objects.create_from_instance(instance)
