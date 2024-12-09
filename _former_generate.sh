#!/bin/sh

if [ ! -e ~/venv_esero_fresk ] ; then
    sudo apt install python3.11-venv ;
    python3 -m venv ~/venv_esero_fresk ;
    source ~/venv_esero_fresk/bin/activate ;
    pip3 install bs4 alive_progress jsonschema ;
    python3 memo-viewer/moulinette/get-pip.py ;
    pip3 install memo-viewer/moulinette/files-manipulator/images-manipulator/. ;
    deactivate ;
fi

cp -f "scripts/cards-pdfs/Adults de-DE V9.0.pdf" "moulinette-data/_pdfs/de-DE_v9.0.pdf"
cp -f "scripts/cards-pdfs/Adults en-GB V9.0.pdf" "moulinette-data/_pdfs/en-GB_v9.0.pdf"
cp -f "scripts/cards-pdfs/Adults fr-FR V9.0.pdf" "moulinette-data/_pdfs/fr-FR_v9.0.pdf"

source ~/venv_esero_fresk/bin/activate
python3 memo-viewer/moulinette/moulinette.py
deactivate
