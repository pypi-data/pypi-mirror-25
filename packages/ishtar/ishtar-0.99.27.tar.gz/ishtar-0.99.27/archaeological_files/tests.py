#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

import datetime
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from ishtar_common.tests import TestCase, COMMON_FIXTURES

from ishtar_common.models import PersonType, Town, IshtarSiteProfile
from archaeological_files import models
from archaeological_operations.models import Parcel, ParcelOwner
from archaeological_operations.tests import OperationInitTest, \
    FILE_TOWNS_FIXTURES


class FileInit(object):
    def login_as_superuser(self):
        self.client.login(username='username', password='tralala')

    def create_file(self):
        self.extra_models, self.model_list = {}, []
        self.user, created = User.objects.get_or_create(username='username',
                                                        is_superuser=True)
        self.user.set_password('tralala')
        self.user.save()
        self.o_user, created = User.objects.get_or_create(username='ousername')
        person_type, created = PersonType.objects.get_or_create(
            label=u'Test ' u'person type', txt_idx='test_person',
            available=True)
        self.extra_models['person_type'] = person_type
        self.model_list.append(person_type)

        person = models.Person(surname='Surname', name='Name',
                               history_modifier=self.o_user)
        person.save()
        self.extra_models['person'] = person
        self.model_list.append(person)

        file_type, created = models.FileType.objects.get_or_create(
            label=u'Test file type', txt_idx='test_file', available=True)
        self.extra_models['file_type'] = file_type
        self.model_list.append(file_type)

        dct = {'year': 2010, 'numeric_reference': 1000, 'file_type': file_type,
               'internal_reference': u'UNIT_testÉ ?', 'in_charge': person,
               'history_modifier': self.o_user, 'total_surface': 10000}
        self.item = self.model(**dct)
        self.item.save()


class FileTest(TestCase, FileInit):
    fixtures = COMMON_FIXTURES
    model = models.File

    def setUp(self):
        IshtarSiteProfile.objects.create()
        self.create_file()

    def testExternalID(self):
        self.assertEqual(
            self.item.external_id,
            u"{}-{}".format(self.item.year,
                            self.item.numeric_reference))

    def testCachedLabel(self):
        # localisation fix
        lbls = []
        for town_lbl in (u'No town', u'Pas de commune'):
            lbls.append(settings.JOINT.join(
                [town_lbl, self.item.external_id,
                 self.item.internal_reference]))
        self.assertIn(self.item.cached_label, lbls)
        default_town = Town.objects.create(name="Paris", numero_insee='75001')
        self.item.towns.add(default_town)
        # manually done inside wizards
        self.item._cached_label_checked = False
        self.item.save()
        lbl = lbls[0].replace('No town', 'Paris')
        self.assertEqual(self.item.cached_label, lbl)

    def testAddAndGetHistorized(self):
        """
        Test correct new version and correct access to history
        """
        nb_hist = self.item.history.count()
        self.assertTrue(self.item.history.count() >= 1)
        base_label = self.item.internal_reference
        self.item.internal_reference = u"Unité_Test"
        self.item.history_modifier = self.user
        self.item.save()
        self.failUnlessEqual(self.item.history.count(), nb_hist + 1)
        self.failUnlessEqual(self.item.history.all()[1].internal_reference,
                             base_label)
        self.item.internal_reference = u"Unité_Testée"
        self.item.history_modifier = self.user
        self.item.skip_history_when_saving = True
        self.item.save()
        self.item.skip_history_when_saving = False
        self.failUnlessEqual(self.item.history.count(), nb_hist + 1)

    def testCreatorHistorized(self):
        """
        Test creator association
        """
        self.failUnlessEqual(self.item.history_creator, self.o_user)
        altuser, created = User.objects.get_or_create(username='altusername')
        self.item.internal_reference = u"Unité_Test"
        self.item.history_modifier = altuser
        self.item.save()
        self.failUnlessEqual(self.item.history_creator, self.o_user)

    def testIntelligentHistorisation(self):
        """
        Test that two identical version are not recorded twice in the history
        and that multiple saving in a short time are not considered
        """
        nb_hist = self.item.history.count()
        self.item.internal_reference = u"Unité_Test"
        self.item.history_modifier = self.user
        self.item.save()
        self.failUnlessEqual(self.item.history.count(), nb_hist + 1)
        nb_hist = self.item.history.count()
        self.item.save()
        self.failUnlessEqual(self.item.history.count(), nb_hist)

    def testRollbackFile(self):
        nb_hist = self.item.history.count()
        initial_values = self.item.values()
        backup_date = self.item.history.all()[0].history_date
        self.item.internal_reference = u"Unité_Test"
        self.item.history_modifier = self.user
        self.item.save()
        self.item.rollback(backup_date)
        self.failUnlessEqual(self.item.history.count(), nb_hist)
        new_values = self.item.values()
        for k in initial_values.keys():
            self.assertTrue(k in new_values)
            self.assertEqual(
                new_values[k], initial_values[k],
                msg=u"for %s: %s != %s" % (k, unicode(new_values[k]),
                                           unicode(initial_values[k])))

    def testRESTGetFile(self):
        response = self.client.post(
            '/get-file/', {'numeric_reference': self.item.numeric_reference})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # not allowed -> no data
        self.assertTrue(not data)

        self.login_as_superuser()
        response = self.client.post(
            '/get-file/', {'numeric_reference': self.item.numeric_reference})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('records' in data)
        self.assertTrue(data['records'] == 1)

    def testRESTGetOldFile(self):
        initial_ref = self.item.internal_reference
        new_ref = u"Unité_Test_old_file"
        new_ref = initial_ref != new_ref and new_ref or new_ref + u"extra"
        self.item.internal_reference = new_ref
        self.item.history_modifier = self.user
        self.item.save()
        response = self.client.post(
            '/get-file/',
            {'numeric_reference': self.item.numeric_reference, 'old': 1})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # not allowed -> no data
        self.assertTrue(not data)

        self.login_as_superuser()
        response = self.client.post(
            '/get-file/',
            {'numeric_reference': self.item.numeric_reference, 'old': 1})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('records' in data)
        self.assertTrue(data['records'] == 1)
        self.assertEqual(data['rows'][0]['internal_reference'], initial_ref)

    def testPostDeleteParcels(self):
        fle = self.item
        town = Town.objects.create(name='plouf', numero_insee='20000')
        parcel = Parcel.objects.create(town=town)
        parcel_nb = Parcel.objects.count()
        fle.parcels.add(parcel)
        fle.delete()
        # our parcel has no operation attached and should be deleted
        self.assertEqual(parcel_nb - 1, Parcel.objects.count())

        self.create_file()
        fle = self.item
        parcel = Parcel.objects.create(town=town)
        parcel_nb = Parcel.objects.count()
        fle.parcels.add(parcel)
        fle.parcels.clear()  # no signal raised... should resave
        Parcel.objects.filter(pk=parcel.pk).all()[0].save()
        # our parcel has no operation attached and should be deleted
        self.assertEqual(parcel_nb - 1, Parcel.objects.count())

    def test_show(self):
        c = Client()
        url = 'show-file'
        pk = self.item.pk
        response = self.client.get(reverse(url, kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)
        # empty content when not allowed
        self.assertEqual(response.content, "")

        self.login_as_superuser()
        response = self.client.get(reverse(url, kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="sheet"', response.content)


class FileOperationTest(TestCase, OperationInitTest, FileInit):
    model = models.File
    fixtures = FILE_TOWNS_FIXTURES

    def setUp(self):
        self.create_file()
        self.orgas = self.create_orgas(self.user)
        self.operations = self.create_operation(self.user, self.orgas[0])
        self.operation = self.operations[0]

    def testFileAssociation(self):
        # parcel association
        default_town = Town.objects.all()[0]
        for p in range(0, 10):
            parcel = Parcel.objects.create(
                parcel_number=unicode(p),
                section='YY',
                town=default_town,
                operation=self.operation)
            if p == 1:
                ParcelOwner.objects.create(
                    owner=self.extra_models['person'],
                    parcel=parcel, start_date=datetime.date.today(),
                    end_date=datetime.date.today())
        initial_nb = self.item.parcels.count()
        # no parcel on the file -> new parcels are copied from the
        # operation
        self.operation.associated_file = self.item
        self.operation.save()
        self.assertEqual(self.item.parcels.count(), initial_nb + 10)
        # parcel owner well attached
        q = ParcelOwner.objects.filter(parcel__associated_file=self.item)
        self.assertEqual(q.count(), 1)

        # when attaching parcel from a file to an operation, copy is done
        parcel = Parcel.objects.create(
            parcel_number='42', section='ZZ',
            town=default_town, associated_file=self.item)
        ParcelOwner.objects.create(
            owner=self.extra_models['person'],
            parcel=parcel, start_date=datetime.date.today(),
            end_date=datetime.date.today())
        parcel.operation = self.operation
        parcel.save()
        # double reference to operation and associated_file is deleted
        self.assertEqual(parcel.operation, None)
        # now 2 objects with the same parameters
        q = Parcel.objects.filter(parcel_number='42', section='ZZ',
                                  town=default_town)
        self.assertEqual(q.count(), 2)
        q = q.filter(operation=self.operation, associated_file=None)
        self.assertEqual(q.count(), 1)
        # parcel owner well attached
        q = ParcelOwner.objects.filter(parcel__operation=self.operation,
                                       parcel__parcel_number='42')
        self.assertEqual(q.count(), 1)
