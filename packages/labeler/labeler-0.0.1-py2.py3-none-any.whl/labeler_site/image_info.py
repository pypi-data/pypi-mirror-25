import os
import sys
# import json

import django
from django.conf import settings  # noqa Django magic starts here

import PIL.Image
from PIL.ExifTags import TAGS as tag_num2name
from PIL.ExifTags import GPSTAGS as gpstag_num2name

from pprint import pprint
# `labeler_site` must be a python package installed in your environment (virtualenv)
# OR "install" it manually before running this: `export PYTHONPATH=$PYTHONPATH:/path/to/labeler_site_basedir/`

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labeler_site.settings')
django.setup()


def get_exif(image_path=os.path.join(settings.BASE_DIR, 'labeler', 'data', 'SUNP0254.jpg')):
    """ Extract Exif header information from an image file and return it as a `dict` with informative keys

    >>> get_exif()
    [{...}]
    """
    img = PIL.Image.open(image_path)
    exif_data = img._getexif()
    exif_data = {} if exif_data is None else exif_data
    exif_data = dict(
        zip(
            # Bad idea because multiple keys coule be mapped to None destroying some data!
            # map(tag_num2name.get, exif_data.keys()),
            map(lambda i: tag_num2name.get(i, i), exif_data.keys()),
            exif_data.values()
        )
    )
    if 'GPSInfo' in exif_data:
        exif_data['GPSInfo'] = dict(
            zip(
                map(lambda i: gpstag_num2name.get(i, i), exif_data['GPSInfo'].keys()),
                exif_data['GPSInfo'].values()
            )
        )
    return exif_data


def main(args):
    return {arg: get_exif(arg) for arg in args}


def run():
    exif_data = main(sys.argv[1:])
    pprint(exif_data)


if __name__ == '__main__':
    exif_data = run()
    pprint(exif_data)
