#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
# File: taxydromikilib.py
"""
Main module file

Put your classes here
"""
from __future__ import unicode_literals
from requests import Session
from bs4 import BeautifulSoup as Bfs
import time
import logging

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''25-09-2017'''

# This is the main prefix used for logging
LOGGER_BASENAME = '''taxydromikilib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class TrackingState(object):
    def __init__(self, data):
        self._data = data

    def _get_data(self, class_name):
        try:
            value = self._data.find('div', {'class': class_name}).contents[1]
        except Exception:  # noqa
            value = None
        return value

    @property
    def status(self):
        return self._get_data('checkpoint-status')

    @property
    def location(self):
        return self._get_data('checkpoint-location')

    @property
    def date(self):
        return self._get_data('checkpoint-date')

    @property
    def time(self):
        return self._get_data('checkpoint-time')

    @property
    def is_final(self):
        return 'tracking-delivery last' in unicode(self._data)


class Taxydromiki(object):
    def __init__(self):
        self._base_url = 'https://www.taxydromiki.com'
        self._headers = {'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) '
                                        'AppleWebKit/537.36 (KHTML, like Gecko)'
                                        ' Chrome/60.0.3112.113 Safari/537.36'),
                         'Accept-Language': 'en-US,en;q=0.5',
                         'Accept-Encoding': 'gzip, deflate, br',
                         'Accept': ('text/html,application/xhtml+xml,'
                                    'application/xml;q=0.9,image/webp,'
                                    'image/apng,*/*;q=0.8')}
        self._session = None

    def _initialize(self):
        self._session = Session()
        headers = self._headers.copy()
        headers.update({'Upgrade-Insecure-Requests': '1',
                        'cache-contol': 'max-age=0'})
        url = '{base}/track'.format(base=self._base_url)
        response = self._session.get(url, headers=headers)
        form_build_id, theme_token = self._get_tokens(response)
        self._perform_ajax_blocks_call()
        return form_build_id, theme_token

    @staticmethod
    def _get_tokens(response):
        soup = Bfs(response.text, "html.parser")
        form = soup.find('form', {'id': 'custom-geniki-tracking-page-form'})
        form_build_id = form.find('input',
                                  {'name': 'form_build_id'}).attrs.get('value')
        index = response.text.find('theme_token')
        theme_token = response.text[index:index + 80].split('"')[1]
        return form_build_id, theme_token

    def _perform_ajax_blocks_call(self):
        url = '{base}/ajaxblocks'.format(base=self._base_url)
        headers = self._headers.copy()
        headers.update({'Accept': ('application/json, text/javascript, */*; '
                                   'q=0.01'),

                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': '{base}/track'.format(base=self._base_url)})
        payload = {'_': str(int(time.time()*1000)),
                   'blocks': 'custom-custom_time_date',
                   'path': 'track',
                   'nocache': '1'}
        response = self._session.get(url, headers=headers, params=payload)
        return response.ok

    def search(self, tracking_number):
        form_build_id, theme_token = self._initialize()
        url = '{base}/system/ajax'.format(base=self._base_url)
        headers = self._headers.copy()
        headers.update({'Host': 'www.taxydromiki.com',
                        'Accept': ('application/json, text/javascript, */*; '
                                   'q=0.01'),
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': '{base}/track'.format(base=self._base_url),
                        'Origin': self._base_url})

        payload = {'_triggering_element_name': 'op',
                   '_triggering_element_value': u'Αναζήτηση',
                   'ajax_html_ids[]': [
                       'mp-pusher',
                       'mp-menu',
                       'block-custom-custom-time-date',
                       'block-custom-custom_time_date-ajax-content',
                       'block-custom-custom-account-menu',
                       'block-lang-dropdown-language-content',
                       'lang_dropdown_form_language_content',
                       'lang-dropdown-select-language_content',
                       'trigger',
                       'block-system-main-menu',
                       'block-custom-geniki-tracking-form',
                       'custom-geniki-tracking-form',
                       'edit-tracking-number--2',
                       'edit-submit--3',
                       'block-block-10',
                       'main-content',
                       'custom-geniki-tracking-page-form',
                       'edit-tracking-searchbox',
                       'edit-tracking-number',
                       'edit-submit',
                       'tracking-result',
                       'block-menu-block-1',
                       'block-user-login',
                       'user-login-form',
                       'edit-name',
                       'edit-pass',
                       'edit-actions',
                       'edit-submit--4',
                       'block-block-3',
                       'block-block-4',
                       'block-block-9',
                       'block-block-2',
                       'block-menu-menu-footer-menu',
                       'block-menu-menu-footer-second',
                       'block-block-8'],
                   'ajax_page_state[css][modules/node/node.css]': '1',
                   'ajax_page_state[css][sites/all/modules/ckeditor/css/ckeditor.css]': '1',
                   'ajax_page_state[css][sites/all/modules/ctools/css/ctools.css]': '1',
                   'ajax_page_state[css][sites/all/modules/date/date_api/date.css]': '1',
                   'ajax_page_state[css][sites/all/modules/date/date_popup/themes/datepicker.1.7.css]': '1',
                   'ajax_page_state[css][sites/all/modules/lang_dropdown/lang_dropdown.css]': '1',
                   'ajax_page_state[css][sites/all/modules/logintoboggan/logintoboggan.css]': '1',
                   'ajax_page_state[css][sites/all/modules/views/css/views.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/field/field.theme.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/search/search.theme.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.base.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.menus.theme.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.messages.theme.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.theme.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/user/user.base.css]': '1',
                   'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/user/user.theme.css]': '1',
                   'ajax_page_state[css][sites/all/themes/taxydromiki/css/after.css]': '1',
                   'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.hacks.css]': '1',
                   'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.no-query.css]': '1',
                   'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.normalize.css]': '1',
                   'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.print.css]': '1',
                   'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.styles.css]': '1',
                   'ajax_page_state[js][0]': '1',
                   'ajax_page_state[js][misc/ajax.js]': '1',
                   'ajax_page_state[js][misc/drupal.js]': '1',
                   'ajax_page_state[js][misc/form.js]': '1',
                   'ajax_page_state[js][misc/jquery.cookie.js]': '1',
                   'ajax_page_state[js][misc/jquery.js]': '1',
                   'ajax_page_state[js][misc/jquery.once.js]': '1',
                   'ajax_page_state[js][misc/progress.js]': '1',
                   'ajax_page_state[js][public://languages/el_j43hC-GL4y98fNlJzVRM9SL0SKGIvZ5zF9vHNPqFpS8.js]': '1',
                   'ajax_page_state[js][sites/all/modules/ajaxblocks/ajaxblocks.js]': '1',
                   'ajax_page_state[js][sites/all/modules/browserclass/browserclass.js]': '1',
                   'ajax_page_state[js][sites/all/modules/clientside_validation/clientside_validation.ie8.js]': '1',
                   'ajax_page_state[js][sites/all/modules/clientside_validation/clientside_validation.js]': '1',
                   'ajax_page_state[js][sites/all/modules/clientside_validation/jquery-validate/jquery.validate.min.js]': '1',
                   'ajax_page_state[js][sites/all/modules/clientside_validation/jquery.form.js]': '1',
                   'ajax_page_state[js][sites/all/modules/custom/custom_geniki/custom_geniki.tracking.js]': '1',
                   'ajax_page_state[js][sites/all/modules/google_analytics/googleanalytics.js]': '1',
                   'ajax_page_state[js][sites/all/modules/lang_dropdown/lang_dropdown.js]': '1',
                   'ajax_page_state[js][sites/all/themes/omega/omega/omega/js/no-js.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/classie.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/jquery.hoverIntent.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/jquery.uniform.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/jquery.wookmark.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/mlpushmenu.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/modernizr.custom.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/taxydromiki.behaviors.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/js/taxydromiki.responsive.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/libraries/html5shiv/html5shiv-printshiv.min.js]': '1',
                   'ajax_page_state[js][sites/all/themes/taxydromiki/libraries/html5shiv/html5shiv.min.js]': '1',
                   'ajax_page_state[theme]': 'taxydromiki',
                   'ajax_page_state[theme_token]': theme_token,
                   'form_build_id': form_build_id,
                   'form_id': 'custom_geniki_tracking_page_form',
                   'tracking_number': tracking_number}
        response = self._session.post(url, headers=headers, data=payload)
        response_data = next((entry for entry in response.json()
                              if entry.get('command') == 'insert'), None)
        soup = Bfs(response_data.get('data'), 'html.parser')
        entries = soup.find_all('div', {'class': 'tracking-checkpoint'})
        return [TrackingState(entry) for entry in entries]
