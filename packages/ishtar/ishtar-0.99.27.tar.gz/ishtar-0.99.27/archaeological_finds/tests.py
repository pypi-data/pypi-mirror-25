#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test.client import Client
from ishtar_common.models import ImporterType, IshtarUser, ImporterColumn,\
    FormaterType, ImportTarget, IshtarSiteProfile

from ishtar_common.models import Person, get_current_profile
from archaeological_context_records.models import Period, Dating
from archaeological_finds import models, views
from archaeological_warehouse.models import Warehouse, WarehouseType

from ishtar_common import forms_common

from ishtar_common.tests import WizardTest, WizardTestFormData as FormData, \
    TestCase
from archaeological_operations.tests import ImportTest
from archaeological_context_records.tests import ContextRecordInit, \
    CONTEXT_RECORD_FIXTURES, CONTEXT_RECORD_TOWNS_FIXTURES


FIND_FIXTURES = CONTEXT_RECORD_FIXTURES + [
    settings.ROOT_PATH +
    '../archaeological_finds/fixtures/initial_data-fr.json',
]

FIND_TOWNS_FIXTURES = CONTEXT_RECORD_TOWNS_FIXTURES + [
    settings.ROOT_PATH +
    '../archaeological_finds/fixtures/initial_data-fr.json',
]

WAREHOUSE_FIXTURES = FIND_FIXTURES + [
    settings.ROOT_PATH +
    '../archaeological_warehouse/fixtures/initial_data-fr.json',
]


class FindInit(ContextRecordInit):
    test_context_records = False

    def create_finds(self, user=None, data_base={}, data={}, force=False):
        if not getattr(self, 'finds', None):
            self.finds = []
        if not getattr(self, 'base_finds', None):
            self.base_finds = []

        default = {'label': "Base find"}
        if not data_base.get('history_modifier'):
            data_base['history_modifier'] = self.get_default_user()
        if force or not data_base.get('context_record'):
            data_base['context_record'] = self.get_default_context_record(
                force=force)
        default.update(data_base)
        base_find = models.BaseFind.objects.create(**default)
        self.base_finds.append(base_find)

        data["history_modifier"] = data_base["history_modifier"]
        find = models.Find.objects.create(**data)
        find.base_finds.add(base_find)
        self.finds.append(find)
        return self.finds, self.base_finds

    def get_default_find(self, force=False):
        finds, base_finds = self.create_finds(force=force)
        if force:
            return finds[-1], base_finds[-1]
        return finds[0], base_finds[0]

    def tearDown(self):
        super(FindInit, self).tearDown()
        if hasattr(self, 'finds'):
            for f in self.finds:
                try:
                    f.delete()
                except:
                    pass
            self.finds = []
        if hasattr(self, 'base_finds'):
            for f in self.base_finds:
                try:
                    f.delete()
                except:
                    pass
            self.base_find = []


class FindWizardCreationTest(WizardTest, FindInit, TestCase):
    fixtures = WAREHOUSE_FIXTURES
    url_name = 'find_creation'
    wizard_name = 'find_wizard'
    steps = views.find_creation_steps
    form_datas = [
        FormData(
            'Find creation',
            form_datas={
                'selecrecord-find_creation': {'pk': 1},
                'find-find_creation': {
                    'label': 'hop',
                    'checked': 'NC',
                    'check_date': '2016-01-01'
                },
                'dating-find_creation': [
                    {
                        'period': None,
                        'start_date': '0',
                        'end_date': '200',
                    },
                    {
                        'period': None,
                        'start_date': '0',
                        'end_date': '200',
                    }
                ]
            },
        )
    ]

    def pre_wizard(self):
        cr = self.create_context_record(
            data={'parcel': self.create_parcel()[-1]}, force=True)[-1]

        self.form_datas[0].form_datas['selecrecord-find_creation']['pk'] = \
            cr.pk
        period = Period.objects.all()[0].pk
        self.form_datas[0].form_datas['dating-find_creation'][0]['period'] = \
            period
        self.form_datas[0].form_datas['dating-find_creation'][1]['period'] = \
            period
        self.find_number = models.Find.objects.count()
        self.basefind_number = models.BaseFind.objects.count()
        super(FindWizardCreationTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.BaseFind.objects.count(),
                         self.basefind_number + 1)
        self.assertEqual(models.Find.objects.count(),
                         self.find_number + 1)
        # identical datings, only one should be finaly save
        f = models.Find.objects.order_by("-pk").all()[0]
        self.assertEqual(f.datings.count(), 1)


class FindWizardDeletionWithWarehouseModTest(WizardTest, FindInit, TestCase):
    fixtures = WAREHOUSE_FIXTURES
    url_name = 'find_deletion'
    wizard_name = 'find_deletion_wizard'
    steps = views.find_deletion_steps
    form_datas = [
        FormData(
            'Find deletion',
            form_datas={
                'selecw': {},
            },
            ignored=['selec-find_deletion']
        )
    ]

    def pre_wizard(self):
        profile, created = IshtarSiteProfile.objects.get_or_create(
            slug='default', active=True)
        profile.warehouse = True
        profile.save()

        find, bf = self.get_default_find(force=True)
        self.form_datas[0].set('selecw', 'pk', find.pk)
        self.find_number = models.Find.objects.count()
        super(FindWizardDeletionWithWarehouseModTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.Find.objects.count(),
                         self.find_number - 1)


class TreatmentWizardCreationTest(WizardTest, FindInit, TestCase):
    fixtures = WAREHOUSE_FIXTURES
    url_name = 'treatment_creation'
    wizard_name = 'treatment_wizard'
    steps = views.treatment_wizard_steps
    form_datas = [
        FormData(
            'Move treament',
            form_datas={
                'file-treatment_creation': {},
                'basetreatment-treatment_creation': {
                    'treatment_type': 4,  # move
                    'person': 1,  # doer
                    'location': 1,  # associated warehouse
                    'year': 2016,
                    'target_is_basket': False
                },
                'selecfind-treatment_creation': {
                    'pk': 1,
                    'resulting_pk': 1
                }
            },
            ignored=('resultfind-treatment_creation',
                     'selecbasket-treatment_creation',
                     'resultfinds-treatment_creation'))
    ]

    def pre_wizard(self):
        q = Warehouse.objects.filter(pk=1)
        if not q.count():
            warehouse = Warehouse.objects.create(
                name="default", warehouse_type=WarehouseType.objects.all()[0])
            warehouse.id = 1
            warehouse.save()
        q = Person.objects.filter(pk=1)
        if not q.count():
            person = Person.objects.create(name="default")
            person.id = 1
            person.save()
        self.find, base_find = self.get_default_find(force=True)
        self.form_datas[0].form_datas['selecfind-treatment_creation'][
            'pk'] = self.find.pk
        self.form_datas[0].form_datas['selecfind-treatment_creation'][
            'resulting_pk'] = self.find.pk
        self.treatment_number = models.Treatment.objects.count()
        super(TreatmentWizardCreationTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.Treatment.objects.count(),
                         self.treatment_number + 1)
        treat = models.Treatment.objects.order_by('-pk').all()[0]
        self.find = models.Find.objects.get(pk=self.find.pk)
        self.assertEqual(models.Find.objects.filter(
            upstream_treatment=treat).count(), 1)
        self.assertEqual(self.find.downstream_treatment,
                         treat)


class ImportFindTest(ImportTest, TestCase):
    fixtures = FIND_TOWNS_FIXTURES

    def test_mcc_import_finds(self):
        self.init_context_record()

        old_nb = models.BaseFind.objects.count()
        old_nb_find = models.Find.objects.count()
        MCC = ImporterType.objects.get(name=u"MCC - Mobilier")

        col = ImporterColumn.objects.create(col_number=25,
                                            importer_type_id=MCC.pk)
        formater = FormaterType.objects.filter(
            formater_type='FileFormater').all()[0]
        ImportTarget.objects.create(target='image',
                                    formater_type_id=formater.pk,
                                    column_id=col.pk)
        mcc_file = open(
            settings.ROOT_PATH +
            '../archaeological_finds/tests/MCC-finds-example.csv', 'rb')
        mcc_images = open(
            settings.ROOT_PATH +
            '../archaeological_finds/tests/images.zip', 'rb')
        file_dict = {'imported_file': SimpleUploadedFile(mcc_file.name,
                                                         mcc_file.read()),
                     'imported_images': SimpleUploadedFile(mcc_images.name,
                                                           mcc_images.read())}
        post_dict = {'importer_type': MCC.pk, 'skip_lines': 1,
                     "encoding": 'utf-8'}
        form = forms_common.NewImportForm(data=post_dict, files=file_dict)
        form.is_valid()
        self.assertTrue(form.is_valid())
        impt = form.save(self.ishtar_user)
        impt.initialize()

        # doing manual connections
        ceram = models.MaterialType.objects.get(txt_idx='ceramic').pk
        glass = models.MaterialType.objects.get(txt_idx='glass').pk
        self.set_target_key('material_types', 'terre-cuite', ceram)
        self.set_target_key('material_types', 'verre', glass)
        impt.importation()
        # new finds has now been imported
        current_nb = models.BaseFind.objects.count()
        self.assertEqual(current_nb, (old_nb + 4))
        current_nb = models.Find.objects.count()
        self.assertEqual(current_nb, (old_nb_find + 4))
        self.assertEqual(
            models.Find.objects.filter(material_types__pk=ceram).count(), 4)
        self.assertEqual(
            models.Find.objects.filter(material_types__pk=glass).count(), 1)
        images = [f.image for f in models.Find.objects.all() if f.image.name]
        self.assertEqual(len(images), 1)


class FindTest(FindInit, TestCase):
    fixtures = FIND_FIXTURES
    model = models.Find

    def setUp(self):
        self.create_finds(force=True)
        self.password = 'mypassword'
        self.username = 'myuser'
        User.objects.create_superuser(self.username, 'myemail@test.com',
                                      self.password)
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def testExternalID(self):
        find = self.finds[0]
        base_find = find.base_finds.all()[0]
        self.assertEqual(
            find.external_id,
            u"{}-{}".format(
                find.get_first_base_find().context_record.external_id,
                find.label))
        self.assertEqual(
            base_find.external_id,
            u"{}-{}".format(
                base_find.context_record.external_id,
                base_find.label))

    def testIndex(self):
        profile = get_current_profile()
        profile.find_index = u"O"
        profile.save()
        profile = get_current_profile(force=True)

        op1 = self.create_operation()[-1]
        op2 = self.create_operation()[-1]
        op1_cr1 = self.create_context_record(data={'label': "CR1",
                                                   'operation': op1})[-1]
        op1_cr2 = self.create_context_record(data={'label': "CR2",
                                                   'operation': op1})[-1]
        op2_cr1 = self.create_context_record(data={'label': "CR3",
                                                   'operation': op2})[-1]
        self.create_finds(data_base={'context_record': op1_cr1})
        find_1 = self.finds[-1]
        bf_1 = models.BaseFind.objects.get(pk=self.base_finds[-1].pk)
        self.assertEqual(find_1.index, 1)
        self.assertEqual(bf_1.index, 1)

        # index is based on operations
        self.create_finds(data_base={'context_record': op1_cr2})
        find_2 = self.finds[-1]
        bf_2 = models.BaseFind.objects.get(pk=self.base_finds[-1].pk)
        self.assertEqual(find_2.index, 2)
        self.assertEqual(bf_2.index, 2)

        self.create_finds(data_base={'context_record': op2_cr1})
        find_3 = self.finds[-1]
        bf_3 = models.BaseFind.objects.get(pk=self.base_finds[-1].pk)
        self.assertEqual(find_3.index, 1)
        self.assertEqual(bf_3.index, 1)

        profile = get_current_profile(force=True)
        profile.find_index = u"CR"
        profile.save()
        profile = get_current_profile(force=True)

        op3 = self.create_operation()[-1]
        op3_cr1 = self.create_context_record(data={'label': "CR1",
                                                   'operation': op3})[-1]
        op3_cr2 = self.create_context_record(data={'label': "CR2",
                                                   'operation': op3})[-1]
        self.create_finds(data_base={'context_record': op3_cr1})
        find_1b = self.finds[-1]
        bf_1b = models.BaseFind.objects.get(pk=self.base_finds[-1].pk)
        self.assertEqual(find_1b.index, 1)
        self.assertEqual(bf_1b.index, 1)

        # index now based on context records
        self.create_finds(data_base={'context_record': op3_cr2})
        find_2b = self.finds[-1]
        bf_2b = models.BaseFind.objects.get(pk=self.base_finds[-1].pk)
        self.assertEqual(find_2b.index, 1)
        self.assertEqual(bf_2b.index, 1)

        self.create_finds(data_base={'context_record': op3_cr2})
        find_3b = self.finds[-1]
        bf_3b = models.BaseFind.objects.get(pk=self.base_finds[-1].pk)
        self.assertEqual(find_3b.index, 2)
        self.assertEqual(bf_3b.index, 2)

    def test_show(self):
        obj = self.finds[0]
        response = self.client.get(reverse('display-find', args=[obj.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('load_window("/show-find/{}/");'.format(obj.pk),
                      response.content)
        c = Client()
        response = c.get(reverse('show-find', kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 200)
        # empty content when not allowed
        self.assertEqual(response.content, "")

        c.login(username=self.username, password=self.password)
        response = self.client.get(reverse('show-find', kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="sheet"', response.content)

    def test_delete(self):
        self.create_finds(force=True)
        first_bf = self.base_finds[0]
        self.finds[1].base_finds.add(first_bf)

        self.finds[0].delete()
        # on delete the selected base find is not deleted if another find
        # is related to it
        self.assertEqual(models.BaseFind.objects.filter(
            pk=self.base_finds[0].pk).count(), 1)
        self.finds[1].delete()
        self.assertEqual(models.BaseFind.objects.filter(
            pk=self.base_finds[0].pk).count(), 0)


class FindSearchTest(FindInit, TestCase):
    fixtures = FIND_FIXTURES
    model = models.Find

    def setUp(self):
        self.create_finds(force=True)
        self.username = 'myuser'
        self.password = 'mypassword'
        User.objects.create_superuser(self.username, 'myemail@test.com',
                                      self.password)
        self.client = Client()

    def testMaterialTypeHierarchicSearch(self):
        find = self.finds[0]
        c = Client()
        metal = models.MaterialType.objects.get(txt_idx='metal')
        iron_metal = models.MaterialType.objects.get(txt_idx='iron_metal')
        not_iron_metal = models.MaterialType.objects.get(
            txt_idx='not_iron_metal')
        find.material_types.add(iron_metal)

        search = {'material_types': iron_metal.pk}

        # no result when no authentication
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not json.loads(response.content))
        c.login(username=self.username, password=self.password)

        # one result for exact search
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertTrue(res['total'] == 1)
        self.assertEqual(res["rows"][0]["material_types__label"],
                         unicode(iron_metal))

        # no result for the brother
        search = {'material_types': not_iron_metal.pk}
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['total'] == 0)

        # one result for the father
        search = {'material_types': metal.pk}
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['total'] == 1)

    def testPeriodHierarchicSearch(self):
        find = self.finds[0]
        c = Client()

        neo = Period.objects.get(txt_idx='neolithic')
        final_neo = Period.objects.get(txt_idx='final_neolithic')
        recent_neo = Period.objects.get(txt_idx='recent_neolithic')
        dating = Dating.objects.create(
            period=final_neo
        )
        find.datings.add(dating)

        search = {'datings__period': final_neo.pk}

        # no result when no authentication
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not json.loads(response.content))

        # one result for exact search
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertTrue(res['total'] == 1)
        self.assertEqual(res["rows"][0]["datings__period__label"],
                         unicode(final_neo))

        # no result for the brother
        search = {'datings__period': recent_neo.pk}
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['total'], 0)

        # one result for the father
        search = {'datings__period': neo.pk}
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['total'], 1)

    def testConservatoryStateHierarchicSearch(self):
        find = self.finds[0]
        c = Client()
        cs1 = models.ConservatoryState.objects.all()[0]
        cs1.parent = None
        cs1.save()
        cs2 = models.ConservatoryState.objects.all()[1]
        cs2.parent = cs1
        cs2.save()
        cs3 = models.ConservatoryState.objects.all()[2]
        cs3.parent = cs1
        cs3.save()
        find.conservatory_state = cs2
        find.save()

        search = {'conservatory_state': cs2.pk}

        # no result when no authentication
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not json.loads(response.content))
        c.login(username=self.username, password=self.password)

        # one result for exact search
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['total'] == 1)

        # no result for the brother
        search = {'conservatory_state': cs3.pk}
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['total'] == 0)

        # one result for the father
        search = {'conservatory_state': cs1.pk}
        response = c.get(reverse('get-find'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['total'] == 1)


class PackagingTest(FindInit, TestCase):
    fixtures = FIND_FIXTURES
    model = models.Find

    def setUp(self):
        img = settings.ROOT_PATH + \
            '../ishtar_common/static/media/images/ishtar-bg.jpg'

        self.create_finds({"label": u"Find 1"}, force=True)
        self.create_finds({"label": u"Find 2"}, force=True)
        self.finds[0].image.save('ishtar-bg.jpg', File(open(img)))
        self.finds[0].save()

        self.basket = models.FindBasket.objects.create(
            label="My basket", user=IshtarUser.objects.get(
                pk=self.get_default_user().pk))
        self.other_basket = models.FindBasket.objects.create(
            label="My other basket", user=IshtarUser.objects.get(
                pk=self.get_default_user().pk))
        for find in self.finds:
            self.basket.items.add(find)
            self.other_basket.items.add(find)

    def testPackaging(self):
        treatment_type = models.TreatmentType.objects.get(txt_idx='packaging')
        treatment = models.Treatment()
        items_nb = models.Find.objects.count()

        first_find = self.finds[0]

        treatment.save(user=self.get_default_user(), items=self.basket)
        self.assertEqual(items_nb + self.basket.items.count(),
                         models.Find.objects.count(),
                         msg="Packaging doesn't generate enough new finds")
        treatment.treatment_types.add(treatment_type)

        resulting_find = models.Find.objects.get(
            upstream_treatment__upstream=first_find,
            base_finds__pk=first_find.base_finds.all()[0].pk
        )

        # image names used to be altered on save: check for this bug
        self.assertEqual(
            resulting_find.image.name,
            models.Find.objects.get(pk=first_find.pk).image.name
        )

        # new version of the find is in the basket
        for item in self.basket.items.all():
            self.assertNotIn(
                item, self.finds,
                msg="Original basket have not been upgraded after packaging")
        for item in self.other_basket.items.all():
            self.assertNotIn(
                item, self.finds,
                msg="Other basket have not been upgraded after packaging")

    def test_delete(self):
        # manage treatment deletion
        treatment_type = models.TreatmentType.objects.get(txt_idx='packaging')
        treatment = models.Treatment()

        initial_find = self.finds[0]
        treatment.save(user=self.get_default_user(), items=self.basket)
        treatment.treatment_types.add(treatment_type)

        resulting_find = models.Find.objects.get(
            upstream_treatment__upstream=initial_find,
            base_finds__pk=initial_find.base_finds.all()[0].pk
        )
        resulting_find.delete()

        self.assertEqual(
            models.Treatment.objects.filter(pk=treatment.pk).count(), 0)
        q = models.Find.objects.filter(pk=initial_find.pk)
        # initial find not deleted
        self.assertEqual(q.count(), 1)
        initial_find = q.all()[0]
        self.assertEqual(initial_find.upstream_treatment, None)
