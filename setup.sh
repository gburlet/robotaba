#!/bin/bash

rm robotaba.db
python manage.py syncdb
python manage.py runserver
