#!/bin/bash

SCRIPTS[0]="./import_imdb/run.sh"
SCRIPTS[1]="./import_netflix/run.sh"
SCRIPTS[2]="./import_tmdb/run.sh"
SCRIPTS[3]="./scripts_js/run_script.sh"
for i in ${SCRIPTS[@]};
do
    d=$(dirname "${i}")
    f=$(basename "${i}")
    cd $d &&  echo $(pwd) &&  bash $f
    cd ..
done