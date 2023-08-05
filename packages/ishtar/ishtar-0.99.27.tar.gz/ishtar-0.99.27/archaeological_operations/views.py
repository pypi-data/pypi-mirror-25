#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017  Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

import json

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from ishtar_common.views import get_item, show_item, revert_item, new_item
from ishtar_common.wizards import SearchWizard, check_rights_condition
from ishtar_common.forms import ClosingDateFormSelection
from ishtar_common.forms_common import AuthorFormset, TownFormset, \
    SourceDeletionForm
from ishtar_common.models import get_current_profile
from wizards import *
from forms import *
import models


def autocomplete_patriarche(request, non_closed=True):
    if (not request.user.has_perm('ishtar_common.view_operation',
                                  models.Operation)
            and not request.user.has_perm('ishtar_common.view_own_operation',
                                          models.Operation)
            and not request.user.ishtaruser.has_right(
                'operation_search', session=request.session)):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        query &= Q(code_patriarche__startswith=q)
    if non_closed:
        query &= Q(end_date__isnull=True)
    limit = 15
    operations = models.Operation.objects\
        .filter(query).order_by('code_patriarche')[:limit]
    data = json.dumps([{'id': operation.code_patriarche,
                        'value': operation.code_patriarche}
                       for operation in operations])
    return HttpResponse(data, mimetype='text/plain')


def autocomplete_archaeologicalsite(request):
    if (not request.user.has_perm(
            'archaeological_operations.view_archaeologicalsite',
            models.ArchaeologicalSite)
        and not request.user.has_perm(
            'archaeological_operations.view_own_archaeologicalsite',
            models.ArchaeologicalSite)):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        qt = Q(reference__icontains=q) | Q(name__icontains=q)
        query = query & qt
    limit = 15
    sites = models.ArchaeologicalSite.objects\
        .filter(query).order_by('reference')[:limit]
    data = json.dumps([{'id': site.pk,
                        'value': unicode(site)[:60]}
                       for site in sites])
    return HttpResponse(data, mimetype='text/plain')

new_archaeologicalsite = new_item(models.ArchaeologicalSite,
                                  ArchaeologicalSiteForm, many=True)


def autocomplete_operation(request, non_closed=True):
    # person_types = request.user.ishtaruser.person.person_type
    if (not request.user.has_perm('ishtar_common.view_operation',
                                  models.Operation)
        and not request.user.has_perm(
            'ishtar_common.view_own_operation', models.Operation)
            and not request.user.ishtaruser.has_right(
                'operation_search', session=request.session)):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        extra = Q(towns__name__icontains=q) | Q(common_name__icontains=q)
        try:
            int(q)
            extra = extra | Q(year=q) | Q(operation_code=q)
        except ValueError:
            pass
        if settings.COUNTRY == 'fr':
            if q.startswith('OA'):
                q = q[2:]
            try:
                int(q)
                extra |= Q(code_patriarche__contains=q)
            except ValueError:
                pass
        query = query & extra
    if non_closed:
        query &= Q(end_date__isnull=True)
    limit = 15
    operations = models.Operation.objects.filter(query)[:limit]
    data = json.dumps([{'id': operation.pk, 'value': unicode(operation)}
                       for operation in operations])
    return HttpResponse(data, mimetype='text/plain')


def get_available_operation_code(request, year=None):
    if not request.user.has_perm(
        'ishtar_common.view_operation', models.Operation)\
        and not request.user.has_perm(
            'ishtar_common.view_own_operation', models.Operation):
        return HttpResponse(mimetype='text/plain')
    data = json.dumps({'id':
                       models.Operation.get_available_operation_code(year)})
    return HttpResponse(data, mimetype='text/plain')

get_operation = get_item(models.Operation, 'get_operation', 'operation')

show_operation = show_item(models.Operation, 'operation')
revert_operation = revert_item(models.Operation)

show_operationsource = show_item(models.OperationSource, 'operationsource')
get_operationsource = get_item(models.OperationSource, 'get_operationsource',
                               'operationsource')

get_administrativeactop = get_item(
    models.AdministrativeAct, 'get_administrativeactop', 'administrativeactop')

get_administrativeact = get_item(
    models.AdministrativeAct, 'get_administrativeact', 'administrativeact')

show_administrativeact = show_item(models.AdministrativeAct,
                                   'administrativeact')


def dashboard_operation(request, *args, **kwargs):
    """
    Operation dashboard
    """
    dct = {'dashboard': models.OperationDashboard()}
    return render_to_response('ishtar/dashboards/dashboard_operation.html',
                              dct, context_instance=RequestContext(request))

operation_search_wizard = SearchWizard.as_view(
    [('general-operation_search', OperationFormSelection)],
    label=_(u"Operation search"),
    url_name='operation_search',)

wizard_steps = [
    ('filechoice-operation_creation', OperationFormFileChoice),
    ('general-operation_creation', OperationFormGeneral),
    ('collaborators-operation_creation', CollaboratorForm),
    ('archaeologicalsite-operation_creation', ArchaeologicalSiteFormSet),
    ('preventive-operation_creation', OperationFormPreventive),
    ('preventivediag-operation_creation', OperationFormPreventiveDiag),
    ('townsgeneral-operation_creation', TownFormset),
    ('towns-operation_creation', SelectedTownFormset),
    ('parcelsgeneral-operation_creation', SelectedParcelGeneralFormSet),
    ('parcels-operation_creation', SelectedParcelFormSet),
    ('remains-operation_creation', RemainForm),
    ('periods-operation_creation', PeriodForm),
    ('relations-operation_creation', RecordRelationsFormSet),
    ('abstract-operation_creation', OperationFormAbstract),
    ('final-operation_creation', FinalForm)]


def get_check_files_for_operation(other_check=None):
    def func(self):
        if not get_current_profile().files or \
                not check_rights_condition(['view_file'])(self):
            return False
        if not other_check:
            return True
        return other_check(self)
    return func

check_files_for_operation = get_check_files_for_operation()


ope_crea_condition_dict = {
    'filechoice-operation_creation': check_files_for_operation,
    'preventive-operation_creation':
    get_check_files_for_operation(
        is_preventive('general-operation_creation', models.OperationType,
                      'operation_type', 'prev_excavation')),
    'preventivediag-operation_creation':
    get_check_files_for_operation(
        is_preventive('general-operation_creation', models.OperationType,
                      'operation_type', 'arch_diagnostic')),
    'townsgeneral-operation_creation': has_associated_file(
        'filechoice-operation_creation', negate=True),
    'towns-operation_creation': has_associated_file(
        'filechoice-operation_creation'),
    'parcelsgeneral-operation_creation': has_associated_file(
        'filechoice-operation_creation', negate=True),
    'parcels-operation_creation': has_associated_file(
        'filechoice-operation_creation'),
}

operation_creation_wizard = OperationWizard.as_view(
    wizard_steps,
    label=_(u"New operation"),
    condition_dict=ope_crea_condition_dict,
    url_name='operation_creation',)

operation_modif_wizard_steps = [
    ('selec-operation_modification', OperationFormSelection),
    ('general-operation_modification', OperationFormModifGeneral),
    ('collaborators-operation_modification', CollaboratorForm),
    ('archaeologicalsite-operation_modification', ArchaeologicalSiteFormSet),
    ('preventive-operation_modification', OperationFormPreventive),
    ('preventivediag-operation_modification', OperationFormPreventiveDiag),
    ('towns-operation_modification', SelectedTownFormset),
    ('townsgeneral-operation_modification', TownFormset),
    ('parcels-operation_modification', SelectedParcelFormSet),
    ('parcelsgeneral-operation_modification', SelectedParcelGeneralFormSet),
    ('remains-operation_modification', RemainForm),
    ('periods-operation_modification', PeriodForm),
    ('relations-operation_modification', RecordRelationsFormSet),
    ('abstract-operation_modification', OperationFormAbstract),
    ('final-operation_modification', FinalForm)
]


ope_modif_condition_dict = {
    'preventive-operation_modification':
    get_check_files_for_operation(
        is_preventive('general-operation_modification', models.OperationType,
                      'operation_type', 'prev_excavation')),
    'preventivediag-operation_modification':
    get_check_files_for_operation(
        is_preventive('general-operation_modification', models.OperationType,
                      'operation_type', 'arch_diagnostic')),
    'townsgeneral-operation_modification': has_associated_file(
        'general-operation_modification', negate=True),
    'towns-operation_modification': has_associated_file(
        'general-operation_modification'),
    'parcelsgeneral-operation_modification': has_associated_file(
        'general-operation_modification', negate=True),
    'parcels-operation_modification': has_associated_file(
        'general-operation_modification'),

}

operation_modification_wizard = OperationModificationWizard.as_view(
    operation_modif_wizard_steps,
    label=_(u"Operation modification"),
    condition_dict=ope_modif_condition_dict,
    url_name='operation_modification',)


def operation_modify(request, pk):
    operation_modification_wizard(request)
    OperationModificationWizard.session_set_value(
        request, 'selec-operation_modification', 'pk', pk, reset=True)
    return redirect(reverse('operation_modification',
                            kwargs={'step': 'general-operation_modification'}))


def operation_add(request, file_id):
    operation_creation_wizard(request)
    OperationWizard.session_set_value(
        request, 'filechoice-operation_creation', 'associated_file',
        file_id, reset=True)
    return redirect(reverse('operation_creation',
                            kwargs={'step': 'general-operation_creation'}))

operation_closing_steps = [
    ('selec-operation_closing', OperationFormSelection),
    ('date-operation_closing', ClosingDateFormSelection),
    ('final-operation_closing', FinalOperationClosingForm)]

operation_closing_wizard = OperationClosingWizard.as_view(
    operation_closing_steps,
    label=_(u"Operation closing"),
    url_name='operation_closing',)


operation_deletion_steps = [
    ('selec-operation_deletion', OperationFormSelection),
    ('final-operation_deletion', OperationDeletionForm)
]

operation_deletion_wizard = OperationDeletionWizard.as_view(
    operation_deletion_steps,
    label=_(u"Operation deletion"),
    url_name='operation_deletion',)

operation_source_search_wizard = SearchWizard.as_view([
    ('selec-operation_source_search', OperationSourceFormSelection)],
    label=_(u"Operation: source search"),
    url_name='operation_source_search',)

operation_source_creation_wizard = OperationSourceWizard.as_view([
    ('selec-operation_source_creation', SourceOperationFormSelection),
    ('source-operation_source_creation', OperationSourceForm),
    ('authors-operation_source_creation', AuthorFormset),
    ('final-operation_source_creation', FinalForm)],
    label=_(u"Operation: source creation"),
    url_name='operation_source_creation',)

operation_source_modification_steps = [
    ('selec-operation_source_modification', OperationSourceFormSelection),
    ('source-operation_source_modification', OperationSourceForm),
    ('authors-operation_source_modification', AuthorFormset),
    ('final-operation_source_modification', FinalForm)
]

operation_source_modification_wizard = OperationSourceWizard.as_view(
    operation_source_modification_steps,
    label=_(u"Operation: source modification"),
    url_name='operation_source_modification',)


def operation_source_modify(request, pk):
    operation_source_modification_wizard(request)
    OperationSourceWizard.session_set_value(
        request, 'selec-operation_source_modification', 'pk', pk, reset=True)
    return redirect(reverse(
        'operation_source_modification',
        kwargs={'step': 'source-operation_source_modification'}))

operation_source_deletion_wizard = OperationSourceDeletionWizard.as_view([
    ('selec-operation_source_deletion', OperationSourceFormSelection),
    ('final-operation_source_deletion', SourceDeletionForm)],
    label=_(u"Operation: source deletion"),
    url_name='operation_source_deletion',)

operation_administrativeactop_search_wizard = SearchWizard.as_view([
    ('general-operation_administrativeactop_search',
     AdministrativeActOpeFormSelection)],
    label=_(u"Administrative act search"),
    url_name='operation_administrativeactop_search',)

administrativeactop_steps = [
    ('selec-operation_administrativeactop', OperationFormSelection),
    ('administrativeact-operation_administrativeactop',
     AdministrativeActOpeForm),
    ('final-operation_administrativeactop', FinalForm)]


operation_administrativeactop_wizard = \
    OperationAdministrativeActWizard.as_view(
        administrativeactop_steps,
        label=_(u"Operation: new administrative act"),
        url_name='operation_administrativeactop',)

operation_administrativeactop_modification_wizard = \
    OperationEditAdministrativeActWizard.as_view([
        ('selec-operation_administrativeactop_modification',
         AdministrativeActOpeFormSelection),
        ('administrativeact-operation_administrativeactop_modification',
         AdministrativeActOpeModifForm),
        ('final-operation_administrativeactop_modification', FinalForm)],
        label=_(u"Operation: administrative act modification"),
        url_name='operation_administrativeactop_modification',)


def operation_administrativeactop_modify(request, pk):
    operation_administrativeactop_modification_wizard(request)
    OperationEditAdministrativeActWizard.session_set_value(
        request, 'selec-operation_administrativeactop_modification',
        'pk', pk, reset=True)
    return redirect(
        reverse(
            'operation_administrativeactop_modification',
            kwargs={
                'step':
                'administrativeact-operation_administrativeactop_modification'
            }))


operation_administrativeactop_deletion_wizard = \
    AdministrativeActDeletionWizard.as_view([
        ('selec-operation_administrativeactop_deletion',
         AdministrativeActOpeFormSelection),
        ('final-operation_administrativeactop_deletion',
         FinalAdministrativeActDeleteForm)],
        label=_(u"Operation: administrative act deletion"),
        url_name='operation_administrativeactop_deletion',)

administrativact_register_wizard = SearchWizard.as_view([
    ('general-administrativact_register',
     AdministrativeActRegisterFormSelection)],
    label=pgettext_lazy('admin act register', u"Register"),
    url_name='administrativact_register',)


def generatedoc_administrativeactop(request, pk, template_pk=None):
    if (not request.user.has_perm(
            'ishtar_common.view_operation', models.Operation)
        and not request.user.has_perm(
            'ishtar_common.view_own_operation', models.Operation)):
        return HttpResponse(mimetype='text/plain')
    try:
        act_file = models.AdministrativeAct.objects.get(pk=pk)
        doc = act_file.publish(template_pk)
    except models.AdministrativeAct.DoesNotExist:
        doc = None
    if doc:
        MIMES = {'odt': 'application/vnd.oasis.opendocument.text',
                 'ods': 'application/vnd.oasis.opendocument.spreadsheet'}
        ext = doc.split('.')[-1]
        doc_name = act_file.get_filename() + "." + ext
        mimetype = 'text/csv'
        if ext in MIMES:
            mimetype = MIMES[ext]
        response = HttpResponse(open(doc), mimetype=mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s' % \
            doc_name
        return response
    return HttpResponse(mimetype='text/plain')


def administrativeactfile_document(
        request, file=False, treatment=False, treatment_file=False):
    search_form = AdministrativeActOpeFormSelection
    document_type = 'O'
    if file:
        from archaeological_files.forms import \
            AdministrativeActFileFormSelection
        search_form = AdministrativeActFileFormSelection
        document_type = 'F'
    elif treatment:
        from archaeological_finds.forms import \
            AdministrativeActTreatmentFormSelection
        search_form = AdministrativeActTreatmentFormSelection
        document_type = 'T'
    elif treatment_file:
        from archaeological_finds.forms import \
            AdministrativeActTreatmentFileFormSelection
        search_form = AdministrativeActTreatmentFileFormSelection
        document_type = 'TF'
    dct = {}
    if request.POST:
        dct['search_form'] = search_form(request.POST)
        dct['template_form'] = DocumentGenerationAdminActForm(
            document_type=document_type)
        c_object = None
        try:
            if dct['search_form'].is_valid():
                c_object = \
                    DocumentGenerationAdminActForm._associated_model\
                    .objects.get(pk=dct['search_form'].cleaned_data.get('pk'))
        except DocumentGenerationAdminActForm._associated_model.DoesNotExist:
            pass
        if c_object:
            dct['template_form'] = DocumentGenerationAdminActForm(
                request.POST, document_type=document_type, obj=c_object)
            if dct['template_form'].is_valid():
                return generatedoc_administrativeactop(
                    request,
                    dct['search_form'].cleaned_data.get('pk'),
                    dct['template_form'].cleaned_data.get('document_template'))
    else:
        dct['search_form'] = search_form()
        dct['template_form'] = DocumentGenerationAdminActForm(
            document_type=document_type)
    return render_to_response('ishtar/administrativeact_document.html', dct,
                              context_instance=RequestContext(request))


def reset_wizards(request):
    for wizard_class, url_name in (
            (OperationWizard, 'operation_creation'),
            (OperationModificationWizard, 'operation_modification'),
            (OperationClosingWizard, 'operation_closing'),
            (OperationDeletionWizard, 'operation_deletion_wizard'),
            (OperationSourceWizard, 'operation_source_creation'),
            (OperationSourceWizard, 'operation_source_modification'),
            (OperationSourceDeletionWizard, 'operation_source_deletion'),
            (OperationAdministrativeActWizard,
             'operation_administrativeactop'),
            (OperationEditAdministrativeActWizard,
             'operation_administrativeactop_modification'),
            (AdministrativeActDeletionWizard,
             'operation_administrativeactop_deletion'),):
        wizard_class.session_reset(request, url_name)
