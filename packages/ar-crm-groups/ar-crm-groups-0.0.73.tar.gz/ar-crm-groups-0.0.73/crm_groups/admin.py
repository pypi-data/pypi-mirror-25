from django.contrib import admin

from crm_groups.models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('name', 'owner', 'date_modified', 'date_added')
    ordering = ('-date_modified', 'name',)
    search_fields = ['^name', '^about', ]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Group, GroupAdmin)
