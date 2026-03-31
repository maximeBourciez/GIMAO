#!/bin/bash
CURRENT_IP=$(hostname -I | awk '{print $1}')

echo "IP initiale : $CURRENT_IP"

./init.sh

while true; do
  sleep 60
  
  NEW_IP=$(hostname -I | awk '{print $1}')
  
  if [ "$NEW_IP" != "$CURRENT_IP" ] && [ ! -z "$NEW_IP" ]; then
    echo "[$(date)] $CURRENT_IP -> $NEW_IP"
    CURRENT_IP=$NEW_IP
    ./init.sh
  fi
done
