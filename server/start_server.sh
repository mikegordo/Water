#!/bin/bash
cd /server || exit
FLASK_APP=water FLASK_ENV=development flask run --host=0.0.0.0
