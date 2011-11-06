#!/bin/bash

source bin/activate

pip -E . install --upgrade gunicorn

cd technex
../bin/gunicorn_django -b 0.0.0.0:$PORT -w 3

