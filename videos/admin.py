# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Video

class VideoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['video_path']}),
        (None,               {'fields': ['thumbnail_path']}),
        (None,               {'fields': ['modified_timestamp']}),
    ]
    list_display = ('video_path', 'thumbnail_path', 'modified_timestamp')

admin.site.register(Video, VideoAdmin)