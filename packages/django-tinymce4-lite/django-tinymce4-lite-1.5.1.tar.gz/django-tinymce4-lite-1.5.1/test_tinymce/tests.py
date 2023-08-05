# coding: utf-8

from __future__ import print_function
import json
import time
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
try:
    from unittest import mock
except ImportError:
    import mock


class RenderTinyMceWidgetTestCase(StaticLiveServerTestCase):
    def setUp(self):
        desired = DesiredCapabilities.PHANTOMJS
        desired['loggingPrefs'] = {'browser': 'ALL'}
        self.browser = PhantomJS(desired_capabilities=desired)
        super(RenderTinyMceWidgetTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(RenderTinyMceWidgetTestCase, self).tearDown()

    def test_rendering_tinymce4_widget(self):
        # Test if TinyMCE 4 widget is actually rendered by JavaScript
        self.browser.get(self.live_server_url + reverse('create'))
        try:
            self.browser.find_element_by_id('mceu_16')
        except WebDriverException:
            print('*** Start browser log ***')
            print(self.browser.get_log('browser'))
            print('**** End browser log ****')
            raise


    def test_rendering_with_different_language(self):
        with self.settings(LANGUAGE_CODE='fr-fr'):
            self.browser.get(self.live_server_url + reverse('create'))
            try:
                self.browser.find_element_by_id('mceu_16')
            except WebDriverException:
                print('*** Start browser log ***')
                print(self.browser.get_log('browser'))
                print('**** End browser log ****')
                raise
            else:
                self.assertTrue('Appuyer sur ALT-F9 pour le menu.' in
                                self.browser.page_source)


class RenderTinyMceAdminWidgetTestCase(StaticLiveServerTestCase):
    def setUp(self):
        desired = DesiredCapabilities.PHANTOMJS
        desired['loggingPrefs'] = {'browser': 'ALL'}
        self.browser = PhantomJS(desired_capabilities=desired)
        User.objects.create_superuser('test', 'test@test.com', 'test')
        self.browser.get(self.live_server_url + '/admin')
        self.browser.find_element_by_id('id_username').send_keys('test')
        self.browser.find_element_by_id('id_password').send_keys('test')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        time.sleep(0.1)
        super(RenderTinyMceAdminWidgetTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(RenderTinyMceAdminWidgetTestCase, self).tearDown()

    def test_rendering_tinymce4_admin_widget(self):
        self.browser.get(self.live_server_url + '/admin/test_tinymce/testmodel/add/')
        time.sleep(0.1)
        editors = self.browser.find_elements_by_class_name('mce-tinymce')
        try:
            self.assertEqual(len(editors), 2)
        except AssertionError:
            print('*** Start browser log ***')
            print(self.browser.get_log('browser'))
            print('**** End browser log ****')
            raise

    def test_adding_tinymce_widget_in_admin_inline(self):
        self.browser.get(self.live_server_url + '/admin/test_tinymce/testmodel/add/')
        time.sleep(0.1)
        self.browser.find_element_by_css_selector('div.add-row a').click()
        editors = self.browser.find_elements_by_class_name('mce-tinymce')
        try:
            self.assertEqual(len(editors), 3)
        except AssertionError:
            print('*** Start browser log ***')
            print(self.browser.get_log('browser'))
            print('**** End browser log ****')
            raise
        self.browser.find_element_by_css_selector('a.inline-deletelink').click()
        editors = self.browser.find_elements_by_class_name('mce-tinymce')
        self.assertEqual(len(editors), 2)
        self.browser.find_element_by_css_selector('div.add-row a').click()
        editors = self.browser.find_elements_by_class_name('mce-tinymce')
        try:
            self.assertEqual(len(editors), 3)
        except AssertionError:
            print('*** Start browser log ***')
            print(self.browser.get_log('browser'))
            print('**** End browser log ****')
            raise


class SpellCheckViewTestCase(TestCase):
    def test_spell_check(self):
        import enchant
        languages = enchant.list_languages()
        lang = 'en_US'
        if lang not in languages:
            lang = lang[:2]
            if lang not in languages:
                raise RuntimeError('Enchant package does not have English spellckecker dictionary!')
        text = 'The quick brown fox jumps over the lazy dog.'
        data = {'id': '0', 'params': {'lang': lang, 'text': text}}
        response = self.client.post(reverse('tinymce-spellchecker'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertTrue('result' in json.loads(response.content.decode('utf-8')))
        text = 'The quik brown fox jumps ower the lazy dog.'
        data['params']['text'] = text
        response = self.client.post(reverse('tinymce-spellchecker'), data=json.dumps(data),
                                    content_type='application/json')
        result = json.loads(response.content.decode('utf-8'))['result']
        self.assertEqual(len(result), 2)

    def test_missing_dictionary(self):
        data = {'id': '0', 'params': {'lang': 'fo_BA', 'text': 'text'}}
        response = self.client.post(reverse('tinymce-spellchecker'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertTrue('error' in json.loads(response.content.decode('utf-8')))


class CssViewTestCase(TestCase):
    def test_css_view(self):
        response = self.client.get(reverse('tinymce-css'))
        self.assertContains(response, 'margin-left')


class FileBrowserViewTestCase(TestCase):
    @mock.patch('tinymce.views.reverse')
    def test_filebrowser_view(self, mock_reverse):
        mock_reverse.return_value = '/filebrowser'
        response = self.client.get(reverse('tinymce-filebrowser'))
        self.assertContains(response, '/filebrowser')
