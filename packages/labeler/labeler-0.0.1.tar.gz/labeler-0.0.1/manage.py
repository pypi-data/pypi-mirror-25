#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labeler_site.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    try:
        from django.conf import settings
        from pugnlp.futil import find_files

        # delete all `.pyc` files
        for ff in find_files(settings.BASE_DIR, '.pyc'):
            if ff['path'].endswith('.pyc'):  # double check that find_files is correct about file extension
                os.remove(ff['path'])
    except ImportError:
        print("WARN: unable to delete all pyc files until you install pugnlp.")

    execute_from_command_line(sys.argv)
