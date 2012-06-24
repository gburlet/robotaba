#!/bin/bash

rm robotaba.db
python manage.py syncdb
