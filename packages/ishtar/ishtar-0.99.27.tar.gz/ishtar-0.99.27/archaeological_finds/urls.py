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

from django.conf.urls import *

from ishtar_common.wizards import check_rights
import views

from archaeological_finds import models

# be careful: each check_rights must be relevant with ishtar_menu

# forms
urlpatterns = patterns(
    '',
    url(r'find_search/(?P<step>.+)?$',
        check_rights(['view_find', 'view_own_find'])(
            views.find_search_wizard), name='find_search'),
    url(r'find_creation/(?P<step>.+)?$',
        check_rights(['add_find', 'add_own_find'])(
            views.find_creation_wizard), name='find_creation'),
    url(r'find_modification/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.find_modification_wizard), name='find_modification'),
    url(r'find_deletion/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.find_deletion_wizard), name='find_deletion'),
    url(r'find_modify/(?P<pk>.+)/$',
        views.find_modify, name='find_modify'),
    url(r'find_source_search/(?P<step>.+)?$',
        check_rights(['view_find', 'view_own_find'])(
            views.find_source_search_wizard),
        name='find_source_search'),
    url(r'find_source_creation/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.find_source_creation_wizard),
        name='find_source_creation'),
    url(r'find_source_modification/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.find_source_modification_wizard),
        name='find_source_modification'),
    url(r'find_source_modify/(?P<pk>.+)/$',
        views.find_source_modify, name='find_source_modify'),
    url(r'find_source_deletion/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.find_source_deletion_wizard),
        name='find_source_deletion'),
    url(r'^find_basket_creation/$',
        check_rights(['change_find', 'change_own_find'])(
            views.NewFindBasketView.as_view()), name='new_findbasket'),
    url(r'^find_basket_modification_add/$',
        check_rights(['change_find', 'change_own_find'])(
            views.SelectBasketForManagement.as_view()),
        name='select_findbasketforadd'),
    url(r'^find_basket_modification_add/(?P<pk>[0-9]+)?/$',
        check_rights(['change_find', 'change_own_find'])(
            views.SelectItemsInBasket.as_view()),
        name='select_itemsinbasket'),
    url(r'^find_basket_modification_add_item/$',
        check_rights(['change_find', 'change_own_find'])(
            views.FindBasketAddItemView.as_view()),
        name='add_iteminbasket'),
    url(r'^find_basket_modification_delete_item/(?P<basket>[0-9]+)?'
        r'/(?P<find_pk>[0-9]+)?/$',
        check_rights(['change_find', 'change_own_find'])(
            views.FindBasketDeleteItemView.as_view()),
        name='delete_iteminbasket'),
    url(r'^find_basket_list/(?P<pk>[0-9]+)?/$',
        check_rights(['change_find', 'change_own_find'])(
            views.FindBasketListView.as_view()),
        name='list_iteminbasket'),
    url(r'^find_basket_deletion/$',
        check_rights(['change_find', 'change_own_find'])(
            views.DeleteFindBasketView.as_view()), name='delete_findbasket'),

    url(r'^treatment_creation/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.treatment_creation_wizard), name='treatment_creation'),
    url(r'^treatment_modification/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.treatment_modification_wizard),
        name='treatment_modification'),
    url(r'treatment_modify/(?P<pk>.+)/$',
        views.treatment_modify, name='treatment_modify'),
    url(r'^treatment_search/(?P<step>.+)?$',
        check_rights(['view_find', 'view_own_find'])(
            views.treatment_search_wizard), name='treatment_search'),
    url(r'^treatment_deletion/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.treatment_deletion_wizard), name='treatment_deletion'),

    url(r'^show-treatmentsource(?:/(?P<pk>.+))?/(?P<type>.+)?$',
        views.show_treatmentsource,
        name=models.TreatmentSource.SHOW_URL),
    url(r'^get-treatmentsource/(?P<type>.+)?$',
        views.get_treatmentsource,
        name='get-treatmentsource'),
    url(r'^treatment_source_search/(?P<step>.+)?$',
        check_rights(['view_treatment', 'view_own_treatment'])(
            views.treatment_source_search_wizard),
        name='treatment_source_search'),
    url(r'^treatment_source_creation/(?P<step>.+)?$',
        check_rights(['change_treatment', 'change_own_treatment'])(
            views.treatment_source_creation_wizard),
        name='treatment_source_creation'),
    url(r'^treatment_source_modification/(?P<step>.+)?$',
        check_rights(['change_treatment', 'change_own_treatment'])(
            views.treatment_source_modification_wizard),
        name='treatment_source_modification'),
    url(r'^treatment_source_modify/(?P<pk>.+)/$',
        views.treatment_source_modify, name='treatment_source_modify'),
    url(r'^treatment_source_deletion/(?P<step>.+)?$',
        check_rights(['change_treatment', 'change_own_treatment'])(
            views.treatment_source_deletion_wizard),
        name='treatment_source_deletion'),

    url(r'^treatment_admacttreatment_search/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatment_administrativeact_search_wizard),
        name='treatment_admacttreatment_search'),
    url(r'^treatment_admacttreatment/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatment_administrativeact_wizard),
        name='treatment_admacttreatment'),
    url(r'^treatment_admacttreatment_modification/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatment_administrativeact_modification_wizard),
        name='treatment_admacttreatment_modification'),
    url(r'^treatment_administrativeacttreatment_modify/(?P<pk>.+)/$',
        views.treatment_administrativeacttreatment_modify,
        name='treatment_administrativeacttreatment_modify'),
    url(r'^treatment_admacttreatment_deletion/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatment_admacttreatment_deletion_wizard),
        name='treatment_admacttreatment_deletion'),
    url(r'^get-administrativeacttreatment/(?P<type>.+)?$',
        views.get_administrativeacttreatment,
        name='get-administrativeacttreatment'),

    url(r'^treatmentfle_admacttreatmentfle_search/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatmentfile_admacttreatmentfile_search_wizard),
        name='treatmentfle_admacttreatmentfle_search'),
    url(r'^treatmentfle_admacttreatmentfle_modification/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatmentfile_admacttreatmentfile_modification_wizard),
        name='treatmentfle_admacttreatmentfle_modification'),
    url(r'^treatmentfle_admacttreatmentfle/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatmentfile_admacttreatmentfile_wizard),
        name='treatmentfle_admacttreatmentfle'),
    url(r'^treatmentfile_administrativeacttreatmentfile_modify/(?P<pk>.+)/$',
        views.treatmentfile_administrativeacttreatmentfile_modify,
        name='treatmentfile_administrativeacttreatmentfile_modify'),
    url(r'^treatmentfle_admacttreatmentfle_deletion/(?P<step>.+)?$',
        check_rights(['change_administrativeact'])(
            views.treatmentfile_admacttreatmentfile_deletion_wizard),
        name='treatmentfle_admacttreatmentfle_deletion'),

    url(r'^show-treatmentfilesource(?:/(?P<pk>.+))?/(?P<type>.+)?$',
        views.show_treatmentfilesource,
        name=models.TreatmentFileSource.SHOW_URL),
    url(r'^get-treatmentfilesource/(?P<type>.+)?$',
        views.get_treatmentfilesource,
        name='get-treatmentfilesource'),
    url(r'^treatmentfile_source_search/(?P<step>.+)?$',
        check_rights(['view_treatmentfile', 'view_own_treatmentfile'])(
            views.treatmentfile_source_search_wizard),
        name='treatmentfile_source_search'),
    url(r'^treatmentfile_source_creation/(?P<step>.+)?$',
        check_rights(['change_treatmentfile', 'change_own_treatmentfile'])(
            views.treatmentfile_source_creation_wizard),
        name='treatmentfile_source_creation'),
    url(r'^treatmentfile_source_modification/(?P<step>.+)?$',
        check_rights(['change_treatmentfile', 'change_own_treatmentfile'])(
            views.treatmentfile_source_modification_wizard),
        name='treatmentfile_source_modification'),
    url(r'^treatmentfile_source_modify/(?P<pk>.+)/$',
        views.treatmentfile_source_modify, name='treatmentfile_source_modify'),
    url(r'^treatmentfile_source_deletion/(?P<step>.+)?$',
        check_rights(['change_treatmentfile', 'change_own_treatmentfile'])(
            views.treatmentfile_source_deletion_wizard),
        name='treatmentfile_source_deletion'),


    url(r'^treatmentfle_search/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.treatmentfile_search_wizard),
        name='treatmentfile_search'),
    url(r'treatmentfle_creation/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.treatmentfile_creation_wizard),
        name='treatmentfile_creation'),
    url(r'treatmentfle_modification/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.treatmentfile_modification_wizard),
        name='treatmentfile_modification'),
    url(r'^treatmentfile_modify/(?P<pk>.+)/$',
        views.treatmentfile_modify, name='treatmentfile_modify'),
    url(r'^treatmentfle_deletion/(?P<step>.+)?$',
        check_rights(['change_find', 'change_own_find'])(
            views.treatmentfile_deletion_wizard),
        name='treatmentfile_deletion'),
    url(r'get-administrativeacttreatmentfile/(?P<type>.+)?$',
        views.get_administrativeacttreatmentfile,
        name='get-administrativeacttreatmentfile'),
    url(r'get-upstreamtreatment/(?P<type>.+)?$', views.get_upstreamtreatment,
        name='get-upstreamtreatment'),
    url(r'get-downstreamtreatment/(?P<type>.+)?$',
        views.get_downstreamtreatment,
        name='get-downstreamtreatment'),
)

urlpatterns += patterns(
    'archaeological_finds.views',
    url(r'autocomplete-objecttype/$', 'autocomplete_objecttype',
        name='autocomplete-objecttype'),
    url(r'autocomplete-materialtype/$', 'autocomplete_materialtype',
        name='autocomplete-materialtype'),
    url(r'autocomplete-preservationtype/$', 'autocomplete_preservationtype',
        name='autocomplete-preservationtype'),
    url(r'autocomplete-integritytype/$', 'autocomplete_integritytype',
        name='autocomplete-integritytype'),
    url(r'autocomplete-treatmentfile/$', 'autocomplete_treatmentfile',
        name='autocomplete-treatmentfile'),
    url(r'get-find/own/(?P<type>.+)?$', 'get_find',
        name='get-own-find', kwargs={'force_own': True}),
    url(r'get-find/(?P<type>.+)?$', 'get_find',
        name='get-find'),
    url(r'get-find-for-ope/own/(?P<type>.+)?$', 'get_find_for_ope',
        name='get-own-find-for-ope', kwargs={'force_own': True}),
    url(r'get-find-for-ope/(?P<type>.+)?$', 'get_find_for_ope',
        name='get-find-for-ope'),
    url(r'get-find-for-treatment/own/(?P<type>.+)?$', 'get_find_for_treatment',
        name='get-own-find-for-treatment', kwargs={'force_own': True}),
    url(r'get-find-for-treatment/(?P<type>.+)?$', 'get_find_for_treatment',
        name='get-find-for-treatment'),
    url(r'get-find-full/own/(?P<type>.+)?$', 'get_find',
        name='get-own-find-full', kwargs={'full': True, 'force_own': True}),
    url(r'get-find-full/(?P<type>.+)?$', 'get_find',
        name='get-find-full', kwargs={'full': True}),
    url(r'get-find-shortcut/(?P<type>.+)?$',
        'get_find', name='get-find-shortcut',
        kwargs={'full': 'shortcut'}),
    url(r'get-findsource/(?P<type>.+)?$',
        'get_findsource', name='get-findsource'),
    url(r'get-findsource-full/(?P<type>.+)?$',
        'get_findsource', name='get-findsource-full',
        kwargs={'full': True}),
    url(r'^show-findsource(?:/(?P<pk>.+))?/(?P<type>.+)?$', 'show_findsource',
        name=models.FindSource.SHOW_URL),
    url(r'^show-find/basket-(?P<pk>.+)/(?P<type>.+)?$', 'show_findbasket',
        name='show-findbasket'),
    url(r'^display-find/basket-(?P<pk>.+)/$', 'display_findbasket',
        name='display-findbasket'),
    url(r'^show-find(?:/(?P<pk>.+))?/(?P<type>.+)?$', 'show_find',
        name=models.Find.SHOW_URL),
    url(r'^display-find/(?P<pk>.+)/$', 'display_find',
        name='display-' + models.Find.SLUG),
    url(r'^show-historized-find/(?P<pk>.+)?/(?P<date>.+)?$',
        'show_find', name='show-historized-find'),
    url(r'^revert-find/(?P<pk>.+)/(?P<date>.+)$',
        'revert_find', name='revert-find'),
    url(r'^get-treatment/(?P<type>.+)?$',
        'get_treatment', name='get-treatment'),
    url(r'get-treatment-shortcut/(?P<type>.+)?$',
        'get_treatment', name='get-treatment-shortcut',
        kwargs={'full': 'shortcut'}),
    url(r'^show-treatment(?:/(?P<pk>.+))?/(?P<type>.+)?$', 'show_treatment',
        name=models.Treatment.SHOW_URL),
    url(r'show-historized-treatment/(?P<pk>.+)?/(?P<date>.+)?$',
        'show_treatment', name='show-historized-treatment'),
    url(r'^revert-treatment/(?P<pk>.+)/(?P<date>.+)$',
        'revert_treatment', name='revert-treatment'),
    url(r'get-treatmentfile/(?P<type>.+)?$',
        'get_treatmentfile', name='get-treatmentfile'),
    url(r'get-treatmentfile-shortcut/(?P<type>.+)?$',
        'get_treatmentfile', name='get-treatmentfile-shortcut',
        kwargs={'full': 'shortcut'}),
    url(r'^show-treatmentfile(?:/(?P<pk>.+))?/(?P<type>.+)?$',
        'show_treatmentfile',
        name=models.TreatmentFile.SHOW_URL),
    url(r'show-historized-treatmentfile/(?P<pk>.+)?/(?P<date>.+)?$',
        'show_treatmentfile', name='show-historized-treatmentfile'),
    url(r'^revert-treatmentfile/(?P<pk>.+)/(?P<date>.+)$',
        'revert_treatmentfile', name='revert-treatmentfile'),
    # url(r'show-treatmentfile(?:/(?P<pk>.+))?/(?P<type>.+)?$',
    # 'show_treatmentfile',
    #     name=models.TreatmentFile.SHOW_URL),
)

urlpatterns += patterns(
    'archaeological_operations.views',
    url(r'^treatment_administrativeact_document/$',
        'administrativeactfile_document',
        name='treatment-administrativeact-document',
        kwargs={'treatment': True}),
    url(r'^treatmentfle_administrativeact_document/$',
        'administrativeactfile_document',
        name='treatmentfle-administrativeact-document',
        kwargs={'treatment_file': True}),
)
