from datetime import datetime
from django.db import models
from django.utils.timezone import utc


class PictureModel(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
    url = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    album = models.ForeignKey('AlbumModel', blank=True, null=True)


class AlbumModel(models.Model):
    user = models.ForeignKey('UserModel', blank=True, null=True)
    description = models.CharField(max_length=500)
    modified = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))


class UserModel(models.Model):
    fb_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
