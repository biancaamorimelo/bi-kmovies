#!/bin/bash
echo "---------------------------"
echo "| Importando dados do TMDB |"
echo "---------------------------"

DATA="data/"

 [ ! -d $DATA ] && mkdir $DATA && echo "Diretorio criado."

echo "Virtualizando o python..."
source tmdb_env/bin/activate

echo "Importando dados do TMDB..."
python3 import.tmdb.py

file="${DATA}movies.json"
echo "Importando para o MongoDB..."
if [ -f $file ]; then
    mongoimport --db tmdb --collection movies --file $file --jsonArray && \
    echo "Importação concluída."
else 
    echo "Não foi possível achar o arquivo '$file'."
fi
echo "Encerrando a virtualização..."
deactivate

echo "Concluído."