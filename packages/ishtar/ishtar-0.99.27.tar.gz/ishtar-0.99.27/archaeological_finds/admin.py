#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from django.contrib import admin

from ishtar_common.admin import HistorizedObjectAdmin, GeneralTypeAdmin

import models


class BaseFindAdmin(HistorizedObjectAdmin):
    list_display = ('label', 'context_record', 'batch')
    search_fields = ('label', 'context_record__parcel__operation__name',)
    model = models.BaseFind

admin.site.register(models.BaseFind, BaseFindAdmin)


class FindAdmin(HistorizedObjectAdmin):
    list_display = ('label', 'dating', 'volume', 'weight',
                    'find_number',)
    search_fields = ('label', "datings__period__label")
    model = models.Find

admin.site.register(models.Find, FindAdmin)


class FindSourceAdmin(admin.ModelAdmin):
    list_display = ('find', 'title', 'source_type',)
    list_filter = ('source_type',)
    search_fields = ('title', )
    model = models.FindSource

admin.site.register(models.FindSource, FindSourceAdmin)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ['find', 'person', 'start_date', 'end_date']
    search_fields = ('find__label', 'person__name')
    model = models.Property

admin.site.register(models.Property, PropertyAdmin)


class TreatmentAdmin(HistorizedObjectAdmin):
    list_display = ('location', 'treatment_types_lbl', 'container', 'person')
    model = models.Treatment

admin.site.register(models.Treatment, TreatmentAdmin)


class TreatmentFileAdmin(HistorizedObjectAdmin):
    list_display = ('year', 'index', 'name', 'internal_reference')
    search_fields = ('cached_label',)
    model = models.TreatmentFile

admin.site.register(models.TreatmentFile, TreatmentFileAdmin)


class TreatmentSourceAdmin(admin.ModelAdmin):
    list_display = ('treatment', 'title', 'source_type',)
    list_filter = ('source_type',)
    search_fields = ('title',)
    model = models.TreatmentSource

admin.site.register(models.TreatmentSource, TreatmentSourceAdmin)


class HierarchicalTypeAdmin(GeneralTypeAdmin):
    list_display = ['label', 'txt_idx', 'parent', 'available', 'comment']

admin.site.register(models.ObjectType, HierarchicalTypeAdmin)


class MaterialTypeAdmin(HierarchicalTypeAdmin):
    list_display = HierarchicalTypeAdmin.list_display + ['recommendation']
    search_fields = ('label', 'parent__label', 'comment',)

admin.site.register(models.MaterialType, MaterialTypeAdmin)


class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = HierarchicalTypeAdmin.list_display + [
        'order', 'virtual', 'upstream_is_many', 'downstream_is_many']
    model = models.TreatmentType
admin.site.register(models.TreatmentType, TreatmentTypeAdmin)

general_models = [
    models.ConservatoryState, models.RemarkabilityType,
    models.PreservationType, models.IntegrityType,
    models.TreatmentFileType, models.TreatmentState,
    models.BatchType
]
for model in general_models:
    admin.site.register(model, GeneralTypeAdmin)
