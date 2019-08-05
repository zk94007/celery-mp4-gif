import os

from django.core.mail import EmailMessage
from django.conf import settings


def send_video_email(email,video):
    msg = EmailMessage('cam_phiid', 'Hello, I am sending the video', settings.EMAIL_HOST_USER, [email])
    msg.attach_file(os.path.join(settings.WATCHING_DIR, video))
    msg.send()