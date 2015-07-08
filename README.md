# judgeSystem
A python/django based system for testing c/c++ solutions to algoritmic problems

What it does now:
  * Basic Login/register funtionality
  * Task/test editing
  * Grading solutions(only exact output)
  * Submiting solutions
  * A simple blog

What it is aiming to do:
  * More solution graders(and support for custom checkers)
  * Competitions
  * Comunity submited problems

Required software:
  * Python 3.\*
  * Python moules: django, celery, django-celery, django-bootsrap3, django-bootstrap-pagination
  * g++ compiler
  * postgreSQL database
  * rabbitmq message broker for celery NOTE: This is optional. If you want you can use django's
    database as backend. You need to uncoment the BROKER_URL line(17) in judgeSystem/celery.py

How to run:
  0. Create database: python manage.py migrate
  1. Run server as root:
    * Actual server : python manage.py runserver
    * Celery server : celery -A judgeSystem 
      (you can mess with the parameters if you want) 

Adittional Notes:
  * You need to create a judgeSystem/sens.py to include the email, password and domain of the system.
  * This project is using a precompiled version of isolate sandbox(https://github.com/cms-dev/isolate). You may need
    to compile it on your own. (The system uses judge/isolate for all it's tesing)
