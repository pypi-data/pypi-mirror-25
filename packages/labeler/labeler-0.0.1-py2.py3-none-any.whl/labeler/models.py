""" Profile model with first and last name an image or profile description

Models:
  Label model with image ID and classification and user id
  Image model with image ID and path to the image on a shared server or a binary blob of the image itself

References:
  [Django tutorial part 1](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)
  [Django tutorial part 2](https://docs.djangoproject.com/en/1.11/intro/tutorial02/)
  [Pattern for uploading files](http://www.bogotobogo.com/python/Django/Python_Django_Image_Files_Uploading_Example.php)
"""
from django.db import models
import jsonfield
# from django.contrib.postgres.fields import JSONField  # only for PostGRESQL (psycopg2 backend)!
from django.contrib.auth.models import User


# FIXME: Unused but don't comment it out because migrations use it
def user_images_directory(instance, filename):
    """ Prepend a directory path to uploaded filenames to prevent multiple files being uploaded with the same name

    If the same user uploads thes same filename twice the original file is overwritten.
    The FileField object places all uploaded files in MEDIA_ROOT/uid_<uid>/<filename>
    """
    return 'images/uid_{uid}/{filename}'.format(
        uid=getattr(instance.uploaded_by, 'id', 0),
        filename=filename)


class Label(models.Model):
    """ A label that can be assigned to an image """
    label = models.CharField(max_length=256, default=None, null=True)
    category = models.CharField(max_length=256, default='animal', null=True)
    created_by = models.ForeignKey(User, default=None, null=True)
    updated_date = models.DateTimeField('Datetime the label was changed or updated.', auto_now=True)
    created_date = models.DateTimeField('Datetime the label was created in the database.', auto_now_add=True)


class Image(models.Model):
    """ A database record for images to be labeled """
    caption = models.CharField("Description of the image, where and when it was taken, who/what is in it, etc",
                               max_length=512, default='', blank=True)
    description = models.TextField("Description of the image, where and when it was taken, who/what is in it, etc",
                                   max_length=512, default='', blank=True)
    label = models.ManyToManyField(Label, through='ImageLabel', blank=True)
    taken_date = models.DateTimeField('Date photo was taken.', null=True, default=None, blank=True)
    updated_date = models.DateTimeField('Date photo was changed.', auto_now=True)
    created_date = models.DateTimeField('Date photo was created.', auto_now_add=True)
    uploaded_by = models.ForeignKey(User, default=None, null=True, blank=True)
    file = models.FileField("Image to be labeled", upload_to='images', blank=False)
    info = jsonfield.JSONField("Metadata about the image (usually from the EXIF header)", null=True, default=None, blank=True)


class ImageLabel(models.Model):
    """ Individual user labels (a filled out ballot that "votes" for a label associated with an image) """
    label = models.ForeignKey(Label, default=None, null=True)
    image = models.ForeignKey(Image, default=None, null=True)
    user = models.ForeignKey(User, default=None, null=True)
    updated_date = models.DateTimeField('Datetime the label was assigned to the image.', auto_now=True)
    created_date = models.DateTimeField('Datetime the label was assigned to the image.', auto_now_add=True)


class TotalVotes(models.Model):
    """ Aggregated (denormalized) votes (by all users, who are allowed to vote multiple times) for an individual Image """
    image = models.ForeignKey(Image, default=None, null=True)
    name = models.CharField(max_length=128)
    votes = models.IntegerField(default=0)
