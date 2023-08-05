#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from archaeological_finds.tests import FindInit

from ishtar_common.tests import WizardTest, WizardTestFormData as FormData, \
    TestCase
from archaeological_finds.tests import WAREHOUSE_FIXTURES

from archaeological_warehouse import models, views, forms


class WarehouseWizardCreationTest(WizardTest, FindInit, TestCase):
    fixtures = WAREHOUSE_FIXTURES
    url_name = 'warehouse_creation'
    wizard_name = 'warehouse_wizard'
    steps = views.warehouse_creation_steps
    form_datas = [
        FormData(
            'Warehouse creation',
            form_datas={
                'warehouse-warehouse_creation': {
                    'name': 'warehouse-ref',
                    'warehouse_type': None,
                    'location': None,
                    'responsible': None,
                },
                'divisions-warehouse_creation': [
                    {
                        'division': None,
                        'order': 42
                    }
                ]
            },
        ),
        FormData(
            'Warehouse creation with no division',
            form_datas={
                'warehouse-warehouse_creation': {
                    'name': 'warehouse-ref',
                    'warehouse_type': None,
                    'location': None,
                    'responsible': None,
                },
                'divisions-warehouse_creation': [
                    {
                        'order': 42
                    }
                ]
            },
        ),
    ]

    def pre_wizard(self):
        main_data = self.form_datas[0].form_datas
        alt_data = self.form_datas[1].form_datas
        main_data['warehouse-warehouse_creation']['warehouse_type'] = \
            models.WarehouseType.objects.all()[0].pk
        alt_data['warehouse-warehouse_creation']['warehouse_type'] = \
            models.WarehouseType.objects.all()[0].pk
        main_data['divisions-warehouse_creation'][0]['division'] = \
            models.WarehouseDivision.create_default_for_test()[0].pk
        self.warehouse_number = models.Warehouse.objects.count()
        self.warehouse_div_link = models.WarehouseDivisionLink.objects.count()
        super(WarehouseWizardCreationTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.Warehouse.objects.count(),
                         self.warehouse_number + 2)
        self.assertEqual(models.WarehouseDivisionLink.objects.count(),
                         self.warehouse_div_link + 1)


class ContainerWizardCreationTest(WizardTest, FindInit, TestCase):
    fixtures = WAREHOUSE_FIXTURES
    url_name = 'container_creation'
    wizard_name = 'container_wizard'
    steps = views.container_creation_steps
    form_datas = [
        FormData(
            'Container creation',
            form_datas={
                'container-container_creation': {
                    'reference': 'hop-ref',
                    'container_type': None,
                    'location': None,
                    'responsible': None,
                },
                'localisation-container_creation': []
            },
        ),
        FormData(
            'Other container on the same warehouse',
            form_datas={
                'container-container_creation': {
                    'reference': 'hop-ref2',
                    'container_type': None,
                    'location': None,
                    'responsible': None,
                },
                'localisation-container_creation': []
            },
        ),
        FormData(
            'Container creation with location',
            form_datas={
                'container-container_creation': {
                    'reference': 'hop-ref3',
                    'container_type': None,
                    'location': None,
                    'responsible': None,
                },
                'localisation-container_creation': []
            },
        ),
    ]

    def pre_wizard(self):
        main_warehouse = models.Warehouse.objects.create(
            name="Main",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        main_data = self.form_datas[0].form_datas
        main_data_bis = self.form_datas[1].form_datas
        alt_data = self.form_datas[2].form_datas
        for data in [main_data, main_data_bis, alt_data]:
            forms_data = data['container-container_creation']
            forms_data["responsible"] = main_warehouse.pk
            forms_data["location"] = main_warehouse.pk
            forms_data["container_type"] = \
                models.ContainerType.objects.all()[0].pk
        alt_warehouse = models.Warehouse.objects.create(
            name="Alt",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        div = models.WarehouseDivision.objects.create(label='division')
        div_link = models.WarehouseDivisionLink.objects.create(
            warehouse=alt_warehouse, division=div)
        alt_data['container-container_creation']["location"] = alt_warehouse.pk
        alt_data['localisation-container_creation'] = {
            'division_{}'.format(div_link.pk): 'Combien ?'
        }

        self.container_number = models.Container.objects.count()
        self.localisation_detail_number = \
            models.ContainerLocalisation.objects.count()
        super(ContainerWizardCreationTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.Container.objects.count(),
                         self.container_number + 3)
        self.assertEqual(models.ContainerLocalisation.objects.count(),
                         self.localisation_detail_number + 1)


class ContainerTest(FindInit, TestCase):
    fixtures = WAREHOUSE_FIXTURES

    def testFormCreation(self):
        main_warehouse = models.Warehouse.objects.create(
            name="Main",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        data = {
            'reference': 'hop-ref',
            "responsible": main_warehouse.pk,
            "location": main_warehouse.pk,
            "container_type": models.ContainerType.objects.all()[0].pk
        }
        form = forms.ContainerForm(data=data)
        self.assertTrue(form.is_valid(), msg="{}".format(form.errors))
        self.container_number = models.Container.objects.count()
        self.create_user()
        form.save(self.user)
        self.assertEqual(models.Container.objects.count(),
                         self.container_number + 1)

    def testChangeLocation(self):
        main_warehouse = models.Warehouse.objects.create(
            name="Main",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        div = models.WarehouseDivision.objects.create(label='division')
        div_link = models.WarehouseDivisionLink.objects.create(
            warehouse=main_warehouse, division=div)

        container = models.Container.objects.create(
            reference="Test", responsible=main_warehouse,
            location=main_warehouse,
            container_type=models.ContainerType.objects.all()[0]
        )
        models.ContainerLocalisation.objects.create(
            container=container, division=div_link,
        )

        self.assertTrue(models.ContainerLocalisation.objects.filter(
            division__warehouse=main_warehouse).count())
        # changing location remove unrelevent localisation
        other_warehouse = models.Warehouse.objects.create(
            name="Other",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        container.location = other_warehouse
        container.save()
        self.assertFalse(models.ContainerLocalisation.objects.filter(
            division__warehouse=main_warehouse).count())

