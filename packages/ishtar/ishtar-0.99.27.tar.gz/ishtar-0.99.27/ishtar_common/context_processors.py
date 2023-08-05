#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

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
from django.contrib.sites.models import Site

from ishtar_common.version import __version__
from ishtar_common.models import get_current_profile

from menus import Menu


def get_base_context(request):
    dct = {'URL_PATH': settings.URL_PATH}
    try:
        dct["APP_NAME"] = Site.objects.get_current().name
    except Site.DoesNotExist:
        dct["APP_NAME"] = settings.APP_NAME
    dct["COUNTRY"] = settings.COUNTRY
    """
    if 'MENU' not in request.session or \
       request.session['MENU'].user != request.user:
        menu = Menu(request.user)
        menu.init()
        request.session['MENU'] = menu
    """  # temporary disabled
    current_action = None
    if 'CURRENT_ACTION' in request.session:
        dct['CURRENT_ACTION'] = request.session['CURRENT_ACTION']
        current_action = dct['CURRENT_ACTION']
    dct['CURRENT_PATH'] = request.path
    menu = Menu(request.user, current_action=current_action,
                session=request.session)
    menu.init()
    if menu.selected_idx is not None:
        dct['current_theme'] = "theme-%d" % (menu.selected_idx + 1)
    request.session['MENU'] = menu
    dct['MENU'] = request.session['MENU']
    dct['JQUERY_URL'] = settings.JQUERY_URL
    dct['JQUERY_UI_URL'] = settings.JQUERY_UI_URL
    dct['COUNTRY'] = settings.COUNTRY
    dct['VERSION'] = __version__
    if settings.EXTRA_VERSION:
        dct['VERSION'] += "-" + unicode(settings.EXTRA_VERSION)
    profile = get_current_profile()
    if profile:
        dct['raw_css'] = profile.get_raw_css()
    return dct
