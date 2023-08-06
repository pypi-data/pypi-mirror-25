# -*- coding: utf-8 -*-
"""Models for the crm_groups app."""

import time

from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from background_task.models import Task
from crm_groups.managers import GroupManager
from cura.contacts.models import Person, Company
from extracontext.models import ExtraContext
from organizations.models import Organization
from tagging.fields import TagField


@python_2_unicode_compatible
class Group(models.Model):
    """Group model."""
    owner = models.ForeignKey(Organization, related_name='groups', help_text="Record owner")
    dirty = models.BooleanField(help_text="Record needs human interaction", default=False)
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    about = models.TextField(_('about'), blank=True)

    people = models.ManyToManyField(Person, verbose_name='people', related_name='groups', blank=True)
    companies = models.ManyToManyField(Company, verbose_name='companies', related_name='groups', blank=True)

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    tags = TagField(_('tags'))

    objects = GroupManager()

    class Meta:
        db_table = 'contacts_groups'
        ordering = ('name',)
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = int(time.time())
            super(Group, self).save(*args, **kwargs)

        uid = self.id
        s = str(self.owner.id) + "-" + str(uid) + "-" + slugify(self.name)
        self.slug = s[:50]
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_number_of_members(self):
        """
        Retuns the total number of members
        """
        return self.people.all().count() + self.companies.all().count()

    def get_number_of_silent_members(self):
        """
        Retuns the number of members have set enquiry to ENQUIRY_DISABLED // Mitglieder ohne Anfragewunsch
        """
        return self.people.filter(enquiry=Person.ENQUIRY_DISABLED).count() +\
            self.companies.filter(enquiry=Company.ENQUIRY_DISABLED).count()

    def get_number_of_email_members(self):
        """
        Retuns the number of members have set enquiry to ENQUIRY_EMAIL // Mitglieder mit Anfrage per Email
        """
        return self.people.filter(enquiry=Person.ENQUIRY_EMAIL).count() +\
            self.companies.filter(enquiry=Company.ENQUIRY_EMAIL).count()

    def get_number_of_letter_members(self):
        """
        Retuns the number of members have set enquiry to ENQUIRY_LETTER // Mitglieder mit Anfrage per Brief
        """
        return self.people.filter(enquiry=Person.ENQUIRY_LETTER).count() +\
            self.companies.filter(enquiry=Company.ENQUIRY_LETTER).count()

    def get_extracontext(self):
        """Return ExtraContext that is linked to this Group.

        Create an ExtraContext instance if not existing.
        """
        extracontext, created = ExtraContext.objects.get_or_create(
            owner=self.owner,
            name="group_extracontext",
            content_type_object=ContentType.objects.get_for_model(self),
            object_id=self.id,
        )
        return extracontext

    def buildout_ready(self):
        """Check if the buildout_task is completed."""
        extracontext = self.get_extracontext()
        buildout_task_id = extracontext.data.get('buildout_task', None)
        # if the tasks can not be found, the buildout is completed
        return not Task.objects.filter(id=buildout_task_id).exists()

    @permalink
    def get_absolute_url(self):
        return ('frcrm_group_detail', None, {
            'slug': self.slug,
        })

    @permalink
    def get_update_url(self):
        return ('frcrm_group_update', None, {
            'slug': self.slug,
        })

    @permalink
    def get_delete_url(self):
        return ('frcrm_group_delete', None, {
            'slug': self.slug,
        })

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id, ))
