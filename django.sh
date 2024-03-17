#!/bin/sh
echo "Creating Migrations..."
python manage.py makemigrations djangotest
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
python manage.py test