from django.test import TransactionTestCase

import tempfile


class SeleniumTestCase(TransactionTestCase):

    def test_simple(self):
        driver = self.driver
        driver.get('http://www.google.com')
        firefox_profile = self.driver.firefox_profile

        self.assertEqual(
            firefox_profile.default_preferences['browser.download.dir'],
            tempfile.gettempdir()
        )

        self.assertEqual(
            firefox_profile.default_preferences['browser.helperApps.neverAsk.saveToDisk'],
            'application/ourfakemimetype'
        )

        self.assertEqual(
            firefox_profile.default_preferences['browser.download.folderList'],
            2
        )

        self.assertEqual(
            firefox_profile.default_preferences['browser.download.manager.showWhenStarting'],
            False
        )


