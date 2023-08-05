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

import json

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView

from ishtar_common.models import IshtarUser, get_current_profile
from archaeological_operations.models import AdministrativeAct

from ishtar_common.forms import FinalForm
from ishtar_common.forms_common import SourceForm, AuthorFormset, \
    SourceDeletionForm
from archaeological_operations.forms import FinalAdministrativeActDeleteForm
from archaeological_context_records.forms \
    import RecordFormSelection as RecordFormSelectionTable

from ishtar_common.views import get_item, show_item, display_item, \
    revert_item, get_autocomplete_generic, IshtarMixin, LoginRequiredMixin

from ishtar_common.wizards import SearchWizard
from archaeological_operations.wizards import AdministrativeActDeletionWizard

from wizards import *
from forms import *
import models

get_find = get_item(models.Find, 'get_find', 'find')

get_find_for_ope = get_item(models.Find, 'get_find', 'find',
                            own_table_cols=models.Find.TABLE_COLS_FOR_OPE)

get_find_for_treatment = get_item(
    models.Find, 'get_find', 'find',
    own_table_cols=models.Find.TABLE_COLS_FOR_OPE, base_request={})

show_treatment = show_item(models.Treatment, 'treatment')
revert_treatment = revert_item(models.Treatment)
get_treatment = get_item(models.Treatment, 'get_treatment', 'treatment')

get_administrativeacttreatment = get_item(
    AdministrativeAct, 'get_administrativeacttreatment',
    'administrativeacttreatment',
    base_request={"treatment__pk__isnull": False})

show_treatmentfile = show_item(models.TreatmentFile, 'treatmentfile')
revert_treatmentfile = revert_item(models.TreatmentFile)
get_treatmentfile = get_item(models.TreatmentFile, 'get_treatmentfile',
                             'treatmentfile')

get_administrativeacttreatmentfile = get_item(
    AdministrativeAct, 'get_administrativeacttreatmentfile',
    'administrativeacttreatmentfile',
    base_request={"treatment_file__pk__isnull": False})


def autocomplete_treatmentfile(request):
    if not request.user.has_perm('ishtar_common.view_treatment',
                                 models.Treatment) and \
            not request.user.has_perm('ishtar_common.view_own_treatment',
                                      models.Treatment) \
            and not request.user.ishtaruser.has_right('treatmentfile_search',
                                                      session=request.session):
        return HttpResponse(mimetype='text/plain')
    if not request.GET.get('term'):
        return HttpResponse(mimetype='text/plain')
    q = request.GET.get('term')
    query = Q()
    for q1 in q.split(' '):
        for q in q1.split(' '):
            extra = Q(internal_reference__icontains=q) | \
                Q(external_id__icontains=q) | \
                Q(name__icontains=q)
            try:
                int(q)
                extra = extra | Q(year=q) | Q(index=q)
            except ValueError:
                pass
            query = query & extra
    limit = 20
    files = models.TreatmentFile.objects.filter(query)[:limit]
    data = json.dumps([{'id': file.pk, 'value': unicode(file)}
                       for file in files])
    return HttpResponse(data, mimetype='text/plain')

show_findsource = show_item(models.FindSource, 'findsource')

get_findsource = get_item(models.FindSource, 'get_findsource', 'findsource')
show_find = show_item(models.Find, 'find')
display_find = display_item(models.Find)
revert_find = revert_item(models.Find)

show_findbasket = show_item(models.FindBasket, 'findbasket')
display_findbasket = display_item(models.FindBasket,
                                  show_url='show-find/basket-')


def check_warehouse_module(self):
    return get_current_profile().warehouse


def check_not_warehouse_module(self):
    return not check_warehouse_module(self)


find_creation_steps = [
    ('selecrecord-find_creation', RecordFormSelectionTable),
    ('find-find_creation', FindForm),
    ('dating-find_creation', DatingFormSet),
    ('final-find_creation', FinalForm)
]

find_creation_wizard = FindWizard.as_view(
    find_creation_steps,
    label=_(u"New find"),
    url_name='find_creation',)

find_search_condition_dict = {
    'general-find_search': check_not_warehouse_module,
    'generalwarehouse-find_search': check_warehouse_module,
}

find_search_wizard = SearchWizard.as_view([
    ('general-find_search', FindFormSelection),
    ('generalwarehouse-find_search', FindFormSelectionWarehouseModule)],
    label=_(u"Find search"),
    url_name='find_search',
    condition_dict=find_search_condition_dict
)

find_modification_condition_dict = {
    'selec-find_modification': check_not_warehouse_module,
    'selecw-find_modification': check_warehouse_module,
}

find_modification_wizard = FindModificationWizard.as_view([
    ('selec-find_modification', FindFormSelection),
    ('selecw-find_modification', FindFormSelectionWarehouseModule),
    ('selecrecord-find_modification', RecordFormSelection),
    ('find-find_modification', FindForm),
    ('dating-find_modification', DatingFormSet),
    ('final-find_modification', FinalForm)],
    condition_dict=find_modification_condition_dict,
    label=_(u"Find modification"),
    url_name='find_modification',)


def find_modify(request, pk):
    find_modification_wizard(request)
    FindModificationWizard.session_set_value(
        request, 'selec-find_modification', 'pk', pk, reset=True)
    return redirect(
        reverse('find_modification',
                kwargs={'step': 'selecrecord-find_modification'}))

find_deletion_condition_dict = {
    'selec-find_deletion': check_not_warehouse_module,
    'selecw-find_deletion': check_warehouse_module,
}

find_deletion_steps = [
    ('selec-find_deletion', FindFormSelection),
    ('selecw-find_deletion', FindFormSelectionWarehouseModule),
    ('final-find_deletion', FindDeletionForm)]

find_deletion_wizard = FindDeletionWizard.as_view(
    find_deletion_steps,
    condition_dict=find_deletion_condition_dict,
    label=_(u"Find deletion"),
    url_name='find_deletion',)

find_source_search_wizard = SearchWizard.as_view([
    ('selec-find_source_search', FindSourceFormSelection)],
    label=_(u"Find: source search"),
    url_name='find_source_search',)

find_source_creation_wizard = FindSourceWizard.as_view([
    ('selec-find_source_creation', SourceFindFormSelection),
    ('source-find_source_creation', SourceForm),
    ('authors-find_source_creation', AuthorFormset),
    ('final-find_source_creation', FinalForm)],
    label=_(u"Find: new source"),
    url_name='find_source_creation',)

find_source_modification_wizard = FindSourceWizard.as_view([
    ('selec-find_source_modification', FindSourceFormSelection),
    ('source-find_source_modification', SourceForm),
    ('authors-find_source_modification', AuthorFormset),
    ('final-find_source_modification', FinalForm)],
    label=_(u"Find: source modification"),
    url_name='find_source_modification',)


def find_source_modify(request, pk):
    find_source_modification_wizard(request)
    FindSourceWizard.session_set_value(
        request, 'selec-find_source_modification', 'pk', pk, reset=True)
    return redirect(reverse(
        'find_source_modification',
        kwargs={'step': 'source-find_source_modification'}))

find_source_deletion_wizard = FindSourceDeletionWizard.as_view([
    ('selec-find_source_deletion', FindSourceFormSelection),
    ('final-find_source_deletion', SourceDeletionForm)],
    label=_(u"Find: source deletion"),
    url_name='find_source_deletion',)

autocomplete_objecttype = get_autocomplete_generic(models.ObjectType)
autocomplete_materialtype = get_autocomplete_generic(models.MaterialType)
autocomplete_preservationtype = get_autocomplete_generic(
    models.PreservationType)
autocomplete_integritytype = get_autocomplete_generic(models.IntegrityType)


class NewFindBasketView(IshtarMixin, LoginRequiredMixin, CreateView):
    template_name = 'ishtar/form.html'
    model = models.FindBasket
    form_class = NewFindBasketForm
    page_name = _(u"New basket")

    def get_form_kwargs(self):
        kwargs = super(NewFindBasketView, self).get_form_kwargs()
        kwargs['user'] = IshtarUser.objects.get(pk=self.request.user.pk)
        return kwargs

    def get_success_url(self):
        return reverse('select_itemsinbasket',
                       kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class SelectBasketForManagement(IshtarMixin, LoginRequiredMixin, FormView):
    template_name = 'ishtar/form.html'
    form_class = SelectFindBasketForm
    page_name = _(u"Manage items in basket")

    def get_form_kwargs(self):
        kwargs = super(SelectBasketForManagement, self).get_form_kwargs()
        kwargs['user'] = IshtarUser.objects.get(pk=self.request.user.pk)
        if 'pk' in self.kwargs:
            kwargs['initial'].update({'basket': self.kwargs['pk']})
        return kwargs

    def get_success_url(self, basket):
        return reverse('select_itemsinbasket',
                       kwargs={'pk': basket})

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url(
            form.cleaned_data['basket']))


class SelectItemsInBasket(IshtarMixin, LoginRequiredMixin, TemplateView):
    template_name = 'ishtar/manage_basket.html'
    page_name = _(u"Manage basket")

    def get_context_data(self, *args, **kwargs):
        context = super(SelectItemsInBasket, self).get_context_data(
            *args, **kwargs)
        self.user = IshtarUser.objects.get(pk=self.request.user.pk)
        try:
            self.basket = models.FindBasket.objects.get(
                pk=self.kwargs['pk'], user=self.user)
        except models.FindBasket.DoesNotExist:
            raise PermissionDenied
        context['basket'] = self.basket
        if get_current_profile().warehouse:
            context['form'] = MultipleFindFormSelectionWarehouseModule()
        else:
            context['form'] = MultipleFindFormSelection()
        context['add_url'] = reverse('add_iteminbasket')
        context['list_url'] = reverse('list_iteminbasket',
                                      kwargs={'pk': self.basket.pk})
        return context

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())


class FindBasketAddItemView(IshtarMixin, LoginRequiredMixin, FormView):
    template_name = 'ishtar/simple_form.html'
    form_class = FindBasketAddItemForm

    def get_success_url(self, basket):
        return reverse('list_iteminbasket', kwargs={'pk': basket.pk})

    def form_valid(self, form):
        user = IshtarUser.objects.get(pk=self.request.user.pk)
        # rights are checked on the form
        basket = form.save(user)
        return HttpResponseRedirect(self.get_success_url(basket))


class FindBasketListView(IshtarMixin, LoginRequiredMixin, TemplateView):
    template_name = 'ishtar/basket_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FindBasketListView, self).get_context_data(
            *args, **kwargs)
        self.user = IshtarUser.objects.get(pk=self.request.user.pk)
        try:
            self.basket = models.FindBasket.objects.get(
                pk=self.kwargs['pk'], user=self.user)
        except models.FindBasket.DoesNotExist:
            raise PermissionDenied
        context['basket'] = self.basket
        context['item_url'] = '/'.join(
            reverse(models.Find.SHOW_URL, args=[1]).split('/')[:-1])
        context['delete_url'] = '/'.join(
            reverse('delete_iteminbasket', args=[1, 1]).split('/')[:-3])
        return context


class FindBasketDeleteItemView(IshtarMixin, LoginRequiredMixin, TemplateView):
    template_name = 'ishtar/simple_form.html'

    def get_success_url(self, basket):
        return reverse('list_iteminbasket', kwargs={'pk': basket.pk})

    def get(self, *args, **kwargs):
        user = self.request.user
        ishtaruser = IshtarUser.objects.get(pk=self.request.user.pk)
        try:
            find = models.Find.objects.get(
                pk=self.kwargs['find_pk'])
        except models.Find.DoesNotExist:
            raise PermissionDenied
        try:
            basket = models.FindBasket.objects.get(
                pk=self.kwargs['basket'], user=ishtaruser)
        except models.FindBasket.DoesNotExist:
            raise PermissionDenied
        if not user.is_superuser and \
                not ishtaruser.has_right('change_find') and \
                not (ishtaruser.has_right('change_own_find')
                     and find.is_own(user)):
            raise PermissionDenied
        basket.items.remove(find)
        return HttpResponseRedirect(self.get_success_url(basket))


class DeleteFindBasketView(IshtarMixin, LoginRequiredMixin, FormView):
    template_name = 'ishtar/form_delete.html'
    form_class = DeleteFindBasketForm
    success_url = '/'
    page_name = _(u"Delete basket")

    def get_form_kwargs(self):
        kwargs = super(DeleteFindBasketView, self).get_form_kwargs()
        kwargs['user'] = IshtarUser.objects.get(pk=self.request.user.pk)
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

get_upstreamtreatment = get_item(
    models.FindUpstreamTreatments, 'get_upstreamtreatment', 'uptreatment')

get_downstreamtreatment = get_item(
    models.FindDownstreamTreatments, 'get_downstreamtreatment',
    'downtreatment')

treatment_wizard_steps = [
    ('file-treatment_creation', TreatmentFormFileChoice),
    ('basetreatment-treatment_creation', BaseTreatmentForm),
    ('selecfind-treatment_creation', UpstreamFindFormSelection),
    ('selecbasket-treatment_creation', SelectFindBasketForm),
    # ('resultfind-treatment_creation', ResultFindForm),
    # ('resultfinds-treatment_creation', ResultFindFormSet),
    ('final-treatment_creation', FinalForm)]

treatment_search_wizard = SearchWizard.as_view([
    ('general-treatment_search', TreatmentFormSelection)],
    label=_(u"Treatment search"),
    url_name='treatment_search',)

treatment_creation_wizard = TreatmentWizard.as_view(
    treatment_wizard_steps,
    condition_dict={
        'selecfind-treatment_creation':
            check_value('basetreatment-treatment_creation',
                        'target_is_basket', False),
        'selecbasket-treatment_creation':
            check_value('basetreatment-treatment_creation',
                        'target_is_basket', True),
        # 'resultfinds-treatment_creation':
        #     check_type_field('basetreatment-treatment_creation',
        #                      'treatment_type', models.TreatmentType,
        #                      'downstream_is_many'),
        # 'resultfind-treatment_creation':
        #     check_type_field('basetreatment-treatment_creation',
        #                      'treatment_type', models.TreatmentType,
        #                      'upstream_is_many')
    },
    label=_(u"New treatment"),
    url_name='treatment_creation',)

treatment_modification_wizard = TreatmentModificationWizard.as_view(
    [('selec-treatment_modification', TreatmentFormSelection),
     ('file-treatment_modification', TreatmentFormFileChoice),
     ('basetreatment-treatment_modification', TreatmentModifyForm),
     ('final-treatment_modification', FinalForm)],
    label=_(u"Modify"),
    url_name='treatment_modification',
)


def treatment_modify(request, pk):
    treatment_modification_wizard(request)
    TreatmentModificationWizard.session_set_value(
        request, 'selec-treatment_modification', 'pk', pk, reset=True)
    return redirect(reverse(
        'treatment_modification',
        kwargs={'step': 'basetreatment-treatment_modification'}))


treatment_deletion_wizard = TreatmentDeletionWizard.as_view([
    ('selec-treatment_deletion', TreatmentFormSelection),
    ('final-treatment_deletion', TreatmentDeletionForm)],
    label=_(u"Treatment deletion"),
    url_name='treatment_deletion',)

treatment_administrativeact_search_wizard = \
    SearchWizard.as_view([
        ('selec-treatment_admacttreatment_search',
         AdministrativeActTreatmentFormSelection)],
        label=_(u"Treatment: search administrative act"),
        url_name='treatment_admacttreatment_search',)

treatment_administrativeact_wizard = \
    TreatmentAdministrativeActWizard.as_view([
        ('selec-treatment_admacttreatment', TreatmentFormSelection),
        ('administrativeact-treatment_admacttreatment',
         AdministrativeActTreatmentForm),
        ('final-treatment_admacttreatment', FinalForm)],
        label=_(u"Treatment: new administrative act"),
        url_name='treatment_admacttreatment',)

treatment_administrativeact_modification_wizard = \
    TreatmentEditAdministrativeActWizard.as_view([
        ('selec-treatment_admacttreatment_modification',
         AdministrativeActTreatmentFormSelection),
        ('administrativeact-treatment_admacttreatment_modification',
         AdministrativeActTreatmentModifForm),
        ('final-treatment_admacttreatment_modification', FinalForm)],
        label=_(u"Treatment: administrative act modification"),
        url_name='treatment_admacttreatment_modification',)

treatment_admacttreatment_deletion_wizard = \
    AdministrativeActDeletionWizard.as_view([
        ('selec-treatment_admacttreatment_deletion',
         AdministrativeActTreatmentFormSelection),
        ('final-treatment_admacttreatment_deletion',
         FinalAdministrativeActDeleteForm)],
        label=_(u"Treatment: administrative act deletion"),
        url_name='treatment_admacttreatment_deletion',)


def treatment_administrativeacttreatment_modify(request, pk):
    treatment_administrativeact_modification_wizard(request)
    TreatmentEditAdministrativeActWizard.session_set_value(
        request,
        'selec-treatment_admacttreatment_modification',
        'pk', pk, reset=True)
    return redirect(
        reverse(
            'treatment_admacttreatment_modification',
            kwargs={
                'step':
                    'administrativeact-treatment_admacttreatment_modification'
            }))


# treatment request

treatmentfile_search_wizard = SearchWizard.as_view([
    ('general-treatmentfile_search', TreatmentFileFormSelection)],
    label=_(u"Treatment request search"),
    url_name='treatmentfile_search',)

treatmentfile_wizard_steps = [
    ('treatmentfile-treatmentfile_creation', TreatmentFileForm),
    ('final-treatmentfile_creation', FinalForm)]


treatmentfile_creation_wizard = TreatmentFileWizard.as_view(
    treatmentfile_wizard_steps,
    label=_(u"New treatment request"),
    url_name='treatmentfile_creation',)

treatmentfile_modification_wizard = TreatmentFileModificationWizard.as_view(
    [('selec-treatmentfile_modification', TreatmentFileFormSelection),
     ('treatmentfile-treatmentfile_modification', TreatmentFileModifyForm),
     ('final-treatmentfile_modification', FinalForm)],
    label=_(u"Modify"),
    url_name='treatmentfile_modification',
)


def treatmentfile_modify(request, pk):
    treatmentfile_modification_wizard(request)
    TreatmentFileModificationWizard.session_set_value(
        request, 'selec-treatmentfile_modification', 'pk', pk, reset=True)
    return redirect(reverse(
        'treatmentfile_modification',
        kwargs={'step': 'treatmentfile-treatmentfile_modification'}))

treatmentfile_deletion_wizard = TreatmentFileDeletionWizard.as_view([
    ('selec-treatmentfile_deletion', TreatmentFileFormSelection),
    ('final-treatmentfile_deletion', TreatmentFileDeletionForm)],
    label=_(u"Treatment request deletion"),
    url_name='treatmentfile_deletion',)

treatmentfile_admacttreatmentfile_search_wizard = \
    SearchWizard.as_view([
        ('selec-treatmentfle_admacttreatmentfle_search',
         AdministrativeActTreatmentFileFormSelection)],
        label=_(u"Treatment request: search administrative act"),
        url_name='treatmentfle_admacttreatmentfle_search',)


treatmentfile_admacttreatmentfile_wizard = \
    TreatmentFileAdministrativeActWizard.as_view([
        ('selec-treatmentfle_admacttreatmentfle', TreatmentFileFormSelection),
        ('admact-treatmentfle_admacttreatmentfle',
         AdministrativeActTreatmentFileForm),
        ('final-treatmentfle_admacttreatmentfle', FinalForm)],
        label=_(u"Treatment request: new administrative act"),
        url_name='treatmentfle_admacttreatmentfle',)

treatmentfile_admacttreatmentfile_modification_wizard = \
    TreatmentFileEditAdministrativeActWizard.as_view([
        ('selec-treatmentfle_admacttreatmentfle_modification',
         AdministrativeActTreatmentFileFormSelection),
        ('admact-treatmentfle_admacttreatmentfle_modification',
         AdministrativeActTreatmentFileModifForm),
        ('final-treatmentfle_admacttreatmentfle_modification', FinalForm)],
        label=_(u"Treatment request: administrative act modification"),
        url_name='treatmentfle_admacttreatmentfle_modification',)

treatmentfile_admacttreatmentfile_deletion_wizard = \
    AdministrativeActDeletionWizard.as_view([
        ('selec-treatmentfle_admacttreatmentfle_deletion',
         AdministrativeActTreatmentFileFormSelection),
        ('final-treatmentfle_admacttreatmentfle_deletion',
         FinalAdministrativeActDeleteForm)],
        label=_(u"Treatment request: administrative act deletion"),
        url_name='treatmentfle_admacttreatmentfle_deletion',)


def treatmentfile_administrativeacttreatmentfile_modify(request, pk):
    treatmentfile_admacttreatmentfile_modification_wizard(request)
    TreatmentFileEditAdministrativeActWizard.session_set_value(
        request,
        'selec-treatmentfle_admacttreatmentfle_modification',
        'pk', pk, reset=True)
    return redirect(
        reverse(
            'treatmentfle_admacttreatmentfle_modification',
            kwargs={
                'step':
                    'admact-treatmentfle_admacttreatmentfle_modification'
            }))

# sources

show_treatmentsource = show_item(models.TreatmentSource, 'treatmentsource')
get_treatmentsource = get_item(models.TreatmentSource, 'get_treatmentsource',
                               'treatmentsource')

treatment_source_search_wizard = SearchWizard.as_view([
    ('selec-treatment_source_search', TreatmentSourceFormSelection)],
    label=_(u"Treatment: source search"),
    url_name='treatment_source_search',)

treatment_source_creation_wizard = TreatmentSourceWizard.as_view([
    ('selec-treatment_source_creation', SourceTreatmentFormSelection),
    ('source-treatment_source_creation', SourceForm),
    ('authors-treatment_source_creation', AuthorFormset),
    ('final-treatment_source_creation', FinalForm)],
    url_name='treatment_source_creation',)

treatment_source_modification_wizard = TreatmentSourceWizard.as_view([
    ('selec-treatment_source_modification', TreatmentSourceFormSelection),
    ('source-treatment_source_modification', SourceForm),
    ('authors-treatment_source_modification', AuthorFormset),
    ('final-treatment_source_modification', FinalForm)],
    label=_(u"Treatment: source modification"),
    url_name='treatment_source_modification',)


def treatment_source_modify(request, pk):
    treatment_source_modification_wizard(request)
    TreatmentSourceWizard.session_set_value(
        request, 'selec-treatment_source_modification', 'pk', pk, reset=True)
    return redirect(reverse(
        'treatment_source_modification',
        kwargs={'step': 'source-treatment_source_modification'}))

treatment_source_deletion_wizard = TreatmentSourceDeletionWizard.as_view([
    ('selec-treatment_source_deletion', TreatmentSourceFormSelection),
    ('final-treatment_source_deletion', SourceDeletionForm)],
    label=_(u"Treatment: source deletion"),
    url_name='treatment_source_deletion',)

# treatment request sources

show_treatmentfilesource = show_item(models.TreatmentFileSource,
                                     'treatmentfilesource')
get_treatmentfilesource = get_item(
    models.TreatmentFileSource, 'get_treatmentfilesource',
    'treatmentfilesource')

treatmentfile_source_search_wizard = SearchWizard.as_view([
    ('selec-treatmentfile_source_search', TreatmentFileSourceFormSelection)],
    label=_(u"Treatment request: source search"),
    url_name='treatmentfile_source_search',)

treatmentfile_source_creation_wizard = TreatmentFileSourceWizard.as_view([
    ('selec-treatmentfile_source_creation', SourceTreatmentFileFormSelection),
    ('source-treatmentfile_source_creation', SourceForm),
    ('authors-treatmentfile_source_creation', AuthorFormset),
    ('final-treatmentfile_source_creation', FinalForm)],
    url_name='treatmentfile_source_creation',)

treatmentfile_source_modification_wizard = TreatmentFileSourceWizard.as_view([
    ('selec-treatmentfile_source_modification',
     TreatmentFileSourceFormSelection),
    ('source-treatmentfile_source_modification', SourceForm),
    ('authors-treatmentfile_source_modification', AuthorFormset),
    ('final-treatmentfile_source_modification', FinalForm)],
    label=_(u"Treatment request: source modification"),
    url_name='treatmentfile_source_modification',)


def treatmentfile_source_modify(request, pk):
    treatmentfile_source_modification_wizard(request)
    TreatmentFileSourceWizard.session_set_value(
        request, 'selec-treatmentfile_source_modification', 'pk', pk,
        reset=True)
    return redirect(reverse(
        'treatmentfile_source_modification',
        kwargs={'step': 'source-treatmentfile_source_modification'}))

treatmentfile_source_deletion_wizard = \
    TreatmentFileSourceDeletionWizard.as_view([
        ('selec-treatmentfile_source_deletion',
         TreatmentFileSourceFormSelection),
        ('final-treatmentfile_source_deletion', SourceDeletionForm)],
        label=_(u"Treatment request: source deletion"),
        url_name='treatmentfile_source_deletion',)
