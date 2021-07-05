#!/bin/bash
echo "---------------------------"
echo "| Importando dados do TMDB |"
echo "---------------------------"

DATA="data/"

[ ! -d $DATA ] && mkdir $DATA && echo "Diretorio criado."

echo "Virtualizando o python..."
[ -d tmdb_env ] && rm -Rf tmdb_env/
python3 -m venv tmdb_env
source tmdb_env/bin/activate

echo "Instalando o mongoDb for python..."
python3 -m pip install pymongo

echo "Instalando o Requests..."
pip3 install requests


echo "Importando dados do TMDB..."
python3 import.tmdb.py

file="${DATA}movies.json"
echo "Importando para o MongoDB..."
if [ -f $file ]; then
    mongoimport --db movies --collection tmdb_titles --file $file --jsonArray && \
    echo "Importação concluída."
else 
    echo "Não foi possível achar o arquivo '$file'."
fi
echo "Encerrando a virtualização..."
deactivate

echo "Concluído."