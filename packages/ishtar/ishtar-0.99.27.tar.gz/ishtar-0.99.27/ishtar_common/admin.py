#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See the file COPYING for details.

"""
Admin description
"""
import csv

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext

from django import forms

import models


class ImportGenericForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    csv_file = forms.FileField(
        "CSV file", help_text="Only unicode encoding is managed - convert your"
        " file first")


def gen_import_generic(self, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ImportGenericForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['csv_file']
            reader = csv.reader(csv_file)
            idx = 0
            for row in reader:
                slug = slugify(row[0])
                if self.model.objects.filter(txt_idx=slug).count():
                    continue
                obj, c = self.model.objects.get_or_create(
                    label=row[0], txt_idx=slug)
                if c:
                    idx += 1
            self.message_user(request, "Successfully added %d new items." % (
                idx))
            return HttpResponseRedirect(request.get_full_path())
    if not form:
        form = ImportGenericForm(
            initial={'_selected_action':
                     request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
    return render_to_response(
        'admin/import_from_csv.html', {'csv_form': form},
        context_instance=RequestContext(request))

gen_import_generic.short_description = "Import from a CSV file"


def export_as_csv_action(description=_(u"Export selected as CSV file"),
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % \
            unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([
                unicode(getattr(obj, field)).encode("utf-8", "replace")
                for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


class HistorizedObjectAdmin(admin.ModelAdmin):
    readonly_fields = ('history_modifier',)

    def save_model(self, request, obj, form, change):
        obj.history_modifier = request.user
        obj.save()


class MyGroupAdmin(GroupAdmin):
    class Media:
        css = {
            "all": ("media/admin.css",)
        }

admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)


class IshtarSiteProfileAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug', 'active', 'files', 'context_record',
                    'find', 'warehouse')
    model = models.IshtarSiteProfile

admin.site.register(models.IshtarSiteProfile, IshtarSiteProfileAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'label',)
    model = models.Department

admin.site.register(models.Department, DepartmentAdmin)


class OrganizationAdmin(HistorizedObjectAdmin):
    list_display = ('pk', 'name', 'organization_type')
    list_filter = ("organization_type",)
    search_fields = ('name',)
    exclude = ('merge_key', 'merge_exclusion', 'merge_candidate', )
    model = models.Organization

admin.site.register(models.Organization, OrganizationAdmin)


class PersonAdmin(HistorizedObjectAdmin):
    list_display = ('pk', 'name', 'surname', 'raw_name', 'email')
    list_filter = ("person_types",)
    search_fields = ('name', 'surname', 'email', 'raw_name')
    exclude = ('merge_key', 'merge_exclusion', 'merge_candidate', )
    model = models.Person

admin.site.register(models.Person, PersonAdmin)


class TownAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']
    if settings.COUNTRY == 'fr':
        list_display += ['numero_insee', 'departement', ]
        search_fields += ['numero_insee', 'departement__label', ]
        list_filter = ("departement",)
    model = models.Town

admin.site.register(models.Town, TownAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['person', 'author_type']
    list_filter = ("author_type",)
    model = models.Author

admin.site.register(models.Author, AuthorAdmin)


class PersonTypeAdmin(admin.ModelAdmin):
    list_display = ['label', 'txt_idx', 'available', 'comment']
    model = models.PersonType
    filter_vertical = ('groups',)

admin.site.register(models.PersonType, PersonTypeAdmin)


class GlobalVarAdmin(admin.ModelAdmin):
    list_display = ['slug', 'description', 'value']
admin.site.register(models.GlobalVar, GlobalVarAdmin)


class GeneralTypeAdmin(admin.ModelAdmin):
    list_display = ['label', 'txt_idx', 'available', 'comment']
    search_fields = ('label', 'txt_idx', 'comment',)
    actions = ['import_generic', export_as_csv_action()]
    import_generic = gen_import_generic


general_models = [models.OrganizationType, models.SourceType,
                  models.AuthorType, models.TitleType, models.Format,
                  models.SupportType]
for model in general_models:
    admin.site.register(model, GeneralTypeAdmin)


class ImporterDefaultValuesInline(admin.TabularInline):
    model = models.ImporterDefaultValues


class ImporterDefaultAdmin(admin.ModelAdmin):
    list_display = ('importer_type', 'target')
    model = models.ImporterDefault
    inlines = (ImporterDefaultValuesInline,)
admin.site.register(models.ImporterDefault, ImporterDefaultAdmin)


class ImporterTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'associated_models', 'is_template')
admin.site.register(models.ImporterType, ImporterTypeAdmin)


class RegexpAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', "regexp")
admin.site.register(models.Regexp, RegexpAdmin)


class ImporterDuplicateFieldInline(admin.TabularInline):
    model = models.ImporterDuplicateField


class ImportTargetForm(forms.ModelForm):
    class Meta:
        model = models.ImportTarget
        exclude = []
        widgets = {
            'comment': forms.TextInput
        }


class ImportTargetInline(admin.TabularInline):
    model = models.ImportTarget
    extra = 1
    form = ImportTargetForm


class ImporterColumnAdmin(admin.ModelAdmin):
    list_display = ('label', 'importer_type', 'col_number', 'description',
                    'targets_lbl', 'duplicate_fields_lbl', 'required')
    list_filter = ('importer_type',)
    inlines = (ImportTargetInline, ImporterDuplicateFieldInline)
admin.site.register(models.ImporterColumn, ImporterColumnAdmin)


class ImporterModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'klass')
    model = models.ImporterModel

admin.site.register(models.ImporterModel, ImporterModelAdmin)


class FormaterTypeAdmin(admin.ModelAdmin):
    list_display = ('formater_type', 'options')
admin.site.register(models.FormaterType, FormaterTypeAdmin)


class ImportAdmin(admin.ModelAdmin):
    list_display = ('name', 'importer_type', 'imported_file', 'user', 'state',
                    'creation_date')
admin.site.register(models.Import, ImportAdmin)


class TargetKeyAdmin(admin.ModelAdmin):
    list_display = ('target', 'importer_type', 'column_nb', 'key',
                    'value', 'is_set')
    list_filter = ("is_set", "target__column__importer_type")
    search_fields = ('target__target', 'value', 'key')
admin.site.register(models.TargetKey, TargetKeyAdmin)


class OperationTypeAdmin(GeneralTypeAdmin):
    list_display = GeneralTypeAdmin.list_display + ['order', 'preventive']
    model = models.OperationType

admin.site.register(models.OperationType, OperationTypeAdmin)


class SpatialReferenceSystemAdmin(GeneralTypeAdmin):
    list_display = GeneralTypeAdmin.list_display + ['order', 'srid']
    model = models.SpatialReferenceSystem
admin.site.register(models.SpatialReferenceSystem, SpatialReferenceSystemAdmin)


class IshtarUserAdmin(admin.ModelAdmin):
    readonly_fields = ('password',)

admin.site.register(models.IshtarUser, IshtarUserAdmin)


class ItemKeyAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'key', 'content_object', 'importer')
    search_fields = ('key', )
admin.site.register(models.ItemKey, ItemKeyAdmin)


class AdministrationScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'path']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('path',)
        return []

admin.site.register(models.AdministrationScript, AdministrationScriptAdmin)


class AdministrationTaskAdmin(admin.ModelAdmin):
    readonly_fields = ('state', 'creation_date', 'launch_date',
                       'finished_date', "result", )
    list_display = ['script', 'state', 'creation_date', 'launch_date',
                    'finished_date', "result"]
    list_filter = ['script', 'state']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("script", ) + self.readonly_fields
        return self.readonly_fields

admin.site.register(models.AdministrationTask, AdministrationTaskAdmin)


basic_models = [models.DocumentTemplate]
if settings.COUNTRY == 'fr':
    basic_models += [models.Arrondissement, models.Canton]

for model in basic_models:
    admin.site.register(model)
