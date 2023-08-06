# -*- coding: utf-8 -*-

try:
    from django.conf.urls import patterns, url
except:
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'crm_groups.views',
    url(r'^groups/$',
        view='list',
        name='frcrm_group_list',),

    url(r'^group/add/$',
        view='create',
        name='frcrm_group_create',),

    url(r'^group/add/contacts-selection/$',
        view='create_contacts_selection',
        name='frcrm_group_create_contacts_selection',),

    url(r'^group/(?P<slug>[-\w]+)/delete/$',
        view='delete',
        name='frcrm_group_delete'),

    url(r'^group/(?P<slug>[-\w]+)/tag-members/$',
        view='tag_members',
        name='frcrm_group_tag_members', ),

    url(r'^group/(?P<slug>[-\w]+)/export-members/$',
        view='export_members',
        name='frcrm_group_export_members',),

    url(r'^group/(?P<slug>[-\w]+)/$',
        view='detail',
        name='frcrm_group_detail',),

    # ajax
    url(r'^group/(?P<slug>[-\w]+)/status/$',
        view='status',
        name='frcrm_group_status', ),

    url(r'^group/(?P<slug>[-\w]+)/data/$',
        view='detail_data',
        name='frcrm_group_detail_data',),

    url(r'^group/(?P<slug>[-\w]+)/remove_member/$',
        view='remove_member',
        name='frcrm_group_remove_member',),

    # app/group/1-50-arteria-gmbh/perform/?action=update
    url(r'^group/(?P<slug>[-\w]+)/perform/$',
        view='group_perform',
        name='frcrm_group_perform',),
)
