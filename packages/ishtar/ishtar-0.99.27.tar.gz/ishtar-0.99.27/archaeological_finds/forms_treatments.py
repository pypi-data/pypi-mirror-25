#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

import datetime
import logging

from django import forms
from django.conf import settings
from django.core import validators
from django.db.models import Max
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from ishtar_common.models import Person, valid_id, Organization, \
    get_current_profile
from archaeological_operations.models import ActType, AdministrativeAct
from archaeological_warehouse.models import Warehouse, Container
import models

from archaeological_operations.forms import AdministrativeActOpeForm, \
    AdministrativeActOpeFormSelection, AdministrativeActModifForm

from ishtar_common.forms import reverse_lazy, TableSelect, FinalForm, \
    ManageOldType, get_form_selection
from ishtar_common.forms_common import SourceForm, SourceSelect, \
    SourceDeletionForm

from ishtar_common import widgets

logger = logging.getLogger(__name__)

# Treatment


class TreatmentSelect(TableSelect):
    label = forms.CharField(label=_(u"Label"))
    other_reference = forms.CharField(label=_(u"Other ref."))
    year = forms.IntegerField(label=_(u"Year"))
    index = forms.IntegerField(label=_(u"Index"))
    treatment_types = forms.ChoiceField(label=_(u"Treatment type"), choices=[])
    image = forms.NullBooleanField(label=_(u"Has an image?"))

    def __init__(self, *args, **kwargs):
        super(TreatmentSelect, self).__init__(*args, **kwargs)
        self.fields['treatment_types'].choices = \
            models.TreatmentType.get_types()
        self.fields['treatment_types'].help_text = \
            models.TreatmentType.get_help()


class TreatmentFormSelection(forms.Form):
    form_label = _("Treatment search")
    associated_models = {'pk': models.Treatment}
    currents = {'pk': models.Treatment}
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-treatment'),
            TreatmentSelect, models.Treatment),
        validators=[valid_id(models.Treatment)])


class BaseTreatmentForm(ManageOldType, forms.Form):
    form_label = _(u"Base treatment")
    base_models = ['treatment_type']
    associated_models = {'treatment_type': models.TreatmentType,
                         'person': Person,
                         'location': Warehouse,
                         'organization': Organization,
                         'container': Container,
                         'treatment_state': models.TreatmentState,
                         }
    file_upload = True
    need_user_for_initialization = True

    label = forms.CharField(label=_(u"Label"),
                            max_length=200, required=False)
    other_reference = forms.CharField(
        label=_(u"Other ref."), max_length=200, required=False)
    year = forms.IntegerField(label=_("Year"),
                              initial=lambda: datetime.datetime.now().year,
                              validators=[validators.MinValueValidator(1000),
                                          validators.MaxValueValidator(2100)])
    treatment_type = forms.MultipleChoiceField(
        label=_(u"Treatment type"), choices=[],
        widget=widgets.CheckboxSelectMultiple)
    treatment_state = forms.ChoiceField(label=_(u"State"),
                                        choices=[], required=False)
    target_is_basket = forms.NullBooleanField(label=_(u"Target"))
    person = forms.IntegerField(
        label=_(u"Responsible"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person'), associated_model=Person,
            new=True),
        validators=[valid_id(Person)], required=False)
    organization = forms.IntegerField(
        label=_(u"Organization"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-organization'),
            associated_model=Organization, new=True),
        validators=[valid_id(Organization)], required=False)
    location = forms.IntegerField(
        label=_(u"Location"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-warehouse'), associated_model=Warehouse,
            new=True),
        validators=[valid_id(Warehouse)])
    container = forms.IntegerField(
        label=_(u"Container (relevant for packaging)"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-container'),
            associated_model=Container, new=True),
        validators=[valid_id(Container)], required=False)
    external_id = forms.CharField(
        label=_(u"External ref."), max_length=200, required=False)
    goal = forms.CharField(label=_(u"Goal"),
                           widget=forms.Textarea, required=False)
    description = forms.CharField(label=_(u"Description"),
                                  widget=forms.Textarea, required=False)
    comment = forms.CharField(label=_(u"Comment"),
                              widget=forms.Textarea, required=False)
    start_date = forms.DateField(label=_(u"Start date"), required=False,
                                 widget=widgets.JQueryDate)
    end_date = forms.DateField(label=_(u"Closing date"), required=False,
                               widget=widgets.JQueryDate)
    estimated_cost = forms.FloatField(label=_(u"Estimated cost ({currency})"),
                                      required=False)
    quoted_cost = forms.FloatField(label=_(u"Quoted cost ({currency})"),
                                   required=False)
    realized_cost = forms.FloatField(label=_(u"Realized cost ({currency})"),
                                     required=False)
    insurance_cost = forms.FloatField(label=_(u"Insurance cost ({currency})"),
                                      required=False)
    image = forms.ImageField(
        label=_(u"Image"), help_text=mark_safe(
            _(u"<p>Heavy images are resized to: %(width)dx%(height)d "
              u"(ratio is preserved).</p>") % {
                'width': settings.IMAGE_MAX_SIZE[0],
                'height': settings.IMAGE_MAX_SIZE[1]}),
        max_length=255, required=False, widget=widgets.ImageFileInput())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BaseTreatmentForm, self).__init__(*args, **kwargs)
        # set current currency
        currency = get_current_profile().currency
        for key in ('estimated_cost', 'quoted_cost', 'realized_cost',
                    'insurance_cost'):
            self.fields[key].label = self.fields[key].label.format(
                currency=currency)

        q = Person.objects.filter(ishtaruser__pk=user.pk)
        if q.count():
            person = q.all()[0]
            self.fields['person'].initial = person.pk
            if person.attached_to:
                self.fields['organization'].initial = person.attached_to.pk
        self.fields['target_is_basket'].widget.choices = \
            ((False, _(u"Single find")), (True, _(u"Basket")))
        self.fields['treatment_type'].choices = models.TreatmentType.get_types(
            initial=self.init_data.get('treatment_type'),
            dct={'upstream_is_many': False, 'downstream_is_many': False},
            empty_first=False
        )
        self.fields['treatment_type'].help_text = \
            models.TreatmentType.get_help(
                dct={'upstream_is_many': False, 'downstream_is_many': False})
        self.fields['treatment_state'].choices = \
            models.TreatmentState.get_types(
                initial=self.init_data.get('treatment_state'),
            )
        self.fields['treatment_state'].help_text = \
            models.TreatmentState.get_help()
        # TODO
        """
        self.fields['basket'].required = False
        self.fields['basket'].help_text = \
            _(u"Leave it blank if you want to select a single item")
        self.fields.keyOrder.pop(self.fields.keyOrder.index('basket'))
        self.fields.keyOrder.insert(self.fields.keyOrder.index('description'),
                                    'basket')
        """

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        packaging = models.TreatmentType.get_cache('packaging')
        if not packaging:
            logger.warning("No 'packaging' treatment type defined")
            return
        if data.get('container', None) \
                and str(packaging.pk) not in data.get('treatment_type', []):
            raise forms.ValidationError(
                _(u"The container field is attached to the treatment. If "
                  u"no packaging treatment is done it is not relevant."))
        if not data.get('container', None) \
                and str(packaging.pk) in data.get('treatment_type', []):
            raise forms.ValidationError(
                _(u"If a packaging treatment is done, the container field "
                  u"must be filled."))
        if not data.get('person', None) and not data.get('organization', None):
            raise forms.ValidationError(
                _(u"A responsible or an organization must be defined."))
        return data
        # TODO
        """
        for treatment_type in self.cleaned_data.get('treatment_type', []):
            try:
                treatment = models.TreatmentType.objects.get(
                    pk=treatment_type, available=True)
            except models.TreatmentType.DoesNotExist:
                raise forms.ValidationError(_(u"This treatment type is not "
                                              u"available."))
            if treatment.upstream_is_many and \
                    not self.cleaned_data.get('basket'):
                raise forms.ValidationError(_(u"This treatment needs a "
                                              u"basket."))
        """


class TreatmentModifyForm(BaseTreatmentForm):
    index = forms.IntegerField(_(u"Index"))
    id = forms.IntegerField(' ', widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super(TreatmentModifyForm, self).__init__(*args, **kwargs)
        self.fields.pop('target_is_basket')
        self.fields.keyOrder.pop(self.fields.keyOrder.index('index'))
        self.fields.keyOrder.insert(
            self.fields.keyOrder.index('year') + 1, 'index')

    def clean(self, *args, **kwargs):
        super(TreatmentModifyForm, self).clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        year = cleaned_data.get('year')
        pk = cleaned_data.get('id')
        index = cleaned_data.get('index')
        q = models.Treatment.objects \
            .filter(year=year, index=index).exclude(pk=pk)
        if index and q.count():
            raise forms.ValidationError(
                _(u"Another treatment with this index exists for {}."
                  ).format(year))
        return cleaned_data


class TreatmentFormFileChoice(forms.Form):
    form_label = _(u"Associated request")
    associated_models = {'file': models.TreatmentFile, }
    currents = {'file': models.TreatmentFile}
    file = forms.IntegerField(
        label=_(u"Treatment request"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-treatmentfile'),
            associated_model=models.TreatmentFile),
        validators=[valid_id(models.TreatmentFile)], required=False)


class TreatmentDeletionForm(FinalForm):
    confirm_msg = _(
        u"Are you sure you want to delete this treatment? All changes "
        u"made to the associated finds since this treatment record will be "
        u"lost!")
    confirm_end_msg = _(u"Would you like to delete this treatment?")

SLICING = (("month", _(u"months")), ('year', _(u"years")),)

DATE_SOURCE = (("start", _(u"Start date")), ("end", _(u"Closing date")),)


class DashboardForm(forms.Form):
    slicing = forms.ChoiceField(label=_("Slicing"), choices=SLICING,
                                required=False)
    date_source = forms.ChoiceField(
        label=_("Date get from"), choices=DATE_SOURCE, required=False)
    treatment_type = forms.ChoiceField(label=_("Treatment type"), choices=[],
                                       required=False)
    after = forms.DateField(label=_(u"Date after"),
                            widget=widgets.JQueryDate, required=False)
    before = forms.DateField(label=_(u"Date before"),
                             widget=widgets.JQueryDate, required=False)

    def __init__(self, *args, **kwargs):
        if 'prefix' not in kwargs:
            kwargs['prefix'] = 'treatments'
        super(DashboardForm, self).__init__(*args, **kwargs)
        self.fields['treatment_type'].choices = \
            models.TreatmentType.get_types()

    def get_date_source(self):
        date_source = 'start'
        if hasattr(self, 'cleaned_data') and \
                self.cleaned_data.get('date_source'):
            date_source = self.cleaned_data['date_source']
        return date_source

    def get_filter(self):
        if not hasattr(self, 'cleaned_data') or not self.cleaned_data:
            return {}
        fltr = {}
        date_source = self.get_date_source()
        if self.cleaned_data.get('treatment_type'):
            fltr['treatment_types__pk'] = self.cleaned_data['treatment_type']
        if self.cleaned_data.get('after'):
            fltr[date_source + '_date__gte'] = self.cleaned_data['after']
        if self.cleaned_data.get('before'):
            fltr[date_source + '_date__lte'] = self.cleaned_data['before']
        return fltr

# administrative act treatment


class AdministrativeActTreatmentSelect(TableSelect):
    year = forms.IntegerField(label=_("Year"))
    index = forms.IntegerField(label=_("Index"))
    act_type = forms.ChoiceField(label=_("Act type"), choices=[])
    indexed = forms.NullBooleanField(label=_(u"Indexed?"))
    act_object = forms.CharField(label=_(u"Object"),
                                 max_length=300)

    signature_date_after = forms.DateField(
        label=_(u"Signature date after"), widget=widgets.JQueryDate)
    signature_date_before = forms.DateField(
        label=_(u"Signature date before"), widget=widgets.JQueryDate)
    treatment__name = forms.CharField(
        label=_(u"Treatment name"), max_length=200)
    treatment__year = forms.IntegerField(label=_(u"Treatment year"))
    treatment__index = forms.IntegerField(label=_(u"Treatment index"))
    treatment__internal_reference = forms.CharField(
        max_length=200, label=_(u"Treatment internal reference"))
    treatment__treatment_types = forms.ChoiceField(label=_(u"Treatment type"),
                                                   choices=[])
    history_modifier = forms.IntegerField(
        label=_(u"Modified by"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person',
                         args=['0', 'user']),
            associated_model=Person),
        validators=[valid_id(Person)])

    def __init__(self, *args, **kwargs):
        super(AdministrativeActTreatmentSelect, self).__init__(*args, **kwargs)
        self.fields['act_type'].choices = ActType.get_types(
            dct={'intented_to': 'T'})
        self.fields['act_type'].help_text = ActType.get_help(
            dct={'intented_to': 'T'})
        self.fields['treatment__treatment_types'].choices = \
            models.TreatmentType.get_types()
        self.fields['treatment__treatment_types'].help_text = \
            models.TreatmentType.get_help()


class AdministrativeActTreatmentFormSelection(
        AdministrativeActOpeFormSelection):
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-administrativeacttreatment'),
            AdministrativeActTreatmentSelect, AdministrativeAct),
        validators=[valid_id(AdministrativeAct)])


class AdministrativeActTreatmentForm(AdministrativeActOpeForm):
    act_type = forms.ChoiceField(label=_(u"Act type"), choices=[])

    def __init__(self, *args, **kwargs):
        super(AdministrativeActTreatmentForm, self).__init__(*args, **kwargs)
        self.fields['act_type'].choices = ActType.get_types(
            initial=self.init_data.get('act_type'),
            dct={'intented_to': 'T'})
        self.fields['act_type'].help_text = ActType.get_help(
            dct={'intented_to': 'T'})


class AdministrativeActTreatmentModifForm(
        AdministrativeActModifForm, AdministrativeActTreatmentForm):
    pk = forms.IntegerField(required=False, widget=forms.HiddenInput)
    index = forms.IntegerField(label=_("Index"), required=False)

# treatment requests


class TreatmentFileSelect(TableSelect):
    name = forms.CharField(label=_(u"Name"))
    internal_reference = forms.CharField(label=_(u"Internal ref."))
    year = forms.IntegerField(label=_(u"Year"))
    index = forms.IntegerField(label=_(u"Index"))
    type = forms.ChoiceField(label=_(u"Type"), choices=[])
    in_charge = forms.IntegerField(
        label=_(u"In charge"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person'),
            associated_model=Person),
        validators=[valid_id(Person)])
    applicant = forms.IntegerField(
        label=_(u"Applicant"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person'),
            associated_model=Person),
        validators=[valid_id(Person)])
    applicant_organisation = forms.IntegerField(
        label=_(u"Applicant organisation"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-organization'),
            associated_model=Organization),
        validators=[valid_id(Organization)])

    def __init__(self, *args, **kwargs):
        super(TreatmentFileSelect, self).__init__(*args, **kwargs)
        self.fields['type'].choices = models.TreatmentFileType.get_types()
        self.fields['type'].help_text = models.TreatmentFileType.get_help()


class TreatmentFileFormSelection(forms.Form):
    form_label = _("Treatment request search")
    associated_models = {'pk': models.TreatmentFile}
    currents = {'pk': models.TreatmentFile}
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-treatmentfile'),
            TreatmentFileSelect, models.TreatmentFile),
        validators=[valid_id(models.TreatmentFile)])


class TreatmentFileForm(ManageOldType, forms.Form):
    form_label = _(u"Treatment request")
    base_models = ['treatment_type_type']
    associated_models = {
        'type': models.TreatmentFileType, 'in_charge': Person,
        'applicant': Person, 'applicant_organisation': Organization}
    need_user_for_initialization = True

    name = forms.CharField(label=_(u"Name"),
                           max_length=1000, required=False)
    year = forms.IntegerField(label=_("Year"),
                              initial=lambda: datetime.datetime.now().year,
                              validators=[validators.MinValueValidator(1000),
                                          validators.MaxValueValidator(2100)])
    internal_reference = forms.CharField(
        label=_(u"Internal ref."), max_length=60, required=False)
    external_id = forms.CharField(
        label=_(u"External ref."), max_length=200, required=False)
    type = forms.ChoiceField(
        label=_(u"Type"), choices=[])
    in_charge = forms.IntegerField(
        label=_(u"Responsible"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person'), associated_model=Person,
            new=True),
        validators=[valid_id(Person)])
    applicant = forms.IntegerField(
        label=_(u"Applicant"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person'), associated_model=Person,
            new=True),
        validators=[valid_id(Person)], required=False)
    applicant_organisation = forms.IntegerField(
        label=_(u"Applicant organisation"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-organization'),
            associated_model=Organization, new=True),
        validators=[valid_id(Organization)], required=False)
    comment = forms.CharField(label=_(u"Comment"),
                              widget=forms.Textarea, required=False)
    creation_date = forms.DateField(label=_(u"Start date"), required=False,
                                    widget=widgets.JQueryDate,
                                    initial=lambda: datetime.datetime.now())
    reception_date = forms.DateField(label=_(u"Reception date"), required=False,
                                     widget=widgets.JQueryDate,
                                     initial=lambda: datetime.datetime.now())
    end_date = forms.DateField(label=_(u"Closing date"), required=False,
                               widget=widgets.JQueryDate)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TreatmentFileForm, self).__init__(*args, **kwargs)
        q = Person.objects.filter(ishtaruser__pk=user.pk)
        if q.count():
            person = q.all()[0]
            self.fields['in_charge'].initial = person.pk
        self.fields['type'].choices = models.TreatmentFileType.get_types(
            initial=[self.init_data.get('type')], empty_first=False
        )
        self.fields['type'].help_text = models.TreatmentFileType.get_help()


class TreatmentFileModifyForm(TreatmentFileForm):
    index = forms.IntegerField(_(u"Index"))
    id = forms.IntegerField(' ', widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super(TreatmentFileModifyForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder.pop(self.fields.keyOrder.index('index'))
        self.fields.keyOrder.insert(
            self.fields.keyOrder.index('year') + 1, 'index')

    def clean(self, *args, **kwargs):
        super(TreatmentFileModifyForm, self).clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        year = cleaned_data.get('year')
        pk = cleaned_data.get('id')
        index = cleaned_data.get('index')
        q = models.TreatmentFile.objects \
            .filter(year=year, index=index).exclude(pk=pk)
        if index and q.count():
            raise forms.ValidationError(
                _(u"Another treatment request with this index exists for {}."
                  ).format(year))
        return cleaned_data


class TreatmentFileDeletionForm(FinalForm):
    confirm_msg = _(u"Are you sure you want to delete this treatment request?")
    confirm_end_msg = _(u"Would you like to delete this treatment request?")

DATE_SOURCE_FILE = (
    ("creation", _(u"Creation date")),
    ("reception", _(u"Reception date")),
    ("end", _(u"Closing date")),)


class DashboardTreatmentFileForm(forms.Form):
    slicing = forms.ChoiceField(label=_("Slicing"), choices=SLICING,
                                required=False)
    date_source = forms.ChoiceField(
        label=_("Date get from"), choices=DATE_SOURCE_FILE, required=False)
    treatmentfile_type = forms.ChoiceField(label=_("Treatment request type"),
                                           choices=[], required=False)
    after = forms.DateField(label=_(u"Date after"),
                            widget=widgets.JQueryDate, required=False)
    before = forms.DateField(label=_(u"Date before"),
                             widget=widgets.JQueryDate, required=False)

    def __init__(self, *args, **kwargs):
        if 'prefix' not in kwargs:
            kwargs['prefix'] = 'treatmentfiles'
        super(DashboardTreatmentFileForm, self).__init__(*args, **kwargs)
        self.fields['treatmentfile_type'].choices = \
            models.TreatmentFileType.get_types()

    def get_date_source(self):
        date_source = 'creation'
        if hasattr(self, 'cleaned_data') and \
                self.cleaned_data.get('date_source'):
            date_source = self.cleaned_data['date_source']
        return date_source

    def get_filter(self):
        if not hasattr(self, 'cleaned_data') or not self.cleaned_data:
            return {}
        fltr = {}
        date_source = self.get_date_source()
        if self.cleaned_data.get('treatmentfile_type'):
            fltr['type__pk'] = self.cleaned_data['treatmentfile_type']
        if self.cleaned_data.get('after'):
            fltr[date_source + '_date__gte'] = self.cleaned_data['after']
        if self.cleaned_data.get('before'):
            fltr[date_source + '_date__lte'] = self.cleaned_data['before']
        return fltr


class AdministrativeActTreatmentFileSelect(TableSelect):
    year = forms.IntegerField(label=_("Year"))
    index = forms.IntegerField(label=_("Index"))
    act_type = forms.ChoiceField(label=_("Act type"), choices=[])
    indexed = forms.NullBooleanField(label=_(u"Indexed?"))
    act_object = forms.CharField(label=_(u"Object"),
                                 max_length=300)

    signature_date_after = forms.DateField(
        label=_(u"Signature date after"), widget=widgets.JQueryDate)
    signature_date_before = forms.DateField(
        label=_(u"Signature date before"), widget=widgets.JQueryDate)
    treatment_file__name = forms.CharField(
        label=_(u"Treatment request name"), max_length=200)
    treatment_file__year = forms.IntegerField(
        label=_(u"Treatment request year"))
    treatment_file__index = forms.IntegerField(
        label=_(u"Treatment request index"))
    treatment_file__internal_reference = forms.CharField(
        max_length=200, label=_(u"Treatment request internal reference"))
    treatment_file__type = forms.ChoiceField(label=_(u"Treatment request type"),
                                             choices=[])
    history_modifier = forms.IntegerField(
        label=_(u"Modified by"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person',
                         args=['0', 'user']),
            associated_model=Person),
        validators=[valid_id(Person)])

    def __init__(self, *args, **kwargs):
        super(AdministrativeActTreatmentFileSelect, self).__init__(*args,
                                                                   **kwargs)
        self.fields['act_type'].choices = ActType.get_types(
            dct={'intented_to': 'TF'})
        self.fields['act_type'].help_text = ActType.get_help(
            dct={'intented_to': 'TF'})
        self.fields['treatment_file__type'].choices = \
            models.TreatmentFileType.get_types()
        self.fields['treatment_file__type'].help_text = \
            models.TreatmentFileType.get_help()


class AdministrativeActTreatmentFileFormSelection(
        AdministrativeActOpeFormSelection):
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-administrativeacttreatmentfile'),
            AdministrativeActTreatmentFileSelect, AdministrativeAct),
        validators=[valid_id(AdministrativeAct)])


class AdministrativeActTreatmentFileForm(AdministrativeActOpeForm):
    act_type = forms.ChoiceField(label=_(u"Act type"), choices=[])

    def __init__(self, *args, **kwargs):
        super(AdministrativeActTreatmentFileForm, self).__init__(*args,
                                                                 **kwargs)
        self.fields['act_type'].choices = ActType.get_types(
            initial=self.init_data.get('act_type'),
            dct={'intented_to': 'TF'})
        self.fields['act_type'].help_text = ActType.get_help(
            dct={'intented_to': 'TF'})


class AdministrativeActTreatmentFileModifForm(
        AdministrativeActModifForm, AdministrativeActTreatmentFileForm):
    pk = forms.IntegerField(required=False, widget=forms.HiddenInput)
    index = forms.IntegerField(label=_("Index"), required=False)

SourceTreatmentFormSelection = get_form_selection(
    'SourceTreatmentFormSelection', _(u"Treatment search"), 'treatment',
    models.Treatment, TreatmentSelect, 'get-treatment',
    _(u"You should select a treatment."))

SourceTreatmentFileFormSelection = get_form_selection(
    'SourceTreatmentFileFormSelection', _(u"Treatment request search"),
    'treatment_file',
    models.TreatmentFile, TreatmentFileSelect, 'get-treatmentfile',
    _(u"You should select a treatment request."))


class TreatmentSourceSelect(SourceSelect):
    treatment__name = forms.CharField(
        label=_(u"Treatment name"), max_length=200)
    treatment__year = forms.IntegerField(label=_(u"Treatment year"))
    treatment__index = forms.IntegerField(label=_(u"Treatment index"))
    treatment__internal_reference = forms.CharField(
        max_length=200, label=_(u"Treatment internal reference"))
    treatment__treatment_types = forms.ChoiceField(label=_(u"Treatment type"),
                                                   choices=[])

    def __init__(self, *args, **kwargs):
        super(TreatmentSourceSelect, self).__init__(*args, **kwargs)
        self.fields['treatment__treatment_types'].choices = \
            models.TreatmentType.get_types()
        self.fields['treatment__treatment_types'].help_text = \
            models.TreatmentType.get_help()


TreatmentSourceFormSelection = get_form_selection(
    'TreatmentSourceFormSelection', _(u"Documentation search"), 'pk',
    models.TreatmentSource, TreatmentSourceSelect, 'get-treatmentsource',
    _(u"You should select a document."))


class TreatmentFileSourceSelect(SourceSelect):
    treatment_file__name = forms.CharField(
        label=_(u"Treatment request name"), max_length=200)
    treatment_file__year = forms.IntegerField(
        label=_(u"Treatment request year"))
    treatment_file__index = forms.IntegerField(
        label=_(u"Treatment request index"))
    treatment_file__internal_reference = forms.CharField(
        max_length=200, label=_(u"Treatment request internal reference"))
    treatment_file__type = forms.ChoiceField(label=_(u"Treatment request type"),
                                             choices=[])

    def __init__(self, *args, **kwargs):
        super(TreatmentFileSourceSelect, self).__init__(*args, **kwargs)
        self.fields['treatment_file__type'].choices = \
            models.TreatmentFileType.get_types()
        self.fields['treatment_file__type'].help_text = \
            models.TreatmentFileType.get_help()


TreatmentFileSourceFormSelection = get_form_selection(
    'TreatmentFileSourceFormSelection', _(u"Documentation search"), 'pk',
    models.TreatmentFileSource, TreatmentFileSourceSelect,
    'get-treatmentfilesource', _(u"You should select a document."))
