#!/usr/bin/env bash

echo 'yes' | ./manage.py reset_db
./manage.py  migrate
./manage.py  migrate --run-syncdb
./manage.py loaddata groups applications test_users test_categories test_business_area
./manage.py set_secrets
