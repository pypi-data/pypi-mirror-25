# -*- coding: utf-8 -*-
from django import forms

from crm_groups.models import Group
from crm_tagging.models import Tag
from organizations.utils import get_current_organization


class GroupCreateForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'chzn-select'}),
        label=u'Schlagwörter',
        help_text=u'Wählen Sie Schlagwörter. Alle Kontakte, die eine der gewählten Schlagwörter tragen, werden der Gruppe hinzugefügt.',
    )
    contacts = forms.CharField(
        required=False,
        label=u'Kontakte',
        help_text=u'Wählen Sie Kontakte, die Sie der Gruppe hinzufügen möchten.',
    )

    class Meta:
        model = Group
        fields = ('name', 'about')
        widgets = {
            'people': forms.SelectMultiple(attrs={'class': 'chzn-select'}),
            'companies': forms.SelectMultiple(attrs={'class': 'chzn-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        # TODO: use/create function/apicall from crm_tagging
        self.fields['tags'].choices = Tag.objects.filter(
            owner=get_current_organization(self.request)).values_list('id', 'name').order_by('name')


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'about')
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(GroupUpdateForm, self).__init__(*args, **kwargs)


class GroupTagForm(forms.Form):
    """
    Is used to tag all members of a group
    """
    tagsToAdd = forms.MultipleChoiceField(
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'chzn-select'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(GroupTagForm, self).__init__(*args, **kwargs)
        self.fields['tagsToAdd'].choices = Tag.objects.filter(
            owner=get_current_organization(self.request)).values_list('id', 'name').order_by('name')
