import datetime
import os
import uuid
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.files.storage import Storage, default_storage


class MP3(models.Model):
    def get_upload_path(instance, filename):
        return filename

    mp3file = models.FileField(upload_to=get_upload_path)
