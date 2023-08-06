# -*- encoding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from cura.contacts.models import Person, Company
from crm_groups.models import Group
from crm_super.crm_api import CRMBaseAPI
from crm_tagging.models import TaggedItem
from crm_tagging.templatetags.crm_tagging_tags import get_tags_for_item


class GroupAPI(CRMBaseAPI):
    """
    Internal API to create and manipulate groups
    """
    class Meta(CRMBaseAPI.Meta):
        model = Group

    def create(self, *args, **kwargs):
        """creates a Group with the given **kwvars using the custom model manager"""
        opts = {
            'owner': self.organization,
        }
        opts.update(kwargs)  # we update opts, so we don't overwrite values of kwargs
        group = self.Meta.model(**opts)
        group.save()
        self.notify(group, self.NOTIFY_CREATED)
        # NOTE: we never call the apis create method, that would update our kwargs with created_by and modified_by
        # which are not valid fields in the legacy branch model
        # group = super(GroupAPI, self).create(*args, **kwargs)
        return group

    def update_by_tags(self, group, **kwargs):
        """updates a Group by ..."""
        group_tags = get_tags_for_item(group)

        for tag in group_tags:
            person_ct = ContentType.objects.get_for_model(Person)
            tagged_people = TaggedItem.objects.filter(tag=tag, content_type=person_ct, object_id__isnull=False)
            for tagged_person in tagged_people:
                if tagged_person.content_object:
                    group.people.add(tagged_person.content_object)

            company_ct = ContentType.objects.get_for_model(Company)
            tagged_companies = TaggedItem.objects.filter(tag=tag, content_type=company_ct, object_id__isnull=False)
            for tagged_company in tagged_companies:
                if tagged_company.content_object:
                    group.companies.add(tagged_company.content_object)

        group.save()
