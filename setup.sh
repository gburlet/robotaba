#!/bin/bash

rm robotaba.db
rm -rf robotaba/media
python manage.py syncdb --noinput
python manage.py runserver
