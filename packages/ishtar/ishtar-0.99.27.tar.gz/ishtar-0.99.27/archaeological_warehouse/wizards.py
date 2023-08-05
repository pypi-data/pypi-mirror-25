#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from django.shortcuts import render_to_response
from django.template import RequestContext

from ishtar_common.forms import reverse_lazy
from ishtar_common.wizards import Wizard, DeletionWizard
from archaeological_finds.wizards import TreatmentWizard

from archaeological_finds.models import Treatment, TreatmentType
import models


class PackagingWizard(TreatmentWizard):
    basket_step = 'base-packaging'

    def save_model(self, dct, m2m, whole_associated_models, form_list,
                   return_object):
        dct = self.get_extra_model(dct, form_list)
        obj = self.get_current_saved_object()
        dct['location'] = dct['container'].location
        items = None
        if 'items' in dct:
            items = dct.pop('items')
        if 'basket' in dct:
            if not items:
                items = dct.pop('basket')
            else:
                dct.pop('basket')
        treatment = Treatment(**dct)
        extra_args_for_new = {"container": dct['container']}
        treatment.save(items=items, user=self.request.user,
                       extra_args_for_new=extra_args_for_new)
        packaging = TreatmentType.objects.get(txt_idx='packaging')
        treatment.treatment_types.add(packaging)
        res = render_to_response('ishtar/wizard/wizard_done.html', {},
                                 context_instance=RequestContext(self.request))
        return return_object and (obj, res) or res


class WarehouseWizard(Wizard):
    model = models.Warehouse
    wizard_done_window = reverse_lazy('show-warehouse')


class WarehouseModificationWizard(Wizard):
    model = models.Warehouse
    modification = True
    wizard_done_window = reverse_lazy('show-warehouse')
    wizard_templates = {
        'divisions-warehouse_modification':
            'ishtar/wizard/wizard_warehouse_divisions.html',
    }

    def get_form_kwargs(self, step=None):
        kwargs = super(WarehouseModificationWizard, self).get_form_kwargs(step)
        if step == "divisions-warehouse_modification":
            current_warehouse = self.get_current_object()
            q = models.ContainerLocalisation.objects.filter(
                    division__warehouse=current_warehouse)
            if q.count():
                kwargs['readonly'] = True
        return kwargs


class WarehouseDeletionWizard(DeletionWizard):
    model = models.Warehouse


class ContainerWizard(Wizard):
    model = models.Container
    wizard_templates = {
        'localisation-container_creation':
            'ishtar/wizard/wizard_containerlocalisation.html',
        'localisation-container_modification':
            'ishtar/wizard/wizard_containerlocalisation.html',
    }
    ignore_init_steps = ['localisation']
    wizard_done_window = reverse_lazy('show-container')

    def get_form_kwargs(self, step=None):
        kwargs = super(ContainerWizard, self).get_form_kwargs(step)
        if step == 'localisation-' + self.url_name:
            container_pk = self.session_get_value(
                'selec-' + self.url_name, 'pk')
            q = models.Container.objects.filter(pk=container_pk)
            if q.count():
                kwargs['container'] = q.all()[0]
            warehouse_pk = self.session_get_value(
                'container-' + self.url_name, 'location')
            q = models.Warehouse.objects.filter(pk=warehouse_pk)
            if q.count():
                kwargs['warehouse'] = q.all()[0]
        return kwargs

    def done(self, form_list, **kwargs):
        """
        Save the localisation
        """
        super(ContainerWizard, self).done(form_list)
        dct = {}
        for idx, form in enumerate(form_list):
            if not form.is_valid():
                return self.render(form)
            container = self.get_current_object() or \
                hasattr(self, 'current_object') and self.current_object
            if container and form.prefix == 'localisation-' + self.url_name:
                for div_name in form.cleaned_data:
                    try:
                        division = models.WarehouseDivisionLink.objects.get(
                            pk=div_name.split('_')[-1],
                            warehouse=container.location
                        )  # check the localisation match with the container
                    except models.WarehouseDivisionLink.DoesNotExist:
                        return self.render(form)
                    localisation, created = \
                        models.ContainerLocalisation.objects.get_or_create(
                            container=container,
                            division=division
                        )
                    localisation.reference = form.cleaned_data[div_name]
                    localisation.save()
            dct = {'item': container}
            self.current_object = container
            # force evaluation of lazy urls
            dct['wizard_done_window'] = unicode(self.wizard_done_window)
        return render_to_response(
            self.wizard_done_template, dct,
            context_instance=RequestContext(self.request))


class ContainerModificationWizard(ContainerWizard):
    modification = True


class ContainerDeletionWizard(DeletionWizard):
    model = models.Container
    fields = ['container_type', 'reference', 'comment', 'location', 'index',
              'cached_label']
