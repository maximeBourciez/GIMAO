#!/bin/bash

IP=$(hostname -I | awk '{print $1}')

echo "VUE_APP_BACKEND_BASE_URL=http://$IP" > frontend/.env.production

docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
