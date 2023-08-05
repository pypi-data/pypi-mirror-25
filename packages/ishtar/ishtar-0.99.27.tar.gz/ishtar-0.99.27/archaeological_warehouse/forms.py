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

from django import forms
from django.conf import settings
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from ishtar_common.models import Person, valid_id
from archaeological_finds.models import TreatmentType, FindBasket
import models
from ishtar_common import widgets
from ishtar_common.forms import name_validator, reverse_lazy, \
    get_form_selection, TableSelect, ManageOldType, FinalForm, FormSet
from archaeological_finds.forms import FindMultipleFormSelection, \
    SelectFindBasketForm


def get_warehouse_field(label=_(u"Warehouse"), required=True):
    # !FIXME hard_link, reverse_lazy doen't seem to work with formsets
    url = "/" + settings.URL_PATH + 'autocomplete-warehouse'
    widget = widgets.JQueryAutoComplete(url, associated_model=models.Warehouse)
    return forms.IntegerField(widget=widget, label=label, required=required,
                              validators=[valid_id(models.Warehouse)])


class SelectedDivisionForm(ManageOldType, forms.Form):
    form_label = _(u"Division")
    base_model = 'associated_division'
    associated_models = {'division': models.WarehouseDivision,
                         'associated_division': models.WarehouseDivisionLink}
    division = forms.ChoiceField(
        label=_(u"Division"), choices=(), required=False,
        validators=[valid_id(models.WarehouseDivision)])
    order = forms.IntegerField(_(u"Order"), initial=10, required=False)

    def __init__(self, *args, **kwargs):
        super(SelectedDivisionForm, self).__init__(*args, **kwargs)
        self.fields['division'].choices = \
            models.WarehouseDivision.get_types(
            initial=self.init_data.get('division')
        )


class DivisionFormSet(FormSet):
    def clean(self):
        """Checks that no divisions are duplicated."""
        return self.check_duplicate(('division',),
                                    _("There are identical divisions."))

SelectedDivisionFormset = formset_factory(
    SelectedDivisionForm, can_delete=True, formset=DivisionFormSet)
SelectedDivisionFormset.form_label = _(u"Divisions")


class WarehouseSelect(TableSelect):
    name = forms.CharField(label=_(u"Name"))
    warehouse_type = forms.ChoiceField(label=_(u"Warehouse type"), choices=[])
    towns = forms.CharField(label=_(u"Town"))

    def __init__(self, *args, **kwargs):
        super(WarehouseSelect, self).__init__(*args, **kwargs)
        self.fields['warehouse_type'].choices = \
            models.WarehouseType.get_types()
        self.fields['warehouse_type'].help_text = \
            models.WarehouseType.get_help()


class WarehouseFormSelection(forms.Form):
    form_label = _("Warehouse search")
    associated_models = {'pk': models.Warehouse}
    currents = {'pk': models.Warehouse}
    pk = forms.IntegerField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-warehouse'),
            WarehouseSelect, models.Warehouse),
        validators=[valid_id(models.Warehouse)])


class WarehouseForm(ManageOldType, forms.Form):
    form_label = _(u"Warehouse")
    associated_models = {'warehouse_type': models.WarehouseType,
                         'person_in_charge': Person}

    name = forms.CharField(label=_(u"Name"), max_length=200,
                           validators=[name_validator])
    warehouse_type = forms.ChoiceField(label=_(u"Warehouse type"),
                                       choices=[])
    person_in_charge = forms.IntegerField(
        label=_(u"Person in charge"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person'),
            associated_model=Person, new=True),
        validators=[valid_id(Person)],
        required=False)
    comment = forms.CharField(label=_(u"Comment"), widget=forms.Textarea,
                              required=False)
    address = forms.CharField(label=_(u"Address"), widget=forms.Textarea,
                              required=False)
    address_complement = forms.CharField(label=_(u"Address complement"),
                                         widget=forms.Textarea, required=False)
    postal_code = forms.CharField(label=_(u"Postal code"), max_length=10,
                                  required=False)
    town = forms.CharField(label=_(u"Town"), max_length=30, required=False)
    country = forms.CharField(label=_(u"Country"), max_length=30,
                              required=False)
    phone = forms.CharField(label=_(u"Phone"), max_length=18, required=False)
    mobile_phone = forms.CharField(label=_(u"Mobile phone"), max_length=18,
                                   required=False)

    def __init__(self, *args, **kwargs):
        if 'limits' in kwargs:
            kwargs.pop('limits')
        super(WarehouseForm, self).__init__(*args, **kwargs)
        self.fields['warehouse_type'].choices = \
            models.WarehouseType.get_types(
                initial=self.init_data.get('warehouse_type'))
        self.fields['warehouse_type'].help_text = \
            models.WarehouseType.get_help()

    def save(self, user):
        dct = self.cleaned_data
        dct['history_modifier'] = user
        dct['warehouse_type'] = models.WarehouseType.objects.get(
            pk=dct['warehouse_type'])
        if 'person_in_charge' in dct and dct['person_in_charge']:
            dct['person_in_charge'] = models.Person.objects.get(
                pk=dct['person_in_charge'])
        new_item = models.Warehouse(**dct)
        new_item.save()
        return new_item


class WarehouseDeletionForm(FinalForm):
    confirm_msg = _(u"Would you like to delete this warehouse?")
    confirm_end_msg = _(u"Would you like to delete this warehouse?")


class ContainerForm(ManageOldType, forms.Form):
    form_label = _(u"Container")
    file_upload = True
    associated_models = {'container_type': models.ContainerType,
                         'location': models.Warehouse,
                         'responsible': models.Warehouse}
    reference = forms.CharField(label=_(u"Ref."))
    container_type = forms.ChoiceField(label=_(u"Container type"), choices=[])
    location = forms.IntegerField(
        label=_(u"Current location (warehouse)"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-warehouse'),
            associated_model=models.Warehouse, new=True),
        validators=[valid_id(models.Warehouse)])
    responsible = forms.IntegerField(
        label=_(u"Responsible warehouse"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-warehouse'),
            associated_model=models.Warehouse, new=True),
        validators=[valid_id(models.Warehouse)])
    image = forms.ImageField(
        label=_(u"Image"), help_text=mark_safe(
            _(u"<p>Heavy images are resized to: %(width)dx%(height)d "
              u"(ratio is preserved).</p>") % {
                'width': settings.IMAGE_MAX_SIZE[0],
                'height': settings.IMAGE_MAX_SIZE[1]}),
        max_length=255, required=False, widget=widgets.ImageFileInput())
    comment = forms.CharField(label=_(u"Comment"),
                              widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        if 'limits' in kwargs:
            kwargs.pop('limits')
        super(ContainerForm, self).__init__(*args, **kwargs)
        self.fields['container_type'].choices = \
            models.ContainerType.get_types(
                initial=self.init_data.get('container_type'))
        self.fields['container_type'].help_text = \
            models.ContainerType.get_help()

    def save(self, user):
        dct = self.cleaned_data
        dct['history_modifier'] = user
        dct['container_type'] = models.ContainerType.objects.get(
            pk=dct['container_type'])
        dct['location'] = models.Warehouse.objects.get(pk=dct['location'])
        dct['responsible'] = models.Warehouse.objects.get(pk=dct['responsible'])
        new_item = models.Container(**dct)
        new_item.save()
        return new_item


class ContainerModifyForm(ContainerForm):
    pk = forms.IntegerField(required=False, widget=forms.HiddenInput)
    index = forms.IntegerField(label=_(u"ID"))

    def __init__(self, *args, **kwargs):
        super(ContainerModifyForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder.pop(self.fields.keyOrder.index('index'))
        self.fields.keyOrder.insert(
            self.fields.keyOrder.index("location") + 1, 'index')

    def clean(self):
        # manage unique ID
        cleaned_data = self.cleaned_data
        index = cleaned_data.get("index")
        warehouse = cleaned_data.get("location")
        q = models.Container.objects.filter(
            index=index, location__pk=warehouse)
        if 'pk' in cleaned_data and cleaned_data['pk']:
            q = q.exclude(pk=int(cleaned_data['pk']))
        if q.count():
            raise forms.ValidationError(_(u"This ID already exists for "
                                          u"this warehouse."))
        return cleaned_data


class ContainerSelect(TableSelect):
    location = get_warehouse_field()
    container_type = forms.ChoiceField(label=_(u"Container type"), choices=[])
    reference = forms.CharField(label=_(u"Ref."))

    def __init__(self, *args, **kwargs):
        super(ContainerSelect, self).__init__(*args, **kwargs)
        self.fields['container_type'].choices = \
            models.ContainerType.get_types()
        self.fields['container_type'].help_text = \
            models.ContainerType.get_help()

ContainerFormSelection = get_form_selection(
    'ContainerFormSelection', _(u"Container search"), 'container',
    models.Container, ContainerSelect, 'get-container',
    _(u"You should select a container."), new=True,
    new_message=_(u"Add a new container"))

MainContainerFormSelection = get_form_selection(
    'ContainerFormSelection', _(u"Container search"), 'pk',
    models.Container, ContainerSelect, 'get-container',
    _(u"You should select a container.")
)


class BasePackagingForm(SelectFindBasketForm):
    form_label = _(u"Packaging")
    associated_models = {'treatment_type': TreatmentType,
                         'person': Person,
                         'location': models.Warehouse,
                         'basket': FindBasket}
    person = forms.IntegerField(
        label=_(u"Packager"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-person'),
            associated_model=Person, new=True),
        validators=[valid_id(Person)])
    start_date = forms.DateField(
        label=_(u"Date"), required=False, widget=widgets.JQueryDate)


class FindPackagingFormSelection(FindMultipleFormSelection):
    form_label = _(u"Packaged finds")


class LocalisationForm(forms.Form):
    form_label = _(u"Localisation")

    def __init__(self, *args, **kwargs):
        self.container, self.warehouse = None, None
        if 'warehouse' in kwargs:
            self.warehouse = kwargs.pop('warehouse')
        if 'container' in kwargs:
            self.container = kwargs.pop('container')
        super(LocalisationForm, self).__init__(*args, **kwargs)
        if not self.warehouse:
            return
        for divlink in self.warehouse.warehousedivisionlink_set.order_by(
                'order').all():
            initial = u"-"
            if self.container:
                q = models.ContainerLocalisation.objects.filter(
                    division=divlink, container=self.container)
                if q.count():
                    initial = q.all()[0].reference
            self.fields['division_{}'.format(divlink.pk)] = forms.CharField(
                label=str(divlink.division), max_length=200, initial=initial,
            )


class ContainerDeletionForm(FinalForm):
    confirm_msg = _(u"Would you like to delete this container?")
    confirm_end_msg = _(u"Would you like to delete this container?")
