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

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils.translation import ugettext_lazy as _

from ishtar_common.forms import reverse_lazy
from ishtar_common.wizards import Wizard, DeletionWizard, SourceWizard
from archaeological_operations.wizards import OperationAdministrativeActWizard

from archaeological_operations.models import AdministrativeAct
from archaeological_context_records.models import ContextRecord
import models


class FindWizard(Wizard):
    model = models.Find
    wizard_done_window = reverse_lazy('show-find')

    def get_current_contextrecord(self):
        step = self.steps.current
        if not step:
            return
        if step.endswith('_creation'):  # a context record has been selected
            main_form_key = 'selecrecord-' + self.url_name
            try:
                idx = int(self.session_get_value(main_form_key, 'pk'))
                current_cr = ContextRecord.objects.get(pk=idx)
                return current_cr
            except(TypeError, ValueError, ObjectDoesNotExist):
                pass
        current_item = self.get_current_object()
        if current_item:
            base_finds = current_item.base_finds.all()
            if base_finds:
                return base_finds[0].context_record

    def get_context_data(self, form, **kwargs):
        """
        Get the operation and context record "reminder" on top of wizard forms
        """
        context = super(FindWizard, self).get_context_data(form, **kwargs)
        current_cr = self.get_current_contextrecord()
        if not current_cr or self.steps.current.startswith('select-'):
            return context
        context['reminders'] = (
            (_(u"Operation"), unicode(current_cr.operation)),
            (_(u"Context record"), unicode(current_cr)))
        return context

    def get_extra_model(self, dct, form_list):
        dct = super(FindWizard, self).get_extra_model(dct, form_list)
        dct['order'] = 1
        if 'pk' in dct and type(dct['pk']) == ContextRecord:
            dct['base_finds__context_record'] = dct.pop('pk')
        return dct


class FindModificationWizard(FindWizard):
    modification = True
    main_item_select_keys = ('selec-', 'selecw-')
    filter_owns = {
        'selec-find_modification': ['pk'],
        'selecw-find_modification': ['pk'],
    }


class FindDeletionWizard(DeletionWizard):
    model = models.Find
    main_item_select_keys = ('selec-', 'selecw-')
    fields = ['label', 'material_types', 'datings', 'find_number',
              'object_types', 'description', 'conservatory_state', 'mark',
              'preservation_to_considers', 'integrities', 'remarkabilities',
              'volume', 'weight', 'length', 'width', 'height', 'diameter',
              'comment']


class TreatmentWizard(Wizard):
    model = models.Treatment
    wizard_done_window = reverse_lazy('show-treatment')
    basket_step = 'basetreatment-treatment_creation'
    saved_args = {"items": []}

    def get_form_kwargs(self, step, **kwargs):
        kwargs = super(TreatmentWizard, self).get_form_kwargs(step, **kwargs)
        if self.basket_step not in step:
            return kwargs
        kwargs['user'] = self.request.user
        return kwargs

    def get_extra_model(self, dct, form_list):
        """
        Get items concerned by the treatment
        """
        dct = super(TreatmentWizard, self).get_extra_model(dct, form_list)
        if 'resulting_pk' in dct:
            try:
                find = models.Find.objects.get(pk=dct.pop('resulting_pk'))
                if 'own' in self.current_right \
                        and not find.is_own(dct['history_modifier']):
                    raise PermissionDenied
                dct['items'] = [find]
            except models.Find.DoesNotExist:
                raise PermissionDenied
        if 'basket' in dct:
            basket = dct.pop('basket')
            if basket.user.pk != dct['history_modifier'].pk:
                raise PermissionDenied
            dct['items'] = list(basket.items.all())
        return dct


class TreatmentModificationWizard(TreatmentWizard):
    modification = True


class TreatmentDeletionWizard(DeletionWizard):
    model = models.Treatment
    fields = ['label', 'other_reference', 'year', 'index',
              'treatment_types', 'location', 'person', 'organization',
              'external_id', 'comment', 'description',
              'goal', 'start_date', 'end_date', 'container']


class TreatmentAdministrativeActWizard(OperationAdministrativeActWizard):
    model = models.Treatment
    current_obj_slug = 'administrativeacttreatment'
    ref_object_key = 'treatment'

    def get_reminder(self):
        return


class TreatmentEditAdministrativeActWizard(TreatmentAdministrativeActWizard):
    model = AdministrativeAct
    edit = True

    def get_associated_item(self, dct):
        return self.get_current_object().treatment


class TreatmentFileWizard(Wizard):
    model = models.TreatmentFile
    wizard_done_window = reverse_lazy('show-treatmentfile')


class TreatmentFileModificationWizard(TreatmentFileWizard):
    modification = True


class TreatmentFileDeletionWizard(DeletionWizard):
    model = models.TreatmentFile
    fields = ['name', 'internal_reference', 'external_id', 'year',
              'index', 'type', 'in_charge', 'reception_date',
              'creation_date', 'end_date', 'comment']


class TreatmentFileAdministrativeActWizard(
        OperationAdministrativeActWizard):
    model = models.TreatmentFile
    current_obj_slug = 'administrativeacttreatmentfile'
    ref_object_key = 'treatment_file'

    def get_reminder(self):
        form_key = 'selec-' + self.url_name
        if self.url_name.endswith('_administrativeactop'):
            # modification and deletion are suffixed with '_modification'
            # and '_deletion' so it is creation
            pk = self.session_get_value(form_key, "pk")
            try:
                return (
                    (_(u"Treatment request"),
                     unicode(models.TreatmentFile.objects.get(pk=pk))),
                )
            except models.TreatmentFile.DoesNotExist:
                return
        else:
            admin_id = self.session_get_value(form_key, "pk")
            try:
                admin = AdministrativeAct.objects.get(pk=admin_id)
                if not admin.operation:
                    return
                return (
                    (_(u"Operation"), unicode(admin.operation)),
                )
            except AdministrativeAct.DoesNotExist:
                return
        return


class TreatmentFileEditAdministrativeActWizard(
        TreatmentFileAdministrativeActWizard):
    model = AdministrativeAct
    edit = True

    def get_associated_item(self, dct):
        return self.get_current_object().treatment_file


class FindSourceWizard(SourceWizard):
    wizard_done_window = reverse_lazy('show-findsource')
    model = models.FindSource


class FindSourceDeletionWizard(DeletionWizard):
    model = models.FindSource
    fields = ['item', 'title', 'source_type', 'authors', ]


class TreatmentSourceWizard(SourceWizard):
    model = models.TreatmentSource


class TreatmentSourceDeletionWizard(DeletionWizard):
    model = models.TreatmentSource
    fields = ['treatment', 'title', 'source_type', 'authors']


class TreatmentFileSourceWizard(SourceWizard):
    model = models.TreatmentFileSource


class TreatmentFileSourceDeletionWizard(DeletionWizard):
    model = models.TreatmentFileSource
    fields = ['treatment_file', 'title', 'source_type', 'authors']
