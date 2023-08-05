#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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

from functools import wraps
import hashlib
import random

from django import forms
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext
from django.template.defaultfilters import slugify


def get_cache(cls, extra_args=[]):
    cache_key = u"{}-{}-{}".format(
        settings.PROJECT_SLUG, cls._meta.app_label, cls.__name__)
    for arg in extra_args:
        if not arg:
            cache_key += '-0'
        else:
            if type(arg) == dict:
                cache_key += '-' + "_".join([unicode(arg[k]) for k in arg])
            elif type(arg) in (list, tuple):
                cache_key += '-' + "_".join([unicode(v) for v in arg])
            else:
                cache_key += '-' + unicode(arg)
    cache_key = slugify(cache_key)
    if not cache_key.endswith('_current_keys') \
            and hasattr(cls, '_add_cache_key_to_refresh'):
        cls._add_cache_key_to_refresh(extra_args)
    if len(cache_key) >= 250:
        m = hashlib.md5()
        m.update(cache_key)
        cache_key = m.hexdigest()
    return cache_key, cache.get(cache_key)


def force_cached_label_changed(sender, **kwargs):
    if not kwargs.get('instance'):
        return
    kwargs['instance']._cached_label_checked = False
    cached_label_changed(sender, **kwargs)


def cached_label_changed(sender, **kwargs):
    if not kwargs.get('instance'):
        return
    instance = kwargs.get('instance')

    if hasattr(instance, 'test_obj'):
        instance.test_obj.reached(sender, **kwargs)

    if hasattr(instance, '_cached_label_checked') \
            and instance._cached_label_checked:
        return
    instance._cached_label_checked = True
    cached_labels = ['cached_label']
    if hasattr(sender, 'CACHED_LABELS'):
        cached_labels = sender.CACHED_LABELS
    changed = False
    for cached_label in cached_labels:
        lbl = getattr(instance, '_generate_' + cached_label)()
        if lbl != getattr(instance, cached_label):
            setattr(instance, cached_label, lbl)
            changed = True
    if changed:
        if hasattr(instance, '_cascade_change') and instance._cascade_change:
            instance.skip_history_when_saving = True
        instance.save()
    updated = False
    if hasattr(instance, '_cached_labels_bulk_update'):
        updated = instance._cached_labels_bulk_update()
    if not updated and hasattr(instance, '_get_associated_cached_labels'):
        for item in instance._get_associated_cached_labels():
            item._cascade_change = True
            if hasattr(instance, 'test_obj'):
                item.test_obj = instance.test_obj
            cached_label_changed(item.__class__, instance=item)

SHORTIFY_STR = ugettext(" (...)")


def shortify(lbl, number=20):
    if not lbl:
        lbl = ''
    if len(lbl) <= number:
        return lbl
    return lbl[:number - len(SHORTIFY_STR)] + SHORTIFY_STR


def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            return
        signal_handler(*args, **kwargs)
    return wrapper


def _get_image_link(item):
    # manage missing images
    if not item.thumbnail or not item.thumbnail.url:
        return ""
    return mark_safe(u"""
    <div class="welcome-image">
        <img src="{}"/><br/>
        <em>{} - {}</em>
        <a href="#" onclick="load_window(\'{}\')">
          <i class="fa fa-info-circle" aria-hidden="true"></i>
        </a>
        <a href="." title="{}">
            <i class="fa fa-random" aria-hidden="true"></i>
        </a><br/>
    </div>""".format(
        item.thumbnail.url,
        unicode(item.__class__._meta.verbose_name),
        unicode(item),
        reverse(item.SHOW_URL, args=[item.pk, '']),
        unicode(_(u"Load another random image?"))))


def get_random_item_image_link(request):
    from archaeological_operations.models import Operation
    from archaeological_context_records.models import ContextRecord
    from archaeological_finds.models import Find

    ope_image_nb, cr_image_nb, find_image_nb = 0, 0, 0
    q_ope = Operation.objects.filter(
        thumbnail__isnull=False).exclude(thumbnail='')
    q_cr = ContextRecord.objects.filter(
        thumbnail__isnull=False).exclude(thumbnail='')
    q_find = Find.objects.filter(
        thumbnail__isnull=False).exclude(thumbnail='')
    if request.user.has_perm('archaeological_operations.view_operation',
                             Operation):
        ope_image_nb = q_ope.count()
    if request.user.has_perm(
            'archaeological_context_records.view_contextrecord',
            ContextRecord):
        cr_image_nb = q_cr.count()
    if request.user.has_perm('archaeological_finds.view_find',
                             Find):
        find_image_nb = q_find.count()

    image_total = ope_image_nb + cr_image_nb + find_image_nb
    if not image_total:
        return ''

    image_nb = random.randint(0, image_total - 1)
    if image_nb >= 0 and image_nb < ope_image_nb:
        return _get_image_link(q_ope.all()[image_nb])
    if image_nb >= ope_image_nb and image_nb < (cr_image_nb + ope_image_nb):
        return _get_image_link(q_cr.all()[image_nb - ope_image_nb])
    if image_nb >= (cr_image_nb + ope_image_nb):
        return _get_image_link(q_find.all()[
            image_nb - ope_image_nb - cr_image_nb])
    # should never happen except in case of deletion during the excution
    return ''


def convert_coordinates_to_point(x, y, z=None, srid=4326):
    if z:
        geom = GEOSGeometry('POINT({} {} {})'.format(x, y, z), srid=srid)
    else:
        geom = GEOSGeometry('POINT({} {})'.format(x, y), srid=srid)
    if not geom.valid:
        raise forms.ValidationError(geom.valid_reason)
    return geom


def post_save_point(sender, **kwargs):
    """
    Convert raw x, y, z point to real geo field
    """
    if not kwargs.get('instance'):
        return
    instance = kwargs.get('instance')
    point = None
    point_2d = None
    if instance.x and instance.y and \
            instance.spatial_reference_system and \
            instance.spatial_reference_system.auth_name == 'EPSG' and \
            instance.spatial_reference_system.srid != 0:
        point_2d = convert_coordinates_to_point(
            instance.x, instance.y, srid=instance.spatial_reference_system.srid)
        if instance.z:
            point = convert_coordinates_to_point(
                instance.x, instance.y, instance.z,
                srid=instance.spatial_reference_system.srid)
    if point_2d != instance.point_2d or point != instance.point:
        instance.point = point
        instance.point_2d = point_2d
        instance.skip_history_when_saving = True
        instance.save()
    return
