# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class Video(models.Model):
    video_path = models.CharField(max_length=200)
    thumbnail_path = models.CharField(max_length=200)
    modified_timestamp = models.DateTimeField(default=datetime.now(),blank=True)
