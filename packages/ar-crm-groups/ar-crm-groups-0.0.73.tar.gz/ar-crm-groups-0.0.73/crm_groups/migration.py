# NOTE: this is not a migrations file
# this is used to migrate groups from frcrm/contacts to crm_groups

from crm_groups.models import Group
from cura.contacts.models import Group as OldGroup


class Migration(object):
    def forward(self):
        for old_grp in OldGroup.objects.all():
            new_grp = Group.objects.create(
                id=old_grp.id,
                owner=old_grp.owner,
                dirty=old_grp.dirty,
                name=old_grp.name,
                slug=old_grp.slug,
                about=old_grp.about,
                date_added=old_grp.date_added,
                date_modified=old_grp.date_modified,
            )

            # for perm in old_grp.user_permissions.all():
            #     new_grp.user_permissions.add(perm)
            # for group in old_grp.groups.all():
            #     new_grp.groups.add(group)

            # instead of looping over perms and groups, you can just assign:
            # new_u.user_permissions = old_u.user_permissions.all()
            # new_u.groups = old_u.groups.all()

            new_grp.people = old_grp.people.all()
            new_grp.companies = old_grp.companies.all()

        # adopt tags
        # update contenty type on generic relations if necessary

        # id uebernehmen sonst stimmen fremdschlüssel auf u.a. kampagnen nicht
