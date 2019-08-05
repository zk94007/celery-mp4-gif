# video_phiid

## Get it to work

    $ git clone https://github.com/Carma-tech/cam_phiid
    $ cd cam_phiid
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver

## To get ingest flow to work

Open up another window, then:
   
    $ celery worker -A core -l info -B -s celery.beat.PersistentScheduler -O fair


## To get Email sending to work
    
Modify `core/settings.py`:
Replace:
```
EMAIL_HOST_USER = '<your_email@gmail.com>'
EMAIL_HOST_PASSWORD = '<your_gmail_password>'
```
With your own Gmail account and password.

You will also need to turn on _allow less secure app_ feature:

https://myaccount.google.com/lesssecureapps

for your account.

## Run it with Docker

First make sure you point videos/static/videos to the your video ingest folder

### Build all app docker images:
    
    $ docker-compose build

### To start the whole app stack:

    $ docker-compose up  # you only have to run --build once

Then visit:
http://localhost/ in your browser to see the app
       
    
### To Run the whole app stack in background:

    $ docker-compose up -d
    
### To watch all docker container's output:

    $ docker-compose logs -f

### To shutdown the app stack:

    $ docker-compose rm --stop --force

### To create a new dqlite db:

    $ docker-compose run --rm --no-deps web bash -c './manage.py migrate'


### To create a superuser db:

    $ docker-compose run --rm --no-deps web bash -c './manage.py createsuperuser'
    
    
    
     

