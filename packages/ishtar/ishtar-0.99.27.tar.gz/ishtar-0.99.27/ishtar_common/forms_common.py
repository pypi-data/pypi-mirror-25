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

"""
Administrative forms definitions: manage accounts and persons
"""

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from django.forms.models import BaseModelFormSet
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import models
import widgets
from ishtar_common.templatetags.link_to_window import link_to_window
from forms import FinalForm, FormSet, reverse_lazy, name_validator, \
    TableSelect, ManageOldType


def get_town_field(label=_(u"Town"), required=True):
    help_text = _(
        u"<p>Type name, department code of the "
        u"town you would like to select. The search is insensitive to case."
        u"</p>\n<p>Only the first twenty results are displayed but specifying "
        u"the department code is generally sufficient to get the appropriate "
        u"result.</p>\n<p class='example'>For instance type \"saint denis 93\""
        u" for getting the french town Saint-Denis in the Seine-Saint-Denis "
        u"department.</p>")
    # !FIXME hard_link, reverse_lazy doen't seem to work with formsets
    return forms.IntegerField(
        widget=widgets.JQueryAutoComplete(
            "/" + settings.URL_PATH + 'autocomplete-town',
            associated_model=models.Town),
        validators=[models.valid_id(models.Town)], label=label,
        help_text=mark_safe(help_text), required=required)


def get_advanced_town_field(label=_(u"Town"), required=True):
    # !FIXME hard_link, reverse_lazy doen't seem to work with formsets
    return forms.IntegerField(
        widget=widgets.JQueryTown(
            "/" + settings.URL_PATH + 'autocomplete-advanced-town'),
        validators=[models.valid_id(models.Town)], label=label,
        required=required)


def get_person_field(label=_(u"Person"), required=True, person_types=[]):
    # !FIXME hard_link, reverse_lazy doen't seem to work with formsets
    widget = None
    url = "/" + settings.URL_PATH + 'autocomplete-person'
    if person_types:
        person_types = [
            unicode(models.PersonType.objects.get(txt_idx=person_type).pk)
            for person_type in person_types]
        url += u"/" + u'_'.join(person_types)
    widget = widgets.JQueryAutoComplete(url, associated_model=models.Person)
    return forms.IntegerField(widget=widget, label=label, required=required,
                              validators=[models.valid_id(models.Person)])


class NewItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.limits = {}
        if 'limits' in kwargs:
            limits = kwargs.pop('limits')
            if limits:
                for item in limits.split(';'):
                    key, values = item.split('__')
                    self.limits[key] = values.split('-')
        super(NewItemForm, self).__init__(*args, **kwargs)

    def limit_fields(self):
        for key in self.limits:
            if key in self.fields and hasattr(self.fields[key], 'choices'):
                new_choices = []
                for value, lbl in self.fields[key].choices:
                    if unicode(value) in self.limits[key]:
                        new_choices.append((value, lbl))
                self.fields[key].choices = new_choices
                if len(new_choices) == 1:
                    self.fields[key].initial = [new_choices[0][0]]


class NewImportForm(forms.ModelForm):
    class Meta:
        model = models.Import
        fields = ('name', 'importer_type', 'imported_file', 'imported_images',
                  'conservative_import', 'encoding', 'skip_lines')

    def clean(self):
        data = self.cleaned_data
        if data.get('conservative_import', None) \
                and data.get('importer_type') \
                and not data.get('importer_type').unicity_keys:
            raise forms.ValidationError(
                _(u"This import type have no unicity type defined. "
                  u"Conservative import is not possible."))
        return data

    def save(self, user, commit=True):
        self.instance.user = user
        return super(NewImportForm, self).save(commit)


class TargetKeyForm(forms.ModelForm):
    class Meta:
        model = models.TargetKey
        fields = ('target', 'key', 'value')
        widgets = {
            'key': forms.TextInput(attrs={'readonly': 'readonly'}),
            'value': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(TargetKeyForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.associated_import = None
        if instance and instance.pk:
            self.associated_import = instance.associated_import
            self.fields['target'].widget.attrs['readonly'] = True
            self.fields['key'].widget.attrs['readonly'] = True
            self.fields['key'].widget.attrs['title'] = unicode(instance)
        self.fields['value'].widget.choices = list(
            instance.target.get_choices())
        self.fields['key'].required = False
        self.fields['value'].required = False

    def clean_target(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.target
        else:
            return self.cleaned_data['target']

    def clean_key(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.key
        else:
            return self.cleaned_data['key']

    def save(self, commit=True):
        super(TargetKeyForm, self).save(commit)
        if self.cleaned_data.get('value'):
            self.instance.is_set = True
            self.instance.associated_import = self.associated_import
            self.instance.save()


class OrganizationForm(ManageOldType, NewItemForm):
    form_label = _(u"Organization")
    associated_models = {'organization_type': models.OrganizationType}
    name = forms.CharField(
        label=_(u"Name"), max_length=300, validators=[name_validator])
    organization_type = forms.ChoiceField(label=_(u"Organization type"),
                                          choices=[])
    address = forms.CharField(label=_(u"Address"), widget=forms.Textarea,
                              required=False)
    address_complement = forms.CharField(label=_(u"Address complement"),
                                         widget=forms.Textarea, required=False)
    postal_code = forms.CharField(label=_(u"Postal code"), max_length=10,
                                  required=False)
    town = forms.CharField(label=_(u"Town"), max_length=30, required=False)
    country = forms.CharField(label=_(u"Country"), max_length=30,
                              required=False)
    email = forms.EmailField(label=_(u"Email"), required=False)
    phone = forms.CharField(label=_(u"Phone"), max_length=18, required=False)
    mobile_phone = forms.CharField(label=_(u"Mobile phone"), max_length=18,
                                   required=False)

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['organization_type'].choices = \
            models.OrganizationType.get_types(
                initial=self.init_data.get('organization_type'))
        self.fields['organization_type'].help_text = \
            models.OrganizationType.get_help()
        self.limit_fields()

    def save(self, user):
        dct = self.cleaned_data
        dct['history_modifier'] = user
        dct['organization_type'] = models.OrganizationType.objects.get(
            pk=dct['organization_type'])
        new_item = models.Organization(**dct)
        new_item.save()
        return new_item


class OrganizationSelect(TableSelect):
    name = forms.CharField(label=_(u"Name"), max_length=300)
    organization_type = forms.ChoiceField(label=_(u"Type"), choices=[])

    def __init__(self, *args, **kwargs):
        super(OrganizationSelect, self).__init__(*args, **kwargs)
        self.fields['organization_type'].choices = \
            models.OrganizationType.get_types()


class OrganizationFormSelection(forms.Form):
    form_label = _(u"Organization search")
    associated_models = {'pk': models.Organization}
    currents = {'pk': models.Organization}
    pk = forms.IntegerField(
        label="",
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-organization'), OrganizationSelect,
            models.Organization,
            source_full=reverse_lazy('get-organization-full')),
        validators=[models.valid_id(models.Organization)])


class ManualMerge(object):
    def clean_to_merge(self):
        value = self.cleaned_data.get('to_merge', None) or []
        if value:
            value = value.split(',')
        values = []
        for val in value:
            try:
                values.append(int(val))
            except ValueError:
                pass
        if len(values) < 2:
            raise forms.ValidationError(_(u"At least two items have to be "
                                          u"selected."))
        self.cleaned_data['to_merge'] = values
        return values

    def get_items(self):
        items = []
        model = self.associated_models['to_merge']
        for pk in sorted(self.cleaned_data['to_merge']):
            try:
                items.append(model.objects.get(pk=pk))
            except model.DoesNotExist:
                pass
        return items


class MergeIntoForm(forms.Form):
    main_item = forms.ChoiceField(
        label=_("Merge all items into"), choices=[],
        widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.items = kwargs.pop('items')
        super(MergeIntoForm, self).__init__(*args, **kwargs)
        self.fields['main_item'].choices = []
        for pk in self.items:
            try:
                item = self.associated_model.objects.get(pk=pk)
            except self.associated_model.DoesNotExist:
                continue
            self.fields['main_item'].choices.append(
                (item.pk, mark_safe(u"{} {}".format(link_to_window(item),
                                                    unicode(item)))))

    def merge(self):
        model = self.associated_model
        try:
            main_item = model.objects.get(pk=self.cleaned_data['main_item'])
        except model.DoesNotExist:
            return
        for pk in self.items:
            if pk == unicode(main_item.pk):
                continue
            try:
                item = model.objects.get(pk=pk)
            except model.DoesNotExist:
                continue
            main_item.merge(item)
        return main_item


class OrgaMergeFormSelection(ManualMerge, forms.Form):
    form_label = _(u"Organization to merge")
    associated_models = {'to_merge': models.Organization}
    currents = {'to_merge': models.Organization}
    to_merge = forms.CharField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-organization'), OrganizationSelect,
            models.Organization,
            multiple_select=True,
            source_full=reverse_lazy('get-organization-full')),)


class OrgaMergeIntoForm(MergeIntoForm):
    associated_model = models.Organization


class BaseOrganizationForm(forms.ModelForm):
    form_prefix = "orga"

    class Meta:
        model = models.Organization
        fields = ['name', 'organization_type', 'address', 'address_complement',
                  'town', 'postal_code']


class PersonSelect(TableSelect):
    name = forms.CharField(label=_(u"Name"), max_length=200)
    surname = forms.CharField(label=_(u"Surname"), max_length=50)
    email = forms.CharField(label=_(u"Email"), max_length=75)
    person_types = forms.ChoiceField(label=_(u"Type"), choices=[])
    attached_to = forms.IntegerField(
        label=_("Organization"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-organization'),
            associated_model=models.Organization),
        validators=[models.valid_id(models.Organization)])

    def __init__(self, *args, **kwargs):
        super(PersonSelect, self).__init__(*args, **kwargs)
        self.fields['person_types'].choices = models.PersonType.get_types()


class PersonFormSelection(forms.Form):
    form_label = _(u"Person search")
    associated_models = {'pk': models.Person}
    currents = {'pk': models.Person}
    pk = forms.IntegerField(
        label="",
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-person'), PersonSelect, models.Person,
            source_full=reverse_lazy('get-person-full')),
        validators=[models.valid_id(models.Person)])


class PersonMergeFormSelection(ManualMerge, forms.Form):
    form_label = _("Person to merge")
    associated_models = {'to_merge': models.Person}
    currents = {'to_merge': models.Person}
    to_merge = forms.CharField(
        label="", required=False,
        widget=widgets.JQueryJqGrid(
            reverse_lazy('get-person'),
            PersonSelect, models.Person,
            multiple_select=True,
            source_full=reverse_lazy('get-person-full')),)


class PersonMergeIntoForm(MergeIntoForm):
    associated_model = models.Person


class SimplePersonForm(ManageOldType, NewItemForm):
    form_label = _("Identity")
    associated_models = {'attached_to': models.Organization,
                         'title': models.TitleType}
    title = forms.ChoiceField(label=_("Title"), choices=[], required=False)
    salutation = forms.CharField(label=_("Salutation"), max_length=200,
                                 required=False)
    surname = forms.CharField(label=_(u"Surname"), max_length=50,
                              validators=[name_validator])
    name = forms.CharField(label=_(u"Name"), max_length=200,
                           validators=[name_validator])
    raw_name = forms.CharField(label=_(u"Raw name"), max_length=300,
                               required=False)
    email = forms.EmailField(label=_(u"Email"), required=False)
    phone_desc = forms.CharField(label=_(u"Phone description"), max_length=300,
                                 required=False)
    phone = forms.CharField(label=_(u"Phone"), max_length=18, required=False)
    phone_desc2 = forms.CharField(label=_(u"Phone description 2"),
                                  max_length=300, required=False)
    phone2 = forms.CharField(label=_(u"Phone 2"), max_length=18,
                             required=False)
    phone_desc3 = forms.CharField(label=_(u"Phone description 3"),
                                  max_length=300, required=False)
    phone3 = forms.CharField(label=_(u"Phone 3"), max_length=18,
                             required=False)
    mobile_phone = forms.CharField(label=_(u"Mobile phone"), max_length=18,
                                   required=False)
    attached_to = forms.IntegerField(
        label=_("Current organization"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-organization'),
            associated_model=models.Organization, new=True),
        validators=[models.valid_id(models.Organization)], required=False)
    address = forms.CharField(label=_(u"Address"), widget=forms.Textarea,
                              required=False)
    address_complement = forms.CharField(
        label=_(u"Address complement"), widget=forms.Textarea, required=False)
    postal_code = forms.CharField(label=_(u"Postal code"), max_length=10,
                                  required=False)
    town = forms.CharField(label=_(u"Town"), max_length=30, required=False)
    country = forms.CharField(label=_(u"Country"), max_length=30,
                              required=False)
    alt_address = forms.CharField(label=_(u"Other address: address"),
                                  widget=forms.Textarea, required=False)
    alt_address_complement = forms.CharField(
        label=_(u"Other address: address complement"),
        widget=forms.Textarea, required=False)
    alt_postal_code = forms.CharField(label=_(u"Other address: postal code"),
                                      max_length=10, required=False)
    alt_town = forms.CharField(label=_(u"Other address: town"), max_length=30,
                               required=False)
    alt_country = forms.CharField(label=_(u"Other address: country"),
                                  max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(SimplePersonForm, self).__init__(*args, **kwargs)
        self.fields['raw_name'].widget.attrs['readonly'] = True
        self.fields['title'].choices = models.TitleType.get_types(
            initial=self.init_data.get('title'))


class PersonUserSelect(PersonSelect):
    ishtaruser__isnull = forms.NullBooleanField(
        label=_(u"Already has an account"), initial=False)


class PersonUserFormSelection(PersonFormSelection):
    form_label = _(u"Person search")
    associated_models = {'pk': models.Person}
    currents = {'pk': models.Person}
    pk = forms.IntegerField(
        label="",
        widget=widgets.JQueryJqGrid(reverse_lazy('get-person'),
                                    PersonUserSelect, models.Person),
        validators=[models.valid_id(models.Person)])


class IshtarUserSelect(TableSelect):
    username = forms.CharField(label=_(u"Username"), max_length=200)
    name = forms.CharField(label=_(u"Name"), max_length=200)
    surname = forms.CharField(label=_(u"Surname"), max_length=50)
    email = forms.CharField(label=_(u"Email"), max_length=75)
    person_types = forms.ChoiceField(label=_(u"Type"), choices=[])
    attached_to = forms.IntegerField(
        label=_("Organization"),
        widget=widgets.JQueryAutoComplete(
            reverse_lazy('autocomplete-organization'),
            associated_model=models.Organization),
        validators=[models.valid_id(models.Organization)])

    def __init__(self, *args, **kwargs):
        super(IshtarUserSelect, self).__init__(*args, **kwargs)
        self.fields['person_types'].choices = models.PersonType.get_types()


class AccountFormSelection(forms.Form):
    form_label = _(u"Account search")
    associated_models = {'pk': models.IshtarUser}
    currents = {'pk': models.IshtarUser}
    pk = forms.IntegerField(
        label="",
        widget=widgets.JQueryJqGrid(reverse_lazy('get-ishtaruser'),
                                    IshtarUserSelect, models.IshtarUser),
        validators=[models.valid_id(models.IshtarUser)])


class BasePersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ['title', 'salutation', 'name', 'surname', 'address',
                  'address_complement', 'town', 'postal_code']


class BaseOrganizationPersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ['attached_to', 'title', 'salutation', 'name', 'surname']
        widgets = {'attached_to': widgets.JQueryPersonOrganization(
            reverse_lazy('autocomplete-organization'),
            reverse_lazy('organization_create'),
            model=models.Organization,
            attrs={'hidden': True},
            new=True),
        }

    def __init__(self, *args, **kwargs):
        super(BaseOrganizationPersonForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        person = super(BaseOrganizationPersonForm, self).save(*args, **kwargs)
        instance = person.attached_to
        form = BaseOrganizationForm(self.data, instance=instance,
                                    prefix=BaseOrganizationForm.form_prefix)
        if form.is_valid():
            orga = form.save()
            if not person.attached_to:
                person.attached_to = orga
                person.save()
        return person


class PersonForm(SimplePersonForm):
    person_types = forms.MultipleChoiceField(
        label=_("Person type"), choices=[],
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['person_types'].choices = models.PersonType.get_types(
            initial=self.init_data.get('person_types'),
            empty_first=False)
        self.fields['person_types'].help_text = models.PersonType.get_help()
        self.limit_fields()

    def save(self, user):
        dct = self.cleaned_data
        dct['history_modifier'] = user
        if 'attached_to' in dct and dct['attached_to']:
            try:
                dct['attached_to'] = models.Organization.objects.get(
                    pk=dct['attached_to'])
            except models.Organization.DoesNotExist:
                dct.pop('attached_to')
        if 'title' in dct:
            try:
                dct['title'] = models.TitleType.objects.get(
                    pk=dct['title'])
            except (models.TitleType.DoesNotExist, ValueError):
                dct.pop('title')
        person_types = dct.pop('person_types')
        new_item = models.Person.objects.create(**dct)
        for pt in person_types:
            new_item.person_types.add(pt)
        return new_item


class NoOrgaPersonForm(PersonForm):
    def __init__(self, *args, **kwargs):
        super(NoOrgaPersonForm, self).__init__(*args, **kwargs)
        self.fields.pop('attached_to')


class PersonTypeForm(ManageOldType, forms.Form):
    form_label = _("Person type")
    base_model = 'person_type'
    associated_models = {'person_type': models.PersonType}
    person_type = forms.MultipleChoiceField(
        label=_("Person type"), choices=[],
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(PersonTypeForm, self).__init__(*args, **kwargs)
        self.fields['person_type'].choices = models.PersonType.get_types(
            initial=self.init_data.get('person_type'),
            empty_first=False)
        self.fields['person_type'].help_text = models.PersonType.get_help()


class AccountForm(forms.Form):
    form_label = _("Account")
    associated_models = {'pk': models.Person}
    currents = {'pk': models.Person}
    pk = forms.IntegerField(label=u"", widget=forms.HiddenInput,
                            required=False)
    username = forms.CharField(label=_(u"Account"), max_length=30)
    email = forms.CharField(label=_(u"Email"), max_length=75,
                            validators=[validators.validate_email])
    hidden_password = forms.CharField(
        label=_(u"New password"), max_length=128, widget=forms.PasswordInput,
        required=False, validators=[validators.MinLengthValidator(4)])
    hidden_password_confirm = forms.CharField(
        label=_(u"New password (confirmation)"), max_length=128,
        widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        person = None
        if 'initial' in kwargs and 'pk' in kwargs['initial']:
            try:
                person = models.Person.objects.get(pk=kwargs['initial']['pk'])
                account = models.IshtarUser.objects.get(person=person)
                if not kwargs['initial'].get('username'):
                    kwargs['initial']['username'] = account.username
                if not kwargs['initial'].get('email'):
                    kwargs['initial']['email'] = account.email
            except ObjectDoesNotExist:
                pass
        if 'person' in kwargs:
            person = kwargs.pop('person')
        super(AccountForm, self).__init__(*args, **kwargs)
        if person and person.raw_name:
            self.fields['username'].initial = \
                person.raw_name.lower().replace(' ', '.')

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("hidden_password")
        if password and \
                password != cleaned_data.get("hidden_password_confirm"):
            raise forms.ValidationError(_(u"Your password and confirmation "
                                          u"password do not match."))
        if not cleaned_data.get("pk"):
            models.is_unique(User, 'username')(cleaned_data.get("username"))
            if not password:
                raise forms.ValidationError(_(u"You must provide a correct "
                                              u"password."))
        # check username unicity
        q = models.IshtarUser.objects.filter(
            username=cleaned_data.get('username'))
        if cleaned_data.get('pk'):
            q = q.exclude(person__pk=cleaned_data.get('pk'))
        if q.count():
            raise forms.ValidationError(_(u"This username already exists."))
        return cleaned_data


class FinalAccountForm(forms.Form):
    final = True
    form_label = _("Confirm")
    send_password = forms.BooleanField(label=_(u"Send the new password by "
                                               u"email?"), required=False)

    def __init__(self, *args, **kwargs):
        self.is_hidden = True
        return super(FinalAccountForm, self).__init__(*args, **kwargs)


class TownForm(forms.Form):
    form_label = _("Towns")
    base_model = 'town'
    associated_models = {'town': models.Town}
    town = get_town_field(required=False)


class TownFormSet(FormSet):
    def clean(self):
        """Checks that no towns are duplicated."""
        return self.check_duplicate(('town',),
                                    _("There are identical towns."))

TownFormset = formset_factory(TownForm, can_delete=True, formset=TownFormSet)
TownFormset.form_label = _("Towns")


class MergeFormSet(BaseModelFormSet):
    from_key = ''
    to_key = ''

    def __init__(self, *args, **kwargs):
        self._cached_list = []
        super(MergeFormSet, self).__init__(*args, **kwargs)

    def merge(self):
        for form in self.initial_forms:
            form.merge()

    def initial_form_count(self):
        """
        Recopied from django source only get_queryset is changed
        """
        if not (self.data or self.files):
            return len(self.get_restricted_queryset())
        return super(MergeFormSet, self).initial_form_count()

    def _construct_form(self, i, **kwargs):
        """
        Recopied from django source only get_queryset is changed
        """
        if self.is_bound and i < self.initial_form_count():
            # Import goes here instead of module-level because importing
            # django.db has side effects.
            #  from django.db import connections
            pk_key = "%s-%s" % (self.add_prefix(i), self.model._meta.pk.name)
            pk = self.data[pk_key]
            """pk_field = self.model._meta.pk
            pk = pk_field.get_db_prep_lookup('exact', pk,
                connection=connections[self.get_queryset().db])"""
            pk = self.get_restricted_queryset()[i].pk
            if isinstance(pk, list):
                pk = pk[0]
            kwargs['instance'] = self._existing_object(pk)
        if i < self.initial_form_count() and not kwargs.get('instance'):
            kwargs['instance'] = self.get_restricted_queryset()[i]
        if i >= self.initial_form_count() and self.initial_extra:
            # Set initial values for extra forms
            try:
                kwargs['initial'] = \
                    self.initial_extra[i - self.initial_form_count()]
            except IndexError:
                pass
        return super(BaseModelFormSet, self)._construct_form(i, **kwargs)

    def get_restricted_queryset(self):
        '''
        Filter (from, to) when (to, from) is already here
        '''
        q = self.queryset
        if self._cached_list:
            return self._cached_list
        existing, res = [], []
        # only get one version of each couple
        for item in q.all():
            tpl = [getattr(item, self.from_key).pk,
                   getattr(item, self.to_key).pk]
            if tpl not in existing:
                res.append(item)
                existing.append(list(reversed(tpl)))
        self._cached_list = res
        return res


class MergeForm(forms.ModelForm):
    id = forms.IntegerField(
        label=u"", widget=forms.HiddenInput, required=False)
    a_is_duplicate_b = forms.BooleanField(required=False)
    b_is_duplicate_a = forms.BooleanField(required=False)
    not_duplicate = forms.BooleanField(required=False)

    def clean(self):
        checked = [True for k in ['a_is_duplicate_b', 'b_is_duplicate_a',
                                  'not_duplicate'] if self.cleaned_data.get(k)]
        if len(checked) > 1:
            raise forms.ValidationError(_(u"Only one choice can be checked."))
        return self.cleaned_data

    def merge(self, *args, **kwargs):
        try:
            to_item = getattr(self.instance, self.TO_KEY)
            from_item = getattr(self.instance, self.FROM_KEY)
        except ObjectDoesNotExist:
            return
        if self.cleaned_data.get('a_is_duplicate_b'):
            to_item.merge(from_item)
        elif self.cleaned_data.get('b_is_duplicate_a'):
            from_item.merge(to_item)
        elif self.cleaned_data.get('not_duplicate'):
            from_item.merge_exclusion.add(to_item)
        else:
            return
        try:
            self.instance.__class__.objects.get(
                **{self.TO_KEY: from_item,
                   self.FROM_KEY: to_item}).delete()
        except ObjectDoesNotExist:
            pass
        self.instance.delete()


class MergePersonForm(MergeForm):
    class Meta:
        model = models.Person
        fields = []

    FROM_KEY = 'from_person'
    TO_KEY = 'to_person'


class MergeOrganizationForm(MergeForm):
    class Meta:
        model = models.Organization
        fields = []

    FROM_KEY = 'from_organization'
    TO_KEY = 'to_organization'


######################
# Sources management #
######################
class SourceForm(ManageOldType, forms.Form):
    form_label = _(u"Documentation informations")
    file_upload = True
    associated_models = {'source_type': models.SourceType}
    title = forms.CharField(label=_(u"Title"),
                            validators=[validators.MaxLengthValidator(200)])
    source_type = forms.ChoiceField(label=_(u"Source type"), choices=[])
    reference = forms.CharField(
        label=_(u"Reference"),
        validators=[validators.MaxLengthValidator(100)], required=False)
    internal_reference = forms.CharField(
        label=_(u"Internal reference"),
        validators=[validators.MaxLengthValidator(100)], required=False)
    associated_url = forms.URLField(
        required=False, label=_(u"Numerical ressource (web address)"))
    receipt_date = forms.DateField(label=_(u"Receipt date"), required=False,
                                   widget=widgets.JQueryDate)
    creation_date = forms.DateField(label=_(u"Creation date"), required=False,
                                    widget=widgets.JQueryDate)
    receipt_date_in_documentation = forms.DateField(
        label=_(u"Receipt date in documentation"), required=False,
        widget=widgets.JQueryDate)
    comment = forms.CharField(label=_(u"Comment"), widget=forms.Textarea,
                              required=False)
    description = forms.CharField(label=_(u"Description"),
                                  widget=forms.Textarea, required=False)
    additional_information = forms.CharField(
        label=_(u"Additional information"), widget=forms.Textarea,
        required=False)
    duplicate = forms.BooleanField(label=_(u"Has a duplicate"),
                                   required=False)
    image = forms.ImageField(
        label=_(u"Image"), help_text=mark_safe(
            _(u"<p>Heavy images are resized to: %(width)dx%(height)d "
              u"(ratio is preserved).</p>") % {
                'width': settings.IMAGE_MAX_SIZE[0],
                'height': settings.IMAGE_MAX_SIZE[1]}),
        max_length=255, required=False, widget=widgets.ImageFileInput())

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        self.fields['source_type'].choices = models.SourceType.get_types(
            initial=self.init_data.get('source_type'))


class SourceSelect(TableSelect):
    authors = forms.IntegerField(
        widget=widgets.JQueryAutoComplete(
            "/" + settings.URL_PATH + 'autocomplete-author',
            associated_model=models.Author),
        validators=[models.valid_id(models.Author)], label=_(u"Author"),
        required=False)

    title = forms.CharField(label=_(u"Title"))
    source_type = forms.ChoiceField(label=_("Source type"), choices=[])
    reference = forms.CharField(label=_(u"Reference"))
    internal_reference = forms.CharField(label=_(u"Internal reference"))
    description = forms.CharField(label=_(u"Description"))
    comment = forms.CharField(label=_(u"Comment"))
    additional_information = forms.CharField(
        label=_(u"Additional informations"))
    duplicate = forms.NullBooleanField(label=_(u"Has a duplicate"))

    def __init__(self, *args, **kwargs):
        super(SourceSelect, self).__init__(*args, **kwargs)
        self.fields['source_type'].choices = models.SourceType.get_types()
        self.fields['source_type'].help_text = models.SourceType.get_help()


class SourceDeletionForm(FinalForm):
    confirm_msg = " "
    confirm_end_msg = _(u"Would you like to delete this documentation?")

######################
# Authors management #
######################


class AuthorForm(ManageOldType, NewItemForm):
    form_label = _(u"Author")
    associated_models = {'person': models.Person,
                         'author_type': models.AuthorType}
    person = forms.IntegerField(
        widget=widgets.JQueryAutoComplete(
            "/" + settings.URL_PATH + 'autocomplete-person',
            associated_model=models.Person, new=True),
        validators=[models.valid_id(models.Person)], label=_(u"Person"))
    author_type = forms.ChoiceField(label=_(u"Author type"), choices=[])

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['author_type'].choices = models.AuthorType.get_types(
            initial=self.init_data.get('author_type'))
        self.limit_fields()

    def save(self, user):
        dct = self.cleaned_data
        dct['author_type'] = models.AuthorType.objects.get(
            pk=dct['author_type'])
        dct['person'] = models.Person.objects.get(pk=dct['person'])
        new_item = models.Author(**dct)
        new_item.save()
        return new_item


class AuthorFormSelection(forms.Form):
    form_label = _(u"Author selection")
    base_model = 'author'
    associated_models = {'author': models.Author}
    author = forms.IntegerField(
        required=False,
        widget=widgets.JQueryAutoComplete(
            "/" + settings.URL_PATH + 'autocomplete-author',
            associated_model=models.Author, new=True),
        validators=[models.valid_id(models.Author)], label=_(u"Author"))


class AuthorFormSet(FormSet):
    def clean(self):
        """Checks that no author are duplicated."""
        return self.check_duplicate(('author',),
                                    _("There are identical authors."))

AuthorFormset = formset_factory(AuthorFormSelection, can_delete=True,
                                formset=AuthorFormSet)
AuthorFormset.form_label = _("Authors")
