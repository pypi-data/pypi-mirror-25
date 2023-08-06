# -*- encoding: utf-8 -*-

import django
from django.db import models


class GroupManager(models.Manager):
    # NOTE: copied from crm_super to ensure compatibility

    def owned_by(self, organization):
        """
        usage:
        Model.objects.owned_by(org)
        """
        if django.VERSION < (1, 7):
            return super(GroupManager, self).get_query_set().filter(owner=organization)
        else:
            return super(GroupManager, self).get_queryset().filter(owner=organization)
