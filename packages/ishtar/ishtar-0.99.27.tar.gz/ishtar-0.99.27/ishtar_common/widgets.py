#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>
# Copyright (C) 2007  skam <massimo dot scamarcia at gmail.com>
#                          (http://djangosnippets.org/snippets/233/)

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

import logging

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import fields
from django.forms import ClearableFileInput
from django.forms.widgets import flatatt, \
    CheckboxSelectMultiple as CheckboxSelectMultipleBase
from django.template import Context, loader
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode
from django.utils.functional import lazy
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.simplejson import JSONEncoder
from django.utils.translation import ugettext_lazy as _

from ishtar_common import models

logger = logging.getLogger(__name__)

reverse_lazy = lazy(reverse, unicode)


class Select2Multiple(forms.SelectMultiple):
    def __init__(self, attrs=None, choices=(), remote=None, model=None,
                 available=None):
        super(Select2Multiple, self).__init__(attrs, choices)
        self.remote = remote
        self.available = available
        self.model = model

    @property
    def media(self):
        media = super(Select2Multiple, self).media
        css = {
            'all': ('select2/css/select2.css',)
        }
        js = ['select2/js/select2.full.min.js']
        for lang_code, lang in settings.LANGUAGES:
            js.append('select2/js/i18n/{}.js'.format(lang_code))
        media.add_css(css)
        media.add_js(js)
        return media

    def get_q(self):
        q = self.model.objects
        if self.available:
            q = q.filter(available=True)
        return q

    def get_choices(self):
        for i in self.get_q().all():
            yield (i.pk, unicode(i))

    def render(self, name, value, attrs=None, choices=()):
        self.remote = unicode(self.remote)
        if self.remote in ('None', 'false'):
            # test on lazy object is buggy... so we have this ugly test
            self.remote = None
        if not choices and not self.remote and self.model:
            choices = self.get_choices()
        new_attrs = self.attrs.copy()
        new_attrs.update(attrs)
        attrs = new_attrs
        klass = attrs and attrs.get('class') or ''
        klass += ' ' if klass else '' + 'js-select2'
        if not attrs:
            attrs = {}
        attrs['class'] = klass
        if 'style' not in attrs:
            if attrs.get('full-width', None):
                attrs['style'] = "width: 100%"
            else:
                attrs['style'] = "width: 370px"

        options = ""
        if self.remote:
            options = """{
            ajax: {
                url: '%s',
                delay: 250,
                dataType: 'json',
                minimumInputLength: 2,
                processResults: function (data) {
                 if(!data) return {results: []};
                 var result = $.map(data, function (item) {
                        return {
                            text: item['value'],
                            id: item['id']
                        }
                      });
                 return {
                    results: result
                  }
                }
              }
            }""" % self.remote
            if value:
                choices = []
                if type(value) not in (list, tuple):
                    value = value.split(',')
                for v in value:
                    try:
                        choices.append((v, self.model.objects.get(pk=v)))
                    except (self.model.DoesNotExist, ValueError):
                        # an old reference? it should not happen
                        pass
        if attrs.get('full-width', None):
            if options:
                options = options[:-1] + ", "
            else:
                options = "{"
            options += "     containerCssClass: 'full-width'}"
        html = super(Select2Multiple, self).render(name, value, attrs,
                                                   choices)
        html += """<script type="text/javascript">
        $(document).ready(function() {{
            $("#id_{}").select2({});
        }});</script>
        """.format(name, options)
        return mark_safe(html)


class CheckboxSelectMultiple(CheckboxSelectMultipleBase):
    """
    Fix initialization bug.
    Should be corrected on recent Django version.
    TODO: test and remove (test case: treatment type not keep on modif)
    """
    def render(self, name, value, attrs=None, choices=()):
        if type(value) in (str, unicode):
            value = value.split(',')
        if type(value) not in (list, tuple):
            value = [value]
        return super(CheckboxSelectMultiple, self).render(name, value, attrs,
                                                          choices)


class Select2MultipleField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        remote = None
        if 'remote' in kwargs:
            remote = kwargs.pop('remote')
        self.model, self.remote = None, None
        if 'model' in kwargs:
            self.model = kwargs.pop('model')
            if remote:
                self.remote = reverse_lazy(
                    'autocomplete-' + self.model.__name__.lower())
        self.available = False
        if 'available' in kwargs:
            self.available = kwargs.pop('available')
        kwargs['widget'] = Select2Multiple(model=self.model,
                                           available=self.available,
                                           remote=self.remote)
        super(Select2MultipleField, self).__init__(*args, **kwargs)

    def get_q(self):
        q = self.model.objects
        if self.available:
            q = q.filter(available=True)
        return q

    def valid_value(self, value):
        if not self.model:
            return super(Select2MultipleField, self).valid_value(value)
        return bool(self.get_q().filter(pk=value).count())


class DeleteWidget(forms.CheckboxInput):
    def render(self, name, value, attrs=None):
        final_attrs = flatatt(self.build_attrs(attrs, name=name,
                                               value='1'))
        output = ['<tr class="delete"><td colspan="2">']
        output.append(u"<button%s>%s</button>" % (final_attrs, _("Delete")))
        output.append('</td></tr>')
        return mark_safe('\n'.join(output))


class ImageFileInput(ClearableFileInput):
    template_with_initial = u'<span class="prettyPhoto">%(initial)s</span>'\
        u' %(clear_template)s<br />%(input_text)s: %(input)s'


class SquareMeterWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if not value:
            value = u""
        final_attrs = flatatt(self.build_attrs(attrs, name=name, value=value))
        dct = {'final_attrs': final_attrs,
               'unit': settings.SURFACE_UNIT_LABEL,
               'id': attrs['id'],
               "safe_id": attrs['id'].replace('-', '_')}
        t = loader.get_template('blocks/SquareMeterWidget.html')
        rendered = t.render(Context(dct))
        return mark_safe(rendered)

AreaWidget = forms.TextInput

if settings.SURFACE_UNIT == 'square-metre':
    AreaWidget = SquareMeterWidget


class JQueryDate(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super(JQueryDate, self).__init__(*args, **kwargs)
        if 'class' not in self.attrs:
            self.attrs['class'] = ''
        self.attrs['class'] = 'date-pickup'

    def render(self, name, value=None, attrs=None):
        if value:
            value = unicode(value)
        # very specific...
        if settings.COUNTRY == 'fr' and value and '/' in value:
            values = value.split('/')
            if len(values) == 3:
                value = "%s-%s-%s" % (values[2], values[1], values[0])
        if not attrs:
            attrs = {}
        attrs['autocomplete'] = 'off'
        rendered = super(JQueryDate, self).render(name, value, attrs)
        # use window.onload to be sure that datepicker don't interfere
        # with autocomplete fields
        var_name = name.replace('-', '_')
        rendered += """
<script type="text/javascript"><!--//
    function load_jquerydate_%(var_name)s(){
        $(".date-pickup").datepicker($.datepicker.regional["%(country)s"]);
        var val = $("#id_%(name)s").val();
        if(val){
            var dt = $.datepicker.parseDate('yy-mm-dd', val);
            val = $.datepicker.formatDate(
                    $.datepicker.regional["%(country)s"]['dateFormat'],
                    dt);
            $("#id_%(name)s").val(val);
        }
    }
    $(window).load(load_jquerydate_%(var_name)s);
//--></script>
""" % {"name": name, "var_name": var_name, "country": settings.COUNTRY}
        return rendered


class JQueryAutoComplete(forms.TextInput):
    def __init__(self, source, associated_model=None, options={}, attrs={},
                 new=False, url_new='', multiple=False, limit={},
                 dynamic_limit=[]):
        """
        Source can be a list containing the autocomplete values or a
        string containing the url used for the request.
        """
        self.options = None
        self.attrs = {}
        self.source = source
        self.associated_model = associated_model
        if len(options) > 0:
            self.options = JSONEncoder().encode(options)
        self.attrs.update(attrs)
        self.new = new
        self.url_new = url_new
        self.multiple = multiple
        self.limit = limit
        self.dynamic_limit = dynamic_limit

    def value_from_datadict(self, data, files, name):
        if self.multiple:
            return data.getlist(name, None)
        else:
            return data.get(name, None)

    def render_js(self, field_id):
        if isinstance(self.source, list):
            source = JSONEncoder().encode(self.source)
        elif isinstance(self.source, str) or isinstance(self.source, unicode):
            source = "'%s'" % escape(self.source)
        else:
            try:
                source = "'" + unicode(self.source) + "'"
            except:
                raise ValueError('source type is not valid')
        dynamic_limit = [
            'id_' + lim.replace('_', '') + '-' +
            '-'.join(field_id.split('-')[1:-1]) + '-' + lim
            for lim in self.dynamic_limit
        ]
        dct = {'source': mark_safe(source),
               'field_id': field_id,
               'dynamic_limit': dynamic_limit}
        if self.options:
            dct['options'] = mark_safe('%s' % self.options)

        js = ""
        tpl = 'blocks/JQueryAutocomplete.js'
        if self.multiple:
            tpl = 'blocks/JQueryAutocompleteMultiple.js'
        t = loader.get_template(tpl)
        js = t.render(Context(dct))
        return js

    def render(self, name, value=None, attrs=None):
        attrs_hidden = self.build_attrs(attrs, name=name)
        attrs_select = self.build_attrs(attrs)
        attrs_select['placeholder'] = _(u"Search...")
        if value:
            hiddens = []
            selects = []
            values = value
            if type(value) not in (list, tuple):
                values = unicode(escape(smart_unicode(value)))
                values = values.replace('[', '').replace(']', '')
                values = values.split(',')
            else:
                values = []
                for v in value:
                    values += v.split(',')
            for v in values:
                if not v:
                    continue
                hiddens.append(v)
                selects.append(v)
                if self.associated_model:
                    try:
                        selects[-1] = unicode(
                            self.associated_model.objects.get(pk=v))
                    except (self.associated_model.DoesNotExist, ValueError):
                        selects.pop()
                        hiddens.pop()
            if self.multiple:
                attrs_hidden['value'] = ", ".join(hiddens)
                if selects:
                    selects.append("")
                attrs_select['value'] = ", ".join(selects)
            else:
                if hiddens and selects:
                    attrs_hidden['value'] = hiddens[0]
                    attrs_select['value'] = selects[0]
        if 'id' not in self.attrs:
            attrs_hidden['id'] = 'id_%s' % name
            attrs_select['id'] = 'id_select_%s' % name
        if 'class' not in attrs_select:
            attrs_select['class'] = 'autocomplete'
        new = ''
        if self.new:
            model_name = self.associated_model._meta.object_name.lower()
            limits = []
            for k in self.limit:
                limits.append(k + "__" + "-".join(
                              [unicode(v) for v in self.limit[k]]))
            args = [attrs_select['id']]
            if limits:
                args.append(';'.join(limits))
            url_new = 'new-' + model_name
            if self.url_new:
                url_new = self.url_new
            url_new = reverse(url_new, args=args)
            new = u'  <a href="#" class="add-button" '\
                  u'onclick="open_window(\'%s\');">+</a>' % url_new
        html = u'''<input%(attrs_select)s/>%(new)s\
<input type="hidden"%(attrs_hidden)s/>\
        <script type="text/javascript"><!--//
        %(js)s//--></script>
        ''' % {
            'attrs_select': flatatt(attrs_select),
            'attrs_hidden': flatatt(attrs_hidden),
            'js': self.render_js(name),
            'new': new
        }
        return html


class JQueryTown(forms.TextInput):
    """
    Town fields whith state and department pre-selections
    """

    def __init__(self, source, options={},
                 attrs={}, new=False, limit={}):
        self.options = None
        self.attrs = {}
        self.source = source
        if len(options) > 0:
            self.options = JSONEncoder().encode(options)
        self.attrs.update(attrs)
        self.new = new
        self.limit = limit

    @classmethod
    def encode_source(cls, source):
        if isinstance(source, list):
            encoded_src = JSONEncoder().encode(source)
        elif isinstance(source, str) \
                or isinstance(source, unicode):
            src = escape(source)
            if not src.endswith('/'):
                src += "/"
            encoded_src = "'%s'" % src
        else:
            try:
                src = unicode(source)
                if not src.endswith('/'):
                    src += "/"
                encoded_src = "'%s'" % src
            except:
                raise ValueError('source type is not valid')
        return encoded_src

    def render(self, name, value=None, attrs=None):
        attrs_hidden = self.build_attrs(attrs, name=name)
        attrs_select = self.build_attrs(attrs)
        attrs_select['placeholder'] = _(u"Search...")
        selected = ''
        selected_state = ''
        selected_department = ''
        if value:
            hiddens = []
            selects = []
            if type(value) not in (list, tuple):
                values = unicode(escape(smart_unicode(value)))
                values = values.replace('[', '').replace(']', '')
                values = values.split(',')
            else:
                values = []
                for v in value:
                    values += v.split(',')
            for v in values:
                if not v:
                    continue
                hiddens.append(v)
                selects.append(v)
                try:
                    item = models.Town.objects.get(pk=v)
                    selects[-1] = unicode(item)
                    if item.departement:
                        selected_department = item.departement.number
                        if item.departement.state:
                            selected_state = item.departement.state.number
                    selected = item.pk
                except (models.Town.DoesNotExist, ValueError):
                    selects.pop()
                    hiddens.pop()
            if hiddens and selects:
                attrs_hidden['value'] = hiddens[0]
                attrs_select['value'] = selects[0]
        if 'id' not in self.attrs:
            attrs_hidden['id'] = 'id_%s' % name
            attrs_select['id'] = 'id_select_%s' % name
        if 'class' not in attrs_select:
            attrs_select['class'] = 'autocomplete'

        source = self.encode_source(self.source)
        dct = {'source': mark_safe(source),
               'selected': selected,
               'safe_field_id': slugify(name).replace('-', '_'),
               'field_id': name}
        if self.options:
            dct['options'] = mark_safe('%s' % self.options)

        dct.update({'attrs_select': mark_safe(flatatt(attrs_select)),
                    'attrs_hidden': mark_safe(flatatt(attrs_hidden)),
                    'name': name,
                    'states': models.State.objects.all().order_by('label'),
                    'selected_department': selected_department,
                    'selected_state': selected_state}
                   )
        html = loader.get_template('blocks/JQueryAdvancedTown.html')\
                     .render(Context(dct))
        return html


class JQueryPersonOrganization(forms.TextInput):
    """
    Complex widget which manage:
     * link between person and organization
     * display addresses of the person and of the organization
     * create new person and new organization
    """

    def __init__(self, source, edit_source, model, options={},
                 attrs={}, new=False, limit={},
                 html_template='blocks/PersonOrganization.html',
                 js_template='blocks/JQueryPersonOrganization.js'):
        self.options = None
        self.attrs = {}
        self.model = model
        self.source = source
        self.edit_source = edit_source
        if len(options) > 0:
            self.options = JSONEncoder().encode(options)
        self.attrs.update(attrs)
        self.new = new
        self.limit = limit
        self.js_template = js_template
        self.html_template = html_template

    @classmethod
    def encode_source(cls, source):
        if isinstance(source, list):
            encoded_src = JSONEncoder().encode(source)
        elif isinstance(source, str) \
                or isinstance(source, unicode):
            encoded_src = "'%s'" % escape(source)
        else:
            try:
                encoded_src = "'" + unicode(source) + "'"
            except:
                raise ValueError('source type is not valid')
        return encoded_src

    def render_js(self, field_id, selected=''):
        source = self.encode_source(self.source)
        edit_source = self.encode_source(self.edit_source)
        dct = {'source': mark_safe(source),
               'edit_source': mark_safe(edit_source),
               'selected': selected,
               'safe_field_id': slugify(field_id).replace('-', '_'),
               'field_id': field_id}
        if self.options:
            dct['options'] = mark_safe('%s' % self.options)
        js = loader.get_template(self.js_template).render(Context(dct))
        return js

    def render(self, name, value=None, attrs=None):
        attrs_hidden = self.build_attrs(attrs, name=name)
        attrs_select = self.build_attrs(attrs)
        attrs_select['placeholder'] = _(u"Search...")
        selected = ''
        if value:
            hiddens = []
            selects = []
            if type(value) not in (list, tuple):
                values = unicode(escape(smart_unicode(value)))
                values = values.replace('[', '').replace(']', '')
                values = values.split(',')
            else:
                values = []
                for v in value:
                    values += v.split(',')
            for v in values:
                if not v:
                    continue
                hiddens.append(v)
                selects.append(v)
                if self.model:
                    try:
                        item = self.model.objects.get(pk=v)
                        selects[-1] = unicode(item)
                        selected = item.pk
                    except (self.model.DoesNotExist, ValueError):
                        selects.pop()
                        hiddens.pop()
            if hiddens and selects:
                attrs_hidden['value'] = hiddens[0]
                attrs_select['value'] = selects[0]
        if 'id' not in self.attrs:
            attrs_hidden['id'] = 'id_%s' % name
            attrs_select['id'] = 'id_select_%s' % name
        if 'class' not in attrs_select:
            attrs_select['class'] = 'autocomplete'
        new = ''
        dct = {'attrs_select': mark_safe(flatatt(attrs_select)),
               'attrs_hidden': mark_safe(flatatt(attrs_hidden)),
               'name': name,
               'js': self.render_js(name, selected),
               'new': mark_safe(new)}
        html = loader.get_template(self.html_template).render(Context(dct))
        return html


class JQueryJqGrid(forms.RadioSelect):
    COL_TPL = "{name:'%(idx)s', index:'%(idx)s', sortable:true}"

    # class Media:
    #    js = ['%s/js/i18n/grid.locale-%s.js' % (settings.STATIC_URL,
    #                                            settings.COUNTRY),
    #          '%s/js/jquery.jqGrid.min.js' % settings.STATIC_URL]
    #    css = {'all': ['%s/media/ui.jqgrid.css' % settings.STATIC_URL]}

    def __init__(self, source, form, associated_model, attrs={},
                 table_cols='TABLE_COLS', multiple=False, multiple_cols=[2],
                 new=False, new_message="", source_full=None,
                 multiple_select=False, sortname="__default__",
                 col_prefix=''):
        """
        JQueryJqGrid widget init.

        :param source: url to get the item from -- get_item
        :param form:
        :param associated_model: model of the listed items
        :param attrs:
        :param table_cols:
        :param multiple:
        :param multiple_cols:
        :param new:
        :param new_message:
        :param source_full: url to get full listing
        :param multiple_select:
        :param sortname: column name (model attribute) to use to sort
        :param col_prefix: prefix to remove to col_names
        """
        super(JQueryJqGrid, self).__init__(attrs=attrs)
        self.source = source
        self.form = form
        if not attrs:
            attrs = {}
        self.attrs = attrs.copy()
        self.associated_model = associated_model
        self.table_cols = table_cols
        self.multiple = multiple
        self.multiple_select = multiple_select
        self.multiple_cols = multiple_cols
        self.new, self.new_message = new, new_message
        self.source_full = source_full
        self.sortname = sortname
        self.col_prefix = col_prefix
        if self.col_prefix and not self.col_prefix.endswith('__'):
            self.col_prefix += "__"

    def get_cols(self, python=False):
        jq_col_names, extra_cols = [], []
        col_labels = {}
        if hasattr(self.associated_model, 'COL_LABELS'):
            col_labels = self.associated_model.COL_LABELS
        for col_names in getattr(self.associated_model, self.table_cols):
            field_verbose_names = []
            field_verbose_name, field_name = "", ""
            if type(col_names) not in (list, tuple):
                col_names = [col_names]
            for col_name in col_names:
                field = self.associated_model
                keys = col_name.split('__')
                if '.' in col_name:
                    keys = col_name.split('.')
                for key in keys:
                    if hasattr(field, 'rel') and field.rel:
                        field = field.rel.to
                    try:
                        field = field._meta.get_field(key)
                        field_verbose_name = field.verbose_name
                    except (fields.FieldDoesNotExist, AttributeError):
                        if hasattr(field, key + '_lbl'):
                            field_verbose_name = getattr(field, key + '_lbl')
                        else:
                            continue
                if field_name:
                    field_name += "__"
                if col_name.startswith(self.col_prefix):
                    field_name += col_name[len(self.col_prefix):]
                else:
                    field_name += col_name
                field_verbose_names.append(unicode(field_verbose_name))
            if not field_name:
                field_name = "__".join(col_names)
            if field_name in col_labels:
                jq_col_names.append(unicode(col_labels[field_name]))
            elif col_names and col_names[0] in col_labels:
                jq_col_names.append(unicode(col_labels[col_names[0]]))
            else:
                jq_col_names.append(settings.JOINT.join(
                    [f for f in field_verbose_names if f]))
            if not python:
                jq_col_names[-1] = u'"%s"' % jq_col_names[-1]
            if python:
                extra_cols.append(field_name)
            else:
                extra_cols.append(self.COL_TPL % {'idx': field_name})
        if not python:
            jq_col_names = jq_col_names and ", ".join(jq_col_names) or ""
            extra_cols = extra_cols and ", ".join(extra_cols) or ""
        return jq_col_names, extra_cols

    def render(self, name, value=None, attrs=None):
        t = loader.get_template('blocks/form_flex_snippet.html')
        form = self.form()
        rendered = t.render(Context({'form': form,
                                     'flex': True}))
        dct = {}
        if self.new:
            model_name = self.associated_model._meta.object_name.lower()
            dct['url_new'] = reverse('new-' + model_name, args=['0'])
            dct['new_message'] = self.new_message

        col_names, extra_cols = self.get_cols()

        col_idx = []
        for k in form.get_input_ids():
            col_idx.append(u'"%s"' % k)
        col_idx = col_idx and ", ".join(col_idx) or ""

        dct['encoding'] = settings.ENCODING or 'utf-8'
        try:
            dct['source'] = unicode(self.source)
        except NoReverseMatch:
            logger.warning('Cannot resolve source for {} widget'.format(
                self.form))
        if unicode(self.source_full) and unicode(self.source_full) != 'None':
            dct['source_full'] = unicode(self.source_full)

        dct['extra_sources'] = []
        if self.associated_model:
            model_name = "{}.{}".format(
                self.associated_model.__module__,
                self.associated_model.__name__)
            for imp in models.ImporterType.objects.filter(
                    slug__isnull=False, associated_models__klass=model_name,
                    is_template=True).all():
                dct['extra_sources'].append((
                    imp.slug, imp.name,
                    reverse('get-by-importer', args=[imp.slug])))
        dct.update({'name': name,
                    'col_names': col_names,
                    'extra_cols': extra_cols,
                    'source': unicode(self.source),
                    'col_idx': col_idx,
                    'no_result': unicode(_("No results")),
                    'loading': unicode(_("Loading...")),
                    'remove': unicode(_(u"Remove")),
                    'sname': name.replace('-', ''),
                    'multiple': self.multiple,
                    'multiple_select': self.multiple_select,
                    'multi_cols': ",".join((u'"%d"' % col
                                           for col in self.multiple_cols))})
        t = loader.get_template('blocks/JQueryJqGrid.html')
        rendered += t.render(Context(dct))
        return mark_safe(rendered)
