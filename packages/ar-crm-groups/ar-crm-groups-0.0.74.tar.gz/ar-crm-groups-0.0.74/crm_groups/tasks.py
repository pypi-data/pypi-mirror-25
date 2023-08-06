# -*- coding: utf-8 -*-
import collections
import os
import re
import tempfile
import zipfile
import xlwt

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from background_task import background
from crm_downloads.models import Download
from crm_groups.models import Group
from crm_tagging.models import TaggedItem, Tag
from crm_tagging.templatetags.crm_tagging_tags import get_tags_for_item
from cura.contacts.models import Person, Company


@background(schedule=1)
def create_group_async(group_pk, contacts, tag_ids):
    """
    Link all selected contacts to the Group.

    This tasks is performed when a Campaign is created through the app-end.
    """
    group = Group.objects.get(pk=group_pk)

    tags = Tag.objects.filter(id__in=tag_ids)
    for tag in tags:
        TaggedItem.objects.tag_item(tag, group)

    for tag in tags:
        person_ct = ContentType.objects.get_for_model(Person)
        tagged_people = TaggedItem.objects.filter(tag=tag, content_type=person_ct, object_id__isnull=False)
        for taggedPerson in tagged_people:
            if taggedPerson.content_object:
                try:
                    group.people.add(taggedPerson.content_object)
                except IntegrityError:
                    pass

        company_ct = ContentType.objects.get_for_model(Company)
        tagged_companies = TaggedItem.objects.filter(tag=tag, content_type=company_ct, object_id__isnull=False)
        for tagged_company in tagged_companies:
            if tagged_company.content_object:
                try:
                    group.companies.add(tagged_company.content_object)
                except IntegrityError:
                    pass

        group.save()

    for object_string in contacts:
        if object_string:
            matches = re.match("type:(\d+)-id:(\d+)", object_string.strip()).groups()
            object_type_id = matches[0]  # get 45 from "type:45-id:38"
            object_id = matches[1]  # get 38 from "type:45-id:38"
            object_type = ContentType.objects.get(id=object_type_id)
            contact = object_type.get_object_for_this_type(id=object_id)
            if isinstance(contact, Person):
                group.people.add(contact)
            elif isinstance(contact, Company):
                group.companies.add(contact)
            else:
                pass

    return group


@background(schedule=1)
def export_members_advanced_async(group_pk, mailto, sheet_name=u"Mitglieder", filename="export.xls", link=False):
    """
    """
    group = Group.objects.get(pk=group_pk)
    fields = collections.OrderedDict()
    fields['type'] = u'Typ'
    fields['id'] = u'ID'
    fields['title'] = u'Titel'
    fields['extra_salutation'] = u'Anrede für Kommunikation'
    fields['gender'] = u'Geschlecht'
    fields['company'] = u'Firma/Familie'
    fields['company_id'] = u'Firma/Familie ID'
    fields['role'] = u'Funktion'
    fields['contact_person'] = u'Kontaktperson'
    fields['first_name'] = u'Vorname'
    fields['last_name'] = u'Nachname'
    fields['salutation_line'] = u'Anschrift/Anrede'
    fields['address'] = u'Adresse'
    fields['country'] = u'Land'
    fields['email'] = u'E-Mail-Adresse'
    fields['phone'] = u'Telefonnummer'
    fields['birthday'] = u'Geburtstag'
    fields['day_of_death'] = u'Todestag'
    fields['date_added'] = u'Registrierungsdatum'
    fields['date_removed'] = u'Austrittsdatum'
    fields['communication'] = u'Kommunikation erwünscht'
    fields['language'] = u'Bevorzugte Kommunikationssprache'
    fields['info'] = u'Info'
    fields['tags'] = u'Zugehörigkeiten'

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    style = xlwt.easyxf('font: bold 1')
    style_nl = xlwt.XFStyle()
    style_nl.alignment.wrap = 1

    # writing the header
    row = 0
    for _key, _label in fields.items():
        sheet.write(row, fields.keys().index(_key), _label, style)
    row += 1

    for person in group.people.all():
        try:
            address = person.full_address.all()[0]
            country = address.country.name
        except (ObjectDoesNotExist, IndexError):
            address = None
            country = ''

        try:
            birthday = person.birthday.strftime('%d.%m.%Y')
        except AttributeError:
            birthday = ''
        try:
            day_of_death = person.day_of_death.strftime('%d.%m.%Y')
        except AttributeError:
            day_of_death = ''
        try:
            date_added = person.date_added.strftime('%d.%m.%Y')
        except AttributeError:
            date_added = ''
        try:
            date_removed = person.date_removed.strftime('%d.%m.%Y')
        except AttributeError:
            date_removed = ''

        sheet.write(row, fields.keys().index('type'), "Person", style_nl)
        sheet.write(row, fields.keys().index('id'), person.id, style_nl)
        sheet.write(row, fields.keys().index('title'), person.get_title_display(), style_nl)
        sheet.write(row, fields.keys().index('extra_salutation'), person.extra_salutation, style_nl)
        sheet.write(row, fields.keys().index('gender'), person.get_gender_display(), style_nl)
        sheet.write(row, fields.keys().index('company'), getattr(person.company, 'name', ''), style_nl)
        sheet.write(row, fields.keys().index('company_id'), person.company_id, style_nl)
        sheet.write(row, fields.keys().index('role'), person.role, style_nl)
        sheet.write(row, fields.keys().index('contact_person'), str(person.contact_person), style_nl)
        sheet.write(row, fields.keys().index('first_name'), person.first_name, style_nl)
        sheet.write(row, fields.keys().index('last_name'), person.last_name, style_nl)
        sheet.write(row, fields.keys().index('salutation_line'), getattr(address, 'salutation_line', ''), style_nl)
        sheet.write(row, fields.keys().index('address'), getattr(address, 'full_address', ''), style_nl)
        sheet.write(row, fields.keys().index('country'), country, style_nl)
        sheet.write(row, fields.keys().index('email'), person.get_primary_email(), style_nl)
        sheet.write(row, fields.keys().index('phone'), person.get_primary_phone_number(), style_nl)
        sheet.write(row, fields.keys().index('birthday'), birthday, style_nl)
        sheet.write(row, fields.keys().index('day_of_death'), day_of_death, style_nl)
        sheet.write(row, fields.keys().index('date_added'), date_added, style_nl)
        sheet.write(row, fields.keys().index('date_removed'), date_removed, style_nl)
        sheet.write(row, fields.keys().index('communication'), str(person.enquiry > 0), style_nl)
        sheet.write(row, fields.keys().index('language'), person.get_language_display(), style_nl)
        sheet.write(row, fields.keys().index('info'), person.about, style_nl)
        sheet.write(row, fields.keys().index('tags'), person.tags, style_nl)
        row += 1

    for company in group.companies.all():
        try:
            address = company.full_address.all()[0]
            country = address.country.name
        except (ObjectDoesNotExist, IndexError):
            address = None
            country = ''

        try:
            date_added = company.date_added.strftime('%d.%m.%Y')
        except AttributeError:
            date_added = ''
        try:
            date_removed = company.date_removed.strftime('%d.%m.%Y')
        except AttributeError:
            date_removed = ''

        sheet.write(row, fields.keys().index('type'), company.get_org_type_display(), style_nl)
        sheet.write(row, fields.keys().index('id'), company.id, style_nl)
        sheet.write(row, fields.keys().index('title'), '', style_nl)
        sheet.write(row, fields.keys().index('extra_salutation'), company.extra_salutation, style_nl)
        sheet.write(row, fields.keys().index('gender'), '', style_nl)
        sheet.write(row, fields.keys().index('company'), '', style_nl)
        sheet.write(row, fields.keys().index('company_id'), '', style_nl)
        sheet.write(row, fields.keys().index('role'), '', style_nl)
        sheet.write(row, fields.keys().index('contact_person'), '', style_nl)
        sheet.write(row, fields.keys().index('first_name'), '', style_nl)
        sheet.write(row, fields.keys().index('last_name'), company.name, style_nl)
        sheet.write(row, fields.keys().index('salutation_line'), getattr(address, 'salutation_line', ''), style_nl)
        sheet.write(row, fields.keys().index('address'), getattr(address, 'full_address', ''), style_nl)
        sheet.write(row, fields.keys().index('country'), country, style_nl)
        sheet.write(row, fields.keys().index('email'), company.get_primary_email(), style_nl)
        sheet.write(row, fields.keys().index('phone'), company.get_primary_phone_number(), style_nl)
        sheet.write(row, fields.keys().index('birthday'), '', style_nl)
        sheet.write(row, fields.keys().index('day_of_death'), '', style_nl)
        sheet.write(row, fields.keys().index('date_added'), date_added, style_nl)
        sheet.write(row, fields.keys().index('date_removed'), date_removed, style_nl)
        sheet.write(row, fields.keys().index('communication'), str(company.enquiry > 0), style_nl)
        sheet.write(row, fields.keys().index('language'), company.get_language_display(), style_nl)
        sheet.write(row, fields.keys().index('info'), company.about, style_nl)
        sheet.write(row, fields.keys().index('tags'), company.tags, style_nl)
        row += 1

    tfile = tempfile.NamedTemporaryFile(delete=False, prefix=filename)
    target_file_path = tfile.name
    tfile.close()

    workbook.save(target_file_path)

    archive_path = target_file_path + ".zip"
    archive = zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED)
    archive.write(target_file_path, filename)
    archive.close()

    if link:
        Download.objects.create_private_download(
            archive_path,
            title=filename + '.zip',
            owner=group.owner,
            protocol='https://',
            subject="[DOWNLOAD] Ihre Daten stehen zum Download bereit",
            message="Sie können die Datei unter folgendem Link herunterladen: {{ download }}",
            to=mailto,
        )
    else:
        Download.objects.create_private_download(
            archive_path,
            title=filename + '.zip',
            owner=group.owner,
            protocol='https://',
            subject="[DOWNLOAD] Ihre Daten stehen zum Download bereit",
            message="Im Anhang finden Sie Ihre generierten Daten.",
            to=mailto,
            attach=True,
        )
    os.remove(target_file_path)
    os.remove(archive_path)


@background(schedule=1)
def export_members_async(group_pk, mailto, sheet_name=u"Mitglieder", filename="export.xls", link=False):
    """
    """
    group = Group.objects.get(pk=group_pk)

    col_type = 0
    col_title = 1
    col_first_name = 2
    col_last_name = 3
    col_address = 4
    col_country = 5
    col_email = 6
    col_phone = 7
    col_tags = 8

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    style = xlwt.easyxf('font: bold 1')

    row = 0
    sheet.write(row, col_type, "Typ", style)
    sheet.write(row, col_title, "Titel", style)
    sheet.write(row, col_first_name, "Vorname", style)
    sheet.write(row, col_last_name, "Nachname", style)
    sheet.write(row, col_address, "Adresse", style)
    sheet.write(row, col_country, "Land", style)
    sheet.write(row, col_email, "Email", style)
    sheet.write(row, col_phone, "Telefon", style)
    sheet.write(row, col_tags, "Tags", style)
    row += 1

    for person in group.people.all():
        sheet.write(row, col_type, "Person")
        sheet.write(row, col_title, person.get_title_display())
        sheet.write(row, col_first_name, person.first_name)
        sheet.write(row, col_last_name, person.last_name)
        sheet.write(row, col_address, person.get_primary_address())
        sheet.write(row, col_country, "")
        sheet.write(row, col_email, person.get_primary_email())
        sheet.write(row, col_phone, person.get_primary_phone_number())

        tags = get_tags_for_item(person)
        tags_as_string = ""
        tag_delimiter = ", "

        if tags:
            for tag in tags:
                tags_as_string += tag.name + tag_delimiter
        sheet.write(row, col_tags, tags_as_string)
        row += 1

    for company in group.companies.all():
        sheet.write(row, col_type, "Firma/Familie")
        sheet.write(row, col_title, "")
        sheet.write(row, col_first_name, "")
        sheet.write(row, col_last_name, company.name)
        sheet.write(row, col_address, company.get_primary_address())
        sheet.write(row, col_country, "")
        sheet.write(row, col_email, company.get_primary_email())
        sheet.write(row, col_phone, company.get_primary_phone_number())

        tags = get_tags_for_item(company)
        tags_as_string = ""
        tag_delimiter = ", "

        if tags:
            for tag in tags:
                tags_as_string += tag.name + tag_delimiter
        sheet.write(row, col_tags, tags_as_string)
        row += 1

    tfile = tempfile.NamedTemporaryFile(delete=False, prefix=filename)
    target_file_path = tfile.name
    tfile.close()

    workbook.save(target_file_path)

    archive_path = target_file_path + ".zip"
    archive = zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED)
    archive.write(target_file_path, filename)
    archive.close()

    if link:
        Download.objects.create_private_download(
            archive_path,
            title=filename + '.zip',
            owner=group.owner,
            protocol='https://',
            subject="[DOWNLOAD] Ihre Daten stehen zum Download bereit",
            message="Sie können die Datei unter folgendem Link herunterladen: {{ download }}",
            to=mailto,
        )
    else:
        Download.objects.create_private_download(
            archive_path,
            title=filename + '.zip',
            owner=group.owner,
            protocol='https://',
            subject="[DOWNLOAD] Ihre Daten stehen zum Download bereit",
            message="Im Anhang finden Sie Ihre generierten Daten.",
            to=mailto,
            attach=True,
        )
    os.remove(target_file_path)
    os.remove(archive_path)
