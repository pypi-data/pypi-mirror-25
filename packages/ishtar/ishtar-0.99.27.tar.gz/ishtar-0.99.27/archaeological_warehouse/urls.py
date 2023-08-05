#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2016 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from django.conf.urls.defaults import *

from ishtar_common.wizards import check_rights
import views
from archaeological_warehouse import models

# be careful: each check_rights must be relevant with ishtar_menu

# forms
urlpatterns = patterns(
    '',
    url(r'warehouse_packaging/(?P<step>.+)?$',
        views.warehouse_packaging_wizard, name='warehouse_packaging'),
)

urlpatterns += patterns(
    'archaeological_warehouse.views',
    url(r'new-warehouse/(?P<parent_name>.+)?/$',
        'new_warehouse', name='new-warehouse'),
    url(r'^show-warehouse(?:/(?P<pk>.+))?/(?P<type>.+)?$', 'show_warehouse',
        name=models.Warehouse.SHOW_URL),
    url(r'autocomplete-warehouse/$', 'autocomplete_warehouse',
        name='autocomplete-warehouse'),
    url(r'new-container/(?P<parent_name>.+)?/$',
        'new_container', name='new-container'),
    url(r'get-container/(?P<type>.+)?$', 'get_container',
        name='get-container'),
    url(r'get-warehouse/(?P<type>.+)?$', 'get_warehouse',
        name='get-warehouse'),
    url(r'autocomplete-container/?$',
        'autocomplete_container', name='autocomplete-container'),
    url(r'^show-container(?:/(?P<pk>.+))?/(?P<type>.+)?$', 'show_container',
        name=models.Container.SHOW_URL),
    url(r'^warehouse_search/(?P<step>.+)?$',
        check_rights(['view_warehouse', 'view_own_warehouse'])(
            views.warehouse_search_wizard), name='warehouse_search'),
    url(r'^warehouse_creation/(?P<step>.+)?$',
        check_rights(['add_warehouse'])(
            views.warehouse_creation_wizard), name='warehouse_creation'),
    url(r'^warehouse_modification/(?P<step>.+)?$',
        check_rights(['change_warehouse'])(
            views.warehouse_modification_wizard),
        name='warehouse_modification'),
    url(r'^warehouse_deletion/(?P<step>.+)?$',
        check_rights(['change_warehouse'])(
            views.warehouse_deletion_wizard),
        name='warehouse_deletion'),
    url(r'warehouse-modify/(?P<pk>.+)/$',
        views.warehouse_modify, name='warehouse_modify'),

    url(r'^container_search/(?P<step>.+)?$',
        check_rights(['change_warehouse'])(
            views.container_search_wizard),
        name='container_search'),
    url(r'^container_creation/(?P<step>.+)?$',
        check_rights(['change_warehouse'])(
            views.container_creation_wizard),
        name='container_creation'),
    url(r'^container_modification/(?P<step>.+)?$',
        check_rights(['change_warehouse'])(
            views.container_modification_wizard),
        name='container_modification'),
    url(r'^container_deletion/(?P<step>.+)?$',
        check_rights(['change_warehouse'])(
            views.container_deletion_wizard),
        name='container_deletion'),
    url(r'container-modify/(?P<pk>.+)/$',
        views.container_modify, name='container_modify'),
)