#!/bin/bash
echo "-------------------------------"
echo "| Importando dados da Netflix |"
echo "-------------------------------"

DATA="data/"

 [ ! -d $DATA ] && mkdir $DATA && echo "Diretorio criado."


python_script () {
    echo "Convertendo... "
    script=$1
    file=$2
    json=$3
    [ -f $script ] && python3 $script $file $json --remove_file 
    echo "------------------------------------------------"
    echo " "
}

import_mongo () {
    echo "Importando para o MongoDB... "
    file=$1
    collection=`echo $2 | sed -e 's/[.]/_/'`    
    [ -f $file ] && mongoimport --db movies --collection $collection --file $file --jsonArray
    echo "------------------------------------------------"
    echo " "
}

filename="netflix_titles.csv"
name="${filename%.*}"
pyname="import.netflix.py"
json="$DATA$name.json"


python_script $pyname "$DATA$filename" $json
import_mongo $json "netflix_title"    

echo "Rodando script de criação netflix_imdb"
mongo movies create_netflix_tmdb.js

echo "Ciando index"
mongo movies create_index.js

