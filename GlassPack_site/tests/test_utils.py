import shutil
from django.test import TestCase
from django.conf import settings
from django.test import override_settings

TEST_DIR = 'test_data'

@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class BaseTestCase(TestCase):
    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        return super().tearDown()