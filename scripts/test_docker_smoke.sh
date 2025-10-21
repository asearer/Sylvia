#!/bin/bash
set -e
SERVICES=(classifier matrix-bot dashboard)
echo "Building images..."
docker-compose build --parallel
for SERVICE in "${SERVICES[@]}"; do
  echo "\nStarting $SERVICE (in background)..."
  docker-compose up -d --profile experimental $SERVICE
  echo "Waiting for $SERVICE to start..."
  sleep 8
  echo "Checking logs for $SERVICE..."
  docker-compose logs --tail=25 $SERVICE
  docker-compose stop $SERVICE
  echo "------------------------------"
done
