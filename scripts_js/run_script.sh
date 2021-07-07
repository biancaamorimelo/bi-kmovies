#!/bin/bash
echo "Iniciando os scripts..."

SCRIPTS[0]="create_netflix_tmdb.js"
SCRIPTS[1]="create_index.js"
SCRIPTS[2]="create_producao.js"

for i in ${SCRIPTS[@]};
do
    echo "Execultado script $i... "
    mongo movies $i
    echo "   "
done
