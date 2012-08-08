#!/bin/bash

rm robotaba.db
python manage.py syncdb --noinput
python manage.py runserver
