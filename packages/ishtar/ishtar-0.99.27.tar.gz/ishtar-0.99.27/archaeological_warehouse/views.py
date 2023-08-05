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
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

import models

from ishtar_common.views import get_item, new_item, show_item
from ishtar_common.wizards import SearchWizard
from wizards import *
from ishtar_common.forms import FinalForm
from forms import *

get_container = get_item(models.Container, 'get_container', 'container')
show_container = show_item(models.Container, 'container')

get_warehouse = get_item(models.Warehouse, 'get_warehouse', 'warehouse')
show_warehouse = show_item(models.Warehouse, 'warehouse')

new_warehouse = new_item(models.Warehouse, WarehouseForm)
new_container = new_item(models.Container, ContainerForm)


def autocomplete_warehouse(request):
    if not request.user.has_perm('ishtar_common.view_warehouse',
                                 models.Warehouse)\
       and not request.user.has_perm(
            'ishtar_common.view_own_warehouse', models.Warehouse):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        extra = Q(name__icontains=q) | \
            Q(warehouse_type__label__icontains=q)
        query = query & extra
    limit = 15
    warehouses = models.Warehouse.objects.filter(query)[:limit]
    data = json.dumps([{'id': warehouse.pk, 'value': unicode(warehouse)}
                       for warehouse in warehouses])
    return HttpResponse(data, mimetype='text/plain')


def autocomplete_container(request):
    if not request.user.has_perm('ishtar_common.view_warehouse',
                                 models.Warehouse)\
       and not request.user.has_perm(
            'ishtar_common.view_own_warehouse', models.Warehouse):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        extra = Q(container_type__label__icontains=q) | \
            Q(container_type__reference__icontains=q) | \
            Q(reference__icontains=q) | \
            Q(location__name=q) | \
            Q(location__town=q)
        query = query & extra
    limit = 15
    containers = models.Container.objects.filter(query)[:limit]
    data = json.dumps([{'id': container.pk, 'value': unicode(container)}
                       for container in containers])
    return HttpResponse(data, mimetype='text/plain')

warehouse_packaging_wizard = PackagingWizard.as_view([
    ('seleccontainer-packaging', ContainerFormSelection),
    ('base-packaging', BasePackagingForm),
    # ('multiselecitems-packaging', FindPackagingFormSelection),
    ('final-packaging', FinalForm)],
    label=_(u"Packaging"),
    url_name='warehouse_packaging',)

warehouse_search_wizard = SearchWizard.as_view([
    ('selec-warehouse_search', WarehouseFormSelection)],
    label=_(u"Warehouse search"),
    url_name='warehouse_search',
)

warehouse_creation_steps = [
    ("warehouse-warehouse_creation", WarehouseForm),
    ('divisions-warehouse_creation', SelectedDivisionFormset),
    ('final-warehouse_creation', FinalForm)]


warehouse_creation_wizard = WarehouseWizard.as_view(
    warehouse_creation_steps,
    label=_(u"Warehouse creation"),
    url_name='warehouse_creation',
)

warehouse_modification_wizard = WarehouseModificationWizard.as_view([
    ('selec-warehouse_modification', WarehouseFormSelection),
    ("warehouse-warehouse_modification", WarehouseForm),
    ('divisions-warehouse_modification', SelectedDivisionFormset),
    ('final-warehouse_modification', FinalForm)],
    label=_(u"Warehouse modification"),
    url_name='warehouse_modification',
)


def warehouse_modify(request, pk):
    WarehouseModificationWizard.session_set_value(
        request, 'selec-warehouse_modification', 'pk', pk, reset=True)
    return redirect(
        reverse('warehouse_modification',
                kwargs={'step': 'warehouse-warehouse_modification'}))


warehouse_deletion_wizard = WarehouseDeletionWizard.as_view([
    ('selec-warehouse_deletion', WarehouseFormSelection),
    ('final-warehouse_deletion', WarehouseDeletionForm)],
    label=_(u"Warehouse deletion"),
    url_name='warehouse_deletion',)

container_search_wizard = SearchWizard.as_view([
    ('selec-container_search', MainContainerFormSelection)],
    label=_(u"Container search"),
    url_name='container_search',
)

container_creation_steps = [
    ('container-container_creation', ContainerForm),
    ('localisation-container_creation', LocalisationForm),
    ('final-container_creation', FinalForm)]

container_creation_wizard = ContainerWizard.as_view(
    container_creation_steps,
    label=_(u"Container creation"),
    url_name='container_creation',
)

container_modification_wizard = ContainerModificationWizard.as_view([
    ('selec-container_modification', MainContainerFormSelection),
    ('container-container_modification', ContainerModifyForm),
    ('localisation-container_modification', LocalisationForm),
    ('final-container_modification', FinalForm)],
    label=_(u"Container modification"),
    url_name='container_modification',
)


def container_modify(request, pk):
    ContainerModificationWizard.session_set_value(
        request, 'selec-container_modification', 'pk', pk, reset=True)
    return redirect(
        reverse('container_modification',
                kwargs={'step': 'container-container_modification'}))

container_deletion_wizard = ContainerDeletionWizard.as_view([
    ('selec-container_deletion', MainContainerFormSelection),
    ('final-container_deletion', ContainerDeletionForm)],
    label=_(u"Container deletion"),
    url_name='container_deletion',)

"""
warehouse_packaging_wizard = ItemSourceWizard.as_view([
         ('selec-warehouse_packaging', ItemsSelection),
         ('final-warehouse_packaging', FinalForm)],
          url_name='warehouse_packaging',)
"""
