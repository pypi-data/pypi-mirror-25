#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from django.utils.translation import ugettext_lazy as _

from ishtar_common.menu_base import SectionItem, MenuItem

from archaeological_operations.models import AdministrativeAct
import models

# be carreful: each access_controls must be relevant with check_rights in urls

MENU_SECTIONS = [
    (50,
     SectionItem(
         'find_management', _(u"Find"),
         profile_restriction='find',
         css='menu-find',
         childs=[
             MenuItem(
                 'find_search', _(u"Search"),
                 model=models.Find,
                 access_controls=['view_find',
                                  'view_own_find']),
             MenuItem(
                 'find_creation', _(u"Creation"),
                 model=models.Find,
                 access_controls=['add_find',
                                  'add_own_find']),
             MenuItem(
                 'find_modification', _(u"Modification"),
                 model=models.Find,
                 access_controls=['change_find',
                                  'change_own_find']),
             MenuItem(
                 'find_deletion', _(u"Deletion"),
                 model=models.Find,
                 access_controls=['change_find',
                                  'change_own_find']),
             SectionItem(
                 'find_basket', _(u"Basket"),
                 childs=[
                     MenuItem('find_basket_creation',
                              _(u"Creation"),
                              model=models.FindBasket,
                              access_controls=['change_find',
                                               'change_own_find']),
                     MenuItem('find_basket_modification_add',
                              _(u"Manage items"),
                              model=models.FindBasket,
                              access_controls=[
                                  'change_find',
                                  'change_own_find']),
                     MenuItem('find_basket_deletion',
                              _(u"Deletion"),
                              model=models.FindBasket,
                              access_controls=['change_find',
                                               'change_own_find']),
                 ]),
             SectionItem(
                 'find_source', _(u"Documentation"),
                 childs=[
                     MenuItem('find_source_search',
                              _(u"Search"),
                              model=models.FindSource,
                              access_controls=['view_find',
                                               'view_own_find']),
                     MenuItem('find_source_creation',
                              _(u"Creation"),
                              model=models.FindSource,
                              access_controls=['change_find',
                                               'change_own_find']),
                     MenuItem('find_source_modification',
                              _(u"Modification"),
                              model=models.FindSource,
                              access_controls=['change_find',
                                               'change_own_find']),
                     MenuItem('find_source_deletion',
                              _(u"Deletion"),
                              model=models.FindSource,
                              access_controls=['change_find',
                                               'change_own_find']),
                 ]),
             # MenuItem(
             #     'treatment_creation', _(u"Add a treatment"),
             #     model=models.Treatment,
             #     access_controls=['change_find',
             #                      'change_own_find']),
         ])),
    (60,
     SectionItem(
         'treatmentfle_management', _(u"Treatment request"),
         profile_restriction='warehouse',
         css='menu-warehouse',
         childs=[
             MenuItem('treatmentfle_search',
                      _(u"Search"),
                      model=models.TreatmentFile,
                      access_controls=['view_treatmentfile',
                                       'view_own_treatmentfile']),
             MenuItem('treatmentfle_creation',
                      _(u"Creation"),
                      model=models.TreatmentFile,
                      access_controls=['change_treatmentfile',
                                       'change_own_treatmentfile']),
             MenuItem('treatmentfle_modification',
                      _(u"Modification"),
                      model=models.TreatmentFile,
                      access_controls=['change_treatmentfile',
                                       'change_own_treatmentfile']),
             MenuItem('treatmentfle_deletion',
                      _(u"Deletion"),
                      model=models.TreatmentFile,
                      access_controls=['change_treatmentfile',
                                       'change_own_treatmentfile']),
             SectionItem(
                 'admin_act_fletreatments', _(u"Administrative act"),
                 childs=[
                     MenuItem('treatmentfle_admacttreatmentfle_search',
                              _(u"Search"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                     MenuItem('treatmentfle_admacttreatmentfle',
                              _(u"Creation"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                     MenuItem('treatmentfle_admacttreatmentfle_modification',
                         _(u"Modification"), model=AdministrativeAct,
                         access_controls=['change_administrativeact']),
                     MenuItem('treatmentfle_admacttreatmentfle_deletion',
                              _(u"Deletion"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                     MenuItem('treatmentfle_administrativeact_document',
                              _(u"Documents"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                 ]
             ),
             SectionItem(
                 'treatmentfile_source', _(u"Source"),
                 childs=[
                     MenuItem('treatmentfile_source_search',
                              _(u"Search"),
                              model=models.TreatmentFileSource,
                              access_controls=['view_treatmentfile',
                                               'view_own_treatmentfile']),
                     MenuItem('treatmentfile_source_creation',
                              _(u"Creation"),
                              model=models.TreatmentFileSource,
                              access_controls=['change_treatmentfile',
                                               'change_own_treatmentfile']),
                     MenuItem('treatmentfile_source_modification',
                              _(u"Modification"),
                              model=models.TreatmentFileSource,
                              access_controls=['change_treatmentfile',
                                               'change_own_treatmentfile']),
                     MenuItem('treatmentfile_source_deletion',
                              _(u"Deletion"),
                              model=models.TreatmentFileSource,
                              access_controls=['change_treatmentfile',
                                               'change_own_treatmentfile']),
                 ]
             ),
         ]
     )),
    (70,
     SectionItem(
         'treatment_management', _(u"Treatment"),
         profile_restriction='warehouse',
         css='menu-warehouse',
         childs=[
            SectionItem(
                'find_treatments', _(u"Simple treatments"),
                childs=[
                    MenuItem('treatment_search',
                             _(u"Search"),
                             model=models.Treatment,
                             access_controls=['view_treatment',
                                              'view_own_treatment']),
                    MenuItem('treatment_creation',
                             _(u"Creation"),
                             model=models.Treatment,
                             access_controls=['change_treatment',
                                              'change_own_treatment']),
                    MenuItem('treatment_modification',
                             _(u"Modification"),
                             model=models.Treatment,
                             access_controls=['change_treatment',
                                              'change_own_treatment']),
                    MenuItem('treatment_deletion',
                             _(u"Deletion"),
                             model=models.Treatment,
                             access_controls=['change_treatment',
                                              'change_own_treatment']),
                ]),
            SectionItem(
                 'admin_act_treatments', _(u"Administrative act"),
                 childs=[
                     MenuItem('treatment_admacttreatment_search',
                              _(u"Search"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                     MenuItem('treatment_admacttreatment',
                              _(u"Creation"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                     MenuItem(
                         'treatment_admacttreatment_modification',
                         _(u"Modification"), model=AdministrativeAct,
                         access_controls=['change_administrativeact']),
                     MenuItem('treatment_admacttreatment_deletion',
                              _(u"Deletion"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                     MenuItem('treatment_administrativeact_document',
                              _(u"Documents"),
                              model=AdministrativeAct,
                              access_controls=['change_administrativeact']),
                 ]),
             SectionItem(
                 'treatment_source', _(u"Source"),
                 childs=[
                     MenuItem('treatment_source_search',
                              _(u"Search"),
                              model=models.TreatmentSource,
                              access_controls=['view_treatment',
                                               'view_own_treatment']),
                     MenuItem('treatment_source_creation',
                              _(u"Creation"),
                              model=models.TreatmentSource,
                              access_controls=['change_treatment',
                                               'change_own_treatment']),
                     MenuItem('treatment_source_modification',
                              _(u"Modification"),
                              model=models.TreatmentSource,
                              access_controls=['change_treatment',
                                               'change_own_treatment']),
                     MenuItem('treatment_source_deletion',
                              _(u"Deletion"),
                              model=models.TreatmentSource,
                              access_controls=['change_treatment',
                                               'change_own_treatment']),
                 ]
             ),
         ]
     )),
]
