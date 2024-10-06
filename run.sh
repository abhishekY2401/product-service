#!/bin/sh

echo "Applying database migrations..."
python3 -m flask db upgrade

echo "Starting the Flask application..."
python3 main.py &  # Start Flask app in background

echo "Starting the consumer..."
python3 consumer.py &  # Start consumer in background

wait  # Wait for all background processes to finish