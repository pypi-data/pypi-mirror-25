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

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template

from menus import menu

from ishtar_common import views
from ishtar_common.wizards import check_rights

# be careful: each check_rights must be relevant with ishtar_menu

# forms
urlpatterns = patterns(
    '',
    url(r'^status/$', views.status, name='status'),
    url(r'^robots\.txt$', direct_to_template,
        {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    # internationalization
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # General
    url(r'shortcut_menu/', views.shortcut_menu, name='shortcut-menu'),
    url(r'display/(?P<item_type>\w+)/(?P<pk>\d+)/',
        views.DisplayItemView.as_view(), name='display-item'),
    url(r'person_search/(?P<step>.+)?$',
        check_rights(['add_person'])(
            views.person_search_wizard), name='person_search'),
    url(r'person_creation/(?P<step>.+)?$',
        check_rights(['add_person'])(
            views.person_creation_wizard), name='person_creation'),
    url(r'person_modification/(?P<step>.+)?$',
        check_rights(['change_person', 'change_own_person'])(
            views.person_modification_wizard), name='person_modification'),
    url(r'person_modify/(?P<pk>.+)/$', views.person_modify,
        name='person_modify'),
    url(r'person_deletion/(?P<step>.+)?$',
        check_rights(['change_person', 'change_own_person'])(
            views.person_deletion_wizard), name='person_deletion'),
    url(r'^person-edit/$',
        check_rights(['add_person'])(
            views.PersonCreate.as_view()), name='person_create'),
    url(r'^person-edit/(?P<pk>\d+)$',
        check_rights(['change_person', 'change_own_person'])(
            views.PersonEdit.as_view()), name='person_edit'),
    url(r'organization_search/(?P<step>.+)?$',
        check_rights(['add_organization'])(
            views.organization_search_wizard), name='organization_search'),
    url(r'organization_creation/(?P<step>.+)?$',
        check_rights(['add_organization'])(
            views.organization_creation_wizard), name='organization_creation'),
    url(r'organization_modification/(?P<step>.+)?$',
        check_rights(['change_organization', 'change_own_organization'])(
            views.organization_modification_wizard),
        name='organization_modification'),
    url(r'organization_modify/(?P<pk>.+)/$', views.organization_modify,
        name='organization_modify'),
    url(r'organization_deletion/(?P<step>.+)?$',
        check_rights(['change_organization', 'change_own_organization'])(
            views.organization_deletion_wizard), name='organization_deletion'),
    url(r'organization-edit/$',
        check_rights(['add_organization'])(
            views.OrganizationCreate.as_view()), name='organization_create'),
    url(r'organization-edit/(?P<pk>\d+)$',
        check_rights(['change_organization', 'change_own_organization'])(
            views.OrganizationEdit.as_view()), name='organization_edit'),
    url(r'organization-person-edit/$',
        check_rights(['add_organization'])(
            views.OrganizationPersonCreate.as_view()),
        name='organization_person_create'),
    url(r'organization-person-edit/(?P<pk>\d+)$',
        check_rights(['change_organization', 'change_own_organization'])(
            views.OrganizationPersonEdit.as_view()),
        name='organization_person_edit'),
    url(r'get-ishtaruser/(?P<type>.+)?$',
        views.get_ishtaruser,
        name='get-ishtaruser'),
    url(r'account_management/(?P<step>.+)?$',
        check_rights(['add_ishtaruser'])(
            views.account_management_wizard), name='account_management'),
    url(r'account_deletion/(?P<step>.+)?$',
        check_rights(['add_ishtaruser'])(
            views.account_deletion_wizard), name='account_deletion'),
    url(r'^import-new/$',
        check_rights(['change_import'])(
            views.NewImportView.as_view()), name='new_import'),
    url(r'^import-list/$',
        check_rights(['change_import'])(
            views.ImportListView.as_view()),
        name='current_imports'),
    url(r'^import-list-old/$',
        check_rights(['change_import'])(
            views.ImportOldListView.as_view()),
        name='old_imports'),
    url(r'^import-delete/(?P<pk>[0-9]+)/$',
        views.ImportDeleteView.as_view(), name='import_delete'),
    url(r'^import-link-unmatched/(?P<pk>[0-9]+)/$',
        views.ImportLinkView.as_view(), name='import_link_unmatched'),
)

actions = []
for section in menu.childs:
    for menu_item in section.childs:
        if hasattr(menu_item, 'childs'):
            for menu_subitem in menu_item.childs:
                actions.append(menu_subitem.idx)
        else:
            actions.append(menu_item.idx)
actions = r"|".join(actions)

# other views
urlpatterns += patterns(
    'ishtar_common.views',
    # General
    url(r'dashboard-main/$', 'dashboard_main',
        name='dashboard-main'),
    url(r'dashboard-main/(?P<item_name>[a-z-]+)/$', 'dashboard_main_detail',
        name='dashboard-main-detail'),
    url(r'update-current-item/$', 'update_current_item',
        name='update-current-item'),
    url(r'pin/(?P<item_type>[a-z-]+)/(?P<pk>\d+)/$', 'update_current_item',
        name='pin'),
    url(r'unpin/(?P<item_type>[a-z-]+)/$', 'unpin', name='unpin'),
    url(r'get-by-importer/(?P<slug>[\w-]+)/(?P<type>[a-z-]+)?$',
        'get_by_importer', name='get-by-importer'),
    url(r'new-person/(?:(?P<parent_name>[^/]+)/)?(?:(?P<limits>[^/]+)/)?$',
        'new_person', name='new-person'),
    url(r'new-person-noorga/'
        r'(?:(?P<parent_name>[^/]+)/)?(?:(?P<limits>[^/]+)/)?$',
        'new_person_noorga', name='new-person-noorga'),
    url(r'autocomplete-person(?:/([0-9_]+))?(?:/([0-9_]*))?/(user)?$',
        'autocomplete_person', name='autocomplete-person'),
    url(r'autocomplete-person-permissive(?:/([0-9_]+))?(?:/([0-9_]*))?'
        r'/(user)?$', 'autocomplete_person_permissive',
        name='autocomplete-person-permissive'),
    url(r'get-person/(?P<type>.+)?$', 'get_person',
        name='get-person'),
    url(r'get-person-full/(?P<type>.+)?$', 'get_person',
        name='get-person-full', kwargs={'full': True}),
    url(r'show-person(?:/(?P<pk>.+))?/(?P<type>.+)?$',
        'show_person', name='show-person'),
    url(r'department-by-state/(?P<state_id>.+)?$', 'department_by_state',
        name='department-by-state'),
    url(r'autocomplete-town/?$', 'autocomplete_town',
        name='autocomplete-town'),
    url(r'autocomplete-advanced-town/(?P<department_id>[0-9]+[ABab]?)?$',
        'autocomplete_advanced_town', name='autocomplete-advanced-town'),
    url(r'autocomplete-department/?$', 'autocomplete_department',
        name='autocomplete-department'),
    url(r'new-author/(?:(?P<parent_name>[^/]+)/)?(?:(?P<limits>[^/]+)/)?$',
        'new_author', name='new-author'),
    url(r'autocomplete-author/$', 'autocomplete_author',
        name='autocomplete-author'),
    url(r'new-organization/(?:(?P<parent_name>[^/]+)/)?'
        r'(?:(?P<limits>[^/]+)/)?$',
        'new_organization', name='new-organization'),
    url(r'get-organization/(?P<type>.+)?$', 'get_organization',
        name='get-organization'),
    url(r'get-organization-full/(?P<type>.+)?$', 'get_organization',
        name='get-organization-full', kwargs={'full': True}),
    url(r'show-organization(?:/(?P<pk>.+))?/(?P<type>.+)?$',
        'show_organization', name='show-organization'),
    url(r'autocomplete-organization/([0-9_]+)?$',
        'autocomplete_organization', name='autocomplete-organization'),
    url(r'admin-globalvar/', views.GlobalVarEdit.as_view(),
        name='admin-globalvar'),
    url(r'person-merge/(?:(?P<page>\d+)/)?$', 'person_merge',
        name='person_merge'),
    url(r'person-manual-merge/$',
        views.PersonManualMerge.as_view(),
        name='person_manual_merge'),
    url(r'person-manual-merge-items/(?P<pks>[0-9_]+?)/$',
        views.PersonManualMergeItems.as_view(),
        name='person_manual_merge_items'),
    url(r'organization-merge/(?:(?P<page>\d+)/)?$', 'organization_merge',
        name='organization_merge'),
    url(r'orga-manual-merge/$', views.OrgaManualMerge.as_view(),
        name='orga_manual_merge'),
    url(r'orga-manual-merge-items/(?P<pks>[0-9_]+?)/$',
        views.OrgaManualMergeItems.as_view(),
        name='orga_manual_merge_items'),
    url(r'reset/$', 'reset_wizards', name='reset_wizards'),
    url(r'activate-all-search/$', 'activate_all_search',
        name='activate-all-search'),
    url(r'activate-own-search/$', 'activate_own_search',
        name='activate-own-search'),
    url(r'activate-advanced-menu/$', 'activate_advanced_shortcut_menu',
        name='activate-advanced-menu'),
    url(r'activate-simple-menu/$', 'activate_simple_shortcut_menu',
        name='activate-simple-menu'),
    url(r'hide-shortcut-menu/$', 'hide_shortcut_menu',
        name='hide-shortcut-menu'),
    url(r'show-shortcut-menu/$', 'show_shortcut_menu',
        name='show-shortcut-menu'),
    url(r'(?P<action_slug>' + actions + r')/$', 'action', name='action'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
