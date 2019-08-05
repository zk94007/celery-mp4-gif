# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .forms import ContactForm
from .tasks import send_video_email_task

# Create your views here.
from .models import Video


def index(request):
    video_list = Video.objects.all().order_by('-modified_timestamp')
    paginator = Paginator(video_list, settings.PAGINATION_PER_PAGE)

    page = request.GET.get('page')
    videos = paginator.get_page(page)
    return render(request, 'index.html', {'videos': videos})


def detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_video_email_task.delay(form.cleaned_data['email'], video.video_path)

    form = ContactForm()
    return render(request, 'detail.html', {'video': video, 'form': form})
