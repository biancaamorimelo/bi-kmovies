#!/bin/bash
echo "-----------------------"
echo "| Importando dados... |"
echo "-----------------------"

DATA="data/"

 [ ! -d $DATA ] && mkdir $DATA && echo "Diretorio criado."

IMPORTS[0]='https://datasets.imdbws.com/name.basics.tsv.gz'
IMPORTS[1]='https://datasets.imdbws.com/title.akas.tsv.gz'
IMPORTS[2]='https://datasets.imdbws.com/title.basics.tsv.gz'
IMPORTS[3]='https://datasets.imdbws.com/title.crew.tsv.gz'
IMPORTS[4]='https://datasets.imdbws.com/title.episode.tsv.gz'
IMPORTS[5]='https://datasets.imdbws.com/title.principals.tsv.gz'
IMPORTS[6]='https://datasets.imdbws.com/title.ratings.tsv.gz'

import_file () {
    echo "Importando... "
    url=$1
    path=$2
    echo "$url"
    wget -P $path $url
    echo "------------------------------------------------"
    echo " "
}

extract_file () {
    file=$1
    echo "Extraindo... "
    gzip -df $file
    echo "------------------------------------------------"
    echo " "
}

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

    [ -f $file ] && mongoimport --db tmdb --collection $collection --file $file --jsonArray
    echo "------------------------------------------------"
    echo " "
}

for i in ${IMPORTS[@]};
do
    name="${i##*/}"
    filename="${name%.*}"
    name="${filename%.*}"
    pyname="python_scripts/$name.py"
    json="$DATA$name.json"
    filecsv="$DATA$filename"

    import_file $i $DATA
    extract_file "$DATA$filename"
    python_script $pyname "$DATA$filename" $json
    import_mongo $json $name    
done