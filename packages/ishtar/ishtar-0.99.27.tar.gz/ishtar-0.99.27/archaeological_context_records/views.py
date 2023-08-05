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

import json

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from ishtar_common.forms_common import AuthorFormset, SourceForm
from ishtar_common.views import get_item, show_item, revert_item
from ishtar_common.wizards import SearchWizard
from wizards import *
from forms import *
import models

show_contextrecord = show_item(models.ContextRecord, 'contextrecord')
revert_contextrecord = revert_item(models.ContextRecord)


def autocomplete_contextrecord(request):
    if (not request.user.has_perm(
            'archaeological_context_records.view_contextrecord',
            models.ContextRecord)
        and not request.user.has_perm(
            'archaeological_context_records.view_own_contextrecord',
            models.ArchaeologicalSite)):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    if request.GET.get('operation__pk'):
        query = Q(operation__pk=request.GET.get('operation__pk'))
    for q in q.split(' '):
        qt = Q(parcel__section__icontains=q) | \
            Q(parcel__parcel_number__icontains=q) | \
            Q(label__icontains=q)
        query = query & qt
    limit = 15
    items = models.ContextRecord.objects\
        .filter(query).order_by('parcel__section', 'parcel__parcel_number',
                                'label')[:limit]
    data = json.dumps([{'id': item.pk,
                        'value': unicode(item)[:60]}
                       for item in items])
    return HttpResponse(data, mimetype='text/plain')

get_contextrecord = get_item(
    models.ContextRecord,
    'get_contextrecord', 'contextrecord')
get_contextrecord_for_ope = get_item(
    models.ContextRecord,
    'get_contextrecord', 'contextrecord',
    own_table_cols=models.ContextRecord.TABLE_COLS_FOR_OPE)

show_contextrecordsource = show_item(models.ContextRecordSource,
                                     'contextrecordsource')

get_contextrecordsource = get_item(
    models.ContextRecordSource,
    'get_contextrecordsource', 'contextrecordsource')

get_contextrecordrelation = get_item(
    models.RecordRelationView, 'get_contextrecordrelation',
    'contextrecordrelation')

get_contextrecordrelationdetail = get_item(
    models.RecordRelations, 'get_contextrecordrelationdetail',
    'contextrecordrelationdetail')

record_search_wizard = SearchWizard.as_view([
    ('general-record_search', RecordFormSelection)],
    label=_(u"Context record search"),
    url_name='record_search',)

record_creation_steps = [
    ('selec-record_creation', OperationRecordFormSelection),
    ('general-record_creation', RecordFormGeneral),
    ('datings-record_creation', DatingFormSet),
    ('interpretation-record_creation', RecordFormInterpretation),
    ('relations-record_creation', RecordRelationsFormSet),
    ('final-record_creation', FinalForm)
]

record_creation_wizard = RecordWizard.as_view(record_creation_steps,
    label=_(u"New context record"),
    url_name='record_creation',)

record_modification_wizard = RecordModifWizard.as_view([
    ('selec-record_modification', RecordFormSelection),
    ('operation-record_modification', OperationFormSelection),
    ('general-record_modification', RecordFormGeneral),
    ('datings-record_modification', DatingFormSet),
    ('interpretation-record_modification', RecordFormInterpretation),
    ('relations-record_modification', RecordRelationsFormSet),
    ('final-record_modification', FinalForm)],
    label=_(u"Context record modification"),
    url_name='record_modification',)


def record_modify(request, pk):
    record_modification_wizard(request)
    RecordModifWizard.session_set_value(
        request, 'selec-record_modification', 'pk', pk, reset=True)
    return redirect(reverse('record_modification',
                    kwargs={'step': 'operation-record_modification'}))

record_deletion_wizard = RecordDeletionWizard.as_view([
    ('selec-record_deletion', RecordFormSelection),
    ('final-record_deletion', RecordDeletionForm)],
    label=_(u"Context record deletion"),
    url_name='record_deletion',)

record_source_search_wizard = SearchWizard.as_view([
    ('selec-record_source_search', RecordSourceFormSelection)],
    label=_(u"Context record: source search"),
    url_name='record_source_search',)

record_source_creation_wizard = RecordSourceWizard.as_view([
    ('selec-record_source_creation', SourceRecordFormSelection),
    ('source-record_source_creation', SourceForm),
    ('authors-record_source_creation', AuthorFormset),
    ('final-record_source_creation', FinalForm)],
    label=_(u"Context record: new source"),
    url_name='record_source_creation',)

record_source_modification_wizard = RecordSourceWizard.as_view([
    ('selec-record_source_modification', RecordSourceFormSelection),
    ('source-record_source_modification', SourceForm),
    ('authors-record_source_modification', AuthorFormset),
    ('final-record_source_modification', FinalForm)],
    label=_(u"Context record: source modification"),
    url_name='record_source_modification',)


def record_source_modify(request, pk):
    record_source_modification_wizard(request)
    RecordSourceWizard.session_set_value(
        request, 'selec-record_source_modification', 'pk', pk, reset=True)
    return redirect(reverse(
        'record_source_modification',
        kwargs={'step': 'source-record_source_modification'}))

record_source_deletion_wizard = RecordSourceDeletionWizard.as_view([
    ('selec-record_source_deletion', RecordSourceFormSelection),
    ('final-record_source_deletion', RecordDeletionForm)],
    label=_(u"Context record: source deletion"),
    url_name='record_source_deletion',)
