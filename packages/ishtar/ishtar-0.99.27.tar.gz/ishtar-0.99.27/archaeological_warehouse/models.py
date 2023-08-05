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

import datetime

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models import Q, Count
from django.db.models.signals import post_save, post_delete
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext

from ishtar_common.utils import cached_label_changed

from ishtar_common.models import GeneralType, get_external_id, \
    LightHistorizedItem, OwnPerms, Address, Person, post_save_cache, \
    ImageModel, DashboardFormItem


class WarehouseType(GeneralType):
    class Meta:
        verbose_name = _(u"Warehouse type")
        verbose_name_plural = _(u"Warehouse types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=WarehouseType)
post_delete.connect(post_save_cache, sender=WarehouseType)


class Warehouse(Address, DashboardFormItem, OwnPerms):
    SHOW_URL = 'show-warehouse'
    name = models.CharField(_(u"Name"), max_length=200)
    warehouse_type = models.ForeignKey(WarehouseType,
                                       verbose_name=_(u"Warehouse type"))
    person_in_charge = models.ForeignKey(
        Person, on_delete=models.SET_NULL, related_name='warehouse_in_charge',
        verbose_name=_(u"Person in charge"), null=True, blank=True)
    comment = models.TextField(_(u"Comment"), null=True, blank=True)
    associated_divisions = models.ManyToManyField(
        'WarehouseDivision', verbose_name=_("Divisions"), blank=True,
        through='WarehouseDivisionLink'
    )
    external_id = models.TextField(_(u"External ID"), blank=True, null=True)
    auto_external_id = models.BooleanField(
        _(u"External ID is set automatically"), default=False)

    TABLE_COLS = ['name', 'warehouse_type']

    class Meta:
        verbose_name = _(u"Warehouse")
        verbose_name_plural = _(u"Warehouses")
        permissions = (
            ("view_warehouse", ugettext(u"Can view all Warehouses")),
            ("view_own_warehouse", ugettext(u"Can view own Warehouse")),
            ("add_own_warehouse", ugettext(u"Can add own Warehouse")),
            ("change_own_warehouse", ugettext(u"Can change own Warehouse")),
            ("delete_own_warehouse", ugettext(u"Can delete own Warehouse")),
        )

    def __unicode__(self):
        return u"%s (%s)" % (self.name, unicode(self.warehouse_type))

    @property
    def associated_filename(self):
        return datetime.date.today().strftime('%Y-%m-%d') + '-' + \
               slugify(unicode(self))

    @classmethod
    def get_query_owns(cls, user):
        return Q(person_in_charge__ishtaruser=user.ishtaruser)

    @property
    def number_of_finds(self):
        from archaeological_finds.models import Find
        return Find.objects.filter(container__responsible=self).count()

    @property
    def number_of_finds_hosted(self):
        from archaeological_finds.models import Find
        return Find.objects.filter(container__location=self).count()

    @property
    def number_of_containers(self):
        return Container.objects.filter(location=self).count()

    def _get_divisions(self, current_path, remaining_division, depth=0):
        if not remaining_division:
            return [current_path]
        current_division = remaining_division.pop(0)
        q = ContainerLocalisation.objects.filter(
            division=current_division,
        )
        for div, ref in current_path:
            q = q.filter(
                container__division__division=div,
                container__division__reference=ref
            )
        res = []
        old_ref = None
        for ref in q.values('reference').order_by('reference').all():
            if ref['reference'] == old_ref:
                continue
            old_ref = ref['reference']
            cpath = current_path[:]
            cpath.append((current_division, ref['reference']))
            for r in self._get_divisions(cpath, remaining_division[:],
                                         depth + 1):
                res.append(r)
        return res

    @property
    def available_division_tuples(self):
        """
        :return: ordered list of available paths. Each path is a list of
        tuple with the WarehouseDivisionLink and the reference.
        """
        divisions = list(
            WarehouseDivisionLink.objects.filter(warehouse=self
                                                 ).order_by('order').all())
        return self._get_divisions([], divisions)

    def _number_of_items_by_place(self, model, division_key='division'):
        res = {}
        paths = self.available_division_tuples[:]
        for path in paths:
            q = model.objects
            cpath = []
            for division, ref in path:
                lbl = u"{} {}".format(division.division, ref)
                cpath.append(lbl)
                attrs = {
                    division_key + "__division": division,
                    division_key + "__reference": ref
                }
                q = q.filter(**attrs)
                if tuple(cpath) not in res:
                    res[tuple(cpath)] = q.count()
        res = [(k, res[k]) for k in res]
        final_res, current_res, depth = [], [], 1
        for path, nb in sorted(res, key=lambda x: (len(x[0]), x[0])):
            if depth != len(path):
                final_res.append(current_res[:])
                current_res = []
                depth = len(path)
            current_res.append((u" | ".join(path), nb))
        final_res.append(current_res[:])
        return final_res

    def _number_of_finds_by_place(self):
        from archaeological_finds.models import Find
        return self._number_of_items_by_place(
            Find, division_key='container__division')

    @property
    def number_of_finds_by_place(self, update=False):
        return self._get_or_set_stats('_number_of_finds_by_place', update,
                                      settings.CACHE_SMALLTIMEOUT)

    def _number_of_containers_by_place(self):
        return self._number_of_items_by_place(Container)

    @property
    def number_of_containers_by_place(self, update=False):
        return self._get_or_set_stats('_number_of_containers_by_place', update,
                                      settings.CACHE_SMALLTIMEOUT)

    def save(self, *args, **kwargs):
        super(Warehouse, self).save(*args, **kwargs)
        for container in self.containers.all():
            cached_label_changed(Container, instance=container)

        self.skip_history_when_saving = True
        if not self.external_id or self.auto_external_id:
            external_id = get_external_id('warehouse_external_id', self)
            if external_id != self.external_id:
                updated = True
                self.auto_external_id = True
                self.external_id = external_id

                self._cached_label_checked = False
                self.save()
                return


class Collection(LightHistorizedItem):
    name = models.CharField(_(u"Name"), max_length=200,
                            null=True, blank=True)
    description = models.TextField(_(u"Description"), null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, verbose_name=_(u"Warehouse"),
                                  related_name='collections')

    class Meta:
        verbose_name = _(u"Collection")
        verbose_name_plural = _(u"Collection")
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class WarehouseDivision(GeneralType):
    class Meta:
        verbose_name = _(u"Warehouse division type")
        verbose_name_plural = _(u"Warehouse division types")
post_save.connect(post_save_cache, sender=WarehouseDivision)
post_delete.connect(post_save_cache, sender=WarehouseDivision)


class WarehouseDivisionLink(models.Model):
    RELATIVE_MODELS = {Warehouse: 'warehouse'}
    warehouse = models.ForeignKey(Warehouse)
    division = models.ForeignKey(WarehouseDivision)
    order = models.IntegerField(_("Order"), default=10)

    class Meta:
        ordering = ('warehouse', 'order')
        unique_together = ('warehouse', 'division')

    def __unicode__(self):
        return u"{} - {}".format(self.warehouse, self.division)


class ContainerType(GeneralType):
    length = models.IntegerField(_(u"Length (mm)"), blank=True, null=True)
    width = models.IntegerField(_(u"Width (mm)"), blank=True, null=True)
    height = models.IntegerField(_(u"Height (mm)"), blank=True, null=True)
    volume = models.FloatField(_(u"Volume (l)"), blank=True, null=True)
    reference = models.CharField(_(u"Ref."), max_length=30)

    class Meta:
        verbose_name = _(u"Container type")
        verbose_name_plural = _(u"Container types")
        ordering = ('label',)
post_save.connect(post_save_cache, sender=ContainerType)
post_delete.connect(post_save_cache, sender=ContainerType)


class Container(LightHistorizedItem, ImageModel):
    TABLE_COLS = ['reference', 'container_type__label', 'cached_location',
                  'divisions_lbl']
    IMAGE_PREFIX = 'containers/'

    # search parameters
    EXTRA_REQUEST_KEYS = {
        'location': 'location__pk',
        'container_type': 'container_type__pk',
        'reference': 'reference__icontains',
    }
    SHOW_URL = 'show-container'
    COL_LABELS = {
        'cached_location': _(u"Location - index"),
        'divisions_lbl': _(u"Precise localisation"),
        'container_type__label': _(u"Type")
    }
    CACHED_LABELS = ['cached_label', 'cached_location']

    # fields
    location = models.ForeignKey(
        Warehouse, verbose_name=_(u"Location (warehouse)"),
        related_name='containers')
    responsible = models.ForeignKey(
        Warehouse, verbose_name=_(u"Responsible warehouse"),
        related_name='owned_containers')
    container_type = models.ForeignKey(ContainerType,
                                       verbose_name=_("Container type"))
    reference = models.CharField(_(u"Container ref."), max_length=40)
    comment = models.TextField(_(u"Comment"), null=True, blank=True)
    cached_label = models.CharField(_(u"Localisation"), max_length=500,
                                    null=True, blank=True)
    cached_location = models.CharField(_(u"Cached location"), max_length=500,
                                       null=True, blank=True)
    index = models.IntegerField(u"ID", default=0)
    external_id = models.TextField(_(u"External ID"), blank=True, null=True)
    auto_external_id = models.BooleanField(
        _(u"External ID is set automatically"), default=False)

    class Meta:
        verbose_name = _(u"Container")
        verbose_name_plural = _(u"Containers")
        ordering = ('cached_label',)
        unique_together = ('index', 'location')

    def __unicode__(self):
        lbl = u"{} ({})".format(self.reference, self.container_type)
        return lbl

    def _generate_cached_label(self):
        items = [self.reference, self.precise_location]
        cached_label = u" | ".join(items)
        return cached_label

    def _generate_cached_location(self):
        items = [self.location.name, unicode(self.index)]
        cached_label = u" - ".join(items)
        return cached_label

    @classmethod
    def get_query_owns(cls, user):
        return Q(history_creator=user) | \
            Q(location__person_in_charge__ishtaruser=user.ishtaruser) | \
            Q(responsible__person_in_charge__ishtaruser=user.ishtaruser)

    @property
    def associated_filename(self):
        filename = datetime.date.today().strftime('%Y-%m-%d')
        filename += u'-' + self.reference
        filename += u"-" + self.location.name
        filename += u"-" + unicode(self.index)
        filename += u"-" + self.divisions_lbl
        return slugify(filename)

    @property
    def precise_location(self):
        return self.location.name + u" - " + self.divisions_lbl

    @property
    def divisions_lbl(self):
        locas = [
            u"{} {}".format(loca.division.division, loca.reference)
            for loca in ContainerLocalisation.objects.filter(
                container=self)
            ]
        return u" | ".join(locas)

    def pre_save(self):
        if not self.index:
            q = Container.objects.filter(responsible=self.responsible).order_by(
                '-index')
            if q.count():
                self.index = q.all()[0].index + 1
            else:
                self.index = 1

    def save(self, *args, **kwargs):
        super(Container, self).save(*args, **kwargs)

        updated = False
        if not self.index:
            self.skip_history_when_saving = True
            q = Container.objects.filter(responsible=self.responsible).order_by(
                '-index')
            if q.count():
                self.index = q.all()[0].index + 1
            else:
                self.index = 1
            updated = True

        self.skip_history_when_saving = True
        if not self.external_id or self.auto_external_id:
            external_id = get_external_id('container_external_id', self)
            if external_id != self.external_id:
                updated = True
                self.auto_external_id = True
                self.external_id = external_id

        if updated:
            self._cached_label_checked = False
            self.save()
            return

        # remove old location in warehouse
        q = ContainerLocalisation.objects.filter(container=self).exclude(
            division__warehouse=self.location)
        for loca in q.all():
            loca.delete()

post_save.connect(cached_label_changed, sender=Container)


class ContainerLocalisation(models.Model):
    container = models.ForeignKey(Container, verbose_name=_(u"Container"),
                                  related_name='division')
    division = models.ForeignKey(WarehouseDivisionLink,
                                 verbose_name=_(u"Division"))
    reference = models.CharField(_(u"Reference"), max_length=200, default='')

    class Meta:
        verbose_name = _(u"Container localisation")
        verbose_name_plural = _(u"Container localisations")
        unique_together = ('container', 'division')
        ordering = ('container', 'division__order')

    def __unicode__(self):
        lbl = u" - ".join((unicode(self.container),
                           unicode(self.division), self.reference))
        return lbl

    def save(self, *args, **kwargs):
        super(ContainerLocalisation, self).save(*args, **kwargs)
        cached_label_changed(Container, instance=self.container)
