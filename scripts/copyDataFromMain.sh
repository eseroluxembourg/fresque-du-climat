#!/bin/bash
# Save data from the memoviewer into a memoviewer.data folder

memoviewer=$1 # source folder
data=$2       # destination folder

echo "Save data from $memoviewer to $data"

# 1. Create data destination directory structure
mkdir -p $data
mkdir -p $data/public/
mkdir -p $data/src/
mkdir -p $data/src/assets
mkdir -p $data/src/assets/icons
mkdir -p $data/src/assets/styles
mkdir -p $data/src/components

# 2 Copy data
rm $memoviewer/public/cards
cp $memoviewer/public/cards $data/public/ -r
cp $memoviewer/public/logo  $data/public/ -r
cp $memoviewer/public/previews $data/public/ -r

cp $memoviewer/src/assets/icons/card-number-icon.svg $data/src/assets/icons/card-number-icon.svg -r
cp $memoviewer/src/assets/styles/local.scss $data/src/assets/styles/local.scss -r

cp $memoviewer/src/data $data/src/ -r

cp $memoviewer/src/locales $data/src/ -r

cp $memoviewer/src/components/about $data/src/components/ -r

cp $memoviewer/settings.json $data/

