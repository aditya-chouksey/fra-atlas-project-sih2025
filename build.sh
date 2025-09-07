#!/usr/bin/env bash
pip install -r requirements.txt
cd frapro
python manage.py collectstatic --noinput
python manage.py migrate