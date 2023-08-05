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

from django.conf import settings
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext_lazy as _, ugettext, pgettext

from ishtar_common.utils import cached_label_changed

from ishtar_common.models import GeneralType, BaseHistorizedItem, \
    HistoricalRecords, OwnPerms, ShortMenuItem, Source, GeneralRelationType,\
    GeneralRecordRelations, post_delete_record_relation, get_external_id, \
    ImageModel, post_save_cache, ValueGetter
from archaeological_operations.models import Operation, Period, Parcel


class DatingType(GeneralType):
    class Meta:
        verbose_name = _(u"Dating type")
        verbose_name_plural = _(u"Dating types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=DatingType)
post_delete.connect(post_save_cache, sender=DatingType)


class DatingQuality(GeneralType):
    class Meta:
        verbose_name = _(u"Dating quality type")
        verbose_name_plural = _(u"Dating quality types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=DatingQuality)
post_delete.connect(post_save_cache, sender=DatingQuality)


class Dating(models.Model):
    period = models.ForeignKey(Period, verbose_name=_(u"Period"))
    start_date = models.IntegerField(_(u"Start date"), blank=True, null=True)
    end_date = models.IntegerField(_(u"End date"), blank=True, null=True)
    dating_type = models.ForeignKey(DatingType, verbose_name=_(u"Dating type"),
                                    blank=True, null=True)
    quality = models.ForeignKey(DatingQuality, verbose_name=_(u"Quality"),
                                blank=True, null=True)
    precise_dating = models.TextField(_(u"Precise dating"), blank=True,
                                      null=True)

    class Meta:
        verbose_name = _(u"Dating")
        verbose_name_plural = _(u"Datings")

    def __unicode__(self):
        start_date = self.start_date and unicode(self.start_date) or u""
        end_date = self.end_date and unicode(self.end_date) or u""
        if not start_date and not end_date:
            return unicode(self.period)
        return u"%s (%s-%s)" % (self.period, start_date, end_date)

    @classmethod
    def fix_dating_association(cls, obj):
        """
        Fix redundant m2m dating association (usually after imports)
        """
        current_datings = []
        for dating in obj.datings.order_by('pk').all():
            key = (dating.period.pk, dating.start_date, dating.end_date,
                   dating.dating_type, dating.quality, dating.precise_dating)
            if key not in current_datings:
                current_datings.append(key)
                continue
            dating.delete()


class Unit(GeneralType):
    order = models.IntegerField(_(u"Order"))
    parent = models.ForeignKey(
        "Unit", verbose_name=_(u"Parent context record type"),
        blank=True, null=True)

    class Meta:
        verbose_name = _(u"Context record Type")
        verbose_name_plural = _(u"Context record Types")
        ordering = ('order', 'label')

    def __unicode__(self):
        return self.label
post_save.connect(post_save_cache, sender=Unit)
post_delete.connect(post_save_cache, sender=Unit)


class ActivityType(GeneralType):
    order = models.IntegerField(_(u"Order"))

    class Meta:
        verbose_name = _(u"Activity Type")
        verbose_name_plural = _(u"Activity Types")
        ordering = ('order',)

    def __unicode__(self):
        return self.label
post_save.connect(post_save_cache, sender=ActivityType)
post_delete.connect(post_save_cache, sender=ActivityType)


class IdentificationType(GeneralType):
    order = models.IntegerField(_(u"Order"))

    class Meta:
        verbose_name = _(u"Identification Type")
        verbose_name_plural = _(u"Identification Types")
        ordering = ('order', 'label')

    def __unicode__(self):
        return self.label
post_save.connect(post_save_cache, sender=IdentificationType)
post_delete.connect(post_save_cache, sender=IdentificationType)


class ExcavationTechnicType(GeneralType):
    class Meta:
        verbose_name = _(u"Excavation technique type")
        verbose_name_plural = _(u"Excavation technique types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=ExcavationTechnicType)
post_delete.connect(post_save_cache, sender=ExcavationTechnicType)


class DocumentationType(GeneralType):
    class Meta:
        verbose_name = _(u"Documentation type")
        verbose_name_plural = _(u"Documentation types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=DocumentationType)
post_delete.connect(post_save_cache, sender=DocumentationType)


class CRBulkView(object):
    CREATE_SQL = """
        CREATE VIEW context_records_cached_label_bulk_update
        AS (
            SELECT cr.id AS id, ope.code_patriarche AS main_code,
                ope.year AS year,
                ope.operation_code AS ope_code,
                parcel.section AS section,
                parcel.parcel_number AS number, cr.label AS label
            FROM archaeological_context_records_contextrecord AS cr
            INNER JOIN archaeological_operations_operation ope
                ON ope.id = cr.operation_id
            INNER JOIN archaeological_operations_parcel parcel
                ON cr.parcel_id = parcel.id
        );"""
    DELETE_SQL = """
        DROP VIEW context_records_cached_label_bulk_update;
    """


class ContextRecord(BaseHistorizedItem, ImageModel, OwnPerms,
                    ValueGetter, ShortMenuItem):
    SHOW_URL = 'show-contextrecord'
    SLUG = 'contextrecord'
    TABLE_COLS = ['label', 'operation__common_name', 'parcel__town__name',
                  'parcel__label', 'unit']
    if settings.COUNTRY == 'fr':
        TABLE_COLS.insert(1, 'operation__code_patriarche')
    TABLE_COLS_FOR_OPE = ['label', 'parcel', 'unit',
                          'datings__period__label', 'description']
    COL_LABELS = {
        'datings__period__label': _(u"Periods"),
        'datings__period': _(u"Datings (period)"),
        'detailled_related_context_records': _(u"Related context records"),
        'operation__code_patriarche': u"Operation (code patriarche)",
        'operation__common_name': u"Operation (name)",
        'parcel__external_id': _(u"Parcel (external ID)"),
        'parcel__town__name': _(u"Parcel (town)"),
        'parcel__town': _(u"Parcel (town)"),
        'parcel__year': _(u"Parcel (year)"),
        'section__parcel_number': _(u"Parcel"),
    }
    CONTEXTUAL_TABLE_COLS = {
        'full': {
            'related_context_records': 'detailled_related_context_records'
        }
    }
    IMAGE_PREFIX = 'context_records/'

    # search parameters
    EXTRA_REQUEST_KEYS = {
        'parcel__town': 'parcel__town__pk',
        'operation__year': 'operation__year__contains',
        'year': 'operation__year__contains',
        'operation__code_patriarche': 'operation__code_patriarche',
        'operation__operation_code': 'operation__operation_code',
        'datings__period': 'datings__period__pk',
        'parcel_0': 'operation__parcels__section',
        'parcel_1': 'operation__parcels__parcel_number',
        'parcel_2': 'operation__parcels__public_domain',
        'label': 'label__icontains',
        'archaeological_sites': 'operation__archaeological_sites__pk',
        'cached_label': 'cached_label__icontains',
    }
    RELATION_TYPES_PREFIX = {'ope_relation_types': 'operation__',
                             'cr_relation_types': ''}
    RELATIVE_SESSION_NAMES = [
        ('operation', 'operation__pk'),
        ('file', 'operation__associated_file__pk')]

    # fields
    external_id = models.TextField(_(u"External ID"), blank=True, null=True)
    auto_external_id = models.BooleanField(
        _(u"External ID is set automatically"), default=False)
    parcel = models.ForeignKey(Parcel, verbose_name=_(u"Parcel"),
                               related_name='context_record')
    operation = models.ForeignKey(Operation, verbose_name=_(u"Operation"),
                                  related_name='context_record')
    label = models.CharField(_(u"ID"), max_length=200)
    description = models.TextField(_(u"Description"), blank=True, null=True)
    comment = models.TextField(_(u"General comment"), blank=True, null=True)
    opening_date = models.DateField(_(u"Opening date"),
                                    blank=True, null=True)
    closing_date = models.DateField(_(u"Closing date"), blank=True, null=True)
    length = models.FloatField(_(u"Length (m)"), blank=True, null=True)
    width = models.FloatField(_(u"Width (m)"), blank=True, null=True)
    thickness = models.FloatField(_(u"Thickness (m)"), blank=True,
                                  null=True)
    diameter = models.FloatField(_(u"Diameter (m)"), blank=True, null=True)
    depth = models.FloatField(_(u"Depth (m)"), blank=True, null=True)
    depth_of_appearance = models.FloatField(
        _(u"Depth of appearance (m)"), blank=True, null=True)
    location = models.TextField(
        _(u"Location"), blank=True, null=True,
        help_text=_(u"A short description of the location of the context "
                    u"record"))
    datings = models.ManyToManyField(Dating)
    documentations = models.ManyToManyField(DocumentationType, blank=True,
                                            null=True)
    datings_comment = models.TextField(_(u"Comment on datings"), blank=True,
                                       null=True)
    unit = models.ForeignKey(Unit, verbose_name=_(u"Context record type"),
                             related_name='+', blank=True, null=True)
    filling = models.TextField(_(u"Filling"), blank=True, null=True)
    interpretation = models.TextField(_(u"Interpretation"), blank=True,
                                      null=True)
    taq = models.IntegerField(
        _(u"TAQ"), blank=True, null=True,
        help_text=_(u"\"Terminus Ante Quem\" the context record can't have "
                    u"been created after this date"))
    taq_estimated = models.IntegerField(
        _(u"Estimated TAQ"), blank=True, null=True,
        help_text=_(u"Estimation of a \"Terminus Ante Quem\""))
    tpq = models.IntegerField(
        _(u"TPQ"), blank=True, null=True,
        help_text=_(u"\"Terminus Post Quem\" the context record can't have "
                    u"been created before this date"))
    tpq_estimated = models.IntegerField(
        _(u"Estimated TPQ"), blank=True, null=True,
        help_text=_(u"Estimation of a \"Terminus Post Quem\""))
    identification = models.ForeignKey(
        IdentificationType, blank=True, null=True,
        verbose_name=_(u"Identification"),)
    activity = models.ForeignKey(ActivityType, blank=True, null=True,
                                 verbose_name=_(u"Activity"),)
    excavation_technic = models.ForeignKey(
        ExcavationTechnicType, blank=True, null=True,
        verbose_name=_(u"Excavation technique"))
    related_context_records = models.ManyToManyField(
        'ContextRecord', through='RecordRelations', blank=True, null=True)
    point = models.PointField(_(u"Point"), blank=True, null=True, dim=3)
    polygon = models.PolygonField(_(u"Polygon"), blank=True, null=True)
    cached_label = models.TextField(_(u"Cached name"), null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _(u"Context Record")
        verbose_name_plural = _(u"Context Record")
        permissions = (
            ("view_contextrecord", ugettext(u"Can view all Context Records")),
            ("view_own_contextrecord",
             ugettext(u"Can view own Context Record")),
            ("add_own_contextrecord",
             ugettext(u"Can add own Context Record")),
            ("change_own_contextrecord",
             ugettext(u"Can change own Context Record")),
            ("delete_own_contextrecord",
             ugettext(u"Can delete own Context Record")),
        )
        ordering = ('cached_label',)

    @property
    def name(self):
        return self.label or ""

    @property
    def short_class_name(self):
        return pgettext("short", u"Context record")

    def __unicode__(self):
        return self.short_label

    @classmethod
    def cached_label_bulk_update(cls, operation_id=None, parcel_id=None):
        if operation_id:
            where = "operation_id = %s"
            args = [int(operation_id)]
            kwargs = {'operation_id': operation_id}
        elif parcel_id:
            where = "parcel_id = %s"
            args = [int(parcel_id)]
            kwargs = {'parcel_id': parcel_id}
        else:
            return
        sql = """
        UPDATE "archaeological_context_records_contextrecord" AS cr
            SET cached_label =
                CASE
                WHEN context_records_cached_label_bulk_update.main_code
                  IS NULL
                THEN
                    CASE
                      WHEN context_records_cached_label_bulk_update.year
                            IS NOT NULL
                      AND context_records_cached_label_bulk_update.ope_code
                            IS NOT NULL
                    THEN
                       '{ope_prefix}' ||
                       context_records_cached_label_bulk_update.year ||
                       '-' ||
                       context_records_cached_label_bulk_update.ope_code
                    ELSE ''
                    END
                ELSE
                    '{main_ope_prefix}' ||
                    context_records_cached_label_bulk_update.main_code
                END
                || '{join}' ||
                context_records_cached_label_bulk_update.section || '{join}' ||
                context_records_cached_label_bulk_update.number || '{join}' ||
                context_records_cached_label_bulk_update.label
            FROM context_records_cached_label_bulk_update
            WHERE cr.id = context_records_cached_label_bulk_update.id
                  AND cr.id IN (
                SELECT id FROM archaeological_context_records_contextrecord
                WHERE {where}
            );
        """.format(main_ope_prefix=settings.ISHTAR_OPE_PREFIX,
                   ope_prefix=settings.ISHTAR_DEF_OPE_PREFIX,
                   join=settings.JOINT, where=where)
        # with connection.cursor() as c:  # django 1.8
        c = connection.cursor()
        c.execute(sql, args)
        transaction.commit_unless_managed()
        cls._meta.get_field_by_name(
            'base_finds')[0].model.cached_label_bulk_update(**kwargs)

    @property
    def short_label(self):
        return settings.JOINT.join([unicode(item) for item in [
            self.operation.get_reference(), self.parcel, self.label] if item])

    @property
    def show_url(self):
        return reverse('show-contextrecord', args=[self.pk, ''])

    @classmethod
    def get_query_owns(cls, user):
        return (Q(operation__scientist=user.ishtaruser.person) |
                Q(operation__in_charge=user.ishtaruser.person) |
                Q(operation__collaborators__pk=user.ishtaruser.person.pk) |
                Q(history_creator=user)) \
            & Q(operation__end_date__isnull=True)

    @classmethod
    def get_owns(cls, user, menu_filtr=None, limit=None,
                 values=None, get_short_menu_class=None):
        replace_query = None
        if menu_filtr and 'operation' in menu_filtr:
            replace_query = Q(operation=menu_filtr['operation'])
        owns = super(ContextRecord, cls).get_owns(
            user, replace_query=replace_query,
            limit=limit, values=values,
            get_short_menu_class=get_short_menu_class)
        return cls._return_get_owns(owns, values, get_short_menu_class)

    def full_label(self):
        return unicode(self)

    def _real_label(self):
        if not self.operation.code_patriarche:
            return
        return settings.JOINT.join((self.operation.code_patriarche,
                                    self.label))

    def _temp_label(self):
        if self.operation.code_patriarche:
            return
        return settings.JOINT.join([unicode(lbl) for lbl in [
            self.operation.year, self.operation.operation_code, self.label]
            if lbl])

    def _generate_cached_label(self):
        return self.full_label()

    def _get_associated_cached_labels(self):
        from archaeological_finds.models import Find, BaseFind
        return list(Find.objects.filter(base_finds__context_record=self).all())\
            + list(BaseFind.objects.filter(context_record=self).all())

    def _cached_labels_bulk_update(self):
        if settings.TESTING and settings.USE_SPATIALITE_FOR_TESTS:
            return
        self.base_finds.model.cached_label_bulk_update(
            context_record_id=self.pk)
        return True

    @property
    def reference(self):
        if not self.operation:
            return "00"
        return self.full_label()

    def get_department(self):
        if not self.operation:
            return "00"
        return self.operation.get_department()

    def get_town_label(self):
        if not self.operation:
            return "00"
        return self.operation.get_town_label()

    @classmethod
    def get_periods(cls, slice='year', fltr={}):
        q = cls.objects
        if fltr:
            q = q.filter(**fltr)
        if slice == 'year':
            years = set()
            for res in list(q.values('operation__start_date')):
                if res['operation__start_date']:
                    yr = res['operation__start_date'].year
                    years.add(yr)
            return list(years)
        return []

    @classmethod
    def get_by_year(cls, year, fltr={}):
        q = cls.objects
        if fltr:
            q = q.filter(**fltr)
        return q.filter(operation__start_date__year=year)

    @classmethod
    def get_operations(cls):
        return [dct['operation__pk']
                for dct in cls.objects.values('operation__pk').distinct()]

    @classmethod
    def get_by_operation(cls, operation_id):
        return cls.objects.filter(operation__pk=operation_id)

    @classmethod
    def get_total_number(cls, fltr={}):
        q = cls.objects
        if fltr:
            q = q.filter(**fltr)
        return q.count()

    def detailled_related_context_records(self):
        crs = []
        for cr in self.right_relations.all():
            crs.append(u"{} ({})".format(cr.right_record,
                                         cr.relation_type.get_tiny_label()))
        return u" ; ".join(crs)

    def find_docs_q(self):
        from archaeological_finds.models import FindSource
        return FindSource.objects.filter(find__base_finds__context_record=self)

    def save(self, *args, **kwargs):
        returned = super(ContextRecord, self).save(*args, **kwargs)
        updated = False
        if not self.external_id or self.auto_external_id:
            external_id = get_external_id('context_record_external_id', self)
            if external_id != self.external_id:
                updated = True
                self.auto_external_id = True
                self.external_id = external_id
        if updated:
            self._cached_label_checked = False
            self.save()
        return returned

    def fix(self):
        """
        Fix redundant m2m dating association (usually after imports)
        """
        Dating.fix_dating_association(self)


post_save.connect(cached_label_changed, sender=ContextRecord)


class RelationType(GeneralRelationType):
    inverse_relation = models.ForeignKey(
        'RelationType', verbose_name=_(u"Inverse relation"), blank=True,
        null=True)

    class Meta:
        verbose_name = _(u"Relation type")
        verbose_name_plural = _(u"Relation types")
        ordering = ('order', 'label')


class RecordRelations(GeneralRecordRelations, models.Model):
    MAIN_ATTR = 'left_record'
    left_record = models.ForeignKey(ContextRecord,
                                    related_name='right_relations')
    right_record = models.ForeignKey(ContextRecord,
                                     related_name='left_relations')
    relation_type = models.ForeignKey(RelationType)
    TABLE_COLS = [
        "left_record__label", "left_record__unit", "left_record__parcel",
        "relation_type",
        "right_record__label", "right_record__unit", "right_record__parcel",
    ]
    COL_LABELS = {
        "left_record__label": _(u"ID (left)"),
        "left_record__unit": _(u"Context record type (left)"),
        "left_record__parcel": _(u"Parcel (left)"),
        "left_record__description": _(u"Description (left)"),
        "left_record__datings__period": _(u"Periods (left)"),
        "relation_type": _(u"Relation type"),
        "right_record__label": _(u"ID (right)"),
        "right_record__unit": _(u"Context record type (right)"),
        "right_record__parcel": _(u"Parcel (right)"),
        "right_record__description": _(u"Description (right)"),
        "right_record__datings__period": _(u"Periods (right)")
    }

    # search parameters
    EXTRA_REQUEST_KEYS = {
        "left_record__operation": "left_record__operation__pk"
    }

    class Meta:
        verbose_name = _(u"Record relation")
        verbose_name_plural = _(u"Record relations")

post_delete.connect(post_delete_record_relation, sender=RecordRelations)


class RecordRelationView(models.Model):
    """
    CREATE VIEW record_relations AS
        SELECT DISTINCT right_record_id as id,
            right_record_id,
            left_record_id,
            relation_type_id
          FROM archaeological_context_records_recordrelations;

    -- deactivate deletion
    CREATE RULE record_relations_del AS ON DELETE TO record_relations
        DO INSTEAD DELETE FROM record_relations where id=NULL;
    """
    TABLE_COLS = [
        "relation_type",
        "right_record__label", "right_record__unit", "right_record__parcel",
        "right_record__datings__period", "right_record__description"]
    COL_LABELS = {
        "relation_type": _(u"Relation type"),
        "right_record__label": _(u"ID"),
        "right_record__unit": _(u"Context record type"),
        "right_record__parcel": _(u"Parcel"),
        "right_record__description": _(u"Description"),
        "right_record__datings__period": _(u"Periods")
    }

    # search parameters
    EXTRA_REQUEST_KEYS = {
        "left_record_id": "left_record_id"
    }
    left_record = models.ForeignKey(ContextRecord, related_name='+',
                                    on_delete=models.DO_NOTHING)
    right_record = models.ForeignKey(ContextRecord, related_name='+',
                                     on_delete=models.DO_NOTHING)
    relation_type = models.ForeignKey(RelationType, related_name='+',
                                      on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'record_relations'
        unique_together = ('id', 'right_record')

    def __unicode__(self):
        return u"{} \"{}\"".format(self.relation_type, self.right_record)


class ContextRecordSource(Source):
    SHOW_URL = 'show-contextrecordsource'
    MODIFY_URL = 'record_source_modify'
    TABLE_COLS = ['context_record__operation__cached_label', 'context_record']\
        + Source.TABLE_COLS
    COL_LABELS = {'context_record__operation__cached_label': _(u"Operation")}

    # search parameters
    RELATIVE_SESSION_NAMES = [
        ('contextrecord', 'context_record__pk'),
        ('operation', 'context_record__operation__pk'),
        ('file', 'context_record__operation__associated_file__pk')]
    BOOL_FIELDS = ['duplicate']
    EXTRA_REQUEST_KEYS = {
        'title': 'title__icontains',
        'description': 'description__icontains',
        'comment': 'comment__icontains',
        'person': 'authors__person__pk',
        'additional_information': 'additional_information__icontains',
        'context_record__parcel__town': 'context_record__parcel__town__pk',
        'context_record__operation__year': 'context_record__operation__year',
        'context_record__operation__operation_code':
        'context_record__operation__operation_code',
        'context_record__operation__code_patriarche':
        'context_record__operation__code_patriarche',
        'context_record__operation': 'context_record__operation__pk',
        'context_record__datings__period':
            'context_record__datings__period__pk',
        'context_record__unit': 'context_record__unit__pk',
    }

    class Meta:
        verbose_name = _(u"Context record documentation")
        verbose_name_plural = _(u"Context record documentations")
        permissions = (
            ("view_contextrecordsource",
             ugettext(u"Can view all Context record sources")),
            ("view_own_contextrecordsource",
             ugettext(u"Can view own Context record source")),
            ("add_own_contextrecordsource",
             ugettext(u"Can add own Context record source")),
            ("change_own_contextrecordsource",
             ugettext(u"Can change own Context record source")),
            ("delete_own_contextrecordsource",
             ugettext(u"Can delete own Context record source")),
        )
    context_record = models.ForeignKey(
        ContextRecord, verbose_name=_(u"Context record"),
        related_name="source")

    @property
    def owner(self):
        return self.context_record

    @classmethod
    def get_query_owns(cls, user):
        return (
            Q(context_record__operation__scientist=user.ishtaruser.person) |
            Q(context_record__operation__in_charge=user.ishtaruser.person) |
            Q(context_record__operation__collaborators__pk=
              user.ishtaruser.person.pk)) \
               & Q(context_record__operation__end_date__isnull=True)
