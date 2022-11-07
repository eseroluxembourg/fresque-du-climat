#!/bin/bash
# Déploiement local des data dans le dossier memo-viewer
#+ qui doit se trouver à coté de ce dossier spécifique à la fresque du climat
mypath=`dirname $0`
source=$1
destination=$2

# 1. Copy data
bash $mypath/deploy.sh $source $destination
