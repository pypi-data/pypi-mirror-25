#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models import Max, Q
from django.db.models.signals import post_save, post_delete, pre_delete
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext


from ishtar_common.utils import cached_label_changed
from ishtar_common.models import GeneralType, ImageModel, BaseHistorizedItem, \
    OwnPerms, HistoricalRecords, Person, Organization, Source, \
    ValueGetter, post_save_cache, ShortMenuItem, DashboardFormItem
from archaeological_warehouse.models import Warehouse, Container
from archaeological_finds.models_finds import Find, FindBasket
from archaeological_operations.models import ClosedItem, Operation


class TreatmentType(GeneralType):
    order = models.IntegerField(_(u"Order"), default=10)
    parent = models.ForeignKey("TreatmentType", verbose_name=_(u"Parent type"),
                               blank=True, null=True)
    virtual = models.BooleanField(_(u"Virtual"))
    upstream_is_many = models.BooleanField(
        _(u"Upstream is many"), default=False,
        help_text=_(
            u"Check this if for this treatment from many finds you'll get "
            u"one."))
    downstream_is_many = models.BooleanField(
        _(u"Downstream is many"), default=False,
        help_text=_(
            u"Check this if for this treatment from one find you'll get "
            u"many."))

    class Meta:
        verbose_name = _(u"Treatment type")
        verbose_name_plural = _(u"Treatment types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=TreatmentType)
post_delete.connect(post_save_cache, sender=TreatmentType)


class TreatmentState(GeneralType):
    class Meta:
        verbose_name = _(u"Treatment state type")
        verbose_name_plural = _(u"Treatment state types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=TreatmentState)
post_delete.connect(post_save_cache, sender=TreatmentState)


class Treatment(DashboardFormItem, ValueGetter, BaseHistorizedItem,
                ImageModel, OwnPerms, ShortMenuItem):
    SHOW_URL = 'show-treatment'
    TABLE_COLS = ('year', 'index', 'treatment_types__label',
                  'treatment_state__label',
                  'label', 'person',
                  'start_date', 'downstream_cached_label',
                  'upstream_cached_label')
    REVERSED_BOOL_FIELDS = ['image__isnull']
    EXTRA_REQUEST_KEYS = {
        "label": 'label__icontains',
        "other_reference": 'other_reference__icontains',
        "treatment_types": "treatment_types__pk",
        "downstream_cached_label": "downstream__cached_label",
        "upstream_cached_label": "upstream__cached_label",
        'image': 'image__isnull',
    }
    COL_LABELS = {
        "downstream_cached_label": _(u"Downstream find"),
        "upstream_cached_label": _(u"Upstream find"),
        "treatment_types__label": _(u"Type"),
        "treatment_state__label": _(u"State"),
    }
    IMAGE_PREFIX = 'treatment'
    # extra keys than can be passed to save method
    EXTRA_SAVED_KEYS = ('items', 'user')
    SLUG = 'treatment'
    label = models.CharField(_(u"Label"), blank=True, null=True,
                             max_length=200)
    other_reference = models.CharField(_(u"Other ref."), blank=True, null=True,
                                       max_length=200)
    year = models.IntegerField(_(u"Year"),
                               default=lambda: datetime.datetime.now().year)
    index = models.IntegerField(_(u"Index"), default=1)
    file = models.ForeignKey(
        'TreatmentFile', related_name='treatments', blank=True, null=True,
        verbose_name=_(u"Associated request"))
    treatment_types = models.ManyToManyField(
        TreatmentType, verbose_name=_(u"Treatment type"))
    treatment_state = models.ForeignKey(
        TreatmentState, verbose_name=_(u"State"), blank=True, null=True,
    )
    location = models.ForeignKey(
        Warehouse, verbose_name=_(u"Location"), blank=True, null=True,
        help_text=_(
            u"Location where the treatment is done. Target warehouse for "
            u"a move."))
    person = models.ForeignKey(
        Person, verbose_name=_(u"Responsible"), blank=True, null=True,
        on_delete=models.SET_NULL, related_name='treatments')
    organization = models.ForeignKey(
        Organization, verbose_name=_(u"Organization"), blank=True, null=True,
        on_delete=models.SET_NULL, related_name='treatments')
    external_id = models.CharField(_(u"External ID"), blank=True, null=True,
                                   max_length=200)
    comment = models.TextField(_(u"Comment"), blank=True, null=True)
    description = models.TextField(_(u"Description"), blank=True, null=True)
    goal = models.TextField(_(u"Goal"), blank=True, null=True)
    start_date = models.DateField(_(u"Start date"), blank=True, null=True)
    end_date = models.DateField(_(u"Closing date"), blank=True, null=True)
    container = models.ForeignKey(Container, verbose_name=_(u"Container"),
                                  blank=True, null=True)
    estimated_cost = models.FloatField(_(u"Estimated cost"),
                                       blank=True, null=True)
    quoted_cost = models.FloatField(_(u"Quoted cost"),
                                    blank=True, null=True)
    realized_cost = models.FloatField(_(u"Realized cost"),
                                      blank=True, null=True)
    insurance_cost = models.FloatField(_(u"Insurance cost"),
                                       blank=True, null=True)
    target_is_basket = models.BooleanField(_(u"Target a basket"),
                                           default=False)
    cached_label = models.TextField(_(u"Cached name"), null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _(u"Treatment")
        verbose_name_plural = _(u"Treatments")
        unique_together = ('year', 'index')
        permissions = (
            ("view_treatment", ugettext(u"Can view all Treatments")),
            ("view_own_treatment", ugettext(u"Can view own Treatment")),
            ("add_own_treatment", ugettext(u"Can add own Treatment")),
            ("change_own_treatment", ugettext(u"Can change own Treatment")),
            ("delete_own_treatment", ugettext(u"Can delete own Treatment")),
        )

    def __unicode__(self):
        if self.cached_label:
            return self.cached_label
        self.skip_history_when_saving = True
        self.save()
        return self.cached_label

    @property
    def short_class_name(self):
        return _(u"TREATMENT")

    @classmethod
    def get_query_owns(cls, user):
        return (Q(history_creator=user) |
                Q(person__ishtaruser=user.ishtaruser)) \
            & Q(end_date__isnull=True)

    @classmethod
    def get_owns(cls, user, menu_filtr=None, limit=None, values=None,
                 get_short_menu_class=None):
        replace_query = None
        if menu_filtr:
            if 'treatmentfile' in menu_filtr:
                replace_query = Q(file=menu_filtr['treatmentfile'])
            if 'find' in menu_filtr and \
                    'basket' not in str(menu_filtr['find']):
                q = Q(upstream=menu_filtr['find']) | Q(
                    downstream=menu_filtr['find'])
                if replace_query:
                    replace_query = replace_query | q
                else:
                    replace_query = q
        owns = super(Treatment, cls).get_owns(
            user, replace_query=replace_query, limit=limit,
            values=values, get_short_menu_class=get_short_menu_class)
        return cls._return_get_owns(owns, values, get_short_menu_class)

    def get_query_operations(self):
        return Operation.objects.filter(
            context_record__base_finds__find__downstream_treatment=self)

    def _generate_cached_label(self):
        items = [unicode(getattr(self, k))
                 for k in ['year', 'index', 'other_reference', 'label'] if
                 getattr(self, k)]
        return u'{} | {}'.format(u"-".join(items), self.treatment_types_lbl())

    def treatment_types_lbl(self):
        """
        Treatment types label
        :return: string
        """
        return u" ; ".join([unicode(t) for t in self.treatment_types.all()])

    def get_values(self, prefix=''):
        values = super(Treatment, self).get_values(prefix=prefix)
        values[prefix + "upstream_finds"] = u" ; ".join(
            [unicode(up) for up in self.upstream.all()])
        values[prefix + "downstream_finds"] = u" ; ".join(
            [unicode(down) for down in self.downstream.all()])
        values[prefix + "operations"] = u" ; ".join(
            [unicode(ope) for ope in self.get_query_operations().all()])
        if self.upstream.count():
            find = self.upstream.all()[0]
            if 'associatedfind_' not in prefix:
                values.update(
                    find.get_values(prefix=prefix + 'associatedfind_'))
        return values

    def pre_save(self):
        # is not new
        if self.pk is not None:
            return
        self.index = 1
        q = Treatment.objects.filter(year=self.year)
        if q.count():
            self.index = q.all().aggregate(Max('index'))['index__max'] + 1

    def save(self, *args, **kwargs):
        items, user, extra_args_for_new = [], None, []
        if "items" in kwargs:
            items = kwargs.pop('items')
        if "user" in kwargs:
            user = kwargs.pop('user')
        if "extra_args_for_new" in kwargs:
            extra_args_for_new = kwargs.pop('extra_args_for_new')
        self.pre_save()
        super(Treatment, self).save(*args, **kwargs)
        updated = []
        if hasattr(items, "items"):
            items = items.items.all()
        for item in items:
            new = item.duplicate(user)
            item.downstream_treatment = self
            item.save()
            new.upstream_treatment = self
            for k in extra_args_for_new:
                setattr(new, k, extra_args_for_new[k])
            new.save()
            updated.append(new.pk)
            # update baskets
            for basket in \
                    FindBasket.objects.filter(items__pk=item.pk).all():
                basket.items.remove(item)
                basket.items.add(new)
        # manage containers
        for find in Find.objects.filter(upstream_treatment=self).all():
            if find.container != self.container:
                find.container = self.container
                if find.pk in updated:
                    # don't record twice history
                    find.skip_history_when_saving = True
                find.save()

    @property
    def associated_filename(self):
        return "-".join([str(slugify(getattr(self, attr)))
                         for attr in ('year', 'index', 'label')])

post_save.connect(cached_label_changed, sender=Treatment)


def pre_delete_treatment(sender, **kwargs):
    treatment = kwargs.get('instance')
    for find in Find.objects.filter(upstream_treatment=treatment).all():
        if find.downstream_treatment:
            # a new treatment have be done since the deleted treatment
            # TODO !
            # raise NotImplemented()
            pass
        find.delete()
    for find in Find.objects.filter(downstream_treatment=treatment).all():
        find.downstream_treatment = None
        find.save()

pre_delete.connect(pre_delete_treatment, sender=Treatment)


class AbsFindTreatments(models.Model):
    find = models.ForeignKey(Find, verbose_name=_(u"Find"),
                             related_name='%(class)s_related')
    treatment = models.ForeignKey(Treatment, verbose_name=_(u"Treatment"),
                                  primary_key=True)
    # primary_key is set to prevent django to ask for an id column
    # treatment is not a primary key
    treatment_nb = models.IntegerField(_(u"Order"))
    TABLE_COLS = ["treatment__" + col for col in Treatment.TABLE_COLS] + \
        ['treatment_nb']
    COL_LABELS = {
        'treatment__treatment_type': _(u"Treatment type"),
        'treatment__start_date': _(u"Start date"),
        'treatment__end_date': _(u"End date"),
        'treatment__location': _(u"Location"),
        'treatment__container': _(u"Container"),
        'treatment__person': _(u"Doer"),
        'treatment__upstream': _(u"Related finds"),
        'treatment__downstream': _(u"Related finds"),
    }

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"{} - {} [{}]".format(
            self.find, self.treatment, self.treatment_nb)


class FindUpstreamTreatments(AbsFindTreatments):
    CREATE_SQL = """
    CREATE VIEW find_uptreatments_tree AS
        WITH RECURSIVE rel_tree AS (
          SELECT id AS find_id, upstream_treatment_id, downstream_treatment_id,
              1 AS level,
              ARRAY[]::integer[] AS path_info
            FROM archaeological_finds_find
            WHERE upstream_treatment_id is NULL AND
              downstream_treatment_id is NOT NULL
          UNION ALL
          SELECT c.id AS find_id, c.upstream_treatment_id,
            c.downstream_treatment_id,
            p.level + 1, p.path_info||c.upstream_treatment_id
            FROM archaeological_finds_find c
          JOIN rel_tree p
            ON c.upstream_treatment_id = p.downstream_treatment_id
              AND (p.path_info = ARRAY[]::integer[] OR
                  NOT (c.upstream_treatment_id =
                    ANY(p.path_info[0:array_upper(p.path_info, 1)-1]))
                  )
        )
        SELECT DISTINCT find_id, path_info, level
          FROM rel_tree ORDER BY find_id;

    CREATE VIEW find_uptreatments AS
        SELECT DISTINCT find_id,
            path_info[nb] AS treatment_id, level - nb + 1 AS treatment_nb
          FROM (SELECT *, generate_subscripts(path_info, 1) AS nb
                FROM find_uptreatments_tree) y
         WHERE path_info[nb] is not NULL
        ORDER BY find_id, treatment_id;

    -- deactivate deletion
    CREATE RULE find_uptreatments_del AS ON DELETE TO find_uptreatments
        DO INSTEAD DELETE FROM archaeological_finds_find where id=NULL;
    """
    DELETE_SQL = """
    DROP VIEW find_uptreatments;
    DROP VIEW find_uptreatments_tree;
    """
    TABLE_COLS = ['treatment__treatment_type',
                  'treatment__upstream',
                  'treatment__start_date', 'treatment__end_date',
                  'treatment__location', 'treatment__container',
                  'treatment__person', 'treatment_nb']

    # search parameters
    EXTRA_REQUEST_KEYS = {'find_id': 'find_id'}

    class Meta:
        managed = False
        db_table = 'find_uptreatments'
        unique_together = ('find', 'treatment')
        ordering = ('find', '-treatment_nb')


class FindDownstreamTreatments(AbsFindTreatments):
    CREATE_SQL = """
    CREATE VIEW find_downtreatments_tree AS
        WITH RECURSIVE rel_tree AS (
          SELECT id AS find_id, downstream_treatment_id, upstream_treatment_id,
              1 AS level,
              ARRAY[]::integer[] AS path_info
            FROM archaeological_finds_find
            WHERE downstream_treatment_id is NULL AND
              upstream_treatment_id is NOT NULL
          UNION ALL
          SELECT c.id AS find_id, c.downstream_treatment_id,
            c.upstream_treatment_id,
            p.level + 1, p.path_info||c.downstream_treatment_id
            FROM archaeological_finds_find c
          JOIN rel_tree p
            ON c.downstream_treatment_id = p.upstream_treatment_id
              AND (p.path_info = ARRAY[]::integer[] OR
                  NOT (c.downstream_treatment_id =
                    ANY(p.path_info[0:array_upper(p.path_info, 1)-1]))
                  )
        )
        SELECT DISTINCT find_id, path_info, level
          FROM rel_tree ORDER BY find_id;

    CREATE VIEW find_downtreatments AS
        SELECT DISTINCT find_id,
            path_info[nb] AS treatment_id, level - nb + 1 AS treatment_nb
          FROM (SELECT *, generate_subscripts(path_info, 1) AS nb
                FROM find_downtreatments_tree) y
         WHERE path_info[nb] is not NULL
        ORDER BY find_id, treatment_id;

    -- deactivate deletion
    CREATE RULE find_downtreatments_del AS ON DELETE TO find_downtreatments
        DO INSTEAD DELETE FROM archaeological_finds_find where id=NULL;
    """
    DELETE_SQL = """
    DROP VIEW find_downtreatments;
    DROP VIEW find_downtreatments_tree;
    """
    TABLE_COLS = ['treatment__treatment_type',
                  'treatment__downstream',
                  'treatment__start_date', 'treatment__end_date',
                  'treatment__location', 'treatment__container',
                  'treatment__person', 'treatment_nb']

    # search parameters
    EXTRA_REQUEST_KEYS = {'find_id': 'find_id'}

    class Meta:
        managed = False
        db_table = 'find_downtreatments'
        unique_together = ('find', 'treatment')
        ordering = ('find', '-treatment_nb')


class FindTreatments(AbsFindTreatments):
    CREATE_SQL = """
    CREATE VIEW find_treatments AS
        SELECT find_id, treatment_id, treatment_nb, TRUE as upstream
         FROM find_uptreatments
        UNION
        SELECT find_id, treatment_id, treatment_nb, FALSE as upstream
         FROM find_downtreatments
        ORDER BY find_id, treatment_id, upstream;

    -- deactivate deletion
    CREATE RULE find_treatments_del AS ON DELETE TO find_treatments
        DO INSTEAD DELETE FROM archaeological_finds_find where id=NULL;
    """
    DELETE_SQL = """
    DROP VIEW find_treatments;
    """
    upstream = models.BooleanField(_(u"Is upstream"))

    class Meta:
        managed = False
        db_table = 'find_treatments'
        unique_together = ('find', 'treatment')
        ordering = ('find', 'upstream', '-treatment_nb')


class TreatmentFileType(GeneralType):
    class Meta:
        verbose_name = _(u"Treatment request type")
        verbose_name_plural = _(u"Treatment request types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=TreatmentFileType)
post_delete.connect(post_save_cache, sender=TreatmentFileType)


class TreatmentFile(DashboardFormItem, ClosedItem, BaseHistorizedItem,
                    OwnPerms, ValueGetter, ShortMenuItem):
    SLUG = 'treatmentfile'
    SHOW_URL = 'show-treatmentfile'
    TABLE_COLS = ['type', 'year', 'index', 'internal_reference', 'name']
    SLUG = 'treatmentfile'

    # fields
    year = models.IntegerField(_(u"Year"),
                               default=lambda: datetime.datetime.now().year)
    index = models.IntegerField(_(u"Index"), default=1)
    internal_reference = models.CharField(_(u"Internal reference"), blank=True,
                                          null=True, max_length=200)
    external_id = models.CharField(_(u"External ID"), blank=True, null=True,
                                   max_length=200)
    name = models.TextField(_(u"Name"), blank=True, null=True)
    type = models.ForeignKey(TreatmentFileType,
                             verbose_name=_(u"Treatment request type"))
    in_charge = models.ForeignKey(
        Person, related_name='treatmentfile_responsability',
        verbose_name=_(u"Person in charge"), on_delete=models.SET_NULL,
        blank=True, null=True)
    applicant = models.ForeignKey(
        Person, related_name='treatmentfile_applicant',
        verbose_name=_(u"Applicant"), on_delete=models.SET_NULL,
        blank=True, null=True)
    applicant_organisation = models.ForeignKey(
        Organization, related_name='treatmentfile_applicant',
        verbose_name=_(u"Applicant organisation"), on_delete=models.SET_NULL,
        blank=True, null=True)
    end_date = models.DateField(_(u"Closing date"), null=True, blank=True)
    creation_date = models.DateField(
        _(u"Creation date"), default=datetime.date.today, blank=True,
        null=True)
    reception_date = models.DateField(_(u'Reception date'), blank=True,
                                      null=True)
    comment = models.TextField(_(u"Comment"), null=True, blank=True)
    cached_label = models.TextField(_(u"Cached name"), null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _(u"Treatment request")
        verbose_name_plural = _(u"Treatment requests")
        unique_together = ('year', 'index')
        permissions = (
            ("view_filetreatment",
             ugettext(u"Can view all Treatment requests")),
            ("add_filetreatment",
             ugettext(u"Can add Treatment request")),
            ("change_filetreatment",
             ugettext(u"Can change Treatment request")),
            ("delete_filetreatment",
             ugettext(u"Can delete Treatment request")),
            ("view_own_filetreatment",
             ugettext(u"Can view own Treatment request")),
            ("add_own_filetreatment",
             ugettext(u"Can add own Treatment request")),
            ("change_own_filetreatment",
             ugettext(u"Can change own Treatment request")),
            ("delete_own_filetreatment",
             ugettext(u"Can delete own Treatment request")),
        )
        ordering = ('cached_label',)

    def __unicode__(self):
        return self.cached_label

    @property
    def short_class_name(self):
        return _(u"Treatment request")

    @classmethod
    def get_query_owns(cls, user):
        return (Q(history_creator=user) |
                Q(in_charge__ishtaruser=user.ishtaruser)) \
            & Q(end_date__isnull=True)

    @property
    def associated_filename(self):
        return "-".join([str(slugify(getattr(self, attr)))
                         for attr in ('year', 'index', 'internal_reference',
                                      'name') if getattr(self, attr)])

    @classmethod
    def get_owns(cls, user, menu_filtr=None, limit=None, values=None,
                 get_short_menu_class=None):
        owns = super(TreatmentFile, cls).get_owns(
            user, limit=limit, values=values,
            get_short_menu_class=get_short_menu_class)
        return cls._return_get_owns(owns, values, get_short_menu_class)

    def _generate_cached_label(self):
        items = [unicode(getattr(self, k))
                 for k in ['year', 'index', 'internal_reference', 'name'] if
                 getattr(self, k)]
        return settings.JOINT.join(items)

    def pre_save(self):
        # is not new
        if self.pk is not None:
            return
        self.index = 1
        q = TreatmentFile.objects.filter(year=self.year)
        if q.count():
            self.index = q.all().aggregate(Max('index'))['index__max'] + 1

    def save(self, *args, **kwargs):
        self.pre_save()
        super(TreatmentFile, self).save(*args, **kwargs)

post_save.connect(cached_label_changed, sender=TreatmentFile)


class TreatmentSource(Source):
    treatment = models.ForeignKey(
        Treatment, verbose_name=_(u"Treatment"), related_name="source")
    BOOL_FIELDS = ['duplicate']
    TABLE_COLS = ['treatment__cached_label'] + Source.TABLE_COLS
    COL_LABELS = {'treatment__cached_label': _(u"Treatment")}
    SHOW_URL = 'show-treatmentsource'

    class Meta:
        verbose_name = _(u"Treatment documentation")
        verbose_name_plural = _(u"Treament documentations")
        permissions = (
            ("view_treatmentsource",
             ugettext(u"Can view all Treatment sources")),
            ("view_own_treatmentsource",
             ugettext(u"Can view own Treatment source")),
            ("add_own_treatmentsource",
             ugettext(u"Can add own Treatment source")),
            ("change_own_treatmentsource",
             ugettext(u"Can change own Treatment source")),
            ("delete_own_treatmentsource",
             ugettext(u"Can delete own Treatment source")),
        )

    @property
    def owner(self):
        return self.treatment


class TreatmentFileSource(Source):
    treatment_file = models.ForeignKey(
        TreatmentFile, verbose_name=_(u"Treatment request"),
        related_name="source")
    BOOL_FIELDS = ['duplicate']
    TABLE_COLS = ['treatment_file__cached_label'] + Source.TABLE_COLS
    COL_LABELS = {'treatment_file__cached_label': _(u"Treatment file")}
    SHOW_URL = 'show-treatmentfilesource'

    class Meta:
        verbose_name = _(u"Treatment request documentation")
        verbose_name_plural = _(u"Treatment request documentations")
        permissions = (
            ("view_filetreatmentsource",
             ugettext(u"Can view Treatment request source")),
            ("view_own_filetreatmentsource",
             ugettext(u"Can view own Treatment request source")),
            ("add_own_filetreatmentsource",
             ugettext(u"Can add own Treatment request source")),
            ("change_own_filetreatmentsource",
             ugettext(u"Can change own Treatment request source")),
            ("delete_own_filetreatmentsource",
             ugettext(u"Can delete own Treatment request source")),
        )

    @property
    def owner(self):
        return self.treatment_file
