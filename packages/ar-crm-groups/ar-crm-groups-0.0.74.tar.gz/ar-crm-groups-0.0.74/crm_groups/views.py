# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from compat import JsonResponse
from crm_groups import forms
from crm_groups.groups_api import GroupAPI
from crm_groups.models import Group
from crm_groups.tasks import export_members_async, export_members_advanced_async, create_group_async
from crm_groups.select2_utils import CreateContactsSelect2Helper
from crm_tagging.models import Tag, TaggedItem
from cura.contacts.models import Person, Company


def _redirect(obj, form_data):
    if '_continue' in form_data:
        # rerirect to detailview
        return redirect('frcrm_group_detail', slug=obj.slug)
    elif '_addanother' in form_data:
        # redirect to create page
        return redirect('frcrm_group_create')
    else:  # _save
        # redirect to listview
        return redirect('frcrm_group_list')


@login_required
def list(request, template='crm_groups/list.html'):
    """List of all the groups.

    :param template: Add a custom template.
    """
    kwvars = {
        'groups': GroupAPI(request.user, request=request).all()
    }
    return render_to_response(template, kwvars, RequestContext(request))


@login_required
def create(request, template='crm_groups/create.html'):
    """Create a group.

    :param template: A custom template.
    """
    errors = False

    form = forms.GroupCreateForm(request.POST or None, request.FILES or None, request=request)

    if form.is_valid():
        # pop extra fields and add process them later
        contacts = form.cleaned_data.pop('contacts', '').split(',')
        tag_ids = form.cleaned_data.pop('tags', [])

        group = GroupAPI(request.user, request=request).create(**form.cleaned_data)

        # start buildout task and save in extracontext
        extracontext = group.get_extracontext()
        buildout_task = create_group_async(group.pk, contacts, tag_ids)
        extracontext.data['buildout_task'] = buildout_task.id
        extracontext.save()
        messages.success(request, '{} wurde erstellt'.format(group))
        return _redirect(group, form.data)

    kwvars = {
        'form': form,
        'errors': False if request.method == 'GET' else errors,
    }

    return render_to_response(template, kwvars, RequestContext(request))


@login_required
def detail(request, slug=None, template_name='crm_groups/detail.html'):
    """View and update a group.

    :param template: A custom template.
    """
    api = GroupAPI(request.user, request=request)
    try:
        a_group = api.get(slug=slug)
    except Group.DoesNotExist:
        raise Http404

    # addToLastViewedItems(request=request, item=a_group)
    form = forms.GroupUpdateForm(request.POST or None, request.FILES or None, instance=a_group, request=request)

    if form.is_valid():
        a_group = api.update(a_group, **form.cleaned_data)
        messages.success(request, '{} wurde gespeichert'.format(a_group))
        return _redirect(a_group, form.data)

    kwvars = {
        'form': form,
        'tag_form': forms.GroupTagForm(request=request),
        'object': a_group,
    }

    return render_to_response(template_name, kwvars, context_instance=RequestContext(request))


@login_required
def detail_data(request, slug=None):
    """View group members."""
    api = GroupAPI(request.user, request=request)
    try:
        a_group = api.get(slug=slug)
    except Group.DoesNotExist:
        raise Http404

    ans = []
    template = u'<div class="btn-group"><button class="btn btn-mini btn-default dropdown-toggle" data-toggle="dropdown"><i class="icon-cog"></i></button><ul class="dropdown-menu pull-right"><li><a href="{0}?member_type={1}&member_id={2}"><i class="icon-remove status-error"></i> Aus Gruppe entfernen</a><li></ul></div>'

    for person in a_group.people.all():
        ans.append([
            u'<a href="{0}"><strong>{1}</strong></a>'.format(person.get_absolute_url(), person.fullname),
            "Person",
            person.get_enquiry_display(),
            person.get_gratitude_display(),
            template.format(
                reverse('frcrm_group_remove_member', args=([a_group.slug])),
                "person",
                person.id,
            )
        ])

    for company in a_group.companies.all():
        ans.append([
            u'<a href="{0}"><strong>{1}</strong></a>'.format(company.get_absolute_url(), company.name),
            "Firma/Familie",
            company.get_enquiry_display(),
            company.get_gratitude_display(),
            template.format(
                reverse('frcrm_group_remove_member', args=([a_group.slug])),
                "company",
                company.id,
            )
        ])

    return JsonResponse({'aaData': ans}, safe=False)


@login_required
def tag_members(request, slug=None):
    """
    Tag members of a group.
    """
    try:
        a_group = GroupAPI(request.user, request=request).get(slug=slug)
    except Group.DoesNotExist:
        raise Http404

    form = forms.GroupTagForm(request=request)

    if request.method == 'POST':
        form = forms.GroupTagForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            tags_ids = form.cleaned_data['tagsToAdd']

            # tagg all people and comapanies in group
            if tags_ids:
                for tag_id in tags_ids:
                    tag = Tag.objects.get(pk=tag_id)

                    for person in a_group.people.all():
                        TaggedItem.objects.tag_item(tag, person)

                    for company in a_group.companies.all():
                        TaggedItem.objects.tag_item(tag, company)
            messages.success(request, 'Mitglieder wurden markiert'.format(a_group))

    return redirect('frcrm_group_detail', slug=a_group.slug)


@login_required
def remove_member(request, slug=None):
    """
    Remove a Group Member.
    """
    try:
        a_group = GroupAPI(request.user, request=request).get(slug=slug)
    except Group.DoesNotExist:
        raise Http404

    member_type = request.GET.get('member_type')
    member_id = request.GET.get('member_id')

    if member_type == 'person':
        person_obj = Person.objects.get(id=member_id)
        a_group.people.remove(person_obj)
    elif member_type == 'company':
        company_obj = Company.objects.get(id=member_id)
        a_group.companies.remove(company_obj)
    messages.success(request, 'Mitglied wurde entfernt'.format(a_group))

    return HttpResponseRedirect(a_group.get_absolute_url())


@login_required
def delete(request, slug=None, template='crm_groups/delete.html'):
    """Delete a group.

    :param template: A custom template.
    """
    api = GroupAPI(request.user, request=request)
    try:
        a_group = api.get(slug=slug)
    except Group.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['delete_group'] == 'Yes':
            api.delete(a_group)
            messages.success(request, '{} wurde gelöscht'.format(a_group))
            return HttpResponseRedirect(reverse('frcrm_group_list'))
        else:
            return HttpResponseRedirect(a_group.get_absolute_url())

    kwvars = {
        'object': a_group,
    }

    return render_to_response(template, kwvars, RequestContext(request))


@login_required
def group_perform(request, slug=None):
    try:
        a_group = GroupAPI(request.user, request=request).get(slug=slug)
    except Group.DoesNotExist:
        raise Http404

    action = request.GET.get("action")

    if action == "update":
        GroupAPI(request.user, request=request).update_by_tags(a_group)
        messages.success(request, '{} wurde aktualisiert'.format(a_group))

    next = request.GET.get("next")
    if next:
        return HttpResponseRedirect(next)

    return redirect('frcrm_group_list')


@login_required
def export_members(request, slug=None):
    try:
        a_group = GroupAPI(request.user, request=request).get(slug=slug)
    except Group.DoesNotExist:
        raise Http404

    curr_time = datetime.now()
    if request.GET.get('advanced', 'false') == 'true':
        export_members_advanced_async(
            a_group.id,
            [request.user.email],
            filename=u"{0}-advanced-{1}.xls".format(slugify(a_group.name), curr_time.strftime("%d-%m-%y")),
            link=bool(request.GET.get('link', False)),
        )
    else:
        export_members_async(
            a_group.id,
            [request.user.email],
            filename=u"{0}-{1}.xls".format(slugify(a_group.name), curr_time.strftime("%d-%m-%y")),
            link=bool(request.GET.get('link', False)),
        )
    messages.success(
        request,
        u'Der Export wurde gestartet. Sie erhalten denächst eine Email in der Sie die Datei herunterladen können'
    )
    return redirect('frcrm_group_detail', slug=a_group.slug)


@login_required
def create_contacts_selection(request):
    """
    List of possible contacts.

    This is used for the select2.js plugin to add
    contacts to a new group.
    """
    select2_helper = CreateContactsSelect2Helper(request)
    query = request.GET.get('q', '').lower()
    ans = select2_helper.get_content_object_choices(query=query)
    return JsonResponse(ans, safe=False)


@login_required
def status(request, slug=None):
    """
    """
    try:
        a_group = GroupAPI(request.user, request=request).get(slug=slug)
    except Group.DoesNotExist:
        return JsonResponse({"status": "error"})
    response = {
        'id': a_group.id,
        'buildout_ready': a_group.buildout_ready(),
    }
    return JsonResponse(response)
