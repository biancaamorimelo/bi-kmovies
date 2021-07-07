#!/bin/bash
echo "Iniciando os scripts..."

SCRIPTS[0]="create_index.js"
SCRIPTS[1]="create_producao.js"

for i in ${SCRIPTS[@]};
do
    echo "Execultado script $i... "
    mongo movies $i
    echo "   "
done
