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
import re

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext_lazy as _

from ishtar_common.views import get_item, show_item, revert_item

from archaeological_operations.models import Operation
import models

from ishtar_common.wizards import SearchWizard
from archaeological_operations.wizards import AdministrativeActDeletionWizard, \
    is_preventive, is_not_preventive
from wizards import *

from ishtar_common.forms_common import TownFormset
from archaeological_operations.forms import ParcelFormSet, \
    FinalAdministrativeActDeleteForm
from ishtar_common.forms import ClosingDateFormSelection
from forms import *


RE_YEAR_INDEX = re.compile(r"([1-2][0-9]{3})-([0-9]+)")  # eg.: 2014-123


def autocomplete_file(request):
    if not request.user.has_perm('ishtar_common.view_file', models.File) and \
       not request.user.has_perm('ishtar_common.view_own_file', models.File) \
       and not request.user.ishtaruser.has_right('file_search',
                                                 session=request.session):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        extra = Q(internal_reference__icontains=q) | \
            Q(towns__name__icontains=q) | \
            Q(address__icontains=q)
        try:
            int(q)
            extra = extra | Q(year=q) | Q(numeric_reference=q)
        except ValueError:
            pass
        m = RE_YEAR_INDEX.match(q)
        if m:
            yr, idx = m.groups()
            extra = extra | Q(year=yr, numeric_reference=idx)
        query = query & extra
    limit = 20
    files = models.File.objects.filter(query)[:limit]
    data = json.dumps([{'id': file.pk, 'value': unicode(file)}
                       for file in files])
    return HttpResponse(data, mimetype='text/plain')

get_file = get_item(models.File, 'get_file', 'file')
revert_file = revert_item(models.File)


def extra_file_dct(request, item):
    dct = {}
    if (request.user.has_perm('ishtar_common.add_operation', Operation)
       or request.user.ishtaruser.has_right('add_operation')):
        dct['can_add_operation'] = True
    return dct

show_file = show_item(models.File, 'file', extra_dct=extra_file_dct)

get_administrativeactfile = get_item(
    AdministrativeAct, 'get_administrativeactfile', 'administrativeactfile',
    base_request={"associated_file__pk__isnull": False})


def dashboard_file(request, *args, **kwargs):
    """
    Main dashboard
    """
    dct = {'dashboard': models.FileDashboard()}
    return render_to_response('ishtar/dashboards/dashboard_file.html', dct,
                              context_instance=RequestContext(request))

file_search_wizard = SearchWizard.as_view(
    [('general-file_search', FileFormSelection)],
    label=_(u"File search"), url_name='file_search',)

file_creation_wizard = FileWizard.as_view(
    [('general-file_creation', FileFormGeneral),
     ('towns-file_creation', TownFormset),
     ('parcels-file_creation', ParcelFormSet),
     ('preventive-file_creation', FileFormPreventive),
     ('research-file_creation', FileFormResearch),
     ('final-file_creation', FinalForm)],
    label=_(u"New file"),
    condition_dict={
        'preventive-file_creation':
            is_preventive('general-file_creation', models.FileType,
                          type_key='file_type'),
        'research-file_creation':
            is_not_preventive('general-file_creation', models.FileType,
                              type_key='file_type'),
    },
    url_name='file_creation',)

file_modification_wizard = FileModificationWizard.as_view(
    [('selec-file_modification', FileFormSelection),
     ('general-file_modification', FileFormGeneralRO),
     ('towns-file_modification', TownFormset),
     ('parcels-file_modification', ParcelFormSet),
     ('preventive-file_modification', FileFormPreventive),
     ('research-file_modification', FileFormResearch),
     ('final-file_modification', FinalForm)],
    label=_(u"File modification"),
    condition_dict={
        'preventive-file_modification':
            is_preventive('general-file_modification',
                          models.FileType, type_key='file_type'),
        'research-file_modification':
            is_not_preventive('general-file_modification',
                              models.FileType, type_key='file_type'),
    },
    url_name='file_modification',)


def file_modify(request, pk):
    file_modification_wizard(request)
    FileModificationWizard.session_set_value(
        request, 'selec-file_modification', 'pk', pk, reset=True)
    return redirect(reverse('file_modification',
                    kwargs={'step': 'general-file_modification'}))

file_closing_wizard = FileClosingWizard.as_view(
    [('selec-file_closing', FileFormSelection),
     ('date-file_closing', ClosingDateFormSelection),
     ('final-file_closing', FinalFileClosingForm)],
    label=_(u"File closing"), url_name='file_closing',)

file_deletion_wizard = FileDeletionWizard.as_view(
    [('selec-file_deletion', FileFormSelection),
     ('final-file_deletion', FinalFileDeleteForm)],
    label=_(u"File deletion"),
    url_name='file_deletion',)

file_administrativeactfile_search_wizard = \
    SearchWizard.as_view([
        ('selec-file_administrativeactfile_search',
         AdministrativeActFileFormSelection)],
        label=_(u"File: search administrative act"),
        url_name='file_administrativeactfile_search',)

file_administrativeactfile_wizard = \
    FileAdministrativeActWizard.as_view([
        ('selec-file_administrativeactfile', FileFormSelection),
        ('administrativeact-file_administrativeactfile',
         AdministrativeActFileForm),
        ('final-file_administrativeactfile', FinalForm)],
        label=_(u"File: new administrative act"),
        url_name='file_administrativeactfile',)

file_administrativeactfile_modification_wizard = \
    FileEditAdministrativeActWizard.as_view([
        ('selec-file_administrativeactfile_modification',
         AdministrativeActFileModifyFormSelection),
        ('administrativeact-file_administrativeactfile_modification',
         AdministrativeActFileModifForm),
        ('final-file_administrativeactfile_modification', FinalForm)],
        label=_(u"File: administrative act modification"),
        url_name='file_administrativeactfile_modification',)


def file_administrativeactfile_modify(request, pk):
    file_administrativeactfile_modification_wizard(request)
    FileEditAdministrativeActWizard.session_set_value(
        request, 'selec-file_administrativeactfile_modification',
        'pk', pk, reset=True)
    return redirect(
        reverse(
            'file_administrativeactfile_modification',
            kwargs={
                'step':
                'administrativeact-file_administrativeactfile_modification'
            }))


file_administrativeactfile_deletion_wizard = \
    AdministrativeActDeletionWizard.as_view([
        ('selec-file_administrativeactfile_deletion',
         AdministrativeActFileFormSelection),
        ('final-file_administrativeactfile_deletion',
         FinalAdministrativeActDeleteForm)],
        label=_(u"File: administrative act deletion"),
        url_name='file_administrativeactfile_deletion',)


def reset_wizards(request):
    for wizard_class, url_name in (
            (FileWizard, 'file_creation'),
            (FileModificationWizard, 'file_modification'),
            (FileClosingWizard, 'file_modification'),
            (FileDeletionWizard, 'file_deletion'),
            (FileAdministrativeActWizard, 'file_administrativeactfile'),
            (FileEditAdministrativeActWizard,
             'file_administrativeactfile_modification_wizard'),
            (AdministrativeActDeletionWizard,
             'file_administrativeactfile_deletion_wizard'),):
        wizard_class.session_reset(request, url_name)
