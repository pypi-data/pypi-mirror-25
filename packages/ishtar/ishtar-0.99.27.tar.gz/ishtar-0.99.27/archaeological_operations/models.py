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

import datetime
from itertools import groupby

from django.conf import settings
from django.contrib.gis.db import models
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q, Count, Sum, Max, Avg
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _, ugettext

from ishtar_common.utils import cached_label_changed, \
    force_cached_label_changed, get_cache, mode

from ishtar_common.models import GeneralType, BaseHistorizedItem, \
    HistoricalRecords, LightHistorizedItem, OwnPerms, Department, Source,\
    SourceType, Person, Organization, Town, Dashboard, IshtarUser, ValueGetter,\
    DocumentTemplate, ShortMenuItem, DashboardFormItem, GeneralRelationType,\
    GeneralRecordRelations, post_delete_record_relation, OperationType, \
    get_external_id, ImageModel, post_save_cache


class RemainType(GeneralType):
    class Meta:
        verbose_name = _(u"Remain type")
        verbose_name_plural = _(u"Remain types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=RemainType)
post_delete.connect(post_save_cache, sender=RemainType)


class Period(GeneralType):
    order = models.IntegerField(_(u"Order"))
    start_date = models.IntegerField(_(u"Start date"))
    end_date = models.IntegerField(_(u"End date"))
    parent = models.ForeignKey("Period", verbose_name=_(u"Parent period"),
                               blank=True, null=True)

    class Meta:
        verbose_name = _(u"Type Period")
        verbose_name_plural = _(u"Types Period")
        ordering = ('order',)

    def __unicode__(self):
        return self.label
post_save.connect(post_save_cache, sender=Period)
post_delete.connect(post_save_cache, sender=Period)


class ReportState(GeneralType):
    order = models.IntegerField(_(u"Order"))

    class Meta:
        verbose_name = _(u"Type of report state")
        verbose_name_plural = _(u"Types of report state")
        ordering = ('order',)

    def __unicode__(self):
        return self.label
post_save.connect(post_save_cache, sender=ReportState)
post_delete.connect(post_save_cache, sender=ReportState)


class ArchaeologicalSite(BaseHistorizedItem):
    reference = models.CharField(_(u"Reference"), max_length=20, unique=True)
    name = models.CharField(_(u"Name"), max_length=200,
                            null=True, blank=True)
    periods = models.ManyToManyField(Period, verbose_name=_(u"Periods"),
                                     blank=True, null=True)
    remains = models.ManyToManyField("RemainType", verbose_name=_(u'Remains'),
                                     blank=True, null=True)

    class Meta:
        verbose_name = _(u"Archaeological site")
        verbose_name_plural = _(u"Archaeological sites")
        permissions = (
            ("view_archaeologicalsite",
             ugettext(u"Can view all Archaeological sites")),
            ("view_own_archaeologicalsite",
             ugettext(u"Can view own Archaeological site")),
            ("add_own_archaeologicalsite",
             ugettext(u"Can add own Archaeological site")),
            ("change_own_archaeologicalsite",
             ugettext(u"Can change own Archaeological site")),
            ("delete_own_archaeologicalsite",
             ugettext(u"Can delete own Archaeological site")),
        )

    def __unicode__(self):
        name = self.reference
        if self.name:
            name += u" %s %s" % (settings.JOINT, self.name)
        if self.remains.count():
            name += u" {} {}".format(
                settings.JOINT,
                u", ".join([unicode(remain) for remain in self.remains.all()]))
        if self.periods.count():
            name += u" [{}]".format(
                u", ".join([unicode(period) for period in self.periods.all()]))
        return name


def get_values_town_related(item, prefix, values):
    values[prefix + 'parcellist'] = item.render_parcels()
    values[prefix + 'towns'] = ''
    values[prefix + 'departments'] = ''
    values[prefix + 'departments_number'] = ''
    values[prefix + 'towns_count'] = unicode(item.towns.count())
    if item.towns.count():
        values[prefix + 'towns'] = u", ".join([
            town.name for town in item.towns.all().order_by('name')])
        if settings.COUNTRY == 'fr':
            dpts_num = set(
                [town.numero_insee[:2] for town in item.towns.all()])
            values[prefix + 'departments_number'] = u", ".join(
                list(sorted(dpts_num)))
            values[prefix + 'departments'] = u", ".join(
                [Department.objects.get(number=dpt).label
                 for dpt in sorted(dpts_num) if Department.objects.filter(
                    number=dpt).count()])
    return values

QUALITY = (('ND', _(u"Not documented")),
           ('A', _(u"Arbitrary")),
           ('R', _(u"Reliable")),)


class ClosedItem(object):
    def closing(self):
        if self.is_active():
            return
        in_history = False
        date = self.end_date
        # last action is closing?
        for idx, item in enumerate(
                self.history.order_by('-history_date').all()):
            if not idx:
                # last action
                continue
            if not item.end_date or item.end_date != self.end_date:
                break
            in_history = True
        user = None
        if in_history:
            if item.history_modifier_id:
                q = IshtarUser.objects.filter(pk=item.history_modifier_id)
                if q.count():
                    user = q.all()[0]
        elif self.history_modifier_id:
            q = IshtarUser.objects.filter(pk=self.history_modifier_id)
            if q.count():
                user = q.all()[0]
        return {'date': date, 'user': user}


class Operation(ClosedItem, BaseHistorizedItem, ImageModel, OwnPerms,
                ValueGetter, ShortMenuItem, DashboardFormItem):
    QUALITY_DICT = dict(QUALITY)
    SHOW_URL = 'show-operation'
    TABLE_COLS = ['year', 'towns', 'common_name', 'operation_type',
                  'start_date', 'excavation_end_date', 'remains']
    IMAGE_PREFIX = 'operations/'
    SLUG = 'operation'

    # search parameters
    BOOL_FIELDS = ['end_date__isnull', 'virtual_operation',
                   'documentation_received', 'finds_received']
    DATED_FIELDS = [
        'start_date__lte', 'start_date__gte', 'excavation_end_date__lte',
        'excavation_end_date__gte', 'documentation_deadline__lte',
        'documentation_deadline__gte', 'finds_deadline__lte',
        'finds_deadline__gte']
    RELATIVE_SESSION_NAMES = [('file', 'associated_file__pk')]
    EXTRA_REQUEST_KEYS = {
        'common_name': 'common_name__icontains',
        'cached_label': 'cached_label__icontains',
        'comment': 'comment__icontains',
        'scientific_documentation_comment':
        'scientific_documentation_comment__icontains',
        'abstract': 'abstract__icontains',
        'end_date': 'end_date__isnull',
        'start_before': 'start_date__lte',
        'start_after': 'start_date__gte',
        'end_before': 'excavation_end_date__lte',
        'end_after': 'excavation_end_date__gte',
        'towns__numero_insee__startswith':
        'towns__numero_insee__startswith',
        'parcel_0': ('parcels__section',
                     'associated_file__parcels__section'),
        'parcel_1': (
            'parcels__parcel_number',
            'associated_file__parcels__parcel_number'),
        'parcel_2': (
            'parcels__public_domain',
            'associated_file__parcels__public_domain'),
        'history_creator':
        'history_creator__ishtaruser__person__pk',
        'history_modifier':
        'history_modifier__ishtaruser__person__pk',
        'archaeological_sites':
        'archaeological_sites__pk',
        'documentation_deadline_before': 'documentation_deadline__lte',
        'documentation_deadline_after': 'documentation_deadline__gte',
        'finds_deadline_before': 'finds_deadline__lte',
        'finds_deadline_after': 'finds_deadline__gte',
        'related_treatment':
        'context_record__base_finds__find__upstream_treatment__id'
    }

    COL_LABELS = {
        'full_code_patriarche': u"Code patriarche",
        'associated_file_short_label': _(u"Associated file (label)"),
        'operator__name': _(u"Operator name"),
        'scientist__raw_name': _(u"Scientist (full name)"),
        'associated_file__external_id': _(u"Associated file (external ID)"),
        'scientist__title': _(u"Scientist (title)"),
        'scientist__surname': _(u"Scientist (surname)"),
        'scientist__name': _(u"Scientist (name)"),
        'scientist__attached_to__name': _(u"Scientist - Organization (name)"),
        'in_charge__title': _(u"In charge (title)"),
        'in_charge__surname': _(u"In charge (surname)"),
        'in_charge__name': _(u"In charge (name)"),
        'in_charge__attached_to__name': _(u"In charge - Organization (name)"),
        'cira_rapporteur__surname': u"Rapporteur CIRA (prénom)",
        'cira_rapporteur__name': u"Rapporteur CIRA (nom)",
        'cira_rapporteur__attached_to__name': u"Rapporteur CIRA - "
                                              u"Organisation (nom)",
        'archaeological_sites__reference': _(u"Archaeological sites ("
                                             u"reference)"),
    }

    # fields definition
    creation_date = models.DateField(_(u"Creation date"),
                                     default=datetime.date.today)
    end_date = models.DateField(_(u"Closing date"), null=True, blank=True)
    start_date = models.DateField(_(u"Start date"), null=True, blank=True)
    excavation_end_date = models.DateField(
        _(u"Excavation end date"), null=True, blank=True)
    report_delivery_date = models.DateField(_(u"Report delivery date"),
                                            null=True, blank=True)
    scientist = models.ForeignKey(
        Person, blank=True, null=True, verbose_name=_(u"In charge scientist"),
        on_delete=models.SET_NULL,
        related_name='operation_scientist_responsability')
    operator = models.ForeignKey(
        Organization, blank=True, null=True, related_name='operator',
        verbose_name=_(u"Operator"), on_delete=models.SET_NULL)
    in_charge = models.ForeignKey(Person, blank=True, null=True,
                                  verbose_name=_(u"In charge"),
                                  on_delete=models.SET_NULL,
                                  related_name='operation_responsability')
    collaborators = models.ManyToManyField(
        Person, blank=True, null=True, verbose_name=_(u"Collaborators"),
        related_name='operation_collaborator'
    )
    year = models.IntegerField(_(u"Year"), null=True, blank=True)
    operation_code = models.IntegerField(_(u"Numeric reference"), null=True,
                                         blank=True)
    associated_file = models.ForeignKey(
        'archaeological_files.File',
        related_name='operations', verbose_name=_(u"File"),
        blank=True, null=True)
    operation_type = models.ForeignKey(OperationType, related_name='+',
                                       verbose_name=_(u"Operation type"))
    surface = models.IntegerField(_(u"Surface (m2)"), blank=True, null=True)
    remains = models.ManyToManyField("RemainType", verbose_name=_(u'Remains'),
                                     null=True, blank=True)
    towns = models.ManyToManyField(Town, verbose_name=_(u"Towns"),
                                   related_name='operations')
    cost = models.IntegerField(_(u"Cost (euros)"),
                               blank=True, null=True)  # preventive
    periods = models.ManyToManyField(Period, verbose_name=_(u"Periods"),
                                     null=True, blank=True)
    # preventive
    scheduled_man_days = models.IntegerField(_(u"Scheduled man-days"),
                                             blank=True, null=True)
    # preventive
    optional_man_days = models.IntegerField(_(u"Optional man-days"),
                                            blank=True, null=True)
    # preventive
    effective_man_days = models.IntegerField(_(u"Effective man-days"),
                                             blank=True, null=True)
    report_processing = models.ForeignKey(
        ReportState, verbose_name=_(u"Report processing"),
        blank=True, null=True)
    old_code = models.CharField(_(u"Old code"), max_length=200, null=True,
                                blank=True)
    if settings.COUNTRY == 'fr':
        code_patriarche = models.TextField(u"Code PATRIARCHE", null=True,
                                           blank=True, unique=True)
        TABLE_COLS = ['full_code_patriarche'] + TABLE_COLS
        # preventive
        fnap_financing = models.FloatField(u"Financement FNAP (%)",
                                           blank=True, null=True)
        # preventive
        fnap_cost = models.IntegerField(u"Financement FNAP (€)",
                                        blank=True, null=True)
        # preventive diag
        zoning_prescription = models.NullBooleanField(
            _(u"Prescription on zoning"), blank=True, null=True)
        # preventive diag
        large_area_prescription = models.NullBooleanField(
            _(u"Prescription on large area"), blank=True, null=True)
        geoarchaeological_context_prescription = models.NullBooleanField(
            _(u"Prescription on geoarchaeological context"), blank=True,
            null=True)  # preventive diag
        cira_rapporteur = models.ForeignKey(
            Person, related_name='cira_rapporteur', null=True, blank=True,
            on_delete=models.SET_NULL, verbose_name=u"Rapporteur CIRA")
        negative_result = models.NullBooleanField(
            u"Résultat considéré comme négatif", blank=True, null=True)
        cira_date = models.DateField(u"Date avis CIRA", null=True, blank=True)
        eas_number = models.CharField(u"Numéro de l'EA", max_length=20,
                                      null=True, blank=True)
    operator_reference = models.CharField(
        _(u"Operator reference"), max_length=20, null=True, blank=True)
    common_name = models.TextField(_(u"Generic name"), null=True, blank=True)
    address = models.TextField(_(u"Address / Locality"), null=True, blank=True)
    comment = models.TextField(_(u"General comment"), null=True, blank=True)
    scientific_documentation_comment = models.TextField(
        _(u"Comment about scientific documentation"), null=True, blank=True)
    cached_label = models.CharField(_(u"Cached name"), max_length=500,
                                    null=True, blank=True)
    archaeological_sites = models.ManyToManyField(
        ArchaeologicalSite, verbose_name=_(u"Archaeological sites"),
        null=True, blank=True)
    virtual_operation = models.BooleanField(
        _(u"Virtual operation"),
        default=False, help_text=_(
            u"If checked, it means that this operation have not been "
            u"officialy registered."))
    record_quality = models.CharField(
        _(u"Record quality"), max_length=2, null=True, blank=True,
        choices=QUALITY)
    abstract = models.TextField(_(u"Abstract"), null=True, blank=True)
    documentation_deadline = models.DateField(
        _(u"Deadline for submission of the documentation"), blank=True,
        null=True)
    documentation_received = models.NullBooleanField(
        _(u"Documentation received"), blank=True, null=True)
    finds_deadline = models.DateField(
        _(u"Deadline for submission of the finds"), blank=True, null=True)
    finds_received = models.NullBooleanField(
        _(u"Finds received"), blank=True, null=True)

    point = models.PointField(_(u"Point"), blank=True, null=True)
    multi_polygon = models.MultiPolygonField(_(u"Multi polygon"), blank=True,
                                             null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _(u"Operation")
        verbose_name_plural = _(u"Operations")
        permissions = (
            ("view_operation", ugettext(u"Can view all Operations")),
            ("view_own_operation", ugettext(u"Can view own Operation")),
            ("add_own_operation", ugettext(u"Can add own Operation")),
            ("change_own_operation", ugettext(u"Can change own Operation")),
            ("delete_own_operation", ugettext(u"Can delete own Operation")),
            ("close_operation", ugettext(u"Can close Operation")),
        )
        ordering = ('cached_label',)

    @classmethod
    def get_owns(cls, user, menu_filtr=None, limit=None, values=None,
                 get_short_menu_class=None):
        replace_query = None
        if menu_filtr and 'file' in menu_filtr:
            replace_query = Q(associated_file=menu_filtr['file'])

        owns = super(Operation, cls).get_owns(
            user, replace_query=replace_query,
            limit=limit, values=values,
            get_short_menu_class=get_short_menu_class)
        return cls._return_get_owns(owns, values, get_short_menu_class)

    def __unicode__(self):
        if self.cached_label:
            return self.cached_label
        self.save()
        return self.cached_label

    def get_values(self, prefix=''):
        values = super(Operation, self).get_values(prefix=prefix)
        return get_values_town_related(self, prefix, values)

    @property
    def short_class_name(self):
        return _(u"OPE")

    @property
    def external_id(self):
        return self.code_patriarche

    @property
    def short_label(self):
        if settings.COUNTRY == 'fr':
            return self.reference
        return unicode(self)

    @property
    def name(self):
        return self.common_name

    @property
    def show_url(self):
        return reverse('show-operation', args=[self.pk, ''])

    def towns_codes(self):
        return [u"{} ({})".format(town.name, town.numero_insee) for town in
                self.towns.all()]

    def has_finds(self):
        from archaeological_finds.models import BaseFind
        return BaseFind.objects.filter(context_record__operation=self).count()

    def finds(self):
        from archaeological_finds.models import BaseFind
        return BaseFind.objects.filter(context_record__operation=self)

    def get_reference(self, full=False):
        ref = ""
        if settings.COUNTRY == 'fr' and self.code_patriarche:
            ref = settings.ISHTAR_OPE_PREFIX + unicode(self.code_patriarche)
            if not full:
                return ref
        if self.year and self.operation_code:
            if ref:
                ref += u" - "
            ref += settings.ISHTAR_DEF_OPE_PREFIX
            ref += u"-".join((unicode(self.year),
                              unicode(self.operation_code)))
        return ref or "00"

    @property
    def reference(self):
        return self.get_reference()

    @property
    def report_delivery_delay(self):
        return None
        # q = self.source.filter(source_type__txt_idx__endswith='_report')
        # if not self.report_delivery_date or not q.count():
        #     return None

    def _generate_cached_label(self):
        items = [self.get_town_label(), self.get_reference(full=True)]
        if self.common_name:
            items.append(self.common_name)
        cached_label = settings.JOINT.join(items)
        return cached_label

    def _get_associated_cached_labels(self):
        return list(self.context_record.all())

    def _cached_labels_bulk_update(self):
        if settings.TESTING and settings.USE_SPATIALITE_FOR_TESTS:
            return
        self.context_record.model.cached_label_bulk_update(operation_id=self.pk)
        return True

    def get_town_label(self):
        lbl = unicode(_('Intercommunal'))
        if self.towns.count() == 1:
            lbl = self.towns.all()[0].name
        return lbl

    def get_department(self):
        if not self.towns.count():
            return '00'
        return self.towns.all()[0].numero_insee[:2]

    def grouped_parcels(self):
        return Parcel.grouped_parcels(list(self.parcels.all()))

    def render_parcels(self):
        return Parcel.render_parcels(list(self.parcels.all()))

    def context_record_relations_q(self):
        from archaeological_context_records.models \
            import RecordRelations as CRRL
        return CRRL.objects.filter(left_record__operation=self)

    def context_record_docs_q(self):
        from archaeological_context_records.models import ContextRecordSource
        return ContextRecordSource.objects.filter(
            context_record__operation=self)

    def find_docs_q(self):
        from archaeological_finds.models import FindSource
        return FindSource.objects.filter(
            find__base_finds__context_record__operation=self)

    def containers_q(self):
        from archaeological_warehouse.models import Container
        return Container.objects.filter(
            finds__base_finds__context_record__operation=self
        )

    associated_file_short_label_lbl = _(u"Archaeological file")
    full_code_patriarche_lbl = _(u"Code patriarche")

    @property
    def associated_file_short_label(self):
        if not self.associated_file:
            return ""
        return self.associated_file.short_label

    @classmethod
    def get_available_operation_code(cls, year=None):
        max_val = cls.objects.filter(year=year).aggregate(
            Max('operation_code'))["operation_code__max"]
        return (max_val + 1) if max_val else 1

    year_index_lbl = _(u"Operation code")

    @property
    def year_index(self):
        if not self.operation_code:
            return ""
        lbl = unicode(self.operation_code)
        year = self.year or 0
        lbl = settings.ISHTAR_DEF_OPE_PREFIX \
              + u"%d-%s%s" % (year, (3 - len(lbl)) * "0", lbl)
        return lbl

    @property
    def full_code_patriarche(self):
        if not self.code_patriarche:
            return ''
        return settings.ISHTAR_OPE_PREFIX + self.code_patriarche

    def clean(self):
        if not self.operation_code:
            return
        objs = self.__class__.objects.filter(
            year=self.year, operation_code=self.operation_code)
        if self.pk:
            objs = objs.exclude(pk=self.pk)
        if objs.count():
            raise ValidationError(_(u"This operation code already exists for "
                                    u"this year"))

    @property
    def surface_ha(self):
        if self.surface:
            return self.surface / 10000.0

    @property
    def cost_by_m2(self):
        if not self.surface or not self.cost:
            return
        return round(float(self.cost) / self.surface, 2)

    @classmethod
    def get_query_owns(cls, user):
        return (
            Q(in_charge=user.ishtaruser.person) |
            Q(scientist=user.ishtaruser.person) |
            Q(collaborators__pk=user.ishtaruser.person.pk) |
            Q(history_creator=user)) & Q(end_date__isnull=True)

    def is_active(self):
        return not bool(self.end_date)

    @property
    def nb_parcels(self):
        _(u"Number of parcels")
        nb = 0
        if self.associated_file:
            nb = self.associated_file.parcels.count()
        if not nb:
            nb = self.parcels.count()
        return nb

    @property
    def nb_acts(self, update=False):
        _(u"Number of administrative acts")
        return self._get_or_set_stats('_nb_acts', update)

    def _nb_acts(self):
        return self.administrative_act.count()

    @property
    def nb_indexed_acts(self, update=False):
        _(u"Number of indexed administrative acts")
        return self._get_or_set_stats('_nb_indexed_acts', update)

    def _nb_indexed_acts(self):
        return self.administrative_act.filter(act_type__indexed=True).count()

    @property
    def nb_context_records(self, update=False):
        _(u"Number of context records")
        return self._get_or_set_stats('_nb_context_records', update)

    def _nb_context_records(self):
        return self.context_record.count()

    @property
    def nb_context_records_by_type(self, update=False):
        return self._get_or_set_stats('_nb_context_records_by_type', update)

    def _nb_context_records_by_type(self):
        nbs = []
        q = self.context_record.values(
            'unit', 'unit__label').distinct().order_by('label')
        for res in q.all():
            nbs.append((unicode(res['unit__label']),
                        self.context_record.filter(unit=res['unit']).count()))
        return list(set(nbs))

    @property
    def nb_context_records_by_periods(self, update=False):
        return self._get_or_set_stats('_nb_context_records_by_periods', update)

    def _nb_context_records_by_periods(self):
        nbs = []
        q = self.context_record.values(
            'datings__period', 'datings__period__label').distinct().order_by(
                'datings__period__order')
        for res in q.all():
            nbs.append((unicode(res['datings__period__label']),
                        self.context_record.filter(
                            datings__period=res['datings__period']).count()))
        return nbs

    @property
    def nb_finds(self, update=False):
        _(u"Number of finds")
        return self._get_or_set_stats('_nb_finds', update)

    def _nb_finds(self):
        from archaeological_finds.models import Find
        q = Find.objects.filter(
            base_finds__context_record__operation=self,
            upstream_treatment_id__isnull=True).distinct()
        return q.count()

    @property
    def nb_finds_by_material_type(self, update=False):
        return self._get_or_set_stats('_nb_finds_by_material_type', update)

    def _nb_finds_by_material_type(self):
        from archaeological_finds.models import Find
        nbs = []
        q = Find.objects.filter(
            upstream_treatment_id__isnull=True,
            base_finds__context_record__operation=self).distinct().values(
            'material_types__pk', 'material_types__label').distinct().order_by(
            'material_types__label')
        for res in q.all():
            nbs.append(
                (unicode(res['material_types__label']),
                 Find.objects.filter(
                    base_finds__context_record__operation=self,
                    upstream_treatment_id__isnull=True,
                    material_types__pk=res['material_types__pk']).count()))
        return nbs

    @property
    def nb_finds_by_types(self, update=False):
        return self._get_or_set_stats('_nb_finds_by_types', update)

    def _nb_finds_by_types(self):
        from archaeological_finds.models import Find
        nbs = []
        q = Find.objects.filter(
            base_finds__context_record__operation=self).values(
            'object_types', 'object_types__label').distinct().order_by(
                'object_types__label')
        for res in q.all():
            label = unicode(res['object_types__label'])
            if label == 'None':
                label = _(u"No type")
            nbs.append(
                (label,
                 Find.objects.filter(
                     base_finds__context_record__operation=self,
                     upstream_treatment_id__isnull=True,
                     object_types=res['object_types']).count()))
        return nbs

    @property
    def nb_finds_by_periods(self, update=False):
        return self._get_or_set_stats('_nb_finds_by_periods', update)

    def _nb_finds_by_periods(self):
        from archaeological_finds.models import Find
        nbs = []
        q = Find.objects.filter(
            base_finds__context_record__operation=self).values(
            'datings__period', 'datings__period__label').distinct().order_by(
                'datings__period__order')
        for res in q.all():
            nbs.append(
                (unicode(res['datings__period__label']),
                 Find.objects.filter(
                    base_finds__context_record__operation=self,
                    upstream_treatment_id__isnull=True,
                    datings__period=res['datings__period']).count()))
        return nbs

    @property
    def nb_documents(self, update=False):
        _(u"Number of sources")
        return self._get_or_set_stats('_nb_documents', update)

    def _nb_documents(self):
        from archaeological_context_records.models import ContextRecordSource
        from archaeological_finds.models import FindSource
        nbs = self.source.count() + \
            ContextRecordSource.objects.filter(
                context_record__operation=self).count() + \
            FindSource.objects.filter(
                find__base_finds__context_record__operation=self).count()
        return nbs

    @property
    def nb_documents_by_types(self, update=False):
        return self._get_or_set_stats('_nb_documents_by_types', update)

    def _nb_documents_by_types(self):
        from archaeological_context_records.models import ContextRecordSource
        from archaeological_finds.models import FindSource
        docs = {}

        qs = [
            self.source,
            ContextRecordSource.objects.filter(context_record__operation=self),
            FindSource.objects.filter(
                find__upstream_treatment_id__isnull=True,
                find__base_finds__context_record__operation=self)]
        for q in qs:
            for res in q.values('source_type').distinct():
                st = res['source_type']
                if st not in docs:
                    docs[st] = 0
                docs[st] += q.filter(source_type=st).count()
        docs = [(unicode(SourceType.objects.get(pk=k)), docs[k]) for k in docs]
        return sorted(docs, key=lambda x: x[0])

    @property
    def nb_stats_finds_by_ue(self, update=False):
        return self._get_or_set_stats('_nb_stats_finds_by_ue', update)

    def _nb_stats_finds_by_ue(self):
        _(u"Mean")
        res, finds = {}, []
        for cr in self.context_record.all():
            finds.append(cr.base_finds.count())
        if not finds:
            return res
        res['mean'] = float(sum(finds)) / max(len(finds), 1)
        res['min'] = min(finds)
        res['max'] = max(finds)
        res['mode'] = u" ; ".join([str(m) for m in mode(finds)])
        return res

    def save(self, *args, **kwargs):
        # put a default year if start_date is defined
        if self.start_date and not self.year:
            self.year = self.start_date.year
        if self.operation_code is None:
            self.operation_code = self.get_available_operation_code(self.year)
        if hasattr(self, 'code_patriarche'):
            self.code_patriarche = self.code_patriarche or None
        return super(Operation, self).save(*args, **kwargs)


m2m_changed.connect(force_cached_label_changed, sender=Operation.towns.through)


def operation_post_save(sender, **kwargs):
    if not kwargs['instance']:
        return
    operation = kwargs['instance']
    operation.skip_history_when_saving = True
    if operation.fnap_financing and operation.cost:
        fnap_cost = int(float(operation.cost) / 100 * operation.fnap_financing)
        if not operation.fnap_cost or operation.fnap_cost != fnap_cost:
            operation.fnap_cost = fnap_cost
            operation.save()
    elif operation.fnap_cost and operation.cost:
        fnap_percent = float(operation.fnap_cost) * 100 / operation.cost
        if operation.fnap_financing != fnap_percent:
            operation.fnap_financing = fnap_percent
            operation.save()
    cached_label_changed(sender, **kwargs)
    if operation.associated_file:
        operation.associated_file.update_short_menu_class()
        # manage parcel association
        for parcel in operation.parcels.all():
            parcel.copy_to_file()
post_save.connect(operation_post_save, sender=Operation)


class RelationType(GeneralRelationType):
    inverse_relation = models.ForeignKey(
        'RelationType', verbose_name=_(u"Inverse relation"), blank=True,
        null=True)

    class Meta:
        verbose_name = _(u"Operation relation type")
        verbose_name_plural = _(u"Operation relation types")
        ordering = ('order', 'label')


class RecordRelations(GeneralRecordRelations, models.Model):
    MAIN_ATTR = 'left_record'
    left_record = models.ForeignKey(Operation,
                                    related_name='right_relations')
    right_record = models.ForeignKey(Operation,
                                     related_name='left_relations')
    relation_type = models.ForeignKey(RelationType)

    class Meta:
        verbose_name = _(u"Operation record relation")
        verbose_name_plural = _(u"Operation record relations")
        ordering = ('left_record', 'relation_type')

post_delete.connect(post_delete_record_relation, sender=RecordRelations)


class OperationByDepartment(models.Model):
    """
    Database view for dashboard
    """
    operation = models.ForeignKey(Operation, verbose_name=_(u"Operation"))
    department = models.ForeignKey(Department, verbose_name=_(u"Department"),
                                   blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operation_department'


class OperationSource(Source):
    SHOW_URL = 'show-operationsource'
    MODIFY_URL = 'operation_source_modify'
    TABLE_COLS = ['operation__code_patriarche', 'operation__year',
                  'operation__operation_code', 'code'] + Source.TABLE_COLS

    # search parameters
    BOOL_FIELDS = ['duplicate']
    EXTRA_REQUEST_KEYS = {
        'title': 'title__icontains',
        'description': 'description__icontains',
        'comment': 'comment__icontains',
        'additional_information': 'additional_information__icontains',
        'person': 'authors__person__pk',
        'operation__towns': 'operation__towns__pk',
        'operation__operation_code': 'operation__operation_code',
        'operation__code_patriarche': 'operation__code_patriarche',
        'operation__operation_type': 'operation__operation_type__pk',
        'operation__year': 'operation__year'}
    COL_LABELS = {
        'operation__year': _(u"Operation year"),
        'operation__operation_code': _(u"Operation code"),
        'code': _(u"Document code")
    }

    # fields
    operation = models.ForeignKey(Operation, verbose_name=_(u"Operation"),
                                  related_name="source")
    index = models.IntegerField(verbose_name=_(u"Index"), blank=True,
                                null=True)

    class Meta:
        verbose_name = _(u"Operation documentation")
        verbose_name_plural = _(u"Operation documentations")
        permissions = (
            ("view_operationsource",
             ugettext(u"Can view all Operation sources")),
            ("view_own_operationsource",
             ugettext(u"Can view own Operation source")),
            ("add_own_operationsource",
             ugettext(u"Can add own Operation source")),
            ("change_own_operationsource",
             ugettext(u"Can change own Operation source")),
            ("delete_own_operationsource",
             ugettext(u"Can delete own Operation source")),
        )

    @property
    def owner(self):
        return self.operation

    @property
    def code(self):
        return u"{}-{:04d}".format(self.operation.code_patriarche or '',
                                   self.index)

    @classmethod
    def get_query_owns(cls, user):
        return (Q(operation__in_charge=user.ishtaruser.person) |
                Q(operation__scientist=user.ishtaruser.person) |
                Q(operation__collaborators__pk=user.ishtaruser.person.pk)) \
               & Q(operation__end_date__isnull=True)


class ActType(GeneralType):
    TYPE = (('F', _(u'Archaeological file')),
            ('O', _(u'Operation')),
            ('TF', _(u'Treatment request')),
            ('T', _(u'Treatment')),
            )
    intented_to = models.CharField(_(u"Intended to"), max_length=2,
                                   choices=TYPE)
    code = models.CharField(_(u"Code"), max_length=10, blank=True, null=True)
    associated_template = models.ManyToManyField(
        DocumentTemplate, blank=True, null=True,
        verbose_name=_(u"Associated template"), related_name='acttypes')
    indexed = models.BooleanField(_(u"Indexed"), default=False)

    class Meta:
        verbose_name = _(u"Act type")
        verbose_name_plural = _(u"Act types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=ActType)
post_delete.connect(post_save_cache, sender=ActType)


class AdministrativeAct(BaseHistorizedItem, OwnPerms, ValueGetter):
    TABLE_COLS = ['full_ref', 'year', 'index', 'act_type', 'act_object',
                  'signature_date', 'associated_file', 'operation',
                  'towns_label']
    TABLE_COLS_FILE = [
        'full_ref', 'year', 'index', 'act_type',
        'act_object', 'associated_file', 'towns_label',
    ]
    TABLE_COLS_OPE = ['full_ref', 'year', 'index', 'act_type', 'operation',
                      'act_object', 'towns_label']
    if settings.COUNTRY == 'fr':
        TABLE_COLS.append('departments_label')
        TABLE_COLS_FILE.append('departments_label')
        TABLE_COLS_OPE.append('departments_label')

    # search parameters
    DATED_FIELDS = ['signature_date__lte', 'signature_date__gte']
    ASSOCIATED_MODELS = [
        ('File', 'associated_file'),
        (Person, 'associated_file__general_contractor')]
    EXTRA_REQUEST_KEYS = {
        'act_object': 'act_object__icontains',
        'act_type__intented_to': 'act_type__intented_to',
        'associated_file__general_contractor__attached_to':
            'associated_file__general_contractor__attached_to__pk',
        'associated_file__name': 'associated_file__name__icontains',
        'associated_file__operations__code_patriarche':
        'associated_file__operations__code_patriarche',
        'associated_file__permit_reference':
            'associated_file__permit_reference__icontains',
        'associated_file__towns': 'associated_file__towns__pk',
        'associated_file__towns__numero_insee__startswith':
        'associated_file__towns__numero_insee__startswith',
        'indexed': 'index__isnull',
        'history_creator':
        'history_creator__ishtaruser__person__pk',
        'history_modifier':
        'history_modifier__ishtaruser__person__pk',
        'operation__code_patriarche': 'operation__code_patriarche',
        'operation__towns': 'operation__towns__pk',
        'operation__towns__numero_insee__startswith':
        'operation__towns__numero_insee__startswith',
        'parcel_0': ('associated_file__parcels__section',
                     'operation__parcels__section',
                     'operation__associated_file__parcels__section'),
        'parcel_1': (
            'associated_file__parcels__parcel_number'
            'operation__parcels__parcel_number',
            'operation__associated_file__parcels__parcel_number'),
        'parcel_2': (
            'associated_file__parcels__public_domain',
            'operation__parcels__public_domain',
            'operation__associated_file__parcels__public_domain'),
        'signature_date_before': 'signature_date__lte',
        'signature_date_after': 'signature_date__gte',
        'year': 'signature_date__year',
    }
    REVERSED_BOOL_FIELDS = ['index__isnull']
    RELATIVE_SESSION_NAMES = [('operation', 'operation__pk'),
                              ('file', 'associated_file__pk')]
    COL_LABELS = {'full_ref': _(u"Ref.")}

    # fields
    act_type = models.ForeignKey(ActType, verbose_name=_(u"Act type"))
    in_charge = models.ForeignKey(
        Person, blank=True, null=True,
        related_name='adminact_operation_in_charge',
        verbose_name=_(u"Person in charge of the operation"),
        on_delete=models.SET_NULL,)
    index = models.IntegerField(verbose_name=_(u"Index"), blank=True,
                                null=True)
    operator = models.ForeignKey(
        Organization, blank=True, null=True,
        verbose_name=_(u"Archaeological preventive operator"),
        related_name='adminact_operator', on_delete=models.SET_NULL)
    scientist = models.ForeignKey(
        Person, blank=True, null=True,
        related_name='adminact_scientist', on_delete=models.SET_NULL,
        verbose_name=_(u"Scientist in charge"))
    signatory = models.ForeignKey(
        Person, blank=True, null=True, related_name='signatory',
        verbose_name=_(u"Signatory"), on_delete=models.SET_NULL,)
    operation = models.ForeignKey(
        Operation, blank=True, null=True,
        related_name='administrative_act', verbose_name=_(u"Operation"))
    associated_file = models.ForeignKey(
        'archaeological_files.File',
        blank=True, null=True,
        related_name='administrative_act',
        verbose_name=_(u"Archaeological file"))
    treatment_file = models.ForeignKey(
        'archaeological_finds.TreatmentFile',
        blank=True, null=True,
        related_name='administrative_act',
        verbose_name=_(u"Treatment request"))
    treatment = models.ForeignKey(
        'archaeological_finds.Treatment',
        blank=True, null=True,
        related_name='administrative_act',
        verbose_name=_(u"Treatment"))
    signature_date = models.DateField(_(u"Signature date"), blank=True,
                                      null=True)
    year = models.IntegerField(_(u"Year"), blank=True, null=True)
    act_object = models.TextField(_(u"Object"), max_length=300, blank=True,
                                  null=True)
    if settings.COUNTRY == 'fr':
        ref_sra = models.CharField(u"Référence SRA", max_length=15,
                                   blank=True, null=True)
        departments_label = models.TextField(
            _(u"Departments"), blank=True, null=True,
            help_text=_(u"Cached values get from associated departments"))
    towns_label = models.TextField(
        _(u"Towns"), blank=True, null=True,
        help_text=_(u"Cached values get from associated towns"))
    history = HistoricalRecords()
    _prefix = 'adminact_'

    class Meta:
        ordering = ('year', 'signature_date', 'index', 'act_type')
        verbose_name = _(u"Administrative act")
        verbose_name_plural = _(u"Administrative acts")
        permissions = (
            ("view_administrativeact",
             ugettext(u"Can view all Administrative acts")),
            ("view_own_administrativeact",
             ugettext(u"Can view own Administrative act")),
            ("add_own_administrativeact",
             ugettext(u"Can add own Administrative act")),
            ("change_own_administrativeact",
             ugettext(u"Can change own Administrative act")),
            ("delete_own_administrativeact",
             ugettext(u"Can delete own Administrative act")),
        )

    def __unicode__(self):
        return settings.JOINT.join(
            [unicode(item) for item in [
                self.related_item, self.act_object]
             if item])

    full_ref_lbl = _(u"Ref.")

    @property
    def full_ref(self):
        lbl = []
        if self.year:
            lbl.append(unicode(self.year))
        if self.index:
            lbl.append(u"n°%d" % self.index)
        if settings.COUNTRY == 'fr' and self.ref_sra:
            lbl.append(u"[%s]" % self.ref_sra)
        return u" ".join(lbl)

    @property
    def associated_filename(self):
        return self.get_filename()

    @property
    def towns(self):
        if self.associated_file:
            return self.associated_file.towns.all()
        elif self.operation:
            return self.operation.towns.all()
        return []

    @property
    def departments(self):
        if settings.COUNTRY != 'fr':
            return ''
        q = None
        if self.associated_file:
            q = self.associated_file.towns.all()
        elif self.operation:
            q = self.operation.towns.all()
        if not q:
            return ''
        dpts = []
        for town in q:
            dpt = town.numero_insee[:2]
            if dpt not in dpts:
                dpts.append(dpt)
        return ', '.join(list(sorted(dpts)))

    @property
    def related_item(self):
        if self.operation:
            return self.operation
        if self.associated_file:
            return self.associated_file
        if self.treatment:
            return self.treatment
        if self.treatment_file:
            return self.treatment_file

    def get_filename(self):
        filename = self.related_item.associated_filename
        filename = u"-".join(filename.split('-')[:-1])  # remove date
        if self.act_type.code:
            filename += u"-" + self.act_type.code
        if self.signature_date and self.index:
            filename += u"-%d-%d" % (self.signature_date.year,
                                     self.index)
        if self.signature_date:
            filename += u"-" + self.signature_date.strftime('%Y%m%d')
        return filename

    def publish(self, template_pk=None):
        if not self.act_type.associated_template.count():
            return
        if not template_pk:
            template = self.act_type.associated_template.all()[0]
        else:
            q = self.act_type.associated_template.filter(pk=template_pk)
            if not q.count():
                return
            template = q.all()[0]
        return template.publish(self)

    def _get_index(self):
        if not self.index:
            c_index = 1
            q = AdministrativeAct.objects.filter(
                act_type__indexed=True, signature_date__year=self.year,
                index__isnull=False).order_by("-index")
            if q.count():
                c_index = q.all()[0].index + 1
            self.index = c_index
        conflict = AdministrativeAct.objects.filter(
            act_type__indexed=True, signature_date__year=self.year,
            index=self.index)
        if self.pk:
            conflict = conflict.exclude(pk=self.pk)
        if conflict.count():
            if self.pk:
                raise ValidationError(_(u"This index already exists for "
                                        u"this year"))
            else:
                self._get_index()

    def clean(self, *args, **kwargs):
        if not self.signature_date:
            return super(AdministrativeAct, self).clean(*args, **kwargs)
        self.year = self.signature_date.year
        if not self.act_type.indexed:
            return super(AdministrativeAct, self).clean(*args, **kwargs)
        self._get_index()
        super(AdministrativeAct, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if settings.COUNTRY == 'fr':
            self.departments_label = self.departments
        self.towns_label = u", ".join(
            list(sorted([unicode(town) for town in self.towns])))

        force = False
        if 'force' in kwargs:
            force = kwargs.pop('force')

        if not self.signature_date:
            return super(AdministrativeAct, self).save(*args, **kwargs)
        self.year = self.signature_date.year

        if not self.act_type.indexed:
            return super(AdministrativeAct, self).save(*args, **kwargs)

        if not force:
            self._get_index()
        else:
            try:
                self._get_index()
            except:
                pass

        super(AdministrativeAct, self).save(*args, **kwargs)
        if hasattr(self, 'associated_file') and self.associated_file:
            self.associated_file.update_has_admin_act()
            self.associated_file.update_short_menu_class()


def strip_zero(value):
    for idx, nb in enumerate(value):
        if nb != '0':
            return value[idx:]
    return value


class Parcel(LightHistorizedItem):
    associated_file = models.ForeignKey(
        'archaeological_files.File',
        related_name='parcels', verbose_name=_(u"File"),
        blank=True, null=True, on_delete=models.CASCADE)
    operation = models.ForeignKey(
        Operation, related_name='parcels', blank=True, null=True,
        verbose_name=_(u"Operation"), on_delete=models.CASCADE)
    year = models.IntegerField(_(u"Year"), blank=True, null=True)
    town = models.ForeignKey(Town, related_name='parcels',
                             verbose_name=_(u"Town"))
    section = models.CharField(_(u"Section"), max_length=4,
                               null=True, blank=True)
    parcel_number = models.CharField(_(u"Parcel number"), max_length=6,
                                     null=True, blank=True)
    public_domain = models.BooleanField(_(u"Public domain"), default=False)
    external_id = models.CharField(_(u"External ID"), max_length=100,
                                   null=True, blank=True)
    auto_external_id = models.BooleanField(
        _(u"External ID is set automatically"), default=False)
    address = models.TextField(_(u"Address - Locality"), null=True, blank=True)

    class Meta:
        verbose_name = _(u"Parcel")
        verbose_name_plural = _(u"Parcels")
        ordering = ('year', 'section', 'parcel_number')

    @property
    def short_label(self):
        items = [unicode(item) for item in [self.section, self.parcel_number]
                 if item]
        if self.public_domain:
            items.append(unicode(_(u"Public domain")))
        return settings.JOINT.join(items)

    def __unicode__(self):
        return self.short_label

    """
    def merge(self, parcel):
        # cannot automatically merge
        if self.address and parcel.address and self.address != parcel.address:
            return
        if self.external_id and parcel.external_id and \
           self.external_id != parcel.external_id:
            return
        if self.year and parcel.year and \
           self.year != parcel.year:
            return
        self.address = self.address or parcel.address
        self.external_id = self.external_id or parcel.external_id
        self.year = self.year or parcel.year
        self.save()
        for owner in parcel.owners.all():
            owner.parcel = self
            owner.save()
        if hasattr(parcel, 'context_record'):
            for cr in parcel.context_record.all():
                cr.parcel = self
                cr.save()
        parcel.delete()
    """

    @classmethod
    def grouped_parcels(cls, parcels):
        sortkeyfn = lambda s: (getattr(s, 'town_id'),
                               getattr(s, 'section'), getattr(s, 'year'))
        parcels = sorted(parcels, key=sortkeyfn)
        grouped = []
        for keys, parcel_grp in groupby(parcels, key=sortkeyfn):
            for idx, parcel in enumerate(parcel_grp):
                if not idx:
                    grouped.append(parcel)
                    grouped[-1].parcel_numbers = []
                nb = ""
                if parcel.parcel_number:
                    nb = u"0" * (12 - len(parcel.parcel_number)) + \
                        parcel.parcel_number
                if parcel.public_domain:
                    if nb:
                        nb += " "
                    nb += unicode(_(u"Public domain"))
                grouped[-1].parcel_numbers.append(nb)
            grouped[-1].parcel_numbers.sort()
            grouped[-1].parcel_numbers = [strip_zero(n)
                                          for n in grouped[-1].parcel_numbers]
        return grouped

    @classmethod
    def render_parcels(cls, parcels):
        parcels = cls.grouped_parcels(parcels)
        res = ''
        c_town, c_section = '', ''
        for idx, parcels in enumerate(parcels):
            if c_town != unicode(parcels.town):
                c_town = unicode(parcels.town)
                c_section = ''
                if idx:
                    res += " ; "
                res += unicode(parcels.town) + u' : '
            if c_section:
                res += u" / "
            c_section = parcels.section
            res += parcels.section + u' '
            res += u", ".join(parcels.parcel_numbers)
            if parcels.year:
                res += " (%s)" % unicode(parcels.year)
        return res

    def long_label(self):
        items = [unicode(self.operation) or
                 unicode(self.associated_file) or ""]
        items += [unicode(item) for item in [self.section, self.parcel_number]
                  if item]
        return settings.JOINT.join(items)

    def copy_to_file(self):
        """
        Copy from operation to file when associating file to operation
        """
        if not self.operation or not self.operation.associated_file:
            # not concerned
            return
        keys = {'town': self.town, 'section': self.section,
                'parcel_number': self.parcel_number}
        if self.operation.associated_file.parcels.filter(**keys).count():
            # everything is OK
            return
        keys['address'] = self.address
        keys['year'] = self.year
        keys['associated_file'] = self.operation.associated_file
        new_p = Parcel.objects.create(**keys)
        # also copy owning
        for owning in self.owners.all():
            ParcelOwner.objects.create(
                owner=owning.owner, parcel=new_p,
                start_date=owning.start_date, end_date=owning.end_date)

    def copy_to_operation(self):
        """
        Parcel cannot have operation and associated_file but on
        new parcel association a copy have to be done before cleaning
        """
        if not (self.operation and self.associated_file):
            # everything is OK
            return
        keys = {'town': self.town, 'section': self.section,
                'parcel_number': self.parcel_number,
                'operation': self.operation,
                'associated_file': None,
                'defaults': {'address': self.address, 'year': self.year}
                }
        new_p, created = Parcel.objects.get_or_create(**keys)
        # copy owning only if created
        if created:
            for owning in self.owners.all():
                ParcelOwner.objects.create(
                    owner=owning.owner, parcel=new_p,
                    start_date=owning.start_date, end_date=owning.end_date)
        self.operation = None
        self.save()


def parcel_post_save(sender, **kwargs):
    if not kwargs['instance']:
        return
    parcel = kwargs['instance']
    created = kwargs.get('created', None)

    updated = False
    # remove when the parcel is linked to nothing
    if not getattr(parcel, '_updated_id', None) and not created \
            and not parcel.operation and not parcel.associated_file:
        if parcel.context_record.count():
            # trying to restore a lost parcel
            parcel.operation = parcel.context_record.all()[0].operation
            updated = True
        else:
            parcel.delete()
            return

    if not parcel.external_id or parcel.auto_external_id:
        external_id = get_external_id('parcel_external_id', parcel)
        if external_id != parcel.external_id:
            updated = True
            parcel._updated_id = True
            parcel.auto_external_id = True
            parcel.external_id = external_id
    if updated:
        parcel.save()
        return

    if parcel.context_record.count():
        if settings.TESTING and settings.USE_SPATIALITE_FOR_TESTS:
            for cr in parcel.context_record.all():
                cr.skip_history_when_saving = True
                cr.save()
        else:
            parcel.context_record.model.cached_label_bulk_update(
                parcel_id=parcel.id)

    if parcel.operation and parcel.operation.pk and \
       parcel.town not in list(parcel.operation.towns.all()):
        parcel.operation.towns.add(parcel.town)
    if parcel.associated_file and \
       parcel.associated_file.pk and \
       parcel.town not in list(parcel.associated_file.towns.all()):
        parcel.associated_file.towns.add(parcel.town)
    if parcel.operation and parcel.associated_file:
        # parcels are copied between files and operations
        parcel.copy_to_operation()

post_save.connect(parcel_post_save, sender=Parcel)


class ParcelOwner(LightHistorizedItem):
    owner = models.ForeignKey(Person, verbose_name=_(u"Owner"),
                              related_name="parcel_owner")
    parcel = models.ForeignKey(Parcel, verbose_name=_(u"Parcel"),
                               related_name='owners')
    start_date = models.DateField(_(u"Start date"))
    end_date = models.DateField(_(u"End date"))

    class Meta:
        verbose_name = _(u"Parcel owner")
        verbose_name_plural = _(u"Parcel owners")

    def __unicode__(self):
        return self.owner + settings.JOINT + self.parcel


class OperationDashboard:
    def __init__(self):
        main_dashboard = Dashboard(Operation)

        self.total_number = main_dashboard.total_number

        self.filters_keys = [
            'recorded', 'effective', 'active', 'field',
            'documented', 'closed', 'documented_closed']
        filters = {
            'recorded': {},
            'effective': {'scientist__isnull': False},
            'active': {'scientist__isnull': False, 'end_date__isnull': True},
            'field': {'excavation_end_date__isnull': True},
            'documented': {'source__isnull': False},
            'documented_closed': {'source__isnull': False,
                                  'end_date__isnull': False},
            'closed': {'end_date__isnull': False}
        }
        filters_label = {
            'recorded': _(u"Recorded"),
            'effective': _(u"Effective"),
            'active': _(u"Active"),
            'field': _(u"Field completed"),
            'documented': _(u"Associated report"),
            'closed': _(u"Closed"),
            'documented_closed': _(u"Documented and closed"),
        }
        self.filters_label = [filters_label[k] for k in self.filters_keys]
        self.total = []
        for fltr_key in self.filters_keys:
            fltr, lbl = filters[fltr_key], filters_label[fltr_key]
            nb = Operation.objects.filter(**fltr).count()
            self.total.append((lbl, nb))

        self.surface_by_type = Operation.objects\
            .values('operation_type__label')\
            .annotate(number=Sum('surface'))\
            .order_by('-number', 'operation_type__label')

        self.by_type = []
        self.types = OperationType.objects.filter(available=True).all()
        for fltr_key in self.filters_keys:
            fltr, lbl = filters[fltr_key], filters_label[fltr_key]
            type_res = Operation.objects.filter(**fltr).\
                values('operation_type', 'operation_type__label').\
                annotate(number=Count('pk')).\
                order_by('operation_type')
            types_dct = {}
            for typ in type_res.all():
                types_dct[typ['operation_type']] = typ["number"]
            types = []
            for typ in self.types:
                if typ.pk in types_dct:
                    types.append(types_dct[typ.pk])
                else:
                    types.append(0)
            self.by_type.append((lbl, types))

        self.by_year = []
        self.years = [res['year'] for res in Operation.objects.values('year')
                      .order_by('-year').distinct()]
        for fltr_key in self.filters_keys:
            fltr, lbl = filters[fltr_key], filters_label[fltr_key]
            year_res = Operation.objects.filter(**fltr)\
                                        .values('year')\
                                        .annotate(number=Count('pk'))\
                                        .order_by('year')
            years_dct = {}
            for yr in year_res.all():
                years_dct[yr['year']] = yr["number"]
            years = []
            for yr in self.years:
                if yr in years_dct:
                    years.append(years_dct[yr])
                else:
                    years.append(0)
            self.by_year.append((lbl, years))

        self.by_realisation_year = []
        self.realisation_years = [
            res['date'] for res in Operation.objects.extra(
                {'date': "date_trunc('year', start_date)"}).values('date')
            .filter(start_date__isnull=False).order_by('-date').distinct()]
        for fltr_key in self.filters_keys:
            fltr, lbl = filters[fltr_key], filters_label[fltr_key]
            year_res = Operation.objects.filter(**fltr).extra(
                {'date': "date_trunc('year', start_date)"}).values('date')\
                .values('date').filter(start_date__isnull=False)\
                .annotate(number=Count('pk'))\
                .order_by('-date')
            years_dct = {}
            for yr in year_res.all():
                years_dct[yr['date']] = yr["number"]
            years = []
            for yr in self.realisation_years:
                if yr in years_dct:
                    years.append(years_dct[yr])
                else:
                    years.append(0)
            self.by_realisation_year.append((lbl, years))

        self.effective = []
        for typ in self.types:
            year_res = Operation.objects.filter(**{'scientist__isnull': False,
                                                   'operation_type': typ})\
                                        .values('year')\
                                        .annotate(number=Count('pk'))\
                                        .order_by('-year').distinct()
            years_dct = {}
            for yr in year_res.all():
                years_dct[yr['year']] = yr["number"]
            years = []
            for yr in self.years:
                if yr in years_dct:
                    years.append(years_dct[yr])
                else:
                    years.append(0)
            self.effective.append((typ, years))

        # TODO: by date
        now = datetime.date.today()
        limit = datetime.date(now.year, now.month, 1) - datetime.timedelta(365)
        by_realisation_month = Operation.objects.filter(
            start_date__gt=limit, start_date__isnull=False).extra(
                {'date': "date_trunc('month', start_date)"})
        self.last_months = []
        date = datetime.datetime(now.year, now.month, 1)
        for mt_idx in xrange(12):
            self.last_months.append(date)
            if date.month > 1:
                date = datetime.datetime(date.year, date.month - 1, 1)
            else:
                date = datetime.datetime(date.year - 1, 12, 1)
        self.by_realisation_month = []
        for fltr_key in self.filters_keys:
            fltr, lbl = filters[fltr_key], filters_label[fltr_key]
            month_res = by_realisation_month.filter(**fltr)\
                .annotate(number=Count('pk')).order_by('-date')
            month_dct = {}
            for mt in month_res.all():
                month_dct[mt.date] = mt.number
            date = datetime.date(now.year, now.month, 1)
            months = []
            for date in self.last_months:
                if date in month_dct:
                    months.append(month_dct[date])
                else:
                    months.append(0)
            self.by_realisation_month.append((lbl, months))

        # survey and excavations
        self.survey, self.excavation = {}, {}
        for dct_res, ope_types in ((self.survey, ('arch_diagnostic',)),
                                   (self.excavation, ('prev_excavation',
                                                      'prog_excavation'))):
            dct_res['total'] = []
            operation_type = {'operation_type__txt_idx__in': ope_types}
            for fltr_key in self.filters_keys:
                fltr, lbl = filters[fltr_key], filters_label[fltr_key]
                fltr.update(operation_type)
                nb = Operation.objects.filter(**fltr).count()
                dct_res['total'].append((lbl, nb))

            dct_res['by_year'] = []
            for fltr_key in self.filters_keys:
                fltr, lbl = filters[fltr_key], filters_label[fltr_key]
                fltr.update(operation_type)
                year_res = Operation.objects.filter(**fltr)\
                                            .values('year')\
                                            .annotate(number=Count('pk'))\
                                            .order_by('year')
                years_dct = {}
                for yr in year_res.all():
                    years_dct[yr['year']] = yr["number"]
                years = []
                for yr in self.years:
                    if yr in years_dct:
                        years.append(years_dct[yr])
                    else:
                        years.append(0)
                dct_res['by_year'].append((lbl, years))

            dct_res['by_realisation_year'] = []
            for fltr_key in self.filters_keys:
                fltr, lbl = filters[fltr_key], filters_label[fltr_key]
                fltr.update(operation_type)
                year_res = Operation.objects.filter(**fltr).extra(
                    {'date': "date_trunc('year', start_date)"})\
                    .values('date')\
                    .filter(start_date__isnull=False)\
                    .annotate(number=Count('pk'))\
                    .order_by('-date')
                years_dct = {}
                for yr in year_res.all():
                    years_dct[yr['date']] = yr["number"]
                years = []
                for yr in self.realisation_years:
                    if yr in years_dct:
                        years.append(years_dct[yr])
                    else:
                        years.append(0)
                dct_res['by_realisation_year'].append((lbl, years))

            current_year_ope = Operation.objects.filter(**operation_type)\
                                        .filter(
                                            year=datetime.date.today().year)
            current_realisation_year_ope = Operation.objects\
                .filter(**operation_type)\
                .filter(start_date__year=datetime.date.today().year)
            res_keys = [('area_realised', current_realisation_year_ope)]
            if dct_res == self.survey:
                res_keys.append(('area',
                                 current_year_ope))
            for res_key, base_ope in res_keys:
                dct_res[res_key] = []
                for fltr_key in self.filters_keys:
                    fltr, lbl = filters[fltr_key], filters_label[fltr_key]
                    area_res = base_ope.filter(**fltr)\
                        .annotate(number=Sum('surface')).all()
                    val = 0
                    if area_res:
                        val = (area_res[0].number or 0) / 10000.0
                    dct_res[res_key].append(val)
            # TODO...
            res_keys = [('manday_realised', current_realisation_year_ope)]
            if dct_res == self.survey:
                res_keys.append(('manday',
                                 current_year_ope))
            for res_key, base_ope in res_keys:
                dct_res[res_key] = []
                for fltr_key in self.filters_keys:
                    dct_res[res_key].append('-')
            # TODO...
            res_keys = [('mandayhect_realised', current_realisation_year_ope)]
            if dct_res == self.survey:
                res_keys.append(('mandayhect',
                                 current_year_ope))
            for res_key, base_ope in res_keys:
                dct_res[res_key] = []
                for fltr_key in self.filters_keys:
                    dct_res[res_key].append('-')
            # TODO...
            dct_res['mandayhect_real_effective'] = '-'
            if dct_res == self.survey:
                dct_res['mandayhect_effective'] = '-'

            res_keys = [('org_realised', current_realisation_year_ope)]
            if dct_res == self.survey:
                res_keys.append(('org', current_year_ope))
            for res_key, base_ope in res_keys:
                org_res = base_ope.filter(scientist__attached_to__isnull=False)\
                    .values('scientist__attached_to',
                            'scientist__attached_to__name')\
                    .annotate(area=Sum('surface'))\
                    .order_by('scientist__attached_to__name').all()
                # TODO: man-days, man-days/hectare

                dct_res[res_key] = []
                for vals in org_res:
                    vals['area'] = (vals['area'] or 0) / 10000.0
                    dct_res[res_key].append(vals)

            year_ope = Operation.objects.filter(**operation_type)
            res_keys = ['org_by_year']
            if dct_res == self.survey:
                res_keys.append('org_by_year_realised')
            q = year_ope.values('scientist__attached_to',
                                'scientist__attached_to__name')\
                .filter(scientist__attached_to__isnull=False)\
                .order_by('scientist__attached_to__name').distinct()
            org_list = [(org['scientist__attached_to'],
                         org['scientist__attached_to__name']) for org in q]
            # org_list_dct = dict(org_list)
            for res_key in res_keys:
                dct_res[res_key] = []
                years = self.years
                if res_key == 'org_by_year_realised':
                    years = self.realisation_years
                for org_id, org_label in org_list:
                    org_res = year_ope.filter(
                        scientist__attached_to__pk=org_id)
                    key_date = ''
                    if res_key == 'org_by_year':
                        org_res = org_res.values('year')
                        key_date = 'year'
                    else:
                        org_res = org_res\
                            .extra({'date': "date_trunc('year', start_date)"})\
                            .values('date')\
                            .filter(start_date__isnull=False)
                        key_date = 'date'
                    org_res = org_res.annotate(area=Sum('surface'),
                                               cost=Sum('cost'))
                    years_dct = {}
                    for yr in org_res.all():
                        area = (yr['area'] if yr['area'] else 0) / 10000.0
                        cost = yr['cost'] if yr['cost'] else 0
                        years_dct[yr[key_date]] = (area, cost)
                    r_years = []
                    for yr in years:
                        if yr in years_dct:
                            r_years.append(years_dct[yr])
                        else:
                            r_years.append((0, 0))
                    dct_res[res_key].append((org_label, r_years))
                area_means, area_sums = [], []
                cost_means, cost_sums = [], []
                for idx, year in enumerate(years):
                    vals = [r_yars[idx] for lb, r_yars in dct_res[res_key]]
                    if not vals:
                        continue
                    sum_area = sum([a for a, c in vals])
                    sum_cost = sum([c for a, c in vals])
                    area_means.append(sum_area / len(vals))
                    area_sums.append(sum_area)
                    cost_means.append(sum_cost / len(vals))
                    cost_sums.append(sum_cost)
                dct_res[res_key + '_area_mean'] = area_means
                dct_res[res_key + '_area_sum'] = area_sums
                dct_res[res_key + '_cost_mean'] = cost_means
                dct_res[res_key + '_cost_mean'] = cost_sums

            if dct_res == self.survey:
                self.survey['effective'] = []
                for yr in self.years:
                    year_res = Operation.objects\
                        .filter(scientist__isnull=False, year=yr,
                                operation_type__txt_idx__in=ope_types)\
                        .annotate(number=Sum('surface'), mean=Avg('surface'))
                    nb = year_res[0].number if year_res.count() else 0
                    nb = nb if nb else 0
                    mean = year_res[0].mean if year_res.count() else 0
                    mean = mean if mean else 0
                    self.survey['effective'].append((nb, mean))

            # TODO:Man-Days/hectare by Year

            # CHECK: month of realisation or month?
            dct_res['by_month'] = []
            for fltr_key in self.filters_keys:
                fltr, lbl = filters[fltr_key], filters_label[fltr_key]
                fltr.update(operation_type)
                month_res = by_realisation_month\
                    .filter(**fltr)\
                    .annotate(number=Count('pk'))\
                    .order_by('-date')
                month_dct = {}
                for mt in month_res.all():
                    month_dct[mt.date] = mt.number
                date = datetime.date(now.year, now.month, 1)
                months = []
                for date in self.last_months:
                    if date in month_dct:
                        months.append(month_dct[date])
                    else:
                        months.append(0)
                dct_res['by_month'].append((lbl, months))

            operation_type = {'operation_type__txt_idx__in': ope_types}
            self.departments = [
                (fd['department__pk'], fd['department__label'])
                for fd in OperationByDepartment
                .objects.filter(department__isnull=False)
                .values('department__label', 'department__pk')
                .order_by('department__label').distinct()]
            dct_res['by_dpt'] = []
            for dpt_id, dpt_label in self.departments:
                vals = OperationByDepartment.objects\
                    .filter(department__pk=dpt_id,
                            operation__operation_type__txt_idx__in=ope_types)\
                    .values('department__pk', 'operation__year')\
                    .annotate(number=Count('operation'))\
                    .order_by('operation__year')
                dct_years = {}
                for v in vals:
                    dct_years[v['operation__year']] = v['number']
                years = []
                for y in self.years:
                    if y in dct_years:
                        years.append(dct_years[y])
                    else:
                        years.append(0)
                years.append(sum(years))
                dct_res['by_dpt'].append((dpt_label, years))
            dct_res['effective_by_dpt'] = []
            for dpt_id, dpt_label in self.departments:
                vals = OperationByDepartment.objects\
                    .filter(department__pk=dpt_id,
                            operation__scientist__isnull=False,
                            operation__operation_type__txt_idx__in=ope_types)\
                    .values('department__pk', 'operation__year')\
                    .annotate(number=Count('operation'),
                              area=Sum('operation__surface'),
                              fnap=Sum('operation__fnap_cost'),
                              cost=Sum('operation__cost'))\
                    .order_by('operation__year')
                dct_years = {}
                for v in vals:
                    values = []
                    for k in ('number', 'area', 'cost', 'fnap'):
                        value = v[k] or 0
                        if k == 'area':
                            value /= 10000.0
                        values.append(value)

                    dct_years[v['operation__year']] = values
                years = []
                for y in self.years:
                    if y in dct_years:
                        years.append(dct_years[y])
                    else:
                        years.append((0, 0, 0, 0))
                nbs, areas, costs, fnaps = zip(*years)
                years.append((sum(nbs), sum(areas), sum(costs), sum(fnaps)))
                dct_res['effective_by_dpt'].append((dpt_label, years))

            OperationTown = Operation.towns.through
            query = OperationTown.objects\
                .filter(operation__scientist__isnull=False,
                        operation__operation_type__txt_idx__in=ope_types)\
                .values('town__name', 'town__departement__number')\
                .annotate(nb=Count('operation'))\
                .order_by('-nb', 'town__name')[:10]
            dct_res['towns'] = []
            for r in query:
                dct_res['towns'].append((u"%s (%s)" % (r['town__name'],
                                         r['town__departement__number']),
                                         r['nb']))

            if dct_res == self.survey:
                query = OperationTown.objects\
                    .filter(operation__scientist__isnull=False,
                            operation__operation_type__txt_idx__in=ope_types,
                            operation__surface__isnull=False)\
                    .values('town__name', 'town__departement__number')\
                    .annotate(nb=Sum('operation__surface'))\
                    .order_by('-nb', 'town__name')[:10]
                dct_res['towns_surface'] = []
                for r in query:
                    dct_res['towns_surface'].append((u"%s (%s)" % (
                        r['town__name'], r['town__departement__number']),
                        r['nb']))
            else:
                query = OperationTown.objects\
                    .filter(operation__scientist__isnull=False,
                            operation__operation_type__txt_idx__in=ope_types,
                            operation__cost__isnull=False)\
                    .values('town__name', 'town__departement__number')\
                    .annotate(nb=Sum('operation__cost'))\
                    .order_by('-nb', 'town__name')[:10]
                dct_res['towns_cost'] = []
                for r in query:
                    dct_res['towns_cost'].append((u"%s (%s)" % (
                        r['town__name'], r['town__departement__number']),
                        r['nb']))


class OperationTypeOld(GeneralType):
    order = models.IntegerField(_(u"Order"), default=1)
    preventive = models.BooleanField(_(u"Is preventive"), default=True)

    class Meta:
        verbose_name = _(u"Operation type old")
        verbose_name_plural = _(u"Operation types old")
        ordering = ['-preventive', 'order', 'label']
