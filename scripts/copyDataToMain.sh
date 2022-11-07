#!/bin/bash
# Copy the data from a data project (source) to the main project memo-viewer (destination)
data=$1        # source folder
memoviewer=$2  # destination folder

echo "Insert Data $data into project $memoviewer"

# 1. Create directory structure
mkdir -p $memoviewer/src/data/

cp $data/public $memoviewer -r
cp $data/src $memoviewer -r
cp $data/settings.json $memoviewer