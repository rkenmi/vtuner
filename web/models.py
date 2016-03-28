from __future__ import unicode_literals
import datetime, os, uuid

from django.db import models
from django.utils import timezone
from django.core.files.storage import Storage, default_storage

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	def __str__(self):
		return self.question_text

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default = 0)

	def __str__(self):
		return self.choice_text



class MP3(models.Model):
	#uu = uuid.uuid4()
	def get_upload_path(instance, filename):

		#filename = "%s_%s" % (filename, uu)
		return filename

	mp3file = models.FileField(upload_to=get_upload_path)
	#id = models.AutoField(primary_key=True)
