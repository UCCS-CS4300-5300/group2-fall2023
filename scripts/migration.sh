#!/bin/bash

# Add new apps with models to this list
APPS=("Events" "Products" "Common" "Reservations")

# Make migrations
python3 ../manage.py makemigrations ${APPS[@]}

# Run migrate
python3 ../manage.py migrate
