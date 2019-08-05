import os
import glob
import socket

from celery.utils.log import get_task_logger
from django.conf import settings
from moviepy.editor import VideoFileClip

from core.celery import app
from core.utils import is_file_locked
from videos.models import Video
from datetime import datetime

from .emails import send_video_email

logger = get_task_logger(__name__)


@app.task(bind=True)
def send_video_email_task(self, email, video):
    try:
        send_video_email(email, video)
        logger.info("Sent email: " + email)
    except socket.gaierror as exc:
        logger.error(str(exc) + " : " + email)
        raise self.retry(exc=exc, max_retries=settings.CELERY_MAX_RETRIES,
                         countdown=settings.CELERY_COUNTDOWN)


@app.task
def folder_listening():
    logger.info("Watching: " + settings.WATCHING_DIR)

    # get all mp4 files in watching folder
    os.chdir(settings.WATCHING_DIR)
    for file_ in glob.glob("*.mp4"):
        # check file's lock status
        if not is_file_locked(os.path.join(settings.WATCHING_DIR, file_), logger):
            filepath = os.path.join(settings.WATCHING_DIR, file_)
            current_change_time = datetime.fromtimestamp(os.path.getctime(filepath))

            # check if the file processed already
            try:
                obj = Video.objects.get(
                    video_path=file_, 
                    modified_timestamp=current_change_time
                )
            except Video.DoesNotExist:
                logger.info("Processing %s" % file_)

                # generate a thumbnail for the video and save it to /videos/static/thumbnails/
                try:
                    # delete all files of which names are equal to file_
                    Video.objects.filter(video_path=file_).delete()

                    # insert video path and thumbnail path to videos table
                    Video.objects.create(
                        video_path=file_,
                        thumbnail_path="%s.gif" % os.path.splitext(file_)[0],
                        modified_timestamp=current_change_time
                    )

                    clip = VideoFileClip(os.path.join(settings.WATCHING_DIR, file_))
                    subclip = clip.subclip(clip.duration / 2, clip.duration + 0.5).resize(0.3)
                    subclip.write_gif(os.path.join(settings.THUMBNAIL_DIR, "%s.gif" % os.path.splitext(file_)[0]))
                except:
                    logger.error("Clip Error: Invalid file %s" % file_)
                    # remove inserted video path
                    Video.objects.get(video_path=file_).delete()
            except Video.MultipleObjectsReturned:
                # detect double processing on a file
                logger.error("Process Error: Duplicated file %s" % file_)
            except Exception as e:
                # detect dabase issue by celery
                logger.error(str(e))
                logger.error("Process Unknown Error" % file_)
