#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012-2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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
import datetime

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test.client import Client

from django.contrib.auth.models import Permission
import models

from archaeological_operations import views

from ishtar_common.models import OrganizationType, Organization, ItemKey, \
    ImporterType, IshtarUser, TargetKey, ImporterModel, IshtarSiteProfile, \
    Town, ImporterColumn, Person, Author, SourceType, AuthorType
from archaeological_context_records.models import Unit

from ishtar_common import forms_common
from ishtar_common.tests import WizardTest, WizardTestFormData as FormData, \
    create_superuser, create_user, TestCase, OPERATION_FIXTURES

OPERATION_TOWNS_FIXTURES = \
    OPERATION_FIXTURES + \
    [settings.ROOT_PATH + '../ishtar_common/fixtures/test_towns.json']

FILE_FIXTURES = OPERATION_FIXTURES + [
    settings.ROOT_PATH +
    '../archaeological_files/fixtures/initial_data.json']

FILE_TOWNS_FIXTURES = OPERATION_TOWNS_FIXTURES + [
    settings.ROOT_PATH +
    '../archaeological_files/fixtures/initial_data.json']


class ImportTest(object):
    def setUp(self):
        self.username, self.password, self.user = create_superuser()
        self.ishtar_user = IshtarUser.objects.get(pk=self.user.pk)

    def set_target_key(self, target, key, value, imp=None):
        keys = {'target__target': target, 'key': key}
        if imp:
            keys['associated_import'] = imp
        tg = TargetKey.objects.get(**keys)
        tg.value = value
        tg.is_set = True
        tg.save()

    def init_ope_import(self, filename='MCC-operations-example.csv'):
        mcc_operation = ImporterType.objects.get(name=u"MCC - Opérations")
        mcc_operation_file = open(
            settings.ROOT_PATH +
            '../archaeological_operations/tests/' + filename,
            'rb')
        file_dict = {'imported_file': SimpleUploadedFile(
            mcc_operation_file.name, mcc_operation_file.read())}
        post_dict = {'importer_type': mcc_operation.pk, 'skip_lines': 1,
                     "encoding": 'utf-8'}
        form = forms_common.NewImportForm(data=post_dict, files=file_dict)
        form.is_valid()
        return mcc_operation, form

    def init_ope_targetkey(self, imp):
        # doing manually connections
        target = TargetKey.objects.filter(
            target__target='operation_type').order_by('-pk').all()[0]
        target.value = models.OperationType.objects.get(
            txt_idx='prog_excavation').pk
        target.is_set = True
        target.associated_import = imp
        target.save()

        target2 = TargetKey.objects.get(key='gallo-romain',
                                        associated_import=imp)
        gallo = models.Period.objects.get(txt_idx='gallo-roman')
        target2.value = gallo.pk
        target2.is_set = True
        target2.associated_import = imp
        target2.save()

        target3 = TargetKey.objects.get(key='age-du-fer',
                                        associated_import=imp)
        iron = models.Period.objects.get(txt_idx='iron_age')
        target3.value = iron.pk
        target3.is_set = True
        target3.associated_import = imp
        target3.save()
        return [target, target2, target3]

    def init_ope(self):
        importer, form = self.init_ope_import()
        impt = form.save(self.ishtar_user)
        impt.initialize()
        self.init_ope_targetkey(imp=impt)
        impt.importation()

    def init_parcel_import(self):
        self.init_ope()
        mcc_parcel = ImporterType.objects.get(name=u"MCC - Parcelles")
        mcc_file = open(
            settings.ROOT_PATH +
            '../archaeological_operations/tests/MCC-parcelles-example.csv',
            'rb')
        file_dict = {'imported_file': SimpleUploadedFile(mcc_file.name,
                                                         mcc_file.read())}
        post_dict = {'importer_type': mcc_parcel.pk, 'skip_lines': 1,
                     "encoding": 'utf-8'}
        form = forms_common.NewImportForm(data=post_dict, files=file_dict)
        form.is_valid()
        return mcc_parcel, form

    def init_parcel(self):
        importer, form = self.init_parcel_import()
        impt = form.save(self.ishtar_user)
        impt.initialize()
        impt.importation()

    def init_context_record_import(self):
        self.init_parcel()
        mcc = ImporterType.objects.get(name=u"MCC - UE")
        mcc_file = open(
            settings.ROOT_PATH +
            '../archaeological_context_records/tests/'
            'MCC-context-records-example.csv', 'rb')
        file_dict = {'imported_file': SimpleUploadedFile(mcc_file.name,
                                                         mcc_file.read())}
        post_dict = {'importer_type': mcc.pk, 'skip_lines': 1,
                     "encoding": 'utf-8'}
        form = forms_common.NewImportForm(data=post_dict, files=file_dict)
        form.is_valid()
        return mcc, form

    def init_cr_targetkey(self, imp):
        hc = Unit.objects.get(txt_idx='not_in_context').pk
        self.set_target_key('unit', 'hc', hc, imp=imp)
        self.set_target_key('unit', 'hors-contexte', hc, imp=imp)
        layer = Unit.objects.get(txt_idx='negative').pk
        self.set_target_key('unit', 'couche', layer, imp=imp)

    def init_context_record(self):
        mcc, form = self.init_context_record_import()
        impt = form.save(self.ishtar_user)
        impt.initialize()
        self.init_cr_targetkey(impt)
        impt.importation()


class ImportOperationTest(ImportTest, TestCase):
    fixtures = OPERATION_TOWNS_FIXTURES

    def test_mcc_import_operation(self):
        first_ope_nb = models.Operation.objects.count()
        first_person_nb = Person.objects.count()
        importer, form = self.init_ope_import()
        self.assertTrue(form.is_valid())
        impt = form.save(self.ishtar_user)
        target_key_nb = TargetKey.objects.count()
        impt.initialize()
        # new key have to be set
        self.assertTrue(TargetKey.objects.count() > target_key_nb)

        # first try to import
        impt.importation()
        current_ope_nb = models.Operation.objects.count()
        # no new operation imported because of a missing connection for
        # operation_type value
        self.assertEqual(current_ope_nb, first_ope_nb)
        self.init_ope_targetkey(imp=impt)

        impt.importation()
        # new operations have now been imported
        current_ope_nb = models.Operation.objects.count()
        self.assertEqual(current_ope_nb, first_ope_nb + 2)
        current_person_nb = Person.objects.count()
        self.assertEqual(current_person_nb, first_person_nb + 1)
        # and well imported
        last_ope = models.Operation.objects.order_by('-pk').all()[0]
        self.assertEqual(last_ope.name, u"Oppìdum de Paris")
        self.assertEqual(last_ope.code_patriarche, '4200')
        self.assertEqual(last_ope.operation_type.txt_idx, 'prog_excavation')
        self.assertEqual(last_ope.periods.count(), 2)
        periods = [period.txt_idx for period in last_ope.periods.all()]
        self.assertIn('iron_age', periods)
        self.assertIn('gallo-roman', periods)

        # a second importation will be not possible: no two same patriarche
        # code
        impt.importation()
        self.assertEqual(last_ope,
                         models.Operation.objects.order_by('-pk').all()[0])

    def test_import_bad_encoding(self):
        self.init_ope_import('MCC-operations-example-bad-encoding.csv')

    def test_keys_limitation(self):
        # each key association is associated to the import
        init_ope_number = models.Operation.objects.count()
        importer, form = self.init_ope_import()
        impt = form.save(self.ishtar_user)
        impt.initialize()
        self.init_ope_targetkey(imp=impt)

        importer, form = self.init_ope_import()
        other_imp = form.save(self.ishtar_user)
        # associate with another import
        for ik in ItemKey.objects.filter(importer=impt).all():
            ik.importer = other_imp
            ik.save()

        impt.importation()
        current_ope_nb = models.Operation.objects.count()
        # no new operation
        self.assertEqual(current_ope_nb, init_ope_number)

    def test_bad_configuration(self):
        importer, form = self.init_ope_import()
        col = ImporterColumn.objects.get(importer_type=importer, col_number=1)
        target = col.targets.all()[0]
        target.target = "cody"  # random and not appropriate string
        target.save()
        # self.init_ope()
        # importer, form = self.init_ope_import()
        impt = form.save(self.ishtar_user)
        impt.initialize()
        self.init_ope_targetkey(imp=impt)
        impt.importation()
        self.assertEqual(len(impt.errors), 2)
        self.assertTrue(
            "Importer configuration error" in impt.errors[0]['error'] or
            "Erreur de configuration de l\'importeur" in impt.errors[0]['error']
        )

    def test_model_limitation(self):
        importer, form = self.init_ope_import()
        importer.created_models.clear()
        impt = form.save(self.ishtar_user)
        impt.initialize()
        self.init_ope_targetkey(imp=impt)

        # no model defined in created_models: normal import
        init_ope_number = models.Operation.objects.count()
        impt.importation()
        current_ope_nb = models.Operation.objects.count()
        self.assertEqual(current_ope_nb, init_ope_number + 2)

        for ope in models.Operation.objects.order_by('-pk').all()[:2]:
            ope.delete()

        importer, form = self.init_ope_import()
        # add an inadequate model to make created_models non empty
        importer.created_models.clear()
        importer.created_models.add(ImporterModel.objects.get(
            klass='ishtar_common.models.Organization'
        ))
        impt = form.save(self.ishtar_user)
        impt.initialize()
        self.init_ope_targetkey(imp=impt)

        # no imports
        impt.importation()
        current_ope_nb = models.Operation.objects.count()
        self.assertEqual(current_ope_nb, init_ope_number)

        importer, form = self.init_ope_import()
        # add operation model to allow creation
        importer.created_models.clear()
        importer.created_models.add(ImporterModel.objects.get(
            klass='archaeological_operations.models.Operation'
        ))
        impt = form.save(self.ishtar_user)
        impt.initialize()
        self.init_ope_targetkey(imp=impt)

        # import of operations
        impt.importation()
        current_ope_nb = models.Operation.objects.count()
        self.assertEqual(current_ope_nb, init_ope_number + 2)

    def test_mcc_import_parcels(self):
        old_nb = models.Parcel.objects.count()
        mcc_parcel, form = self.init_parcel_import()
        impt = form.save(self.ishtar_user)
        impt.initialize()
        impt.importation()
        # new parcels has now been imported
        current_nb = models.Parcel.objects.count()
        self.assertEqual(current_nb, old_nb + 3)

        # and well imported
        last_parcels = models.Parcel.objects.order_by('-pk').all()[0:3]
        external_ids = sorted(['4200-59350-YY55', '4200-75101-XXXX',
                               '4201-59350-YY55'])
        parcel_numbers = sorted(['42', '55', '55'])
        sections = sorted(['ZX', 'YY', 'YY'])
        self.assertEqual(external_ids,
                         sorted([p.external_id for p in last_parcels]))
        self.assertEqual(parcel_numbers,
                         sorted([p.parcel_number for p in last_parcels]))
        self.assertEqual(sections,
                         sorted([p.section for p in last_parcels]))
        ope1 = models.Operation.objects.filter(code_patriarche='4200').all()[0]
        towns_ope = ope1.towns.all()
        imported = [imp for acc, imp in impt.get_all_imported()]
        for p in last_parcels:
            self.assertTrue(p.town in towns_ope)
            self.assertTrue(p in imported)
        self.assertEqual(len(imported), len(last_parcels))
        self.assertEqual(
            models.Parcel.objects.get(
                parcel_number='55', section='YY',
                operation_id=ope1.pk).external_id,
            '4200-59350-YY55')
        # cached_label update
        ope2 = models.Operation.objects.filter(code_patriarche='4201').all()[0]
        self.assertIn('LILLE', ope2.cached_label.upper())
        # delete associated parcel with the import deletion
        parcel_count = models.Parcel.objects.count()
        impt.delete()
        self.assertEqual(parcel_count - 3, models.Parcel.objects.count())


class ParcelTest(ImportTest, TestCase):
    fixtures = OPERATION_TOWNS_FIXTURES

    def test_parse_parcels(self):
        # the database needs to be initialised before importing
        from archaeological_operations.import_from_csv import parse_parcels
        # default_town = Town.objects.create(numero_insee="12345",
        #                                    name="default_town")
        test_values = (
            (u"1996 : XT:53,54,56,57,59,60,61,62",
             {1996: [
                 ("XT", "53"), ("XT", "54"), ("XT", "56"), ("XT", "57"),
                 ("XT", "59"), ("XT", "60"), ("XT", "61"), ("XT", "62"),
             ]}
             ),
            (u"AD:23",
             {None: [
                 ("AD", "23")
             ]}),
            (u"1961 :B1:227;",
             {1961: [
                 ("B1", '227')
             ]}),
            (u"1982 CV:35;CV:36",
             {1982: [
                 ("CV", "35"), ("CV", "36"),
             ]}),
            (u"E:24;E:25",
             {None: [
                 ("E", "24"), ("E", "25"),
             ]}),
            (u"B : 375, 376, 386, 387, 645, 646 / C : 412 à 415, 432 à 435, "
             u"622 / F : 120, 149, 150, 284, 287, 321 à 323",
             {None: [
                 ("B", "375"), ("B", "376"), ("B", "386"), ("B", "387"),
                 ("B", "645"), ("B", "646"),
                 ("C", "412"), ("C", "413"), ("C", "414"), ("C", "415"),
                 ("C", "432"), ("C", "433"), ("C", "434"), ("C", "435"),
                 ("C", "622"),
                 ("F", "120"), ("F", "149"), ("F", "150"), ("F", "284"),
                 ("F", "287"), ("F", "321"), ("F", "322"), ("F", "323"),
             ]}),
            (u"AD : 95, 96, 86, 87, 81, 252, AE : 58, AD : 115 à 132",
             {None: [
                 ("AD", "95"), ("AD", "96"), ("AD", "86"), ("AD", "87"),
                 ("AD", "81"), ("AD", "252"), ("AD", "115"), ("AD", "116"),
                 ("AD", "117"), ("AD", "118"), ("AD", "119"), ("AD", "120"),
                 ("AD", "121"), ("AD", "122"), ("AD", "123"), ("AD", "124"),
                 ("AD", "125"), ("AD", "126"), ("AD", "127"), ("AD", "128"),
                 ("AD", "129"), ("AD", "130"), ("AD", "131"), ("AD", "132"),
                 ("AE", "58"),
             ]}),
            (u"XD:1 à 13, 24 à 28, 33 à 39, 50 à 52, 80, 83, 84 à 86, 259 à "
             u"261, 182, 225 ; XH:5 ; P:1640, 1888, 1889, 1890 ; R:1311, "
             u"1312, 1314,1342, 1343, 1559 à 1569",
             {None: [
                 ('XD', "1"), ('XD', "2"), ('XD', "3"), ('XD', "4"),
                 ('XD', "5"), ('XD', "6"), ('XD', "7"), ('XD', "8"),
                 ('XD', "9"), ('XD', "10"), ('XD', "11"), ('XD', "12"),
                 ('XD', "13"), ("XD", "24"), ("XD", "25"), ("XD", "26"),
                 ("XD", "27"), ("XD", "28"), ("XD", "33"), ("XD", "34"),
                 ("XD", "35"), ("XD", "36"), ("XD", "37"), ("XD", "38"),
                 ("XD", "39"), ("XD", "50"), ("XD", "51"), ("XD", "52"),
                 ("XD", "80"), ("XD", "83"), ("XD", "84"), ("XD", "85"),
                 ("XD", "86"), ("XD", "259"), ("XD", "260"), ("XD", "261"),
                 ("XD", "182"), ("XD", "225"), ("XH", "5"),
                 ("P", "1640"), ("P", "1888"), ("P", "1889"), ("P", "1890"),
                 ("R", "1311"), ("R", "1312"), ("R", "1314"), ("R", "1342"),
                 ("R", "1343"), ("R", "1559"), ("R", "1560"), ("R", "1561"),
                 ("R", "1562"), ("R", "1563"), ("R", "1564"), ("R", "1565"),
                 ("R", "1566"), ("R", "1567"), ("R", "1568"), ("R", "1569"),
             ]}),
            (u"BZ:2 à 5, 365 ; CD:88 à 104, 106, 108, 326",
             {None: [
                 ('BZ', '2'), ('BZ', '3'), ('BZ', '4'), ('BZ', '5'),
                 ('BZ', '365'), ('CD', '88'), ('CD', '89'), ('CD', '90'),
                 ('CD', '91'), ('CD', '92'), ('CD', '93'), ('CD', '94'),
                 ('CD', '95'), ('CD', '96'), ('CD', '97'), ('CD', '98'),
                 ('CD', '99'), ('CD', '100'), ('CD', '101'), ('CD', '102'),
                 ('CD', '103'), ('CD', '104'), ('CD', '106'), ('CD', '326'),
                 ('CD', '108')
             ]}),
            (u"AV 118 à 125, 127, 132 à 137, 153, 398p, 399, 402; BI 27, 30, "
             u"32, 33, 188, 255, 256 à 258, 260, 284p, 294; BL 297",
             {None: [
                 ('AV', '118'), ('AV', '119'), ('AV', '120'), ('AV', '121'),
                 ('AV', '122'), ('AV', '123'), ('AV', '124'), ('AV', '125'),
                 ('AV', '127'), ('AV', '132'), ('AV', '133'), ('AV', '134'),
                 ('AV', '135'), ('AV', '136'), ('AV', '137'), ('AV', '153'),
                 ('AV', '398p'), ('AV', '399'), ('AV', '402'),
                 ('BI', '27'), ('BI', '30'), ('BI', '32'), ('BI', '33'),
                 ('BI', '188'), ('BI', '255'), ('BI', '256'), ('BI', '257'),
                 ('BI', '258'), ('BI', '260'), ('BI', '284p'), ('BI', '294'),
                 ('BL', '297'),
             ]}),
            (u"A : 904 à 906, 911 ; E:40, 41",
             {None: [
                 ("A", '904'), ("A", '905'), ("A", '906'), ("A", '911'),
                 ("E", '40'), ("E", "41")
             ]}),
            (u"1991 : BE:8, 12",
             {"1991": [
                 ('BE', '8'), ('BE', '12'),
             ]}),
            (u"1979 : EM:1",
             {"1979": [
                 ('EM', '1')
             ]},),
            (u"B:448;B:449;B:450;B:451;B:452;B:455;B:456;B:457;B:458;B:459;"
             u"B:1486;",
             {None: [
                 ("B", "448"), ("B", "449"), ("B", "450"), ("B", "451"),
                 ("B", "452"), ("B", "455"), ("B", "456"), ("B", "457"),
                 ("B", "458"), ("B", "459"), ("B", "1486"),
             ]}),
            (u"AC : 72 à 81, 91 à 100, 197 / ZC:180 à 189",
             {None: [
                 ('AC', '72'), ('AC', '73'), ('AC', '74'), ('AC', '75'),
                 ('AC', '76'), ('AC', '77'), ('AC', '78'), ('AC', '79'),
                 ('AC', '80'), ('AC', '81'), ('AC', '91'), ('AC', '92'),
                 ('AC', '93'), ('AC', '94'), ('AC', '95'), ('AC', '96'),
                 ('AC', '97'), ('AC', '98'), ('AC', '99'), ('AC', '100'),
                 ('AC', '197'), ('ZC', '180'), ('ZC', '181'), ('ZC', '182'),
                 ('ZC', '183'), ('ZC', '184'), ('ZC', '185'), ('ZC', '186'),
                 ('ZC', '187'), ('ZC', '188'), ('ZC', '189'),
             ]}),
            (u"AB 37 et 308",
             {None: [
                 ('AB', '37'), ('AB', '308'),
             ]}),
            (u"1983  D2 n° 458 et 459",
             {"1983": [
                 ('D2', '458'), ('D2', '459'),
             ]}),
            (u"ZS : 21p, 66",
             {None: [
              ('ZS', '21p'), ('ZS', '66'),
              ]}),
            (u"VV:166, 167, domaine public",
             {None: [
                 ('VV', '166'), ('VV', '167'),
             ]}),
            (u" AS:13 à 15, 17 à 19, 21 à 32, 34 à 45, 47 à 53, 69, 70, 82, "
             u"84 / CK:1, 24, 25, 29, 30, 37 à 43",
             {None: [
              ("AS", "13"), ("AS", "14"), ("AS", "15"), ("AS", "17"),
              ("AS", "18"), ("AS", "19"), ("AS", "21"), ("AS", "22"),
              ("AS", "23"), ("AS", "24"), ("AS", "25"), ("AS", "26"),
              ("AS", "27"), ("AS", "28"), ("AS", "29"), ("AS", "30"),
              ("AS", "31"), ("AS", "32"), ("AS", "34"), ("AS", "35"),
              ("AS", "36"), ("AS", "37"), ("AS", "38"), ("AS", "39"),
              ("AS", "40"), ("AS", "41"), ("AS", "42"), ("AS", "43"),
              ("AS", "44"), ("AS", "45"), ("AS", "47"), ("AS", "48"),
              ("AS", "49"), ("AS", "50"), ("AS", "51"), ("AS", "52"),
              ("AS", "53"), ('AS', "69"), ('AS', "70"), ('AS', "82"),
              ('AS', "84"), ('CK', "1"), ('CK', "24"), ('CK', "25"),
              ('CK', "29"), ('CK', "30"), ('CK', "37"), ('CK', "38"),
              ('CK', "39"), ('CK', "40"), ('CK', "41"), ('CK', "42"),
              ('CK', "43"), ]}),
            (u" ZN:37, 15, 35, 28, 29 / ZM:9, 73",
             {None: [
                 ("ZN", "37"), ("ZN", "15"), ("ZN", "35"), ("ZN", "28"),
                 ("ZN", "29"), ("ZM", "9"), ("ZM", "73"),
             ]}),
            (u" Tranche n°1 : YP:243, 12, 14 à 16, 18 à 26, DP / Tranche n°2 :"
             u"YP:17, 307, 27, 308, 44 à 46, 683, BM:1, 250, 488 à 492",
             {None: [
                 ('YP', '243'), ('YP', '12'), ('YP', '14'), ('YP', '15'),
                 ('YP', '16'), ('YP', '18'), ('YP', '19'), ('YP', '20'),
                 ('YP', '21'), ('YP', '22'), ('YP', '23'), ('YP', '24'),
                 ('YP', '25'), ('YP', '26'), ('YP', '17'), ('YP', '27'),
                 ('YP', '308'), ('YP', '44'), ('YP', '45'), ('YP', '46'),
                 ('YP', '683'), ('YP', '307'), ('BM', '1'), ('BM', '250'),
                 ('BM', '488'), ('BM', '489'), ('BM', '490'), ('BM', '491'),
                 ('BM', '492'),
             ]}),
            (u" H : 106, 156, 158",
             {None: [
                 ('H', '106'), ('H', '156'), ('H', '158'),
             ]}),
            (u"Section YO : parcelles n° 19; 20",
             {None: [
                 ('YO', '19'), ('YO', '20'),
             ]}),
            (u"1991 :AI:23;19;20;21;22;181;AM:116;214;215;233;235",
             {u"1991": [
                 (u"AI", "19"), (u"AI", "20"), (u"AI", "21"), (u"AI", "22"),
                 (u"AI", "23"), (u"AI", "181"),
                 (u"AM", "116"), (u"AM", "214"), (u"AM", "215"),
                 (u"AM", "233"), (u"AM", "235"),
             ]})
        )
        # ),(u"Domaine public", {}
        # ),(u"Tranche 1 : AV:4 à 6, 18, 80, 104 / partiellement : 5 et 18", {}
        # ),(u" 1987 : ZD: ?", {}
        # ),(u"A:26a, 26b, 27 / AB:95 / AK:4, 12, 20", {}
        for value, result in test_values:
            parcels = parse_parcels(value)
            if not parcels and not result:
                continue
            self.assertTrue(parcels != [],
                            msg="No parcel parsed for \"%s\"" % value)
            parcels_copy = parcels[:]
            for year in result.keys():
                for values in parcels_copy:
                    if values['year'] != year and \
                       values['year'] != unicode(year):
                        continue
                    self.assertTrue(
                        (values['section'], values['parcel_number'])
                        in result[year],
                        msg="Section - Parcel number: \"%s - %s\" is not "
                        "in \"%s\"" % (
                            values['section'], values['parcel_number'],
                            unicode(result[year])))
                    parcels.pop(parcels.index(values))
                    result[year].pop(result[year].index(
                        (values['section'], values['parcel_number'])))
            # all parcels have been imported
            self.assertEqual(parcels, [], msg="Parcel(s): \"%s\" haven't be "
                             "recognized in \"%s\"" % (str(parcels), value))
            not_imported = [data for data in result.values() if data]
            self.assertEqual(
                not_imported, [], msg="Parcel(s): \"%s\" haven't be "
                "recognized in \"%s\"" % (str(not_imported), value))


def create_orga(user):
    orga_type, created = OrganizationType.objects.get_or_create(
        txt_idx='operator')
    orga, created = Organization.objects.get_or_create(
        name='Operator', organization_type=orga_type, history_modifier=user)
    return orga


def create_operation(user, orga=None, values={}):
    dct = {'year': 2010, 'operation_type_id': 1,
           'history_modifier': user}
    dct.update(values)
    if orga:
        dct['operator'] = orga
    operation = models.Operation.objects.create(**dct)
    return operation


class OperationInitTest(object):
    def create_user(self):
        username, password, self.user = create_user()

    def get_default_user(self):
        if not hasattr(self, 'user') or not self.user:
            self.create_user()
        return self.user

    def create_orgas(self, user=None):
        if not user:
            user = self.get_default_user()
        self.orgas = [create_orga(user)]
        return self.orgas

    def get_default_orga(self, user=None):
        if not hasattr(self, 'orgas') or not self.orgas:
            self.create_orgas(user)
        return self.orgas[0]

    def create_towns(self, datas={}):
        default = {'numero_insee': '12345', 'name': 'default_town'}
        default.update(datas)
        town = models.Town.objects.create(**default)
        if not hasattr(self, 'towns') or not self.towns:
            self.towns = []
        self.towns.append(town)
        return self.towns

    def get_default_town(self):
        towns = getattr(self, 'towns', None)
        if not towns:
            self.create_towns()
        return self.towns[0]

    def create_parcel(self, data={}):
        default = {'town': self.get_default_town(),
                   'section': 'A', 'parcel_number': '1'}
        if not hasattr(self, 'operations'):
            self.create_operation()
        default['operation'] = self.operations[0]
        default.update(data)
        if not getattr(self, 'parcels', None):
            self.parcels = []
        self.parcels.append(models.Parcel.objects.create(**default))
        return self.parcels

    def get_default_parcel(self, force=False):
        if force:
            return self.create_parcel()[-1]
        parcel = self.create_parcel()[0]
        if models.Parcel.objects.filter(pk=parcel.pk).count():
            return parcel
        self.parcels.pop(0)
        return self.create_operation()[-1]

    def create_operation(self, user=None, orga=None):
        if not orga:
            self.get_default_orga(user)
        if not user:
            self.get_default_user()
        if not getattr(self, 'operations', None):
            self.operations = []
        self.operations.append(create_operation(user, orga))
        return self.operations

    def get_default_operation(self, force=False):
        if force:
            return self.create_operation()[-1]
        ope = self.create_operation()[0]
        if models.Operation.objects.filter(pk=ope.pk).count():
            return ope
        self.operations.pop(0)
        return self.create_operation()[-1]

    def tearDown(self):
        # cleanup for further test
        if hasattr(self, 'user'):
            self.user.delete()
            self.user = None
        # all try/except is necessary for bad migrations on master...
        # should be removed at the next big version
        if hasattr(self, 'operations'):
            for ope in self.operations:
                try:
                    ope.delete()
                except:
                    pass
            self.operations = []
        if hasattr(self, 'parcels'):
            for p in self.parcels:
                try:
                    p.delete()
                except:
                    pass
            self.parcels = []


class OperationTest(TestCase, OperationInitTest):
    fixtures = FILE_FIXTURES

    def setUp(self):
        IshtarSiteProfile.objects.get_or_create(
            slug='default', active=True)
        self.username, self.password, self.user = create_superuser()
        self.alt_username, self.alt_password, self.alt_user = create_user()
        self.alt_user.user_permissions.add(Permission.objects.get(
            codename='view_own_operation'))
        self.orgas = self.create_orgas(self.user)
        self.operations = self.create_operation(self.user, self.orgas[0])
        self.operations += self.create_operation(self.alt_user, self.orgas[0])
        self.item = self.operations[0]

    def testExternalID(self):
        self.item.code_patriarche = '123456789'
        self.item.save()
        parcel = self.get_default_parcel()
        parcel.operation = self.item
        parcel.save()
        correct_ext_id = u"{}-{}-{}{}".format(
            self.item.code_patriarche, parcel.town.numero_insee,
            parcel.section, parcel.parcel_number)
        self.assertEqual(parcel.external_id, correct_ext_id)
        # auto has been previously set
        parcel.external_id = 'blabla'
        parcel.save()
        self.assertEqual(parcel.external_id, correct_ext_id)
        # deactivate auto
        parcel.auto_external_id = False
        parcel.external_id = 'blabla'
        parcel.save()
        self.assertEqual(parcel.external_id, 'blabla')

    def create_relations(self):
        rel1 = models.RelationType.objects.create(
            symmetrical=True, label='Include', txt_idx='include')
        rel2 = models.RelationType.objects.create(
            symmetrical=False, label='Included', txt_idx='included',
            inverse_relation=rel1)
        models.RecordRelations.objects.create(
            left_record=self.operations[0],
            right_record=self.operations[1],
            relation_type=rel1)
        return rel1, rel2

    def testPostDeleteRelations(self):
        self.create_relations()
        self.operations[0].delete()

    def testPostDeleteParcels(self):
        ope = self.operations[0]
        town = Town.objects.create(name='plouf', numero_insee='20000')
        parcel = models.Parcel.objects.create(town=town)
        parcel_nb = models.Parcel.objects.count()
        ope.parcels.add(parcel)
        ope.delete()
        # our parcel has no operation attached and should be deleted
        self.assertEqual(parcel_nb - 1, models.Parcel.objects.count())
        ope = self.operations[1]
        parcel = models.Parcel.objects.create(town=town)
        parcel_nb = models.Parcel.objects.count()
        ope.parcels.add(parcel)
        ope.parcels.clear()  # no signal raised... should resave
        models.Parcel.objects.filter(pk=parcel.pk).all()[0].save()
        # our parcel has no operation attached and should be deleted
        self.assertEqual(parcel_nb - 1, models.Parcel.objects.count())

    def testIndex(self):
        ope = create_operation(self.user, values={'year': 2042})
        self.assertEqual(ope.operation_code, 1)
        ope2 = create_operation(self.user, values={'year': 2042})
        self.assertEqual(ope2.operation_code, 2)
        ope = create_operation(self.user, values={'year': 0})
        self.assertEqual(ope.operation_code, 1)
        ope2 = create_operation(self.user, values={'year': 0})
        self.assertEqual(ope2.operation_code, 2)

    def test_cache_update(self):
        self.create_towns()
        operation = self.operations[0]
        town, ope_id = operation.cached_label.split(' | ')
        self.assertIn(town, (u'Intercommunal', u"Multi-town"))
        self.assertEqual(ope_id, 'OP2010-1')
        operation = models.Operation.objects.get(pk=operation.pk)
        operation.year = 2011
        operation.save()
        operation.towns.add(self.towns[0])
        operation = models.Operation.objects.get(pk=operation.pk)
        town, ope_id = operation.cached_label.split(' | ')
        self.assertEqual(ope_id, 'OP2011-1')
        self.assertEqual(town, self.towns[0].name)

    def test_cache_bulk_update(self):
        if settings.USE_SPATIALITE_FOR_TESTS:
            # using views - can only be tested with postgresql
            return

        operation = self.operations[0]
        init_parcel = self.create_parcel()[0]
        operation.parcels.add(init_parcel)

        from archaeological_context_records.models import ContextRecord
        cr_data = {'label': "Context record", "operation": operation,
                   'parcel': init_parcel,
                   'history_modifier': self.get_default_user()}
        cr = ContextRecord.objects.create(**cr_data)

        from archaeological_finds.models import BaseFind, Find, MaterialType
        bf_data = {
            'label': "Base find", 'history_modifier': self.get_default_user(),
            'context_record': cr
        }
        base_find = BaseFind.objects.create(**bf_data)
        find = Find.objects.create(
            history_modifier=self.get_default_user(),
            label='Find me'
        )
        find.base_finds.add(base_find)
        mat = MaterialType.objects.create(
            label='Adamentium', txt_idx='admentium', code='ADA')
        find.material_types.add(mat)

        class TestObj(object):
            def __init__(self):
                self.context_record_reached = []

            def reached(self, sender, **kwargs):
                instance = kwargs.get('instance')
                if sender == ContextRecord:
                    self.context_record_reached.append(instance)

        test_obj = TestObj()
        operation = models.Operation.objects.get(pk=operation.pk)
        operation.test_obj = test_obj
        operation.year = 2011
        operation.save()
        # bulk update of context records cached label gen don't have to be
        # reached
        self.assertEqual(len(test_obj.context_record_reached), 0)

        # verify the relevance of the update
        cr = ContextRecord.objects.get(pk=cr.pk)
        ope_id, parcel_sec, parcel_nb, cr_label = cr.cached_label.split(' | ')
        self.assertEqual(ope_id, '{}2011-1'.format(
            settings.ISHTAR_DEF_OPE_PREFIX))

        base_find = BaseFind.objects.get(pk=base_find.pk)
        op_code, idx = base_find.cache_short_id.split(' | ')
        self.assertEqual(op_code, 'OP2011-1')
        self.assertEqual(idx, '00001')
        op_code, mat_code, lbl, idx = base_find.cache_complete_id.split(' | ')
        self.assertEqual(op_code, 'OP2011-1')
        self.assertEqual(mat_code, 'ADA')
        self.assertEqual(lbl, 'Context record')
        self.assertEqual(idx, '00001')

        find = Find.objects.get(pk=find.pk)
        op_code_idx, lbl = find.cached_label.split(' | ')
        self.assertEqual(op_code_idx, 'OP2011-1-00001')
        self.assertEqual(lbl, 'Find me')

        operation = models.Operation.objects.get(pk=operation.pk)
        operation.code_patriarche = '666'
        operation.save()
        cr = ContextRecord.objects.get(pk=cr.pk)
        ope_id, parcel_sec, parcel_nb, cr_label = cr.cached_label.split(' | ')
        self.assertEqual(ope_id, '{}666'.format(settings.ISHTAR_OPE_PREFIX))

        base_find = BaseFind.objects.get(pk=base_find.pk)
        op_code, idx = base_find.cache_short_id.split(' | ')
        self.assertEqual(op_code, 'OA666')
        op_code, mat_code, lbl, idx = base_find.cache_complete_id.split(' | ')
        self.assertEqual(op_code, 'OA666')

        find = Find.objects.get(pk=find.pk)
        op_code_idx, lbl = find.cached_label.split(' | ')
        self.assertEqual(op_code_idx, 'OA666-00001')

    def test_show(self):
        operation = self.operations[0]
        c = Client()
        response = c.get(reverse('show-operation', kwargs={'pk': operation.pk}))
        self.assertEqual(response.status_code, 200)
        # empty content when not allowed
        self.assertEqual(response.content, "")

        c.login(username=self.username, password=self.password)
        response = c.get(reverse('show-operation', kwargs={'pk': operation.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="sheet"', response.content)


class OperationSearchTest(TestCase, OperationInitTest):
    fixtures = FILE_FIXTURES

    def setUp(self):
        IshtarSiteProfile.objects.get_or_create(
            slug='default', active=True)
        self.username, self.password, self.user = create_superuser()
        self.alt_username, self.alt_password, self.alt_user = create_user()
        self.alt_user.user_permissions.add(Permission.objects.get(
            codename='view_own_operation'))
        self.orgas = self.create_orgas(self.user)
        self.operations = self.create_operation(self.user, self.orgas[0])
        self.operations += self.create_operation(self.alt_user, self.orgas[0])
        self.item = self.operations[0]

    def test_base_search(self):
        c = Client()
        response = c.get(reverse('get-operation'), {'year': '2010'})
        # no result when no authentication
        self.assertTrue(not json.loads(response.content))
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('get-operation'), {'year': '2010'})
        self.assertEqual(json.loads(response.content)['total'], 2)
        response = c.get(reverse('get-operation'),
                         {'operator': self.orgas[0].pk})
        result = json.loads(response.content)
        self.assertEqual(result['total'], 2)

    def create_relations(self):
        rel1 = models.RelationType.objects.create(
            symmetrical=True, label='Include', txt_idx='include')
        rel2 = models.RelationType.objects.create(
            symmetrical=False, label='Included', txt_idx='included',
            inverse_relation=rel1)
        models.RecordRelations.objects.create(
            left_record=self.operations[0],
            right_record=self.operations[1],
            relation_type=rel1)
        return rel1, rel2

    def testRelatedSearch(self):
        c = Client()
        rel1, rel2 = self.create_relations()
        self.operations[1].year = 2011
        self.operations[1].save()
        search = {'year': '2010', 'relation_types_0': rel2.pk}
        response = c.get(reverse('get-operation'), search)
        # no result when no authentification
        self.assertTrue(not json.loads(response.content))
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('get-operation'), search)
        self.assertTrue(json.loads(response.content)['total'] == 2)

    def testHierarchicSearch(self):
        ope = self.operations[1]
        c = Client()

        neo = models.Period.objects.get(txt_idx='neolithic')
        final_neo = models.Period.objects.get(txt_idx='final_neolithic')
        recent_neo = models.Period.objects.get(txt_idx='recent_neolithic')
        ope.periods.add(final_neo)

        search = {'periods': final_neo.pk}

        # no result when no authentication
        response = c.get(reverse('get-operation'), search)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not json.loads(response.content))
        c.login(username=self.username, password=self.password)

        # one result for exact search
        response = c.get(reverse('get-operation'), search)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertTrue(res['total'] == 1)

        # no result for the brother
        search = {'periods': recent_neo.pk}
        response = c.get(reverse('get-operation'), search)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['total'], 0)

        # one result for the father
        search = {'periods': neo.pk}
        response = c.get(reverse('get-operation'), search)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['total'], 1)

    def testOwnSearch(self):
        c = Client()
        response = c.get(reverse('get-operation'), {'year': '2010'})
        # no result when no authentification
        self.assertTrue(not json.loads(response.content))
        c.login(username=self.alt_username, password=self.alt_password)
        response = c.get(reverse('get-operation'), {'year': '2010'})
        # only one "own" operation available
        self.assertTrue(json.loads(response.content)['total'] == 1)
        response = c.get(reverse('get-operation'),
                         {'operator': self.orgas[0].pk})
        self.assertTrue(json.loads(response.content)['total'] == 1)


def create_administrativact(user, operation):
    act_type, created = models.ActType.objects.get_or_create(
        txt_idx='act_type')
    dct = {'history_modifier': user,
           'act_type': act_type,
           'operation': operation,
           'signature_date': datetime.date(2014, 05, 12),
           'index': 322}
    adminact, created = models.AdministrativeAct.objects.get_or_create(**dct)
    return [act_type], [adminact]


class RegisterTest(TestCase, OperationInitTest):
    fixtures = FILE_FIXTURES

    def setUp(self):
        self.username, self.password, self.user = create_superuser()
        self.operations = self.create_operation(self.user)
        self.act_types, self.operations = create_administrativact(
            self.user, self.operations[0])

    def testSearch(self):
        c = Client()
        response = c.get(reverse('get-administrativeact'), {'year': '2014'})
        # no result when no authentication
        self.assertTrue(not json.loads(response.content))
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('get-administrativeact'), {'year': '2014'})
        self.assertTrue(json.loads(response.content)['total'] == 1)
        response = c.get(reverse('get-administrativeact'), {'indexed': '2'})
        self.assertTrue(json.loads(response.content)['total'] == 1)


class OperationWizardCreationTest(WizardTest, OperationInitTest, TestCase):
    fixtures = FILE_FIXTURES
    url_name = 'operation_creation'
    wizard_name = 'operation_wizard'
    steps = views.wizard_steps
    form_datas = [
        FormData(
            "Create a preventive diag",
            form_datas={
                'filechoice-operation_creation': {},
                'general-operation_creation': {
                    'operation_type': 1,  # preventive diag
                    'year': 2016},
                'townsgeneral-operation_creation': [],
                'parcelsgeneral-operation_creation': [],
            },
            ignored=('towns-operation_creation',
                     'parcels-operation_creation',
                     'preventive-operation_creation',)
        ),
        FormData(
            "Create another preventive diag with same parcel name",
            form_datas={
                'filechoice-operation_creation': {},
                'general-operation_creation': {
                    'operation_type': 1,  # preventive diag
                    'year': 2016},
                'townsgeneral-operation_creation': [],
                'parcelsgeneral-operation_creation': [],
            },
            ignored=('towns-operation_creation',
                     'parcels-operation_creation',
                     'preventive-operation_creation',)
        )
    ]

    def pre_wizard(self):
        profile, created = IshtarSiteProfile.objects.get_or_create(
            slug='default', active=True)
        profile.files = True
        profile.save()

        if 'townsgeneral-operation_creation' not in \
                self.form_datas[0].form_datas:
            return super(OperationWizardCreationTest, self).pre_wizard()
        town = self.create_towns()[0]
        town_data = {'town': town.pk}
        self.form_datas[0].form_datas[
            'townsgeneral-operation_creation'].append(town_data)
        self.form_datas[1].form_datas[
            'townsgeneral-operation_creation'].append(town_data)
        parcel_data = {
            'town': town.pk, 'year': 2017, 'section': 'S',
            'parcel_number': '42'}
        self.form_datas[0].form_datas[
            'parcelsgeneral-operation_creation'].append(parcel_data)
        self.form_datas[1].form_datas[
            'parcelsgeneral-operation_creation'].append(parcel_data)
        self.operation_number = models.Operation.objects.count()
        self.parcel_number = models.Parcel.objects.count()
        super(OperationWizardCreationTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.Operation.objects.count(),
                         self.operation_number + 2)
        self.assertEqual(models.Parcel.objects.count(),
                         self.parcel_number + 2)


class OperationWizardModifTest(WizardTest, OperationInitTest, TestCase):
    fixtures = FILE_FIXTURES
    url_name = 'operation_modification'
    wizard_name = url_name + '_wizard'
    steps = views.operation_modif_wizard_steps
    base_ignored_steps = (
        'archaeologicalsite-operation_modification',
        'preventive-operation_modification',
        'preventivediag-operation_modification',
        'towns-operation_modification',
        'parcels-operation_modification',
        'remains-operation_modification',
        'periods-operation_modification',
        'relations-operation_modification',
        'abstract-operation_modification',)
    form_datas = [
        FormData(
            "Update an operation",
            form_datas={
                'selec-operation_modification': {},
                'general-operation_modification': {
                    'operation_type': 2,
                    'year': 2017},
                'townsgeneral-operation_modification': [],
                'parcelsgeneral-operation_modification': [],
            },
            ignored=base_ignored_steps
        ),
        FormData(
            "Operation: try to remove a parcel with attached context record",
            form_datas={
                'selec-operation_modification': {},
                'general-operation_modification': {
                    'operation_type': 2,
                    'year': 2017},
                'townsgeneral-operation_modification': [],
                'parcelsgeneral-operation_modification': [],
            },
            ignored=base_ignored_steps
        ),
        FormData(
            "Operation: remove a parcel with no attached context record",
            form_datas={
                'selec-operation_modification': {},
                'general-operation_modification': {
                    'operation_type': 2,
                    'year': 2017},
                'townsgeneral-operation_modification': [],
                'parcelsgeneral-operation_modification': [],
            },
            ignored=base_ignored_steps
        ),
    ]

    def pre_wizard(self):
        self.create_operation()
        operation = self.operations[0]
        init_town = self.create_towns()[0]
        operation.towns.add(init_town)
        init_parcel = self.create_parcel()[0]
        operation.parcels.add(init_parcel)

        from archaeological_context_records.models import ContextRecord
        cr_data = {'label': "Context record", "operation": operation,
                   'parcel': init_parcel,
                   'history_modifier': self.get_default_user()}
        self.cr = ContextRecord.objects.create(**cr_data)

        data = self.form_datas[0].form_datas
        data2 = self.form_datas[1].form_datas
        data3 = self.form_datas[2].form_datas

        data['selec-operation_modification']['pk'] = operation.pk
        data2['selec-operation_modification']['pk'] = operation.pk
        data3['selec-operation_modification']['pk'] = operation.pk

        town = self.create_towns(
            datas={'numero_insee': '67890', 'name': 'Twin Peaks'})[-1]
        towns = [{'town': town.pk}, {'town': init_town.pk}]
        data['townsgeneral-operation_modification'] = towns
        data2['townsgeneral-operation_modification'] = towns
        data3['townsgeneral-operation_modification'] = towns

        parcel_data = {
            'town': town.pk, 'year': 2017, 'section': 'S',
            'parcel_number': '42'}
        data['parcelsgeneral-operation_modification'].append(parcel_data)
        data2['parcelsgeneral-operation_modification'].append(parcel_data)
        data3['parcelsgeneral-operation_modification'].append(parcel_data)

        parcel_data_2 = {
            'town': init_parcel.town.pk, 'year': init_parcel.year or '',
            'section': init_parcel.section,
            'parcel_number': init_parcel.parcel_number}
        data['parcelsgeneral-operation_modification'].append(parcel_data_2)
        # no init parcel for data2 and data3

        self.operation_number = models.Operation.objects.count()
        self.parcel_number = models.Parcel.objects.count()

        def post_first_wizard(test_object, final_step_response):
            test_object.assertEqual(models.Operation.objects.count(),
                                    test_object.operation_number)
            operation = models.Operation.objects.get(
                pk=test_object.operations[0].pk)
            test_object.assertEqual(operation.operation_type.pk, 2)
            test_object.assertEqual(operation.year, 2017)
            test_object.assertEqual(models.Parcel.objects.count(),
                                    test_object.parcel_number + 1)
            test_object.assertEqual(operation.parcels.count(),
                                    test_object.parcel_number + 1)

        def post_second_wizard(test_object, final_step_response):
            test_object.assertEqual(models.Operation.objects.count(),
                                    test_object.operation_number)
            operation = models.Operation.objects.get(
                pk=test_object.operations[0].pk)
            test_object.assertEqual(operation.operation_type.pk, 2)
            test_object.assertEqual(operation.year, 2017)
            test_object.assertEqual(models.Parcel.objects.count(),
                                    test_object.parcel_number + 1)
            # the init parcel is not submited but have a context record
            # the init parcel is not detached from the operation
            test_object.assertEqual(operation.parcels.count(),
                                    test_object.parcel_number + 1)

        def pre_third_wizard(test_object):
            parcel_nb = models.Parcel.objects.count()
            test_object.cr.delete()
            test_object.assertEqual(
                parcel_nb, models.Parcel.objects.count())

        def post_third_wizard(test_object, final_step_response):
            test_object.assertEqual(models.Operation.objects.count(),
                                    test_object.operation_number)
            operation = models.Operation.objects.get(
                pk=test_object.operations[0].pk)
            test_object.assertEqual(operation.operation_type.pk, 2)
            test_object.assertEqual(operation.year, 2017)
            # with no attach the parcel is deleted
            test_object.assertEqual(operation.parcels.count(),
                                    test_object.parcel_number)
            test_object.assertEqual(models.Parcel.objects.count(),
                                    test_object.parcel_number)

        self.form_datas[0].extra_tests = [post_first_wizard]
        self.form_datas[1].extra_tests = [post_second_wizard]
        self.form_datas[2].pre_tests = [pre_third_wizard]
        self.form_datas[2].extra_tests = [post_third_wizard]
        super(OperationWizardModifTest, self).pre_wizard()


class OperationWizardDeleteTest(OperationWizardCreationTest):
    fixtures = FILE_FIXTURES
    url_name = 'operation_deletion'
    wizard_name = 'operation_deletion_wizard'
    steps = views.operation_deletion_steps
    form_datas = [
        FormData(
            "Wizard deletion test",
            form_datas={
                'selec-operation_deletion': {'pk': None},
            }
        )
    ]

    def pass_test(self):
        if not settings.SOUTH_TESTS_MIGRATE:
            # with no migration the views are not created
            return True

    def pre_wizard(self):
        self.ope = self.get_default_operation(force=True)
        self.ope.parcels.add(self.create_parcel()[0])
        self.parcel_nb = models.Parcel.objects.count()
        self.form_datas[0].form_datas['selec-operation_deletion']['pk'] = \
            self.ope.pk
        self.operation_number = models.Operation.objects.count()
        super(OperationWizardDeleteTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(self.operation_number - 1,
                         models.Operation.objects.count())
        # associated parcel removed
        self.assertEqual(self.parcel_nb - 1, models.Parcel.objects.count())


class OperationWizardClosingTest(OperationWizardCreationTest):
    fixtures = FILE_FIXTURES
    url_name = 'operation_closing'
    wizard_name = 'operation_closing_wizard'
    steps = views.operation_closing_steps
    form_datas = [
        FormData(
            "Wizard closing test",
            form_datas={
                'selec-operation_closing': {'pk': None},
                'date-operation_closing': {'end_date': '2016-01-01'},
            }
        )
    ]

    def pre_wizard(self):
        self.ope = self.get_default_operation()
        self.form_datas[0].form_datas['selec-operation_closing']['pk'] = \
            self.ope.pk
        self.assertTrue(self.ope.is_active())
        super(OperationWizardClosingTest, self).pre_wizard()

    def post_wizard(self):
        ope = models.Operation.objects.get(pk=self.ope.pk)
        self.assertFalse(ope.is_active())
        self.assertEqual(
            ope.closing()['date'].strftime('%Y-%d-%m'),
            self.form_datas[0].form_datas['date-operation_closing']['end_date']
        )


class OperationAdminActWizardCreationTest(WizardTest, OperationInitTest,
                                          TestCase):
    fixtures = FILE_FIXTURES
    url_name = 'operation_administrativeactop'
    wizard_name = 'operation_administrative_act_wizard'
    steps = views.administrativeactop_steps
    form_datas = [
        FormData(
            "Admin act creation",
            form_datas={
                'selec-operation_administrativeactop': {},
                'administrativeact-operation_administrativeactop': {
                    'signature_date': str(datetime.date.today())
                }
            },
        )
    ]

    def pre_wizard(self):
        ope = self.get_default_operation()
        self.number = models.AdministrativeAct.objects.count()

        data = self.form_datas[0].form_datas
        data['selec-operation_administrativeactop']['pk'] = ope.pk
        act = models.ActType.objects.filter(intented_to='O').all()[0].pk

        data['administrativeact-operation_administrativeactop'][
            'act_type'] = act
        super(OperationAdminActWizardCreationTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.AdministrativeAct.objects.count(),
                         self.number + 1)


class OperationSourceWizardModificationTest(WizardTest, OperationInitTest,
                                            TestCase):
    fixtures = FILE_FIXTURES
    url_name = 'operation_source_modification'
    wizard_name = 'operation_source_wizard'
    steps = views.operation_source_modification_steps
    form_datas = [
        FormData(
            "Test remove all authors",
            form_datas={
                'selec-operation_source_modification': {},
                'source-operation_source_modification': {
                    'title': "New title",
                    'source_type': None,
                    'index': 42
                },
                'authors-operation_source_modification': []
            },
        )
    ]

    def pre_wizard(self):
        ope = self.get_default_operation()
        self.source = models.OperationSource.objects.create(
            title="Old title", source_type=SourceType.objects.all()[0],
            operation=ope
        )
        author = Author.objects.create(
            author_type=AuthorType.objects.all()[0],
            person=Person.objects.all()[0]
        )

        self.source.authors.add(author)

        data = self.form_datas[0].form_datas
        data['selec-operation_source_modification']['pk'] = self.source.pk

        data['source-operation_source_modification']['hidden_operation_id'] = \
            self.source.pk
        data['source-operation_source_modification'][
            'source_type'] = SourceType.objects.all()[1].pk
        super(OperationSourceWizardModificationTest, self).pre_wizard()

    def post_wizard(self):
        source = models.OperationSource.objects.get(pk=self.source.pk)
        self.assertEqual(source.authors.count(), 0)