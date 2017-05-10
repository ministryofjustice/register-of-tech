#!/usr/bin/env bash

echo 'yes' | ./manage.py reset_db
./manage.py  migrate
./manage.py  migrate --run-syncdb
./manage.py loaddata test_users
