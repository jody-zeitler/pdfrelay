#!/bin/bash

#uwsgi -s /tmp/uwsgi.sock -w wsgi:app --master --processes 4 --threads 2
uwsgi --http 127.0.0.1:8080 -w wsgi:app --master --processes 4 --threads 2

