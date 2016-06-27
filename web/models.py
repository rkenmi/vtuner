from django.db import models


class MP3(models.Model):
    def get_upload_path(instance, filename):
        return filename

    mp3file = models.FileField(upload_to=get_upload_path)
