import os
import datetime

from django.test import TestCase
from django.utils import timezone
# from django.core.urlresolvers import reverse

import labeler_site.settings
from .models import Image

import doctest
from labeler_site import bot


# from .forms import FileUploadForm

MEDIA_ROOT = labeler_site.settings.MEDIA_ROOT


class ImageModelTest(TestCase):
    fixtures = ['labeler_test_data.json']
    caption = "This is only a test ... image take 2.5 years ago."

    def create_image(self, caption=caption):
        return Image.objects.create(caption=caption,
                                    taken_date=timezone.now() - datetime.timedelta(365.25 * 2.5),
                                    file=os.path.join(
                                        MEDIA_ROOT, 'images', 'test_image.jpg'),
                                    # uploaded_by=,
                                    created_date=timezone.now())

    def test_image_creation(self):
        image = self.create_image()
        self.assertTrue(isinstance(image, Image))
        # self.assertEqual(image.__unicode__(), image.caption)
        self.assertEqual(self.caption, image.caption)


class BotTest(TestCase):
    """Run doctests for the bot module"""

    def test_doctests(self):
        results = doctest.testmod(bot)
        self.assertEqual(results.failed, 0)
