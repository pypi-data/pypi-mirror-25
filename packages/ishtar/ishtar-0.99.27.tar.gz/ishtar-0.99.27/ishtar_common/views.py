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

from tidylib import tidy_document as tidy

from copy import copy
import csv
import cStringIO as StringIO
import datetime
import ho.pisa as pisa
import json
import logging
from markdown import markdown
import optparse
import re
from tempfile import NamedTemporaryFile
import unicodedata

from extra_views import ModelFormSetView

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q, ImageField
from django.db.models.fields import FieldDoesNotExist
from django.forms.models import modelformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect, \
    HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import ListView, UpdateView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView

from xhtml2odt import xhtml2odt

from menus import menu

from archaeological_files.models import File
from archaeological_operations.models import Operation
from archaeological_context_records.models import ContextRecord
from archaeological_finds.models import Find, Treatment, TreatmentFile, \
    FindBasket

from archaeological_operations.forms import DashboardForm as DashboardFormOpe
from archaeological_files.forms import DashboardForm as DashboardFormFile
from archaeological_finds.forms import DashboardTreatmentForm, \
    DashboardTreatmentFileForm

from ishtar_common.forms import FinalForm, FinalDeleteForm
from ishtar_common.widgets import JQueryAutoComplete
from ishtar_common.utils import get_random_item_image_link, shortify
from ishtar_common import forms_common as forms
from ishtar_common import wizards
from ishtar_common.models import HistoryError, PRIVATE_FIELDS, \
    get_current_profile

import models

CSV_OPTIONS = {'delimiter': ',', 'quotechar': '"', 'quoting': csv.QUOTE_ALL}
ENCODING = settings.ENCODING or 'utf-8'

logger = logging.getLogger(__name__)


def status(request):
    return HttpResponse('OK')


def index(request):
    """
    Main page
    """
    dct = {'warnings': []}
    if settings.PROJECT_SLUG == 'default':
        dct['warnings'].append(_(
            u"PROJECT_SLUG is set to \"default\" change it in your "
            u"local_settings (or ask your admin to do it)."))
    profile = get_current_profile()
    if profile.slug == 'default':
        dct['warnings'].append(_(
            u"The slug of your current profile is set to \"default\" change it "
            u"on the administration page (or ask your admin to do it)."))
    image = get_random_item_image_link(request)
    if hasattr(profile, 'homepage') and profile.homepage:
        dct['homepage'] = markdown(profile.homepage)
        if '{random_image}' in dct['homepage']:
            dct['homepage'] = dct['homepage'].replace(
                '{random_image}', image)
    else:
        dct['random_image'] = image
    try:
        return render_to_response('index.html', dct,
                                  context_instance=RequestContext(request))
    except NoReverseMatch:
        # probably rights exception (rights revoked)
        logout(request)
        return render_to_response('index.html', dct,
                                  context_instance=RequestContext(request))

person_search_wizard = wizards.SearchWizard.as_view(
    [('general-person_search', forms.PersonFormSelection)],
    label=_(u"Person search"),
    url_name='person_search',)

person_creation_wizard = wizards.PersonWizard.as_view(
    [('identity-person_creation', forms.SimplePersonForm),
     ('person_type-person_creation', forms.PersonTypeForm),
     ('final-person_creation', FinalForm)],
    label=_(u"New person"),
    url_name='person_creation')

person_modification_wizard = wizards.PersonModifWizard.as_view(
    [('selec-person_modification', forms.PersonFormSelection),
     ('identity-person_modification', forms.SimplePersonForm),
     ('person_type-person_creation', forms.PersonTypeForm),
     ('final-person_modification', FinalForm)],
    label=_(u"Person modification"),
    url_name='person_modification')


def person_modify(request, pk):
    person_modification_wizard(request)
    wizards.PersonModifWizard.session_set_value(
        request, 'selec-person_modification', 'pk', pk, reset=True)
    return redirect(reverse('person_modification',
                            kwargs={'step': 'identity-person_modification'}))


person_deletion_wizard = wizards.PersonDeletionWizard.as_view(
    [('selec-person_deletion', forms.PersonFormSelection),
     ('final-person_deletion', FinalDeleteForm)],
    label=_(u"Person deletion"),
    url_name='person_deletion',)

organization_search_wizard = wizards.SearchWizard.as_view(
    [('general-organization_search', forms.OrganizationFormSelection)],
    label=_(u"Organization search"),
    url_name='organization_search',)

organization_creation_wizard = wizards.OrganizationWizard.as_view(
    [('identity-organization_creation', forms.OrganizationForm),
     ('final-organization_creation', FinalForm)],
    label=_(u"New organization"),
    url_name='organization_creation')

organization_modification_wizard = wizards.OrganizationModifWizard.as_view(
    [('selec-organization_modification', forms.OrganizationFormSelection),
     ('identity-organization_modification', forms.OrganizationForm),
     ('final-organization_modification', FinalForm)],
    label=_(u"Organization modification"),
    url_name='organization_modification')


def organization_modify(request, pk):
    organization_modification_wizard(request)
    wizards.OrganizationModifWizard.session_set_value(
        request, 'selec-organization_modification', 'pk', pk, reset=True)
    return redirect(
        reverse('organization_modification',
                kwargs={'step': 'identity-organization_modification'}))


organization_deletion_wizard = wizards.OrganizationDeletionWizard.as_view(
    [('selec-organization_deletion', forms.OrganizationFormSelection),
     ('final-organization_deletion', FinalDeleteForm)],
    label=_(u"Organization deletion"),
    url_name='organization_deletion',)

account_management_wizard = wizards.AccountWizard.as_view(
    [('selec-account_management', forms.PersonUserFormSelection),
     ('account-account_management', forms.AccountForm),
     ('final-account_management', forms.FinalAccountForm)],
    label=_(u"Account management"),
    url_name='account_management',)

account_deletion_wizard = wizards.IshtarUserDeletionWizard.as_view(
    [('selec-account_deletion', forms.AccountFormSelection),
     ('final-account_deletion', FinalDeleteForm)],
    label=_(u"Account deletion"),
    url_name='account_deletion',)


def get_autocomplete_generic(model, extra={'available': True}):
    def func(request):
        q = request.GET.get('term')
        query = Q(**extra)
        for q in q.split(' '):
            if not q:
                continue
            query = query & Q(label__icontains=q)
        limit = 20
        objects = model.objects.filter(query)[:limit]
        get_label = lambda x: x.full_label() if hasattr(x, 'full_label') \
            else unicode(x)
        data = json.dumps([{'id': obj.pk, 'value': get_label(obj)}
                           for obj in objects])
        return HttpResponse(data, mimetype='text/plain')
    return func


def hide_shortcut_menu(request):
    request.session['SHORTCUT_SHOW'] = 'off'
    return HttpResponse('OK', mimetype='text/plain')


def show_shortcut_menu(request):
    request.session['SHORTCUT_SHOW'] = 'on'
    return HttpResponse('OK', mimetype='text/plain')


def activate_all_search(request):
    request.session['SHORTCUT_SEARCH'] = 'all'
    return HttpResponse('OK', mimetype='text/plain')


def activate_own_search(request):
    request.session['SHORTCUT_SEARCH'] = 'own'
    return HttpResponse('OK', mimetype='text/plain')


def activate_advanced_shortcut_menu(request):
    if not hasattr(request.user, 'ishtaruser'):
        return HttpResponse('KO', mimetype='text/plain')
    request.user.ishtaruser.advanced_shortcut_menu = True
    request.user.ishtaruser.save()
    return HttpResponse('OK', mimetype='text/plain')


def activate_simple_shortcut_menu(request):
    if not hasattr(request.user, 'ishtaruser'):
        return HttpResponse('KO', mimetype='text/plain')
    request.user.ishtaruser.advanced_shortcut_menu = False
    request.user.ishtaruser.save()
    return HttpResponse('OK', mimetype='text/plain')


def shortcut_menu(request):
    profile = get_current_profile()
    CURRENT_ITEMS = []
    if profile.files:
        CURRENT_ITEMS.append((_(u"Archaeological file"), File))
    CURRENT_ITEMS.append((_(u"Operation"), Operation))
    if profile.context_record:
        CURRENT_ITEMS.append((_(u"Context record"), ContextRecord))
    if profile.find:
        CURRENT_ITEMS.append((_(u"Find"), Find))
    if profile.warehouse:
        CURRENT_ITEMS.append((_(u"Treatment request"), TreatmentFile))
        CURRENT_ITEMS.append((_(u"Treatment"), Treatment))
    if hasattr(request.user, 'ishtaruser') and \
            request.user.ishtaruser.advanced_shortcut_menu:
        dct = {
            'current_menu': [], 'menu': [],
            'SHORTCUT_SEARCH': request.session['SHORTCUT_SEARCH']
            if 'SHORTCUT_SEARCH' in request.session else 'own',
            'SHORTCUT_SHOW': request.session['SHORTCUT_SHOW']
            if 'SHORTCUT_SHOW' in request.session else 'on'
        }

        for lbl, model in CURRENT_ITEMS:
            model_name = model.SLUG
            current = model_name in request.session \
                and request.session[model_name]
            dct['menu'].append((
                lbl, model_name, current or 0,
                JQueryAutoComplete(
                    reverse('get-' + model.SLUG + '-shortcut'),
                    model).render(
                        model.SLUG + '-shortcut', value=current,
                        attrs={'id': 'current_' + model.SLUG})))
        return render_to_response(
            'ishtar/blocks/advanced_shortcut_menu.html',
            dct, context_instance=RequestContext(request))
    dct = {
        'current_menu': [],
        'SHORTCUT_SHOW': request.session['SHORTCUT_SHOW']
        if 'SHORTCUT_SHOW' in request.session else 'off'
    }
    current_selected_item = {}
    for lbl, model in CURRENT_ITEMS:
        new_selected_item = None
        model_name = model.SLUG
        cls = ''
        current = model_name in request.session and request.session[model_name]
        items = []
        current_items = []
        for item, shortmenu_class in model.get_owns(
                request.user, menu_filtr=current_selected_item, limit=100,
                values=['id', 'cached_label'], get_short_menu_class=True):
            pk = unicode(item['id'])
            if shortmenu_class == 'basket':
                pk = "basket-" + pk
            # prevent duplicates
            if pk in current_items:
                continue
            current_items.append(pk)
            selected = pk == current
            if selected:
                cls = shortmenu_class
                new_selected_item = pk
            items.append((pk, shortify(item['cached_label'], 60),
                          selected, shortmenu_class))
        # selected is not in owns - add it to the list
        if not new_selected_item and current:
            try:
                item = model.objects.get(pk=int(current))
                new_selected_item = item.pk
                items.append((item.pk, shortify(unicode(item), 60),
                              True, item.get_short_menu_class(item.pk)))
            except (model.DoesNotExist, ValueError):
                pass
        if items:
            dct['current_menu'].append((lbl, model_name, cls, items))
        if new_selected_item:
            current_selected_item[model_name] = new_selected_item
    return render_to_response('ishtar/blocks/shortcut_menu.html', dct,
                              context_instance=RequestContext(request))

CURRENT_ITEM_KEYS = (('file', File),
                     ('operation', Operation),
                     ('contextrecord', ContextRecord),
                     ('find', Find),
                     ('treatmentfile', TreatmentFile),
                     ('treatment', Treatment))
CURRENT_ITEM_KEYS_DICT = dict(CURRENT_ITEM_KEYS)


def get_current_items(request):
    currents = {}
    for key, model in CURRENT_ITEM_KEYS:
        currents[key] = None
        if key in request.session and request.session[key]:
            try:
                currents[key] = model.objects.get(pk=int(request.session[key]))
            except (ValueError, File.DoesNotExist):
                continue
    return currents


def unpin(request, item_type):
    if item_type not in ('find', 'contextrecord', 'operation', 'file',
                         'treatment', 'treatmentfile'):
        logger.warning("unpin unknow type: {}".format(item_type))
        return HttpResponse('nok')
    request.session['treatment'] = ''
    if item_type == 'treatment':
        return HttpResponse('ok')
    request.session['treatmentfile'] = ''
    if item_type == 'treatmentfile':
        return HttpResponse('ok')
    request.session['find'] = ''
    if item_type == 'find':
        return HttpResponse('ok')
    request.session['contextrecord'] = ''
    if item_type == 'contextrecord':
        return HttpResponse('ok')
    request.session['operation'] = ''
    if item_type == 'operation':
        return HttpResponse('ok')
    request.session['file'] = ''
    if item_type == 'file':
        return HttpResponse('ok')


def update_current_item(request, item_type=None, pk=None):
    if not item_type or not pk:
        if not request.is_ajax() and not request.method == 'POST':
            raise Http404
        item_type = request.POST['item']
        if 'value' in request.POST and 'item' in request.POST:
            request.session[item_type] = request.POST['value']
    else:
        request.session[item_type] = str(pk)
    request.session['SHORTCUT_SEARCH'] = 'all'

    currents = get_current_items(request)
    # re-init when descending item are not relevant
    if item_type == 'file' and currents['file'] and currents['operation'] and \
            currents['operation'].associated_file != currents['file']:
        request.session["operation"] = ''
        currents['operation'] = None
    if item_type in ('operation', 'file') and currents['contextrecord'] and \
            (not request.session.get("operation", None) or
             currents['contextrecord'].operation != currents['operation']):
        request.session["contextrecord"] = ''
        currents['contextrecord'] = None
    from archaeological_finds.models import Find
    if item_type in ('contextrecord', 'operation', 'file') and \
        currents['find'] and \
        (not request.session.get("contextrecord", None) or
         not Find.objects.filter(
             downstream_treatment__isnull=True,
             base_finds__context_record__pk=request.session["contextrecord"],
             pk=currents['find'].pk).count()):
        request.session["find"] = ''
        currents['find'] = None

    # re-init ascending item with relevant values
    if item_type == "find" and currents['find']:
        from archaeological_context_records.models import ContextRecord
        q = ContextRecord.objects.filter(
            base_finds__find__pk=currents['find'].pk)
        if q.count():
            currents['contextrecord'] = q.all()[0]
            request.session['contextrecord'] = str(
                currents['contextrecord'].pk)
    if item_type in ("find", 'contextrecord') and currents['contextrecord']:
        currents['operation'] = currents['contextrecord'].operation
        request.session['operation'] = str(currents['operation'].pk)
    if item_type in ("find", 'contextrecord', 'operation') and \
            currents['operation']:
        currents['file'] = currents['operation'].associated_file
        request.session['file'] = str(currents['file'].pk) if currents['file'] \
            else None
    return HttpResponse('ok')


def check_permission(request, action_slug, obj_id=None):
    if action_slug not in menu.items:
        # TODO
        return True
    if obj_id:
        return menu.items[action_slug].is_available(request.user, obj_id,
                                                    session=request.session)
    return menu.items[action_slug].can_be_available(request.user,
                                                    session=request.session)


def autocomplete_person_permissive(request, person_types=None,
                                   attached_to=None, is_ishtar_user=None):
    return autocomplete_person(
        request, person_types=person_types, attached_to=attached_to,
        is_ishtar_user=is_ishtar_user, permissive=True)


def autocomplete_person(request, person_types=None, attached_to=None,
                        is_ishtar_user=None, permissive=False):
    all_items = request.user.has_perm('ishtar_common.view_person',
                                      models.Person)
    own_items = False
    if not all_items:
        own_items = request.user.has_perm('ishtar_common.view_own_person',
                                          models.Person)
    if not all_items and not own_items or not request.GET.get('term'):
        return HttpResponse('[]', mimetype='text/plain')
    q = request.GET.get('term')
    limit = request.GET.get('limit', 20)
    try:
        limit = int(limit)
    except ValueError:
        return HttpResponseBadRequest()
    query = Q()
    for q in q.split(' '):
        qu = (Q(name__icontains=q) | Q(surname__icontains=q) |
              Q(email__icontains=q) | Q(attached_to__name__icontains=q))
        if permissive:
            qu = qu | Q(raw_name__icontains=q)
        query = query & qu
    if attached_to:
        query = query & Q(attached_to__pk__in=attached_to.split('_'))

    if person_types and unicode(person_types) != '0':
        try:
            typs = [int(tp) for tp in person_types.split('_') if tp]
            typ = models.PersonType.objects.filter(pk__in=typs).all()
            query = query & Q(person_types__in=typ)
        except (ValueError, ObjectDoesNotExist):
            pass
    if is_ishtar_user:
        query = query & Q(ishtaruser__isnull=False)
    if own_items:
        query &= models.Person.get_query_owns(request.user)
    persons = models.Person.objects.filter(query)[:limit]
    data = json.dumps([{'id': person.pk, 'value': unicode(person)}
                       for person in persons if person])
    return HttpResponse(data, mimetype='text/plain')


def autocomplete_department(request):
    if not request.GET.get('term'):
        return HttpResponse('[]', mimetype='text/plain')
    q = request.GET.get('term')
    q = unicodedata.normalize("NFKD", q).encode('ascii', 'ignore')
    query = Q()
    for q in q.split(' '):
        extra = (Q(label__icontains=q) | Q(number__istartswith=q))
        query = query & extra
    limit = 20
    departments = models.Department.objects.filter(query)[:limit]
    data = json.dumps([{'id': department.pk, 'value': unicode(department)}
                       for department in departments])
    return HttpResponse(data, mimetype='text/plain')


def autocomplete_town(request):
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    q = unicodedata.normalize("NFKD", q).encode('ascii', 'ignore')
    query = Q()
    for q in q.split(' '):
        extra = Q(name__icontains=q)
        if settings.COUNTRY == 'fr':
            extra |= Q(numero_insee__istartswith=q)
        query &= extra
    limit = 20
    towns = models.Town.objects.filter(query)[:limit]
    data = json.dumps([{'id': town.pk, 'value': unicode(town)}
                       for town in towns])
    return HttpResponse(data, mimetype='text/plain')


def autocomplete_advanced_town(request, department_id=None, state_id=None):
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    q = unicodedata.normalize("NFKD", q).encode('ascii', 'ignore')
    query = Q()
    for q in q.split(' '):
        extra = Q(name__icontains=q)
        if settings.COUNTRY == 'fr':
            extra = extra | Q(numero_insee__istartswith=q)
            if not department_id:
                extra = extra | Q(departement__label__istartswith=q)
        query = query & extra
    if department_id:
        query = query & Q(departement__number__iexact=department_id)
    if state_id:
        query = query & Q(departement__state__number__iexact=state_id)
    limit = 20
    towns = models.Town.objects.filter(query)[:limit]
    result = []
    for town in towns:
        val = town.name
        if hasattr(town, 'numero_insee'):
            val += " (%s)" % town.numero_insee
        result.append({'id': town.pk, 'value': val})
    data = json.dumps(result)
    return HttpResponse(data, mimetype='text/plain')


def department_by_state(request, state_id=''):
    if not state_id:
        data = []
    else:
        departments = models.Department.objects.filter(state__number=state_id)
        data = json.dumps([{'id': department.pk, 'number': department.number,
                            'value': unicode(department)}
                           for department in departments])
    return HttpResponse(data, mimetype='text/plain')


def format_val(val):
    if val is None:
        return u""
    if type(val) == bool:
        if val:
            return unicode(_(u"True"))
        else:
            return unicode(_(u"False"))
    return unicode(val)

HIERARCHIC_LEVELS = 5
HIERARCHIC_FIELDS = ['periods', 'period', 'unit', 'material_types',
                     'material_type', 'conservatory_state']


def get_item(model, func_name, default_name, extra_request_keys=[],
             base_request=None, bool_fields=[], reversed_bool_fields=[],
             dated_fields=[], associated_models=[], relative_session_names=[],
             specific_perms=[], own_table_cols=None, relation_types_prefix={}):
    """
    Generic treatment of tables
    """
    def func(request, data_type='json', full=False, force_own=False,
             col_names=None, **dct):
        available_perms = []
        if specific_perms:
            available_perms = specific_perms[:]
        EMPTY = ''
        if 'type' in dct:
            data_type = dct.pop('type')
        if not data_type:
            EMPTY = '[]'
            data_type = 'json'

        allowed, own = models.check_model_access_control(request, model,
                                                         available_perms)
        if not allowed:
            return HttpResponse(EMPTY, mimetype='text/plain')

        if force_own:
            own = True
        if full == 'shortcut' and 'SHORTCUT_SEARCH' in request.session and \
                request.session['SHORTCUT_SEARCH'] == 'own':
            own = True

        # get defaults from model
        if not extra_request_keys and hasattr(model, 'EXTRA_REQUEST_KEYS'):
            my_extra_request_keys = copy(model.EXTRA_REQUEST_KEYS)
        else:
            my_extra_request_keys = copy(extra_request_keys)
        if base_request is None and hasattr(model, 'BASE_REQUEST'):
            my_base_request = copy(model.BASE_REQUEST)
        elif base_request is not None:
            my_base_request = copy(base_request)
        else:
            my_base_request = {}
        if not bool_fields and hasattr(model, 'BOOL_FIELDS'):
            my_bool_fields = model.BOOL_FIELDS[:]
        else:
            my_bool_fields = bool_fields[:]
        if not reversed_bool_fields and hasattr(model, 'REVERSED_BOOL_FIELDS'):
            my_reversed_bool_fields = model.REVERSED_BOOL_FIELDS[:]
        else:
            my_reversed_bool_fields = reversed_bool_fields[:]
        if not dated_fields and hasattr(model, 'DATED_FIELDS'):
            my_dated_fields = model.DATED_FIELDS[:]
        else:
            my_dated_fields = dated_fields[:]
        if not associated_models and hasattr(model, 'ASSOCIATED_MODELS'):
            my_associated_models = model.ASSOCIATED_MODELS[:]
        else:
            my_associated_models = associated_models[:]
        if not relative_session_names and hasattr(model,
                                                  'RELATIVE_SESSION_NAMES'):
            my_relative_session_names = model.RELATIVE_SESSION_NAMES[:]
        else:
            my_relative_session_names = relative_session_names[:]
        if not relation_types_prefix and hasattr(model,
                                                 'RELATION_TYPES_PREFIX'):
            my_relation_types_prefix = copy(model.RELATION_TYPES_PREFIX)
        else:
            my_relation_types_prefix = copy(relation_types_prefix)

        fields = [model._meta.get_field_by_name(k)[0]
                  for k in model._meta.get_all_field_names()]
        request_keys = dict([
            (field.name,
             field.name + (hasattr(field, 'rel') and field.rel and '__pk'
                           or ''))
            for field in fields])
        for associated_model, key in my_associated_models:
            if type(associated_model) in (str, unicode):
                if associated_model not in globals():
                    continue
                associated_model = globals()[associated_model]
            associated_fields = [
                associated_model._meta.get_field_by_name(k)[0]
                for k in associated_model._meta.get_all_field_names()]
            request_keys.update(
                dict([(key + "__" + field.name,
                       key + "__" + field.name +
                       (hasattr(field, 'rel') and field.rel and '__pk' or ''))
                      for field in associated_fields]))
        request_keys.update(my_extra_request_keys)
        request_items = request.method == 'POST' and request.POST \
            or request.GET
        dct = my_base_request
        if full == 'shortcut':
            dct['cached_label__icontains'] = request.GET.get('term', None)
        and_reqs, or_reqs = [], []
        try:
            old = 'old' in request_items and int(request_items['old'])
        except ValueError:
            return HttpResponse('[]', mimetype='text/plain')

        # manage relations types
        if 'relation_types' not in my_relation_types_prefix:
            my_relation_types_prefix['relation_types'] = ''
        relation_types = {}
        for rtype_key in my_relation_types_prefix:
            relation_types[my_relation_types_prefix[rtype_key]] = set()
            for k in request_items:
                if k.startswith(rtype_key):
                    relation_types[my_relation_types_prefix[rtype_key]].add(
                        request_items[k])
                    continue

        for k in request_keys:
            val = request_items.get(k)
            if not val:
                continue
            req_keys = request_keys[k]
            if type(req_keys) not in (list, tuple):
                dct[req_keys] = val
                continue
            # multiple choice target
            reqs = Q(**{req_keys[0]: val})
            for req_key in req_keys[1:]:
                q = Q(**{req_key: val})
                reqs |= q
            and_reqs.append(reqs)
        pinned_search = ""
        if 'submited' not in request_items and full != 'shortcut':
            # default search
            # an item is selected in the default menu
            if default_name in request.session and \
               request.session[default_name]:
                value = request.session[default_name]
                if 'basket-' in value:
                    try:
                        dct = {"basket__pk":
                               request.session[default_name].split('-')[-1]}
                        pinned_search = unicode(FindBasket.objects.get(
                            pk=dct["basket__pk"]))
                    except FindBasket.DoesNotExist:
                        pass
                else:
                    try:
                        dct = {"pk": request.session[default_name]}
                        pinned_search = unicode(model._meta.verbose_name)\
                            + u" - " +  unicode(
                                model.objects.get(pk=dct["pk"]))
                    except model.DoesNotExist:
                        pass
            elif dct == (base_request or {}):
                # a parent item may be selected in the default menu
                for name, key in my_relative_session_names:
                    if name in request.session and request.session[name] \
                            and 'basket-' not in request.session[name] \
                            and name in CURRENT_ITEM_KEYS_DICT:
                        up_model = CURRENT_ITEM_KEYS_DICT[name]
                        try:
                            dct.update({key: request.session[name]})
                            pinned_search = unicode(up_model._meta.verbose_name)\
                                + u" - " + unicode(
                                    up_model.objects.get(pk=dct[key]))
                            break
                        except up_model.DoesNotExist:
                            pass
            if (not dct or data_type == 'csv') \
                    and func_name in request.session:
                dct = request.session[func_name]
        else:
            request.session[func_name] = dct
        for k in (list(my_bool_fields) + list(my_reversed_bool_fields)):
            if k in dct:
                if dct[k] == u"1":
                    dct.pop(k)
                else:
                    dct[k] = dct[k] == u"2" and True or False
                    if k in my_reversed_bool_fields:
                        dct[k] = not dct[k]
                    # check also for empty value with image field
                    field_name = k.split('__')[0]
                    # TODO: can be improved in later version of Django
                    try:
                        c_field = model._meta.get_field(field_name)
                        if k.endswith('__isnull') and \
                           isinstance(c_field, ImageField):
                            if dct[k]:
                                or_reqs.append(
                                    (k, {k.split('__')[0] + '__exact': ''}))
                            else:
                                dct[k.split('__')[0] + '__regex'] = '.{1}.*'
                    except FieldDoesNotExist:
                        pass
        for k in my_dated_fields:
            if k in dct:
                if not dct[k]:
                    dct.pop(k)
                try:
                    items = dct[k].split('/')
                    assert len(items) == 3
                    dct[k] = datetime.date(*map(lambda x: int(x),
                                                reversed(items)))\
                                     .strftime('%Y-%m-%d')
                except AssertionError:
                    dct.pop(k)
        # manage hierarchic conditions
        for req in dct.copy():
            for k_hr in HIERARCHIC_FIELDS:
                if type(req) in (list, tuple):
                    val = dct.pop(req)
                    q = None
                    for idx, r in enumerate(req):
                        if not idx:
                            q = Q(**{r: val})
                        else:
                            q |= Q(**{r: val})
                    and_reqs.append(q)
                    break
                elif req.endswith(k_hr + '__pk'):
                    val = dct.pop(req)
                    reqs = Q(**{req: val})
                    req = req[:-2] + '__'
                    for idx in xrange(HIERARCHIC_LEVELS):
                        req = req[:-2] + 'parent__pk'
                        q = Q(**{req: val})
                        reqs |= q
                    and_reqs.append(reqs)
                    break
        query = Q(**dct)
        for k, or_req in or_reqs:
            alt_dct = dct.copy()
            alt_dct.pop(k)
            alt_dct.update(or_req)
            query |= Q(**alt_dct)

        for rtype_prefix in relation_types:
            vals = list(relation_types[rtype_prefix])
            if not vals:
                continue
            alt_dct = {
                rtype_prefix + 'right_relations__relation_type__pk__in': vals}
            for k in dct:
                val = dct[k]
                if rtype_prefix:
                    # only get conditions related to the object
                    if rtype_prefix not in k:
                        continue
                    # tricky: reconstruct the key to make sense - remove the
                    # prefix from the key
                    k = k[0:k.index(rtype_prefix)] + k[
                        k.index(rtype_prefix) + len(rtype_prefix):]
                if k.endswith('year'):
                    k += '__exact'
                alt_dct[rtype_prefix + 'right_relations__right_record__' + k] =\
                    val
            if not dct:
                # fake condition to trick Django (1.4): without it only the
                # alt_dct is managed
                query &= Q(pk__isnull=False)
            query |= Q(**alt_dct)
            for k, or_req in or_reqs:
                altor_dct = alt_dct.copy()
                altor_dct.pop(k)
                for j in or_req:
                    val = or_req[j]
                    if j == 'year':
                        j = 'year__exact'
                    altor_dct[
                        rtype_prefix + 'right_relations__right_record__' + j] =\
                        val
                query |= Q(**altor_dct)

        if own:
            query = query & model.get_query_owns(request.user)

        for and_req in and_reqs:
            query = query & and_req

        # manage hierarchic in shortcut menu
        if full == 'shortcut':
            ASSOCIATED_ITEMS = {
                Operation: (File, 'associated_file__pk'),
                ContextRecord: (Operation, 'operation__pk'),
                Find: (ContextRecord, 'base_finds__context_record__pk'),
            }
            if model in ASSOCIATED_ITEMS:
                upper_model, upper_key = ASSOCIATED_ITEMS[model]
                model_name = upper_model.SLUG
                current = model_name in request.session \
                    and request.session[model_name]
                if current:
                    dct = {upper_key: current}
                    query &= Q(**dct)

        items = model.objects.filter(query).distinct()
        # print(items.query)

        # table cols
        if own_table_cols:
            table_cols = own_table_cols
        else:
            if full:
                table_cols = [field.name for field in model._meta.fields
                              if field.name not in PRIVATE_FIELDS]
                table_cols += [field.name for field in model._meta.many_to_many
                               if field.name not in PRIVATE_FIELDS]
                if hasattr(model, 'EXTRA_FULL_FIELDS'):
                    table_cols += model.EXTRA_FULL_FIELDS
            else:
                table_cols = model.TABLE_COLS
        query_table_cols = []
        for cols in table_cols:
            if type(cols) not in (list, tuple):
                cols = [cols]
            for col in cols:
                query_table_cols += col.split('|')

        # contextual (full, simple, etc.) col
        contxt = full and 'full' or 'simple'
        if hasattr(model, 'CONTEXTUAL_TABLE_COLS') and \
                contxt in model.CONTEXTUAL_TABLE_COLS:
            for idx, col in enumerate(table_cols):
                if col in model.CONTEXTUAL_TABLE_COLS[contxt]:
                    query_table_cols[idx] = \
                        model.CONTEXTUAL_TABLE_COLS[contxt][col]
        if full == 'shortcut':
            query_table_cols = ['cached_label']
            table_cols = ['cached_label']

        # manage sort tables
        manual_sort_key = None
        order = request_items.get('sord')
        sign = order and order == u'desc' and "-" or ''

        q = request_items.get('sidx')
        if q == '__default__' and model._meta.ordering:
            orders = [sign + k for k in model._meta.ordering]
            items = items.order_by(*orders)
        elif q and q in request_keys:
            ks = request_keys[q]
            if type(ks) not in (list, tuple):
                ks = [ks]
            orders = []
            for k in ks:
                if k.endswith("__pk"):
                    k = k[:-len("__pk")] + "__label"
                if '__' in k:
                    k = k.split('__')[0]
                orders.append(sign + k)
            items = items.order_by(*orders)
        elif q:
            for ke in query_table_cols:
                if type(ke) in (list, tuple):
                    ke = ke[0]
                if ke.endswith(q):
                    manual_sort_key = ke
                    logger.warning("**WARN get_item - {}**: manual sort key '{"
                                   "}'".format(func_name, q))
                    break
            if not manual_sort_key and model._meta.ordering:
                orders = [sign + k for k in model._meta.ordering]
                items = items.order_by(*orders)
        # pager management
        start, end = 0, None
        page_nb = 1
        try:
            row_nb = int(request_items.get('rows'))
        except (ValueError, TypeError):
            row_nb = None
        if row_nb:
            try:
                page_nb = int(request_items.get('page'))
                assert page_nb >= 1
            except (ValueError, AssertionError):
                pass
            start = (page_nb - 1) * row_nb
            end = page_nb * row_nb
        if full == 'shortcut':
            start = 0
            end = 20
        items_nb = items.count()
        if manual_sort_key:
            items = items.all()
        else:
            items = items[start:end]

        datas = []
        if old:
            items = [item.get_previous(old) for item in items]
        c_ids = []
        for item in items:
            # manual deduplicate when distinct is not enough
            if item.pk in c_ids:
                continue
            c_ids.append(item.pk)
            data = [item.pk]
            for keys in query_table_cols:
                if type(keys) not in (list, tuple):
                    keys = [keys]
                my_vals = []
                for k in keys:
                    if hasattr(model, 'EXTRA_REQUEST_KEYS') \
                            and k in model.EXTRA_REQUEST_KEYS:
                        k = model.EXTRA_REQUEST_KEYS[k]
                        if type(k) in (list, tuple):
                            k = k[0]
                    for filtr in ('__icontains', '__contains'):
                        if k.endswith(filtr):
                            k = k[:len(k) - len(filtr)]
                    vals = [item]
                    # foreign key may be divided by "." or "__"
                    splitted_k = []
                    for ky in k.split('.'):
                        if '__' in ky:
                            splitted_k += ky.split('__')
                        else:
                            splitted_k.append(ky)
                    for ky in splitted_k:
                        new_vals = []
                        for val in vals:
                            if hasattr(val, 'all'):  # manage related objects
                                val = list(val.all())
                                for v in val:
                                    v = getattr(v, ky)
                                    if callable(v):
                                        v = v()
                                    if hasattr(v, 'url'):
                                        v = request.is_secure() and \
                                            'https' or 'http' + '://' + \
                                            request.get_host() + v.url
                                    new_vals.append(v)
                            elif val:
                                try:
                                    val = getattr(val, ky)
                                    if callable(val):
                                        val = val()
                                    if hasattr(val, 'url'):
                                        val = request.is_secure() and \
                                            'https' or 'http' + '://' + \
                                            request.get_host() + val.url
                                    new_vals.append(val)
                                except AttributeError:
                                    # must be a query key such as "contains"
                                    pass
                        vals = new_vals
                    # manage last related objects
                    if vals and hasattr(vals[0], 'all'):
                        new_vals = []
                        for val in vals:
                            new_vals += list(val.all())
                        vals = new_vals
                    if not my_vals:
                        my_vals = [format_val(va) for va in vals]
                    else:
                        new_vals = []
                        if not vals:
                            for idx, my_v in enumerate(my_vals):
                                new_vals.append(u"{}{}{}".format(
                                    my_v, u' - ', ''))
                        else:
                            for idx, v in enumerate(vals):
                                new_vals.append(u"{}{}{}".format(
                                    vals[idx], u' - ', format_val(v)))
                        my_vals = new_vals[:]
                data.append(u" & ".join(my_vals) or u"")
            datas.append(data)
        if manual_sort_key:
            # +1 because the id is added as a first col
            idx_col = None
            if manual_sort_key in query_table_cols:
                idx_col = query_table_cols.index(manual_sort_key) + 1
            else:
                for idx, col in enumerate(query_table_cols):
                    if type(col) in (list, tuple) and \
                            manual_sort_key in col:
                        idx_col = idx + 1
            if idx_col is not None:
                datas = sorted(datas, key=lambda x: x[idx_col])
                if sign == '-':
                    datas = reversed(datas)
                datas = list(datas)[start:end]
        link_template = "<a class='display_details' href='#' "\
            "onclick='load_window(\"%s\")'>"\
            "<i class=\"fa fa-info-circle\" aria-hidden=\"true\"></i></a>"
        link_ext_template = '<a href="{}" target="_blank">{}</a>'
        if data_type == "json":
            rows = []
            for data in datas:
                try:
                    lnk = link_template % reverse('show-' + default_name,
                                                  args=[data[0], ''])
                except NoReverseMatch:
                    logger.warning(
                        '**WARN "show-' + default_name + '" args ('
                        + unicode(data[0]) + ") url not available")
                    lnk = ''
                res = {'id': data[0], 'link': lnk}
                for idx, value in enumerate(data[1:]):
                    if value:
                        table_col = table_cols[idx]
                        if type(table_col) not in (list, tuple):
                            table_col = [table_col]
                        tab_cols = []
                        # foreign key may be divided by "." or "__"
                        for tc in table_col:
                            if '.' in tc:
                                tab_cols += tc.split('.')
                            elif '__' in tc:
                                tab_cols += tc.split('__')
                            else:
                                tab_cols.append(tc)
                        k = "__".join(tab_cols)
                        if hasattr(model, 'COL_LINK') and k in model.COL_LINK:
                            value = link_ext_template.format(value, value)
                        res[k] = value
                if full == 'shortcut' and 'cached_label' in res:
                    res['value'] = res.pop('cached_label')
                rows.append(res)
            if full == 'shortcut':
                data = json.dumps(rows)
            else:
                data = json.dumps({
                    "records": items_nb,
                    "rows": rows,
                    "pinned-search": pinned_search,
                    "page": page_nb,
                    "total": (items_nb / row_nb + 1) if row_nb else items_nb,
                })
            return HttpResponse(data, mimetype='text/plain')
        elif data_type == "csv":
            response = HttpResponse(mimetype='text/csv')
            n = datetime.datetime.now()
            filename = u'%s_%s.csv' % (default_name,
                                       n.strftime('%Y%m%d-%H%M%S'))
            response['Content-Disposition'] = 'attachment; filename=%s'\
                                              % filename
            writer = csv.writer(response, **CSV_OPTIONS)
            if col_names:
                col_names = [name.encode(ENCODING, errors='replace')
                             for name in col_names]
            else:
                col_names = []
                for field_name in table_cols:
                    if type(field_name) in (list, tuple):
                        field_name = u" & ".join(field_name)
                    if hasattr(model, 'COL_LABELS') and\
                            field_name in model.COL_LABELS:
                        field = model.COL_LABELS[field_name]
                        col_names.append(unicode(field).encode(ENCODING))
                        continue
                    else:
                        try:
                            field = model._meta.get_field(field_name)
                        except:
                            col_names.append(u"".encode(ENCODING))
                            logger.warning(
                                "**WARN get_item - csv export**: no col name "
                                "for {}\nadd explicit label to "
                                "COL_LABELS attribute of "
                                "{}".format(field_name, model))
                            continue
                        col_names.append(
                            unicode(field.verbose_name).encode(ENCODING))
            writer.writerow(col_names)
            for data in datas:
                row, delta = [], 0
                # regroup cols with join "|"
                for idx, col_name in enumerate(table_cols):
                    val = data[1:][idx + delta].encode(
                        ENCODING, errors='replace')
                    if col_name and "|" in col_name[0]:
                        for delta_idx in range(len(col_name[0].split('|')) - 1):
                            delta += 1
                            val += data[1:][idx + delta].encode(
                                ENCODING, errors='replace')
                    row.append(val)
                writer.writerow(row)
            return response
        return HttpResponse('{}', mimetype='text/plain')

    return func


def get_by_importer(request, slug, data_type='json', full=False,
                    force_own=False, **dct):
    q = models.ImporterType.objects.filter(slug=slug)
    if not q.count():
        res = ''
        if data_type == "json":
            res = '{}'
        return HttpResponse(res, mimetype='text/plain')
    imp = q.all()[0].get_importer_class()
    cols, col_names = [], []
    for formater in imp.LINE_FORMAT:
        if not formater:
            continue
        cols.append(formater.export_field_name)
        col_names.append(formater.label)
    obj_name = imp.OBJECT_CLS.__name__.lower()
    return get_item(
        imp.OBJECT_CLS, 'get_' + obj_name, obj_name, own_table_cols=cols
    )(request, data_type, full, force_own, col_names=col_names, **dct)


def display_item(model, extra_dct=None, show_url=None):
    def func(request, pk, **dct):
        if show_url:
            dct['show_url'] = "/{}{}/".format(show_url, pk)
        else:
            dct['show_url'] = "/show-{}/{}/".format(model.SLUG, pk)
        return render_to_response('ishtar/display_item.html', dct,
                                  context_instance=RequestContext(request))
    return func


def show_item(model, name, extra_dct=None):
    def func(request, pk, **dct):
        allowed, own = models.check_model_access_control(request, model)
        if not allowed:
            return HttpResponse('', content_type="application/xhtml")
        q = model.objects
        if own:
            query_own = model.get_query_owns(request.user)
            if query_own:
                q = q.filter(query_own)
        try:
            item = q.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse('NOK')
        doc_type = 'type' in dct and dct.pop('type')
        url_name = u"/".join(reverse('show-' + name, args=['0', '']
                                     ).split('/')[:-2]) + u"/"
        dct['CURRENCY'] = get_current_profile().currency
        dct['ENCODING'] = settings.ENCODING
        dct['current_window_url'] = url_name
        date = None
        if 'date' in dct:
            date = dct.pop('date')
        dct['window_id'] = "%s-%d-%s" % (
            name, item.pk, datetime.datetime.now().strftime('%M%s'))
        if hasattr(item, 'history'):
            if date:
                try:
                    date = datetime.datetime.strptime(date,
                                                      '%Y-%m-%dT%H:%M:%S.%f')
                    item = item.get_previous(date=date)
                    assert item is not None
                except (ValueError, AssertionError):
                    return HttpResponse(None, mimetype='text/plain')
                dct['previous'] = item._previous
                dct['next'] = item._next
            else:
                historized = item.history.all()
                if historized:
                    item.history_date = historized[0].history_date
                if len(historized) > 1:
                    dct['previous'] = historized[1].history_date
        dct['item'], dct['item_name'] = item, name
        # add context
        if extra_dct:
            dct.update(extra_dct(request, item))
        context_instance = RequestContext(request)
        context_instance.update(dct)
        context_instance['output'] = 'html'
        if hasattr(item, 'history_object'):
            filename = item.history_object.associated_filename
        else:
            filename = item.associated_filename
        if doc_type == "odt" and settings.ODT_TEMPLATE:
            tpl = loader.get_template('ishtar/sheet_%s.html' % name)
            context_instance['output'] = 'ODT'
            content = tpl.render(context_instance)
            try:
                tidy_options = {'output-xhtml': 1, 'indent': 1,
                                'tidy-mark': 0, 'doctype': 'auto',
                                'add-xml-decl': 1, 'wrap': 1}
                html, errors = tidy(content, options=tidy_options)
                html = html.encode('utf-8').replace("&nbsp;", "&#160;")
                html = re.sub('<pre([^>]*)>\n', '<pre\\1>', html)

                odt = NamedTemporaryFile()
                options = optparse.Values()
                options.with_network = True
                for k, v in (('input', ''),
                             ('output', odt.name),
                             ('template', settings.ODT_TEMPLATE),
                             ('with_network', True),
                             ('top_header_level', 1),
                             ('img_width', '8cm'),
                             ('img_height', '6cm'),
                             ('verbose', False),
                             ('replace_keyword', 'ODT-INSERT'),
                             ('cut_start', 'ODT-CUT-START'),
                             ('htmlid', None),
                             ('url', "#")):
                    setattr(options, k, v)
                odtfile = xhtml2odt.ODTFile(options)
                odtfile.open()
                odtfile.import_xhtml(html)
                odtfile = odtfile.save()
            except xhtml2odt.ODTExportError:
                return HttpResponse(content, content_type="application/xhtml")
            response = HttpResponse(
                mimetype='application/vnd.oasis.opendocument.text')
            response['Content-Disposition'] = 'attachment; filename=%s.odt' % \
                                              filename
            response.write(odtfile)
            return response
        elif doc_type == 'pdf':
            tpl = loader.get_template('ishtar/sheet_%s_pdf.html' % name)
            context_instance['output'] = 'PDF'
            content = tpl.render(context_instance)
            result = StringIO.StringIO()
            html = content.encode('utf-8')
            html = html.replace("<table", "<pdf:nextpage/><table repeat='1'")
            pdf = pisa.pisaDocument(StringIO.StringIO(html), result,
                                    encoding='utf-8')
            response = HttpResponse(result.getvalue(),
                                    mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s.pdf' % \
                                              filename
            if not pdf.err:
                return response
            return HttpResponse(content, content_type="application/xhtml")
        else:
            tpl = loader.get_template('ishtar/sheet_%s_window.html' % name)
            content = tpl.render(context_instance)
            return HttpResponse(content, content_type="application/xhtml")
    return func


def revert_item(model):
    def func(request, pk, date, **dct):
        try:
            item = model.objects.get(pk=pk)
            date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
            item.rollback(date)
        except (ObjectDoesNotExist, ValueError, HistoryError):
            return HttpResponse(None, mimetype='text/plain')
        return HttpResponse("True", mimetype='text/plain')
    return func


def autocomplete_organization(request, orga_type=None):
    if (not request.user.has_perm('ishtar_common.view_organization',
        models.Organization) and
        not request.user.has_perm('ishtar_common.view_own_organization',
                                  models.Organization)
       and not request.user.ishtaruser.has_right(
            'person_search', session=request.session)):
        return HttpResponse('[]', mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse('[]', mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        extra = Q(name__icontains=q)
        query = query & extra
    if orga_type:
        try:
            typs = [int(tp) for tp in orga_type.split('_') if tp]
            typ = models.OrganizationType.objects.filter(pk__in=typs).all()
            query = query & Q(organization_type__in=typ)
        except (ValueError, ObjectDoesNotExist):
            pass
    limit = 15
    organizations = models.Organization.objects.filter(query)[:limit]
    data = json.dumps([{'id': org.pk, 'value': unicode(org)}
                       for org in organizations])
    return HttpResponse(data, mimetype='text/plain')


def autocomplete_author(request):
    if not request.user.has_perm('ishtar_common.view_author', models.Author)\
       and not request.user.has_perm('ishtar_common.view_own_author',
                                     models.Author):
        return HttpResponse('[]', mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse('[]', mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q in q.split(' '):
        extra = Q(person__name__icontains=q) | \
            Q(person__surname__icontains=q) | \
            Q(person__email__icontains=q) | \
            Q(author_type__label__icontains=q)
        query = query & extra
    limit = 15
    authors = models.Author.objects.filter(query)[:limit]
    data = json.dumps([{'id': author.pk, 'value': unicode(author)}
                       for author in authors])
    return HttpResponse(data, mimetype='text/plain')


def new_item(model, frm, many=False):
    def func(request, parent_name, limits=''):
        model_name = model._meta.object_name
        if not check_permission(request, 'add_' + model_name.lower()):
            not_permitted_msg = ugettext(u"Operation not permitted.")
            return HttpResponse(not_permitted_msg)
        dct = {'title': unicode(_(u'New %s' % model_name.lower())),
               'many': many}
        if request.method == 'POST':
            dct['form'] = frm(request.POST, limits=limits)
            if dct['form'].is_valid():
                new_item = dct['form'].save(request.user)
                dct['new_item_label'] = unicode(new_item)
                dct['new_item_pk'] = new_item.pk
                dct['parent_name'] = parent_name
                dct['parent_pk'] = parent_name
                if dct['parent_pk'] and '_select_' in dct['parent_pk']:
                    parents = dct['parent_pk'].split('_')
                    dct['parent_pk'] = "_".join([parents[0]] + parents[2:])
                return render_to_response(
                    'window.html', dct,
                    context_instance=RequestContext(request))
        else:
            dct['form'] = frm(limits=limits)
        return render_to_response('window.html', dct,
                                  context_instance=RequestContext(request))
    return func

new_person = new_item(models.Person, forms.PersonForm)
new_person_noorga = new_item(models.Person, forms.NoOrgaPersonForm)
new_organization = new_item(models.Organization, forms.OrganizationForm)
show_organization = show_item(models.Organization, 'organization')
get_organization = get_item(models.Organization, 'get_organization',
                            'organization')
new_author = new_item(models.Author, forms.AuthorForm)
show_person = show_item(models.Person, 'person')

get_person = get_item(models.Person, 'get_person', 'person')

get_ishtaruser = get_item(models.IshtarUser, 'get_ishtaruser', 'ishtaruser')


def action(request, action_slug, obj_id=None, *args, **kwargs):
    """
    Action management
    """
    if not check_permission(request, action_slug, obj_id):
        not_permitted_msg = ugettext(u"Operation not permitted.")
        return HttpResponse(not_permitted_msg)
    request.session['CURRENT_ACTION'] = action_slug
    dct = {}
    globals_dct = globals()
    if action_slug in globals_dct:
        return globals_dct[action_slug](request, dct, obj_id, *args, **kwargs)
    return render_to_response('index.html', dct,
                              context_instance=RequestContext(request))


def dashboard_main(request, dct, obj_id=None, *args, **kwargs):
    """
    Main dashboard
    """
    app_list = []
    profile = models.get_current_profile()
    if profile.files:
        app_list.append((_(u"Archaeological files"), 'files'))
    app_list.append((_(u"Operations"), 'operations'))
    if profile.context_record:
        app_list.append((_(u"Context records"), 'contextrecords'))
    if profile.find:
        app_list.append((_(u"Finds"), 'finds'))
    if profile.warehouse:
        app_list.append((_(u"Treatment requests"), 'treatmentfiles'))
        app_list.append((_(u"Treatments"), 'treatments'))
    dct = {'app_list': app_list}
    return render_to_response('ishtar/dashboards/dashboard_main.html', dct,
                              context_instance=RequestContext(request))

DASHBOARD_FORMS = {
    'files': DashboardFormFile, 'operations': DashboardFormOpe,
    'treatments': DashboardTreatmentForm,
    'treatmentfiles': DashboardTreatmentFileForm
}


def dashboard_main_detail(request, item_name):
    """
    Specific tab of the main dashboard
    """
    if item_name == 'users':
        dct = {'ishtar_users': models.UserDashboard()}
        return render_to_response(
            'ishtar/dashboards/dashboard_main_detail_users.html',
            dct, context_instance=RequestContext(request))
    form = None
    slicing, date_source, fltr, show_detail = 'year', None, {}, False
    profile = models.get_current_profile()
    has_form = (item_name == 'files' and profile.files) \
        or item_name == 'operations' \
        or (item_name in ('treatmentfiles', 'treatments')
            and profile.warehouse)
    if has_form:
        slicing = 'month'
    if item_name in DASHBOARD_FORMS:
        if request.method == 'POST':
            form = DASHBOARD_FORMS[item_name](request.POST)
            if form.is_valid():
                slicing = form.cleaned_data['slicing']
                fltr = form.get_filter()
                if hasattr(form, 'get_date_source'):
                    date_source = form.get_date_source()
                if hasattr(form, 'get_show_detail'):
                    show_detail = form.get_show_detail()
        else:
            form = DASHBOARD_FORMS[item_name]()
    lbl, dashboard = None, None
    dashboard_kwargs = {}
    if has_form:
        dashboard_kwargs = {'slice': slicing, 'fltr': fltr,
                            'show_detail': show_detail}
        # date_source is only relevant when the form has set one
        if date_source:
            dashboard_kwargs['date_source'] = date_source
    if item_name == 'files' and profile.files:
        lbl, dashboard = (_(u"Archaeological files"),
                          models.Dashboard(File, **dashboard_kwargs))
    elif item_name == 'operations':
        from archaeological_operations.models import Operation
        lbl, dashboard = (_(u"Operations"),
                          models.Dashboard(Operation, **dashboard_kwargs))
    elif item_name == 'contextrecords' and profile.context_record:
        lbl, dashboard = (
            _(u"Context records"),
            models.Dashboard(ContextRecord, slice=slicing, fltr=fltr))
    elif item_name == 'finds' and profile.find:
        lbl, dashboard = (_(u"Finds"), models.Dashboard(Find,
                                                        slice=slicing,
                                                        fltr=fltr))
    elif item_name == 'treatmentfiles' and profile.warehouse:
        lbl, dashboard = (
            _(u"Treatment requests"),
            models.Dashboard(TreatmentFile, **dashboard_kwargs))
    elif item_name == 'treatments' and profile.warehouse:
        if 'date_source' not in dashboard_kwargs:
            dashboard_kwargs['date_source'] = 'start'
        lbl, dashboard = (
            _(u"Treatments"),
            models.Dashboard(Treatment, **dashboard_kwargs))
    if not lbl:
        raise Http404
    dct = {'lbl': lbl, 'dashboard': dashboard,
           'item_name': item_name.replace('-', '_'),
           'VALUE_QUOTE': '' if slicing == "year" else "'",
           'form': form, 'slicing': slicing}
    n = datetime.datetime.now()
    dct['unique_id'] = dct['item_name'] + "_" + \
        '%d_%d_%d' % (n.minute, n.second, n.microsecond)
    return render_to_response('ishtar/dashboards/dashboard_main_detail.html',
                              dct, context_instance=RequestContext(request))


def reset_wizards(request):
    # dynamically execute each reset_wizards of each ishtar app
    for app in settings.INSTALLED_APPS:
        if app == 'ishtar_common':
            # no need for infinite recursion
            continue
        try:
            module = __import__(app)
        except ImportError:
            continue
        if hasattr(module, 'views') and hasattr(module.views, 'reset_wizards'):
            module.views.reset_wizards(request)
    return redirect(reverse('start'))

ITEM_PER_PAGE = 20


def merge_action(model, form, key):
    def merge(request, page=1):
        current_url = key + '_merge'
        if not page:
            page = 1
        page = int(page)
        FormSet = modelformset_factory(
            model.merge_candidate.through, form=form,
            formset=forms.MergeFormSet, extra=0)
        q = model.merge_candidate.through.objects
        context = {'current_url': current_url,
                   'current_page': page,
                   'max_page': q.count() / ITEM_PER_PAGE}
        if page < context["max_page"]:
            context['next_page'] = page + 1
        if page > 1:
            context['previous_page'] = page - 1

        item_nb = page * ITEM_PER_PAGE
        item_nb_1 = item_nb + ITEM_PER_PAGE
        from_key = 'from_' + key
        to_key = 'to_' + key
        queryset = q.all().order_by(from_key + '__name')[item_nb:item_nb_1]
        FormSet.from_key = from_key
        FormSet.to_key = to_key
        if request.method == 'POST':
            context['formset'] = FormSet(request.POST, queryset=queryset)
            if context['formset'].is_valid():
                context['formset'].merge()
                return redirect(reverse(current_url, kwargs={'page': page}))
        else:
            context['formset'] = FormSet(queryset=queryset)
        return render_to_response(
            'ishtar/merge_' + key + '.html', context,
            context_instance=RequestContext(request))

    return merge

person_merge = merge_action(models.Person, forms.MergePersonForm, 'person')
organization_merge = merge_action(
    models.Organization,
    forms.MergeOrganizationForm,
    'organization'
)


class IshtarMixin(object):
    page_name = u""

    def get_context_data(self, **kwargs):
        context = super(IshtarMixin, self).get_context_data(**kwargs)
        context['page_name'] = self.page_name
        return context


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)
        if kwargs.get('pk') and not self.request.user.is_staff and \
           not str(kwargs['pk']) == str(self.request.user.company.pk):
            return redirect(reverse('index'))
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class AdminLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(reverse('start'))
        return super(AdminLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class DisplayItemView(IshtarMixin, LoginRequiredMixin, TemplateView):
    template_name = 'ishtar/display_item.html'

    def get_context_data(self, *args, **kwargs):
        data = super(DisplayItemView, self).get_context_data(*args, **kwargs)
        pk = unicode(kwargs.get('pk')) + '/'
        item_url = '/show-' + kwargs.get('item_type')
        data['show_url'] = item_url + "/" + pk
        return data


class GlobalVarEdit(IshtarMixin, AdminLoginRequiredMixin, ModelFormSetView):
    template_name = 'ishtar/formset.html'
    model = models.GlobalVar
    extra = 1
    can_delete = True
    page_name = _(u"Global variables")
    fields = ['slug', 'value', 'description']


class NewImportView(IshtarMixin, LoginRequiredMixin, CreateView):
    template_name = 'ishtar/form.html'
    model = models.Import
    form_class = forms.NewImportForm
    page_name = _(u"New import")

    def get_success_url(self):
        return reverse('current_imports')

    def form_valid(self, form):
        user = models.IshtarUser.objects.get(pk=self.request.user.pk)
        self.object = form.save(user=user)
        return HttpResponseRedirect(self.get_success_url())


class ImportListView(IshtarMixin, LoginRequiredMixin, ListView):
    template_name = 'ishtar/import_list.html'
    model = models.Import
    page_name = _(u"Current imports")
    current_url = 'current_imports'

    def get_queryset(self):
        q = self.model.objects.exclude(state='AC')
        if self.request.user.is_superuser:
            return q.order_by('-creation_date')
        user = models.IshtarUser.objects.get(pk=self.request.user.pk)
        return q.filter(user=user).order_by('-creation_date')

    def post(self, request, *args, **kwargs):
        for field in request.POST:
            if not field.startswith('import-action-') or \
               not request.POST[field]:
                continue
            # prevent forged forms
            try:
                imprt = models.Import.objects.get(pk=int(field.split('-')[-1]))
            except (models.Import.DoesNotExist, ValueError):
                continue
            if not self.request.user.is_superuser:
                # user can only edit his own imports
                user = models.IshtarUser.objects.get(pk=self.request.user.pk)
                if imprt.user != user:
                    continue
            action = request.POST[field]
            if action == 'D':
                return HttpResponseRedirect(reverse('import_delete',
                                                    kwargs={'pk': imprt.pk}))
            elif action == 'A':
                imprt.initialize()
            elif action == 'I':
                imprt.importation()
            elif action == 'AC':
                imprt.archive()
        return HttpResponseRedirect(reverse(self.current_url))


class ImportOldListView(ImportListView):
    page_name = _(u"Old imports")
    current_url = 'old_imports'

    def get_queryset(self):
        q = self.model.objects.filter(state='AC')
        if self.request.user.is_superuser:
            return q.order_by('-creation_date')
        user = models.IshtarUser.objects.get(pk=self.request.user.pk)
        return q.filter(user=user).order_by('-creation_date')


class ImportLinkView(IshtarMixin, LoginRequiredMixin, ModelFormSetView):
    template_name = 'ishtar/formset.html'
    model = models.TargetKey
    page_name = _(u"Link unmatched items")
    extra = 0
    form_class = forms.TargetKeyForm

    def get_queryset(self):
        return self.model.objects.filter(
            is_set=False, associated_import=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('current_imports')


class ImportDeleteView(IshtarMixin, LoginRequiredMixin, DeleteView):
    template_name = 'ishtar/import_delete.html'
    model = models.Import
    page_name = _(u"Delete import")

    def get_success_url(self):
        return reverse('current_imports')


class PersonCreate(LoginRequiredMixin, CreateView):
    model = models.Person
    form_class = forms.BasePersonForm
    template_name = 'ishtar/person_form.html'

    def get_success_url(self):
        return reverse('person_edit', args=[self.object.pk])


class PersonEdit(LoginRequiredMixin, UpdateView):
    model = models.Person
    form_class = forms.BasePersonForm
    template_name = 'ishtar/person_form.html'

    def get_success_url(self):
        return reverse('person_edit', args=[self.object.pk])


class ManualMergeMixin(object):
    def form_valid(self, form):
        self.items = form.get_items()
        return super(ManualMergeMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            self.redir_url,
            args=[u"_".join([str(item.pk) for item in self.items])])


class PersonManualMerge(ManualMergeMixin, IshtarMixin, LoginRequiredMixin,
                        FormView):
    form_class = forms.PersonMergeFormSelection
    template_name = 'ishtar/form.html'
    page_name = _(u"Merge persons")
    current_url = 'person-manual-merge'
    redir_url = 'person_manual_merge_items'


class ManualMergeItemsMixin(object):
    def get_form_kwargs(self):
        kwargs = super(ManualMergeItemsMixin, self).get_form_kwargs()
        kwargs['items'] = self.kwargs['pks'].split('_')
        return kwargs

    def form_valid(self, form):
        self.item = form.merge()
        return super(ManualMergeItemsMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('display-item', args=[self.item_type, self.item.pk])


class PersonManualMergeItems(
        ManualMergeItemsMixin, IshtarMixin,
        LoginRequiredMixin, FormView):
    form_class = forms.PersonMergeIntoForm
    template_name = 'ishtar/form.html'
    page_name = _(u"Select the main person")
    current_url = 'person-manual-merge-items'
    item_type = 'person'


class OrgaManualMerge(ManualMergeMixin, IshtarMixin, LoginRequiredMixin,
                      FormView):
    form_class = forms.OrgaMergeFormSelection
    template_name = 'ishtar/form.html'
    page_name = _(u"Merge organization")
    current_url = 'orga-manual-merge'
    redir_url = 'orga_manual_merge_items'


class OrgaManualMergeItems(
        ManualMergeItemsMixin, IshtarMixin,
        LoginRequiredMixin, FormView):
    form_class = forms.OrgaMergeIntoForm
    template_name = 'ishtar/form.html'
    page_name = _(u"Select the main organization")
    current_url = 'orga-manual-merge-items'
    item_type = 'organization'


class OrganizationCreate(LoginRequiredMixin, CreateView):
    model = models.Organization
    form_class = forms.BaseOrganizationForm
    template_name = 'ishtar/organization_form.html'
    form_prefix = "orga"

    def get_form_kwargs(self):
        kwargs = super(OrganizationCreate, self).get_form_kwargs()
        if hasattr(self.form_class, 'form_prefix'):
            kwargs.update({'prefix': self.form_class.form_prefix})
        return kwargs

    def get_success_url(self):
        return reverse('organization_edit', args=[self.object.pk])


class OrganizationEdit(LoginRequiredMixin, UpdateView):
    model = models.Organization
    form_class = forms.BaseOrganizationForm
    template_name = 'ishtar/organization_form.html'

    def get_form_kwargs(self):
        kwargs = super(OrganizationEdit, self).get_form_kwargs()
        if hasattr(self.form_class, 'form_prefix'):
            kwargs.update({'prefix': self.form_class.form_prefix})
        return kwargs

    def get_success_url(self):
        return reverse('organization_edit', args=[self.object.pk])


class OrganizationPersonCreate(LoginRequiredMixin, CreateView):
    model = models.Person
    form_class = forms.BaseOrganizationPersonForm
    template_name = 'ishtar/organization_person_form.html'
    relative_label = _("Corporation manager")

    def get_context_data(self, *args, **kwargs):
        data = super(OrganizationPersonCreate, self).get_context_data(*args,
                                                                      **kwargs)
        data['relative_label'] = self.relative_label
        return data

    def get_success_url(self):
        return reverse('organization_person_edit', args=[self.object.pk])


class OrganizationPersonEdit(LoginRequiredMixin, UpdateView):
    model = models.Person
    form_class = forms.BaseOrganizationPersonForm
    template_name = 'ishtar/organization_person_form.html'
    relative_label = _("Corporation manager")

    def get_context_data(self, *args, **kwargs):
        data = super(OrganizationPersonEdit, self).get_context_data(*args,
                                                                    **kwargs)
        data['relative_label'] = self.relative_label
        return data

    def get_success_url(self):
        return reverse('organization_person_edit', args=[self.object.pk])
