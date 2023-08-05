#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2016  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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
Finds forms definitions
"""

import logging

from django import forms
from django.conf import settings
from django.core import validators
from django.core.exceptions import PermissionDenied
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from ishtar_common.models import valid_id, valid_ids, get_current_profile, \
    SpatialReferenceSystem
from archaeological_operations.models import Period, ArchaeologicalSite, \
    RelationType as OpeRelationType
from archaeological_context_records.models import DatingType, DatingQuality, \
    ContextRecord, RelationType as CRRelationType
import models

from ishtar_common.forms import FormSet, FloatField, \
    get_form_selection, reverse_lazy, TableSelect, get_now, FinalForm, \
    ManageOldType

from ishtar_common.forms_common import get_town_field, SourceSelect
from ishtar_common.utils import convert_coordinates_to_point
from ishtar_common import widgets
from archaeological_operations.widgets import OAWidget

from archaeological_warehouse.models import Warehouse

from archaeological_finds.forms_treatments import TreatmentSelect, \
    TreatmentFormSelection, BaseTreatmentForm, TreatmentModifyForm, \
    AdministrativeActTreatmentForm, TreatmentFormFileChoice, \
    TreatmentDeletionForm, TreatmentFileSelect, TreatmentFileFormSelection, \
    TreatmentFileForm, TreatmentFileModifyForm, TreatmentFileDeletionForm, \
    AdministrativeActTreatmentFormSelection, \
    AdministrativeActTreatmentModifForm, \
    AdministrativeActTreatmentFileForm, \
    AdministrativeActTreatmentFileFormSelection, \
    AdministrativeActTreatmentFileModifForm, SourceTreatmentFormSelection, \
    SourceTreatmentFileFormSelection, TreatmentSourceFormSelection, \
    TreatmentFileSourceFormSelection, DashboardForm as DashboardTreatmentForm, \
    DashboardTreatmentFileForm

__all__ = [
    'TreatmentSelect', 'TreatmentFormSelection', 'BaseTreatmentForm',
    'TreatmentModifyForm', 'AdministrativeActTreatmentForm',
    'TreatmentFormFileChoice', 'TreatmentDeletionForm',
    'AdministrativeActTreatmentModifForm', 'TreatmentFileSelect',
    'TreatmentFileFormSelection', 'TreatmentFileForm',
    'TreatmentFileModifyForm', 'TreatmentFileDeletionForm',
    'AdministrativeActTreatmentFileForm',
    'AdministrativeActTreatmentFileFormSelection',
    'AdministrativeActTreatmentFormSelection',
    'AdministrativeActTreatmentFileModifForm', 'SourceTreatmentFormSelection',
    'SourceTreatmentFileFormSelection', 'TreatmentSourceFormSelection',
    'TreatmentFileSourceFormSelection', 'DashboardTreatmentForm',
    'DashboardTreatmentFileForm',
    'RecordFormSelection', 'FindForm', 'DateForm', 'DatingFormSet',
    'FindSelect', 'FindFormSelection', 'FindFormSelectionWarehouseModule',
    'MultipleFindFormSelection', 'MultipleFindFormSelectionWarehouseModule',
    'FindMultipleFormSelection', 'check_form', 'check_exist', 'check_not_exist',
    'check_value', 'check_type_field', 'check_type_not_field',
    'check_treatment', 'ResultFindForm', 'ResultFindFormSet',
    'FindDeletionForm', 'UpstreamFindFormSelection', 'SourceFindFormSelection',
    'FindSourceSelect', 'FindSourceFormSelection', 'NewFindBasketForm',
    'SelectFindBasketForm', 'DeleteFindBasketForm', 'FindBasketAddItemForm']

logger = logging.getLogger(__name__)


class RecordFormSelection(forms.Form):
    form_label = _("Context record")
    base_models = ['get_first_base_find']
    associated_models = {'get_first_base_find__context_record': ContextRecord}
    get_first_base_find__context_record = forms.IntegerField(
        label=_(u"Context record"), required=False,
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-contextrecord'),
            associated_model=ContextRecord),
        validators=[valid_id(ContextRecord)])

    def __init__(self, *args, **kwargs):
        super(RecordFormSelection, self).__init__(*args, **kwargs)
        # get the current operation and restrict search to it
        cr_pk = None
        if 'data' in kwargs and kwargs['data']:
            cr_pk = kwargs['data'].get(
                'get_first_base_find__context_record')
        if not cr_pk and 'initial' in kwargs and kwargs['initial']:
            cr_pk = kwargs['initial'].get(
                'get_first_base_find__context_record')
        if not cr_pk:
            return
        try:
            cr = ContextRecord.objects.get(pk=cr_pk)
        except ContextRecord.DoesNotExist:
            return
        widget = self.fields['get_first_base_find__context_record'].widget
        widget.source = unicode(widget.source) + "?operation__pk={}".format(
            cr.operation.pk)


class FindForm(ManageOldType, forms.Form):
    file_upload = True
    form_label = _("Find")
    base_models = ['get_first_base_find', 'object_type', 'material_type',
                   'preservation_to_consider', 'integritie',
                   'remarkabilitie']
    associated_models = {'material_type': models.MaterialType,
                         'conservatory_state': models.ConservatoryState,
                         'object_type': models.ObjectType,
                         'preservation_to_consider': models.PreservationType,
                         'integritie': models.IntegrityType,
                         'get_first_base_find__batch': models.BatchType,
                         'remarkabilitie': models.RemarkabilityType,
                         'get_first_base_find__spatial_reference_system':
                         SpatialReferenceSystem}
    label = forms.CharField(
        label=_(u"Free ID"),
        validators=[validators.MaxLengthValidator(60)])
    previous_id = forms.CharField(label=_("Previous ID"), required=False)
    description = forms.CharField(label=_("Description"),
                                  widget=forms.Textarea, required=False)
    get_first_base_find__discovery_date = forms.DateField(
        label=_(u"Discovery date"), widget=widgets.JQueryDate, required=False)
    get_first_base_find__batch = forms.ChoiceField(
        label=_(u"Batch/object"), choices=[],
        required=False)
    is_complete = forms.NullBooleanField(label=_(u"Is complete?"),
                                         required=False)
    material_type = widgets.Select2MultipleField(
        label=_(u"Material type"), required=False
    )
    conservatory_state = forms.ChoiceField(label=_(u"Conservatory state"),
                                           choices=[], required=False)
    conservatory_comment = forms.CharField(
        label=_(u"Conservatory comment"), required=False,
        widget=forms.Textarea)
    object_type = widgets.Select2MultipleField(
        label=_(u"Object types"), required=False,
    )
    preservation_to_consider = forms.MultipleChoiceField(
        label=_(u"Preservation type"), choices=[],
        widget=widgets.Select2Multiple, required=False)
    integritie = forms.MultipleChoiceField(
        label=_(u"Integrity / interest"), choices=[],
        widget=widgets.Select2Multiple, required=False)
    remarkabilitie = forms.MultipleChoiceField(
        label=_(u"Remarkability"), choices=[],
        widget=widgets.Select2Multiple, required=False)
    get_first_base_find__topographic_localisation = forms.CharField(
        label=_(u"Point of topographic reference"),
        required=False, max_length=120
    )
    get_first_base_find__x = forms.FloatField(label=_(u"X"), required=False)
    get_first_base_find__y = forms.FloatField(label=_(u"Y"), required=False)
    get_first_base_find__z = forms.FloatField(label=_(u"Z"), required=False)
    get_first_base_find__spatial_reference_system = \
        forms.ChoiceField(label=_(u"Spatial Reference System"), required=False,
                          choices=[])
    get_first_base_find__estimated_error_x = \
        forms.FloatField(label=_(u"Estimated error for X"), required=False)
    get_first_base_find__estimated_error_y = \
        forms.FloatField(label=_(u"Estimated error for Y"), required=False)
    get_first_base_find__estimated_error_z = \
        forms.FloatField(label=_(u"Estimated error for Z"), required=False)
    length = FloatField(label=_(u"Length (cm)"), required=False)
    width = FloatField(label=_(u"Width (cm)"), required=False)
    height = FloatField(label=_(u"Height (cm)"), required=False)
    diameter = FloatField(label=_(u"Diameter (cm)"), required=False)
    thickness = FloatField(label=_(u"Thickness (cm)"), required=False)
    volume = FloatField(label=_(u"Volume (l)"), required=False)
    weight = FloatField(label=_(u"Weight (g)"), required=False)
    dimensions_comment = forms.CharField(
        label=_(u"Dimensions comment"), required=False, widget=forms.Textarea)
    find_number = forms.IntegerField(label=_(u"Find number"), required=False)
    min_number_of_individuals = forms.IntegerField(
        label=_(u"Minimum number of individuals (MNI)"), required=False)
    mark = forms.CharField(label=_(u"Mark"), required=False)
    checked = forms.ChoiceField(label=_(u"Check"))
    check_date = forms.DateField(
        initial=get_now, label=_(u"Check date"), widget=widgets.JQueryDate)
    comment = forms.CharField(label=_(u"Comment"), required=False,
                              widget=forms.Textarea)
    dating_comment = forms.CharField(
        label=_(u"Comment on dating"), required=False, widget=forms.Textarea)
    estimated_value = FloatField(label=_(u"Estimated value"), required=False)
    image = forms.ImageField(
        label=_(u"Image"), help_text=mark_safe(
            _(u"<p>Heavy images are resized to: %(width)dx%(height)d "
              u"(ratio is preserved).</p>") % {
                'width': settings.IMAGE_MAX_SIZE[0],
                'height': settings.IMAGE_MAX_SIZE[1]}),
        max_length=255, required=False, widget=widgets.ImageFileInput())

    def __init__(self, *args, **kwargs):
        super(FindForm, self).__init__(*args, **kwargs)
        if not get_current_profile().mapping:
            for k in ['get_first_base_find__x', 'get_first_base_find__y',
                      'get_first_base_find__z',
                      'get_first_base_find__estimated_error_x',
                      'get_first_base_find__estimated_error_y',
                      'get_first_base_find__estimated_error_z',
                      'get_first_base_find__spatial_reference_system',]:
                self.fields.pop(k)
        else:
            srs = 'get_first_base_find__spatial_reference_system'
            self.fields[srs].choices = \
                SpatialReferenceSystem.get_types(
                    initial=self.init_data.get(srs))
            self.fields[srs].help_text = \
                SpatialReferenceSystem.get_help()
        self.fields['checked'].choices = models.CHECK_CHOICES
        self.fields['material_type'].choices = models.MaterialType.get_types(
            initial=self.init_data.get('material_type'),
            empty_first=False
        )
        self.fields['material_type'].help_text = models.MaterialType.get_help()

        self.fields['object_type'].choices = models.ObjectType.get_types(
            initial=self.init_data.get('object_type'),
            empty_first=False
        )
        self.fields['object_type'].help_text = models.ObjectType.get_help()

        self.fields['get_first_base_find__batch'].choices = \
            models.BatchType.get_types(
                initial=self.init_data.get('get_first_base_find__batch'))
        self.fields['get_first_base_find__batch'].help_text = \
            models.BatchType.get_help()

        self.fields['conservatory_state'].choices = \
            models.ConservatoryState.get_types(
                initial=self.init_data.get('conservatory_state'))
        self.fields['conservatory_state'].help_text = \
            models.ConservatoryState.get_help()

        self.fields['preservation_to_consider'].choices = \
            models.PreservationType.get_types(
                empty_first=False,
                initial=self.init_data.get('preservation_to_consider'))
        self.fields['preservation_to_consider'].help_text = \
            models.PreservationType.get_help()
        self.fields['integritie'].choices = \
            models.IntegrityType.get_types(
                empty_first=False,
                initial=self.init_data.get('integritie'))
        self.fields['integritie'].help_text = \
            models.IntegrityType.get_help()
        self.fields['remarkabilitie'].choices = \
            models.RemarkabilityType.get_types(
                empty_first=False,
                initial=self.init_data.get('remarkabilitie'))
        self.fields['remarkabilitie'].help_text = \
            models.RemarkabilityType.get_help()
        self.fields['estimated_value'].label = u"{} ({})".format(
            unicode(self.fields['estimated_value'].label),
            get_current_profile().currency)

    def clean(self):
        if not get_current_profile().mapping:
            return self.cleaned_data
        x = self.cleaned_data.get('get_first_base_find__x', None)
        y = self.cleaned_data.get('get_first_base_find__y', None)
        s = 'get_first_base_find__spatial_reference_system'
        srs = self.cleaned_data.get(s, None)
        if srs:
            try:
                srs = SpatialReferenceSystem.objects.get(pk=srs)
            except SpatialReferenceSystem.DoesNotExist:
                srs = None
        if x and y and not srs:
            raise forms.ValidationError(
                _(u"You should at least provide X, Y and the spatial "
                  u"reference system used."))
        if x and y and srs:
            try:
                convert_coordinates_to_point(
                    x, y, self.cleaned_data.get('get_first_base_find__z', None),
                    srs.srid)
            except forms.ValidationError as e:
                raise forms.ValidationError(
                    unicode(_(u"Coordinates are not relevant for the spatial "
                              u"reference system used: {}.")).format(e))
        return self.cleaned_data


class DateForm(ManageOldType, forms.Form):
    form_label = _("Dating")
    base_model = 'dating'
    associated_models = {'dating_type': DatingType,
                         'quality': DatingQuality,
                         'period': Period}
    period = forms.ChoiceField(label=_("Period"), choices=[])
    start_date = forms.IntegerField(label=_(u"Start date"),
                                    required=False)
    end_date = forms.IntegerField(label=_(u"End date"), required=False)
    quality = forms.ChoiceField(label=_("Quality"), required=False,
                                choices=[])
    dating_type = forms.ChoiceField(label=_("Dating type"),
                                    required=False, choices=[])
    precise_dating = forms.CharField(label=_("Precise dating"),
                                     required=False)

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['dating_type'].choices = DatingType.get_types(
            initial=self.init_data.get('dating_type'))
        self.fields['dating_type'].help_text = DatingType.get_help()
        self.fields['period'].choices = Period.get_types(
            initial=self.init_data.get('period'))
        self.fields['period'].help_text = Period.get_help()
        self.fields['quality'].choices = DatingQuality.get_types(
            initial=self.init_data.get('quality'))
        self.fields['quality'].help_text = DatingQuality.get_help()


DatingFormSet = formset_factory(DateForm, can_delete=True,
                                formset=FormSet)
DatingFormSet.form_label = _("Dating")


class FindSelect(TableSelect):
    base_finds__cache_short_id = forms.CharField(label=_(u"Short ID"))
    base_finds__cache_complete_id = forms.CharField(label=_(u"Complete ID"))
    label = forms.CharField(label=_(u"Free ID"))
    base_finds__context_record__parcel__town = get_town_field()
    base_finds__context_record__operation__year = forms.IntegerField(
        label=_(u"Year"))
    base_finds__context_record__operation__operation_code = forms.IntegerField(
        label=_(u"Operation's number (index by year)"))
    base_finds__context_record__operation__code_patriarche = \
        forms.IntegerField(
            label=_(u"Code PATRIARCHE"),
            widget=OAWidget
        )
    archaeological_sites = forms.IntegerField(
        label=_("Archaeological site"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-archaeologicalsite'),
            associated_model=ArchaeologicalSite),
        validators=[valid_id(ArchaeologicalSite)])
    base_finds__context_record = forms.IntegerField(
        label=_("Context record"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-contextrecord'),
            associated_model=ContextRecord),
        validators=[valid_id(ContextRecord)])
    ope_relation_types = forms.MultipleChoiceField(
        label=_(u"Search within related operations"), choices=[],
        widget=widgets.CheckboxSelectMultiple)
    cr_relation_types = forms.MultipleChoiceField(
        label=_(u"Search within related context records"), choices=[],
        widget=widgets.CheckboxSelectMultiple)
    datings__period = forms.ChoiceField(label=_(u"Period"), choices=[])
    material_types = forms.ChoiceField(label=_(u"Material type"), choices=[])
    object_types = forms.ChoiceField(label=_(u"Object type"), choices=[])
    preservation_to_considers = forms.ChoiceField(
        choices=[], label=_(u"Preservation type"))
    conservatory_state = forms.ChoiceField(label=_(u"Conservatory state"),
                                           choices=[])
    integrities = forms.ChoiceField(label=_(u"Integrity / interest"),
                                    choices=[])
    remarkabilities = forms.ChoiceField(label=_(u"Remarkability"),
                                        choices=[])
    base_finds__find__description = forms.CharField(label=_(u"Description"))
    base_finds__batch = forms.ChoiceField(
        label=_(u"Batch/object"), choices=[])
    checked = forms.ChoiceField(label=_("Check"))
    image__isnull = forms.NullBooleanField(label=_(u"Has an image?"))

    def __init__(self, *args, **kwargs):
        super(FindSelect, self).__init__(*args, **kwargs)
        self.fields['datings__period'].choices = Period.get_types()
        self.fields['datings__period'].help_text = Period.get_help()
        self.fields['material_types'].choices = \
            models.MaterialType.get_types()
        self.fields['material_types'].help_text = \
            models.MaterialType.get_help()
        self.fields['conservatory_state'].choices = \
            models.ConservatoryState.get_types()
        self.fields['conservatory_state'].help_text = \
            models.ConservatoryState.get_help()

        self.fields['base_finds__batch'].choices = \
            models.BatchType.get_types()
        self.fields['base_finds__batch'].help_text = \
            models.BatchType.get_help()

        self.fields['object_types'].choices = \
            models.ObjectType.get_types()
        self.fields['checked'].choices = \
            [('', '--')] + list(models.CHECK_CHOICES)
        self.fields['preservation_to_considers'].choices = \
            models.PreservationType.get_types()
        self.fields['preservation_to_considers'].help_text = \
            models.PreservationType.get_help()
        self.fields['integrities'].choices = \
            models.IntegrityType.get_types()
        self.fields['integrities'].help_text = \
            models.IntegrityType.get_help()
        self.fields['remarkabilities'].choices = \
            models.RemarkabilityType.get_types()
        self.fields['remarkabilities'].help_text = \
            models.RemarkabilityType.get_help()
        self.fields['ope_relation_types'].choices = OpeRelationType.get_types(
            empty_first=False)
        self.fields['cr_relation_types'].choices = CRRelationType.get_types(
            empty_first=False)

    def get_input_ids(self):
        ids = super(FindSelect, self).get_input_ids()
        ids.pop(ids.index('ope_relation_types'))
        for idx, c in enumerate(self.fields['ope_relation_types'].choices):
            ids.append('ope_relation_types_{}'.format(idx))
        ids.pop(ids.index('cr_relation_types'))
        for idx, c in enumerate(self.fields['cr_relation_types'].choices):
            ids.append('cr_relation_types_{}'.format(idx))
        return ids


class FindSelectWarehouseModule(FindSelect):
    container__location = forms.IntegerField(
        label=_(u"Warehouse (location)"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-warehouse'),
            associated_model=Warehouse),
        validators=[valid_id(Warehouse)])
    container__responsible = forms.IntegerField(
        label=_(u"Warehouse (responsible)"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-warehouse'),
            associated_model=Warehouse),
        validators=[valid_id(Warehouse)])
    container__index = forms.IntegerField(label=_(u"Container ID"))
    container__reference = forms.IntegerField(label=_(u"Container ref."))


class FindFormSelection(forms.Form):
    form_label = _("Find search")
    associated_models = {'pk': models.Find}
    currents = {'pk': models.Find}
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-find'),
            FindSelect, models.Find,
            source_full=reverse_lazy('get-find-full')),
        validators=[valid_id(models.Find)])


class FindFormSelectionWarehouseModule(FindFormSelection):
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-find'),
            FindSelectWarehouseModule, models.Find,
            source_full=reverse_lazy('get-find-full')),
        validators=[valid_id(models.Find)])


class MultipleFindFormSelection(forms.Form):
    form_label = _("Find search")
    associated_models = {'pk': models.Find}
    currents = {'pk': models.Find}
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-find'),
            FindSelect, models.Find,
            multiple_select=True,
            source_full=reverse_lazy('get-find-full')),
        validators=[valid_id(models.Find)])


class MultipleFindFormSelectionWarehouseModule(MultipleFindFormSelection):
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-find'),
            FindSelectWarehouseModule, models.Find,
            multiple_select=True,
            source_full=reverse_lazy('get-find-full')),
        validators=[valid_id(models.Find)])


class FindMultipleFormSelection(forms.Form):
    form_label = _(u"Upstream finds")
    associated_models = {'finds': models.Find}
    associated_labels = {'finds': _(u"Finds")}
    # using FindSelectWarehouseModule because this form is only used with
    # the warehouse module activated
    finds = forms.CharField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-find'), FindSelectWarehouseModule, models.Find,
            multiple=True, multiple_cols=[2, 3, 4]),
        validators=[valid_ids(models.Find)])

    def clean(self):
        if 'finds' not in self.cleaned_data or not self.cleaned_data['finds']:
            raise forms.ValidationError(_(u"You should at least select one "
                                          u"archaeological find."))
        return self.cleaned_data


def check_form(wizard, form_name, key):
    request = wizard.request
    storage = wizard.storage
    if storage.prefix not in request.session or \
            'step_data' not in request.session[storage.prefix] or \
            form_name not in request.session[storage.prefix]['step_data'] or \
                            form_name + '-' + key not in \
            request.session[storage.prefix]['step_data'][form_name]:
        return False
    return True


def check_exist(form_name, key):
    def func(self):
        request = self.request
        storage = self.storage
        if not check_form(self, form_name, key):
            return False
        try:
            val = request.session[storage.prefix][
                'step_data'][form_name][form_name + '-' + key]
            if val and len(val) > 0:
                val = val[0]
            return bool(val)
        except ValueError:
            return False
    return func


def check_not_exist(form_name, key):
    def func(self):
        return not check_exist(form_name, key)(self)
    return func


def check_value(form_name, key, value):
    def func(self):
        request = self.request
        storage = self.storage
        if not check_form(self, form_name, key):
            return False
        try:
            val = request.session[storage.prefix][
                'step_data'][form_name][form_name + '-' + key]
            if val and len(val) > 0:
                val = val[0]
            return unicode(val) == unicode(value)
        except ValueError:
            return False
    return func


def check_type_field(form_name, key, model, field):
    def func(self):
        request = self.request
        storage = self.storage
        if not check_form(self, form_name, key):
            return False
        try:
            val = model.objects.get(pk=request.session[storage.prefix][
                'step_data'][form_name][form_name + '-' + key][0])
            return bool(getattr(val, field))
        except (ValueError, model.DoesNotExist):
            return False
    return func


def check_type_not_field(form_name, key, model, field):
    def func(self):
        return not check_type_field(form_name, key, model, field)(self)
    return func


def check_treatment(form_name, type_key, type_list=[], not_type_list=[]):
    type_list = [models.TreatmentType.objects.get(txt_idx=tpe).pk
                 for tpe in type_list]
    not_type_list = [models.TreatmentType.objects.get(txt_idx=tpe).pk
                     for tpe in not_type_list]

    def func(self):
        request = self.request
        storage = self.storage
        if not check_form(self, form_name, type_key):
            return False
        try:
            tpe = request.session[storage.prefix][
                'step_data'][form_name][form_name + '-' + type_key]
            if not tpe:
                return False
            type = int(tpe[0])
            return (not type_list or type in type_list) \
                and type not in not_type_list
        except ValueError:
            return False
    return func


class ResultFindForm(ManageOldType, forms.Form):
    form_label = _(u"Resulting find")
    associated_models = {'material_type': models.MaterialType}
    label = forms.CharField(
        label=_(u"Free ID"),
        validators=[validators.MaxLengthValidator(60)])
    description = forms.CharField(label=_(u"Precise description"),
                                  widget=forms.Textarea)
    material_type = forms.ChoiceField(label=_(u"Material type"), choices=[])
    volume = forms.IntegerField(label=_(u"Volume (l)"))
    weight = forms.IntegerField(label=_(u"Weight (g)"))
    find_number = forms.IntegerField(label=_(u"Find number"))

    def __init__(self, *args, **kwargs):
        super(ResultFindForm, self).__init__(*args, **kwargs)
        self.fields['material_type'].choices = models.MaterialType.get_types(
            initial=self.init_data.get('material_type'))
        self.fields['material_type'].help_text = models.MaterialType.get_help()

ResultFindFormSet = formset_factory(ResultFindForm, can_delete=True,
                                    formset=FormSet)
ResultFindFormSet.form_label = _(u"Resulting finds")


class FindDeletionForm(FinalForm):
    confirm_msg = " "
    confirm_end_msg = _(u"Would you like to delete this find?")


class UpstreamFindFormSelection(FindFormSelection):
    form_label = _(u"Upstream find")

    def __init__(self, *args, **kwargs):
        super(UpstreamFindFormSelection, self).__init__(*args, **kwargs)
        self.fields['pk'].required = True
        self.fields['resulting_pk'] = self.fields.pop('pk')


##############################################
# Source management for archaeological finds #
##############################################

SourceFindFormSelection = get_form_selection(
    'SourceFindFormSelection', _(u"Archaeological find search"), 'find',
    models.Find, FindSelect, 'get-find',
    _(u"You should select an archaeological find."))


class FindSourceSelect(SourceSelect):
    find__base_finds__context_record__operation__year = forms.IntegerField(
        label=_(u"Year of the operation"))
    find__base_finds__context_record__operation__operation_code = \
        forms.IntegerField(label=_(u"Numeric reference"))
    if settings.COUNTRY == 'fr':
        find__base_finds__context_record__operation__code_patriarche = \
            forms.IntegerField(
                widget=OAWidget,
                label="Code PATRIARCHE")
    find__datings__period = forms.ChoiceField(
        label=_(u"Period of the archaeological find"), choices=[])
    find__material_type = forms.ChoiceField(
        label=_("Material type of the archaeological find"), choices=[])
    find__description = forms.CharField(
        label=_(u"Description of the archaeological find"))

    def __init__(self, *args, **kwargs):
        super(FindSourceSelect, self).__init__(*args, **kwargs)
        self.fields['find__datings__period'].choices = Period.get_types()
        self.fields['find__datings__period'].help_text = Period.get_help()
        self.fields['find__material_type'].choices = \
            models.MaterialType.get_types()
        self.fields['find__material_type'].help_text = \
            models.MaterialType.get_help()

FindSourceFormSelection = get_form_selection(
    'FindSourceFormSelection', _(u"Documentation search"), 'pk',
    models.FindSource, FindSourceSelect, 'get-findsource',
    _(u"You should select a document."),
    get_full_url='get-findsource-full')


class NewFindBasketForm(forms.ModelForm):
    class Meta:
        model = models.FindBasket
        fields = ('label', 'comment')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewFindBasketForm, self).__init__(*args, **kwargs)

    def clean(self):
        q = models.FindBasket.objects.filter(user=self.user,
                                             label=self.cleaned_data['label'])
        if q.count():
            raise forms.ValidationError(_(u"Another basket already exists with "
                                          u"this name."))
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.user = self.user
        return super(NewFindBasketForm, self).save(commit)


class SelectFindBasketForm(forms.Form):
    form_label = _(u"Basket")
    associated_models = {'basket': models.FindBasket}
    need_user_for_initialization = True

    basket = forms.ChoiceField(label=_(u"Basket"), required=True, choices=[])

    def __init__(self, *args, **kwargs):
        self.user = None
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(SelectFindBasketForm, self).__init__(*args, **kwargs)
        if not self.user:
            return
        self.fields['basket'].choices = [('', '--')] + [
            (b.pk, unicode(b))
            for b in models.FindBasket.objects.filter(user=self.user)]


class DeleteFindBasketForm(SelectFindBasketForm):
    def save(self):
        try:
            models.FindBasket.objects.get(pk=self.cleaned_data['basket'],
                                          user=self.user).delete()
        except models.FindBasket.DoesNotExist:
            # something strange... TODO: log it
            pass
        return


class FindBasketAddItemForm(forms.Form):
    basket_id = forms.IntegerField(required=True)
    item_id = forms.IntegerField(required=True)

    def save(self, user):
        try:
            basket = models.FindBasket.objects.get(
                pk=self.cleaned_data['basket_id'], user=user.ishtaruser)
            item = models.Find.objects.get(
                pk=self.cleaned_data['item_id'])
        except models.FindBasket.DoesNotExist or\
                models.Find.DoesNotExist:
            # something strange... TODO: log it
            raise PermissionDenied
        # check rights
        if not user.is_superuser and \
                not user.ishtaruser.has_right('change_find') and \
                not (user.ishtaruser.has_right('change_own_find')
                     and item.is_own(user)):
            raise PermissionDenied
        basket.items.add(item)
        return basket
