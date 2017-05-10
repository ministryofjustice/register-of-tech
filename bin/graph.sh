#!/usr/bin/env bash

./manage.py graph_models -a -o docs/graph_model/latest.png
./manage.py graph_models -a -o docs/graph_model/$(date +"%Y-%m-%d-%H:%M:%S").png
