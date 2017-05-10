#!/usr/bin/env bash

echo 'yes' | ./manage.py reset_db
./manage.py  migrate
