# -*- coding: utf-8 -*-
from select2utils.helper import Select2Helper
from cura.contacts.models import Person, Company
from cura.contacts.contacts_api import ContactsAPI


class CreateContactsSelect2Helper(Select2Helper):
    """Select Perople ans Companies in Group create views."""

    models = [
        (Person, 'nickname'),
        (Company, 'name'),
    ]

    def _get_inital_queryset(self, model_map, query='', extra_filter={}):
        """Override the default for custom functionality."""
        if model_map[0].__name__ == 'Person':
            qs = ContactsAPI(self.request.user, request=self.request).get_people()
        elif model_map[0].__name__ == 'Company':
            qs = ContactsAPI(self.request.user, request=self.request).get_companies()

        if query:
            extra_filter['{}__icontains'.format(model_map[1])] = query

        return qs.filter(**extra_filter).values('id', model_map[1])
