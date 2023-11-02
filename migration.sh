#!/bin/bash

# Add new apps with models to this list
APPS=("Events" "Products")

# Make migrations
python manage.py makemigrations ${APPS[@]}

# Run migrate
python manage.py migrate
