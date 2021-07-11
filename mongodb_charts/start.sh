#!/bin/bash

echo "Iniciando docker-compose..."

[ ! -d data/ ] && mkdir data/
[ ! -d charts/ ] && mkdir charts/

docker-compose up -d

echo "Aguarde..."

sleep 60

echo "Criando usuário..."

docker exec -it \
  $(docker container ls --filter name=_charts -q) \
  charts-cli add-user --first-name "Admin" --last-name "Admin" \
  --email "admin@admin.com" --password "admin123" \
  --role "UserAdmin"

echo "Usuário criado."
echo "Username: admin@admin.com"
echo "Password: admin123"