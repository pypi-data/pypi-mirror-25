#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015-2016 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from bs4 import BeautifulSoup as Soup
import datetime
from StringIO import StringIO

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.base import File as DjangoFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.template.defaultfilters import slugify
from django.test import TestCase as BaseTestCase
from django.test.client import Client
from django.test.simple import DjangoTestSuiteRunner

from ishtar_common import models
from ishtar_common import forms_common
from ishtar_common.utils import post_save_point

from archaeological_context_records.models import CRBulkView
from archaeological_finds.models import BFBulkView, FBulkView, FirstBaseFindView

"""
from django.conf import settings
import tempfile, datetime
from zipfile import ZipFile, ZIP_DEFLATED

from oook_replace.oook_replace import oook_replace

class OOOGenerationTest(TestCase):
    def testGeneration(self):
        context = {'test_var':u"Testé", 'test_var2':u"",
                   "test_date":datetime.date(2015, 1, 1)}
        tmp = tempfile.TemporaryFile()
        oook_replace("../ishtar_common/tests/test-file.odt", tmp, context)
        inzip = ZipFile(tmp, 'r', ZIP_DEFLATED)
        value = inzip.read('content.xml')
        self.assertTrue(u"Testé" in value or "Test&#233;" in value)
        self.assertTrue("testé 2" not in value and "test&#233; 2" not in value)
        self.assertTrue("2015" in value)
        lg, ct = settings.LANGUAGE_CODE.split('-')
        if lg == 'fr':
            self.assertTrue('janvier' in value)
        if lg == 'en':
            self.assertTrue('january' in value)
"""


COMMON_FIXTURES = [
    settings.ROOT_PATH + '../fixtures/initial_data-auth-fr.json',
    settings.ROOT_PATH + '../ishtar_common/fixtures/initial_data-fr.json',
    settings.ROOT_PATH +
    '../ishtar_common/fixtures/initial_spatialrefsystem-fr.json',
    settings.ROOT_PATH +
    '../ishtar_common/fixtures/initial_importtypes-fr.json',
    ]

OPERATION_FIXTURES = COMMON_FIXTURES + [
    settings.ROOT_PATH +
    '../archaeological_operations/fixtures/initial_data-fr.json'
]


def create_superuser():
    username = 'username4277'
    password = 'dcbqj756456!@%'
    user = User.objects.create_superuser(username, "nomail@nomail.com",
                                         password)
    return username, password, user


def create_user():
    username = 'username678'
    password = 'dcbqj756456!@%'
    user = User.objects.create_user(username, email="nomail2@nomail.com")
    user.set_password(password)
    user.save()
    return username, password, user


class TestCase(BaseTestCase):
    def _pre_setup(self):
        super(TestCase, self)._pre_setup()
        if settings.USE_SPATIALITE_FOR_TESTS:
            return
        c = connection.cursor()
        for view in [CRBulkView, FirstBaseFindView, BFBulkView, FBulkView]:
            c.execute(view.CREATE_SQL)
            transaction.commit_unless_managed()


class CommandsTestCase(TestCase):
    def test_clean_ishtar(self):
        """
        Clean ishtar db
        """
        from archaeological_operations.models import Parcel
        p = Parcel.objects.create(
            town=models.Town.objects.create(name='test', numero_insee='25000'))
        parcel_nb = Parcel.objects.count()
        out = StringIO()
        call_command('clean_ishtar', stdout=out)
        # no operation or file attached - the parcel should have disappear
        self.assertEqual(parcel_nb - 1, Parcel.objects.count())
        self.assertEqual(Parcel.objects.filter(pk=p.pk).count(), 0)


class WizardTestFormData(object):
    """
    Test set to simulate wizard steps
    """
    def __init__(self, name, form_datas, ignored=[], pre_tests=[],
                 extra_tests=[]):
        """
        :param name: explicit name of the test
        :param form_datas: dict with data for each step - dict key are wizard
        step name
        :param ignored: steps to be ignored in wizard processing
        :param pre_tests: list of function to be executed before the wizard
        :param extra_tests: list of extra tests. Theses tests must be functions
        accepting two parameters: the current test object and the final step
        response
        """
        self.name = name
        self.form_datas = form_datas
        self.ignored = ignored[:]
        self.pre_tests = pre_tests
        self.extra_tests = extra_tests

    def set(self, form_name, field_name, value):
        """
        Set data value.

        :param form_name: form name without wizard name
        :param field_name: field name
        :param value: value
        :return: None
        """
        self.form_datas[form_name][field_name] = value

    def append(self, form_name, value):
        """
        Add data value to formset.

        :param form_name: form name without wizard name
        :param value: value
        :return: None
        """
        self.form_datas[form_name].append(value)

    def inits(self, test_object):
        """
        Initialisations before the wizard.
        """

        suffix = '-' + test_object.url_name
        # if form names are defined without url_name fix it
        for form_name in self.form_datas.keys():
            if suffix in form_name:
                continue
            self.form_datas[form_name + suffix] = self.form_datas.pop(form_name)

        for pre in self.pre_tests:
            pre(test_object)

    def tests(self, test_object, final_step_response):
        """
        Specific tests for theses datas. Raise Exception if not OK.
        """
        for test in self.extra_tests:
            test(test_object, final_step_response)


class ManagedModelTestRunner(DjangoTestSuiteRunner):
    """
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run, so that one doesn't need
    to execute the SQL manually to create them.
    """
    def setup_test_environment(self, *args, **kwargs):
        from django.db.models.loading import get_models
        self.unmanaged_models = [m for m in get_models()
                                 if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(ManagedModelTestRunner, self).setup_test_environment(*args,
                                                                   **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(ManagedModelTestRunner, self).teardown_test_environment(*args,
                                                                      **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False


class WizardTest(object):
    url_name = None
    wizard_name = ''
    steps = None
    condition_dict = None
    form_datas = []

    def setUp(self):
        self.username, self.password, self.user = create_superuser()

    def pre_wizard(self):
        self.client.login(**{'username': self.username,
                             'password': self.password})

    def post_wizard(self):
        pass

    def pass_test(self):
        return False

    def check_response(self, response, current_step):
        if "errorlist" in response.content:
            soup = Soup(response.content)
            errorlist = soup.findAll(
                "ul", {"class": "errorlist"})
            errors = []
            for li in errorlist:
                lbl = li.findParent().findParent().findChild().text
                errors.append(u"{} - {}".format(lbl, li.text))
            raise ValidationError(u"Errors: {} on {}.".format(
                u" ".join(errors), current_step))

    def test_wizard(self):
        if self.pass_test():
            return
        url = reverse(self.url_name)
        self.pre_wizard()
        for test_form_data in self.form_datas:
            test_form_data.inits(self)
            form_data = test_form_data.form_datas
            ignored = test_form_data.ignored
            for idx, step in enumerate(self.steps):
                current_step, current_form = step
                if current_step in ignored:
                    continue
                data = {
                    '{}{}-current_step'.format(self.url_name,
                                               self.wizard_name):
                    [current_step],
                }

                # reconstruct a POST request
                if current_step in form_data:
                    d = form_data[current_step]
                    if type(d) in (list, tuple):  # is a formset
                        for d_idx, item in enumerate(d):
                            for k in item:
                                data['{}-{}-{}'.format(
                                    current_step, d_idx, k)] = item[k]
                    else:
                        for k in d:
                            data['{}-{}'.format(current_step, k)] = d[k]

                next_form_is_checked = len(self.steps) > idx + 1 and \
                    self.steps[idx + 1][0] not in ignored
                try:
                    response = self.client.post(url, data,
                                                follow=not next_form_is_checked)
                except ValidationError as e:
                    msg = u"Errors: {} on {}. On \"ManagementForm data is " \
                          u"missing or...\" error verify the wizard_name or " \
                          u"step name".format(u" - ".join(e.messages),
                                              current_step)
                    raise ValidationError(msg)
                self.check_response(response, current_step)
                if next_form_is_checked:
                    next_form = self.steps[idx + 1][0]
                    self.assertRedirects(
                        response,
                        '/{}/{}'.format(self.url_name, next_form),
                        msg_prefix="Redirection to {} has failed - "
                                   "Error on previous form ({})?".format(
                            next_form, current_step)
                    )
                if idx == len(self.steps) - 1:
                    #  last form
                    self.assertRedirects(
                        response,
                        '/{}/done'.format(self.url_name))
            test_form_data.tests(self, response)
        self.post_wizard()


class CacheTest(TestCase):
    def testAdd(self):
        models.OrganizationType.refresh_cache()
        cached = models.OrganizationType.get_cache('test')
        self.assertEqual(cached, None)
        orga = models.OrganizationType.objects.create(
            txt_idx='test', label='testy')
        cached = models.OrganizationType.get_cache('test')
        self.assertEqual(cached.pk, orga.pk)
        orga.txt_idx = 'testy'
        orga.save()
        cached = models.OrganizationType.get_cache('testy')
        self.assertEqual(cached.pk, orga.pk)

    def testList(self):
        models.OrganizationType.refresh_cache()
        types = models.OrganizationType.get_types()
        # only empty
        self.assertTrue(len(types), 1)
        org = models.OrganizationType.objects.create(
            txt_idx='test', label='testy')
        types = [
            unicode(lbl) for idx, lbl in models.OrganizationType.get_types()]
        self.assertTrue('testy' in types)
        org.delete()
        types = [
            unicode(lbl) for idx, lbl in models.OrganizationType.get_types()]
        self.assertFalse('testy' in types)


class AccessControlTest(TestCase):
    def test_administrator(self):
        admin, created = models.PersonType.objects.get_or_create(
            txt_idx='administrator', defaults={'label': 'Admin'})
        user, created = User.objects.get_or_create(username='myusername')
        user.is_superuser = True
        user.save()
        ishtar_user = models.IshtarUser.objects.get(username=user.username)
        self.assertIn(admin, ishtar_user.person.person_types.all())


class AdminGenTypeTest(TestCase):
    fixtures = OPERATION_FIXTURES
    gen_models = [
        models.OrganizationType, models.PersonType, models.TitleType,
        models.AuthorType, models.SourceType, models.OperationType,
        models.SpatialReferenceSystem, models.Format, models.SupportType]
    models_with_data = gen_models + [models.ImporterModel]
    models = models_with_data
    module_name = 'ishtar_common'

    def setUp(self):
        password = 'mypassword'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.client = Client()
        self.client.login(username=my_admin.username, password=password)

    def test_listing_and_detail(self):
        for model in self.models:
            # quick test to verify basic access to listing
            base_url = '/admin/{}/{}/'.format(self.module_name,
                                              model.__name__.lower())
            url = base_url
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                msg="Can not access admin list for {}.".format(model))
            if model in self.models_with_data:
                url = base_url + "{}/".format(model.objects.all()[0].pk)
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, 200,
                    msg="Can not access admin detail for {}.".format(model))

    def test_csv_export(self):
        for model in self.gen_models:
            url = '/admin/{}/{}/'.format(self.module_name,
                                         model.__name__.lower())
            response = self.client.post(url, {'action': 'export_as_csv'})
            self.assertEqual(
                response.status_code, 200,
                msg="Can not export as CSV for {}.".format(model))

    def test_str(self):
        # test __str__
        for model in self.models_with_data:
            self.assertTrue(str(model.objects.all()[0]))

    def test_user_creation(self):
        url = '/admin/auth/user/add/'
        password = 'ishtar is the queen'
        response = self.client.post(
            url, {'username': 'test', 'password1': password,
                  'password2': password})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username='test', password=password))


class MergeTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='username')
        self.organisation_types = \
            models.OrganizationType.create_default_for_test()

        self.person_types = [models.PersonType.objects.create(label='Admin'),
                             models.PersonType.objects.create(label='User')]
        self.author_types = [models.AuthorType.objects.create(label='1'),
                             models.AuthorType.objects.create(label='2')]

        self.company_1 = models.Organization.objects.create(
            history_modifier=self.user, name='Franquin Comp.',
            organization_type=self.organisation_types[0])
        self.person_1 = models.Person.objects.create(
            name='Boule', surname=' ', history_modifier=self.user,
            attached_to=self.company_1)
        self.person_1.person_types.add(self.person_types[0])
        self.author_1_pk = models.Author.objects.create(
            person=self.person_1, author_type=self.author_types[0]).pk

        self.title = models.TitleType.objects.create(label='Test')

        self.company_2 = models.Organization.objects.create(
            history_modifier=self.user, name='Goscinny Corp.',
            organization_type=self.organisation_types[1])
        self.person_2 = models.Person.objects.create(
            name='Bill', history_modifier=self.user, surname='Peyo',
            title=self.title, attached_to=self.company_2)
        self.person_2.person_types.add(self.person_types[1])
        self.author_2_pk = models.Author.objects.create(
            person=self.person_2, author_type=self.author_types[1]).pk
        self.person_3 = models.Person.objects.create(
            name='George', history_modifier=self.user,
            attached_to=self.company_1)

    def testPersonMerge(self):
        self.person_1.merge(self.person_2)
        # preserve existing fields
        self.assertEqual(self.person_1.name, 'Boule')
        # fill missing fields
        self.assertEqual(self.person_1.title, self.title)
        # string field with only spaces is an empty field
        self.assertEqual(self.person_1.surname, 'Peyo')
        # preserve existing foreign key
        self.assertEqual(self.person_1.attached_to, self.company_1)
        # preserve existing many to many
        self.assertTrue(self.person_types[0]
                        in self.person_1.person_types.all())
        # add new many to many
        self.assertTrue(self.person_types[1]
                        in self.person_1.person_types.all())
        # update reverse foreign key association and dont break the existing
        self.assertEqual(models.Author.objects.get(pk=self.author_1_pk).person,
                         self.person_1)
        self.assertEqual(models.Author.objects.get(pk=self.author_2_pk).person,
                         self.person_1)

        self.person_3.merge(self.person_1)
        # manage well empty many to many fields
        self.assertTrue(self.person_types[1]
                        in self.person_3.person_types.all())

    def testPersonMergeCandidate(self):
        init_mc = self.person_1.merge_candidate.count()
        person = models.Person.objects.create(
            name=self.person_1.name,
            surname=self.person_1.surname, history_modifier=self.user,
            attached_to=self.person_1.attached_to)
        self.assertEqual(self.person_1.merge_candidate.count(),
                         init_mc + 1)
        person.archive()
        self.assertEqual(self.person_1.merge_candidate.count(),
                         init_mc)


class ShortMenuTest(TestCase):
    def setUp(self):
        self.username = 'username666'
        self.password = 'dcbqj7xnjkxnjsknx!@%'
        self.user = User.objects.create_superuser(
            self.username, "nomail@nomail.com", self.password)
        self.other_user = User.objects.create_superuser(
            'John', "nomail@nomail.com", self.password)
        profile = models.get_current_profile()
        profile.files = True
        profile.context_record = True
        profile.find = True
        profile.warehouse = True
        profile.save()

    def _create_ope(self, user=None):
        if not user:
            user = self.other_user
        from archaeological_operations.models import Operation, OperationType
        ope_type, created = OperationType.objects.get_or_create(label="test")
        return Operation.objects.create(
            operation_type=ope_type,
            history_modifier=user,
            year=2042, operation_code=54
        )

    def testNotConnected(self):
        c = Client()
        response = c.get(reverse('shortcut-menu'))
        # no content if not logged
        self.assertFalse("shortcut-menu" in response.content)
        c = Client()
        c.login(username=self.username, password=self.password)
        # no content because the user owns no object
        response = c.get(reverse('shortcut-menu'))
        self.assertFalse("shortcut-menu" in response.content)
        self._create_ope(user=self.user)
        # content is here
        response = c.get(reverse('shortcut-menu'))
        self.assertTrue("shortcut-menu" in response.content)

    def testOperation(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        ope = self._create_ope()
        # not available at first
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(ope.cached_label) in response.content)

        # available because is the creator
        ope.history_creator = self.user
        ope.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(ope.cached_label) in response.content)

        # available because is in charge
        ope.history_creator = self.other_user
        ope.in_charge = self.user.ishtaruser.person
        ope.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(ope.cached_label) in response.content)

        # available because is the scientist
        ope.history_creator = self.other_user
        ope.in_charge = None
        ope.scientist = self.user.ishtaruser.person
        ope.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(ope.cached_label) in response.content)

        # end date is reached - no more available
        ope.end_date = datetime.date(1900, 1, 1)
        ope.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(ope.cached_label) in response.content)

        # test current is not owned
        ope.end_date = None
        ope.history_creator = self.other_user
        ope.in_charge = None
        ope.scientist = None
        ope.save()
        session = c.session
        session[ope.SLUG] = ope.pk
        session.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(ope.cached_label) in response.content)

    def testFile(self):
        from archaeological_files.models import File, FileType
        c = Client()
        c.login(username=self.username, password=self.password)
        file_type = FileType.objects.create()
        fle = File.objects.create(
            file_type=file_type,
            history_modifier=self.other_user,
            year=2043,
        )
        # not available at first
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(fle.cached_label) in response.content)

        # available because is the creator
        fle.history_creator = self.user
        fle.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(fle.cached_label) in response.content)

        # available because is in charge
        fle.history_creator = self.other_user
        fle.in_charge = self.user.ishtaruser.person
        fle.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(fle.cached_label) in response.content)

        # end date is reached - no more available
        fle.end_date = datetime.date(1900, 1, 1)
        fle.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(fle.cached_label) in response.content)

    def _create_cr(self):
        from archaeological_context_records.models import ContextRecord
        from archaeological_operations.models import Parcel
        ope = self._create_ope()
        town = models.Town.objects.create()
        parcel = Parcel.objects.create(
            operation=ope,
            town=town,
            section="AA",
            parcel_number=42
        )
        return ContextRecord.objects.create(
            parcel=parcel,
            operation=ope,
            history_modifier=self.other_user,
        )

    def testContextRecord(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        cr = self._create_cr()

        # not available at first
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(cr.cached_label) in response.content)

        # available because is the creator
        cr.history_creator = self.user
        cr.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(cr.cached_label) in response.content)

        # available because is in charge
        cr.history_creator = self.other_user
        cr.save()
        cr.operation.in_charge = self.user.ishtaruser.person
        cr.operation.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(cr.cached_label) in response.content)

        # available because is the scientist
        cr.history_creator = self.other_user
        cr.save()
        cr.operation.in_charge = None
        cr.operation.scientist = self.user.ishtaruser.person
        cr.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(cr.cached_label) in response.content)

    def _create_find(self):
        from archaeological_finds.models import BaseFind, Find
        cr = self._create_cr()
        base_find = BaseFind.objects.create(
            context_record=cr
        )
        find = Find.objects.create(
            label="Where is my find?"
        )
        find.base_finds.add(base_find)
        return base_find, find

    def testFind(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        base_find, find = self._create_find()

        # not available at first
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(find.cached_label) in response.content)

        # available because is the creator
        find.history_creator = self.user
        find.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(find.cached_label) in response.content)

        # available because is in charge
        find.history_creator = self.other_user
        find.save()
        base_find.context_record.operation.in_charge = \
            self.user.ishtaruser.person
        base_find.context_record.operation.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(find.cached_label) in response.content)

        # available because is the scientist
        find.history_creator = self.other_user
        find.save()
        base_find.context_record.operation.in_charge = None
        base_find.context_record.operation.scientist = \
            self.user.ishtaruser.person
        base_find.context_record.operation.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(find.cached_label) in response.content)

    def testBasket(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        from archaeological_finds.models import FindBasket
        basket = FindBasket.objects.create(
            label="My basket",
        )

        # not available at first
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(basket.label) in response.content)

        # available because is the owner
        basket.user = self.user.ishtaruser
        basket.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(basket.label) in response.content)

    def test_treatment_file(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        from archaeological_finds.models import TreatmentFile, TreatmentFileType
        tf = TreatmentFile.objects.create(
            type=TreatmentFileType.objects.create(),
            year=2050
        )

        # not available at first
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(tf.cached_label) in response.content)

        # available because is the creator
        tf.history_creator = self.user
        tf.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(tf.cached_label) in response.content)

        # available because is in charge
        tf.history_creator = self.other_user
        tf.in_charge = self.user.ishtaruser.person
        tf.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(tf.cached_label) in response.content)

        # end date is reached - no more available
        tf.end_date = datetime.date(1900, 1, 1)
        tf.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(tf.cached_label) in response.content)

    def _create_treatment(self):
        from archaeological_finds.models import Treatment
        return Treatment.objects.create(
            label="My treatment",
            year=2052
        )

    def test_treatment(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        treat = self._create_treatment()

        # not available at first
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(treat.cached_label) in response.content)

        # available because is the creator
        treat.history_creator = self.user
        treat.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(treat.cached_label) in response.content)

        # available because is in charge
        treat.history_creator = self.other_user
        treat.person = self.user.ishtaruser.person
        treat.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(treat.cached_label) in response.content)

        # end date is reached - no more available
        treat.end_date = datetime.date(1900, 1, 1)
        treat.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(treat.cached_label) in response.content)

    def test_update_current_item(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        base_find, find = self._create_find()

        response = c.get(reverse('pin', args=['find', find.pk]))
        self.assertEqual(response.status_code, 200)
        # the selected find is pined
        self.assertEqual(c.session['find'], str(find.pk))
        # dependant items are also pined
        self.assertEqual(c.session['contextrecord'],
                         str(base_find.context_record.pk))
        self.assertEqual(c.session['operation'],
                         str(base_find.context_record.operation.pk))

        # pin another operation - dependant items are nullify
        ope = self._create_ope()
        response = c.get(reverse('pin', args=['operation', ope.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(c.session['find'])
        self.assertFalse(c.session['contextrecord'])

        # current find is set as an integer
        session = c.session
        session['find'] = find.id
        session.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)

        self._create_treatment()

    def test_basket_is_current_item(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        from archaeological_finds.models import FindBasket
        basket = FindBasket.objects.create(
            label="My basket",
            user=self.user.ishtaruser
        )
        session = c.session
        session['find'] = 'basket-{}'.format(basket.pk)
        session.save()
        response = c.get(reverse('shortcut-menu'))
        self.assertEqual(response.status_code, 200)
        response = c.get(reverse('get-findsource'))
        self.assertEqual(response.status_code, 200)


class ImportTest(TestCase):
    def testDeleteRelated(self):
        town = models.Town.objects.create(name='my-test')
        self.assertEqual(models.Town.objects.filter(name='my-test').count(), 1)

        # create an import, fields are not relevant...
        create_user()
        imp_model = models.ImporterModel.objects.create(
            klass='ishtar_common.models.Person', name='Person')
        importer_type = models.ImporterType.objects.create(
            associated_models=imp_model)
        mcc_operation_file = DjangoFile(file(
            settings.ROOT_PATH +
            '../archaeological_operations/tests/MCC-operations-example.csv',
            'rb'))
        imprt = models.Import.objects.create(
            user=models.IshtarUser.objects.all()[0],
            importer_type=importer_type,
            imported_file=mcc_operation_file)

        town.imports.add(imprt)
        imprt.delete()
        # town should be deleted
        self.assertEqual(models.Town.objects.filter(name='my-test').count(), 0)

    def test_keys(self):
        content_type = ContentType.objects.get_for_model(
            models.OrganizationType)

        # creation
        label = u"Ploufé"
        ot = models.OrganizationType.objects.create(label=label)
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot.pk, key=slugify(label),
                         content_type=content_type).count(), 1)
        label_2 = u"Plif"
        ot_2 = models.OrganizationType.objects.create(label=label_2)
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label_2),
                         content_type=content_type).count(), 1)

        # replace key
        ot_2.add_key(slugify(label), force=True)
        # one key point to only one item
        self.assertEqual(models.ItemKey.objects.filter(
                         key=slugify(label),
                         content_type=content_type).count(), 1)
        # this key point to the right item
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label),
                         content_type=content_type).count(), 1)

        # modification
        label_3 = "Yop"
        ot_2.label = label_3
        ot_2.txt_idx = slugify(label_3)
        ot_2.save()
        # old label not referenced anymore
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label_2),
                         content_type=content_type).count(), 0)
        # # forced key association is always here
        # new key is here
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label),
                         content_type=content_type).count(), 1)
        self.assertEqual(models.ItemKey.objects.filter(
                         object_id=ot_2.pk, key=slugify(label_3),
                         content_type=content_type).count(), 1)


class IshtarSiteProfileTest(TestCase):
    def testRelevance(self):
        cache.set('default-ishtarsiteprofile-is-current-profile', None,
                  settings.CACHE_TIMEOUT)
        profile = models.get_current_profile()
        default_slug = profile.slug
        profile2 = models.IshtarSiteProfile.objects.create(
            label="Test profile 2", slug='test-profile-2')
        profile2.save()
        # when no profile is the current, activate by default the first created
        self.assertTrue(profile.active and not profile2.active)
        profile2.active = True
        profile2 = profile2.save()
        # only one profile active at a time
        profile = models.IshtarSiteProfile.objects.get(slug=default_slug)
        self.assertTrue(profile2.active and not profile.active)
        # activate find active automatically context records
        self.assertFalse(profile.context_record)
        profile.find = True
        profile = profile.save()
        self.assertTrue(profile.context_record)
        # activate warehouse active automatically context records and finds
        self.assertFalse(profile2.context_record or profile2.find)
        profile2.warehouse = True
        profile2 = profile2.save()
        self.assertTrue(profile2.context_record and profile2.find)

    def testDefaultProfile(self):
        cache.set('default-ishtar_common-IshtarSiteProfile', None,
                  settings.CACHE_TIMEOUT)
        self.assertFalse(models.IshtarSiteProfile.objects.count())
        profile = models.get_current_profile(force=True)
        self.assertTrue(profile)
        self.assertEqual(models.IshtarSiteProfile.objects.count(), 1)

    def testMenuFiltering(self):
        cache.set('default-ishtarsiteprofile-is-current-profile', None,
                  settings.CACHE_TIMEOUT)
        username = 'username4277'
        password = 'dcbqj756456!@%'
        User.objects.create_superuser(username, "nomail@nomail.com",
                                      password)
        c = Client()
        c.login(username=username, password=password)
        response = c.get(reverse('start'))
        self.assertFalse("section-file_management" in response.content)
        profile = models.get_current_profile()
        profile.files = True
        profile.save()
        response = c.get(reverse('start'))
        self.assertTrue("section-file_management" in response.content)

    def testExternalKey(self):
        profile = models.get_current_profile()
        p = models.Person.objects.create(name='plouf', surname=u'Tégada')
        self.assertEqual(p.raw_name, u"PLOUF Tégada")
        profile.person_raw_name = u'{surname|slug} {name}'
        profile.save()
        p.raw_name = ''
        p.save()
        self.assertEqual(p.raw_name, u"tegada plouf")


class IshtarBasicTest(TestCase):
    def setUp(self):
        password = 'mypassword'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.client = Client()
        self.client.login(username=my_admin.username, password=password)

    def test_status(self):
        response = self.client.get(reverse('status'))
        self.assertEqual(response.status_code, 200)

    def test_person_rawname(self):
        person = models.Person.objects.create(name="Weasley", surname="Bill")
        self.assertEqual(person.raw_name, "WEASLEY Bill")
        person.surname = "George"
        person.save()
        self.assertEqual(person.raw_name, "WEASLEY George")


class GeomaticTest(TestCase):
    def test_post_save_point(self):
        class FakeGeomaticObject(object):
            def __init__(self, x, y, z, spatial_reference_system, point=None,
                         point_2d=None):
                self.x = x
                self.y = y
                self.z = z
                self.spatial_reference_system = spatial_reference_system
                self.point = point
                self.point_2d = point_2d

            def save(self, *args, **kwargs):
                pass

        srs = models.SpatialReferenceSystem.objects.create(
            label='WGS84', txt_idx='wgs84', srid=4326
        )
        obj = FakeGeomaticObject(
            x=2, y=3, z=4,
            spatial_reference_system=srs)
        self.assertIsNone(obj.point_2d)
        post_save_point(None, instance=obj)
        self.assertIsNotNone(obj.point_2d)
        self.assertIsNotNone(obj.point)
