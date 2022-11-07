#!/bin/bash
# Save data from the memoviewer into a memoviewer.data folder
mypath=`dirname $0`
memoviewer=$1   # memoviewer main folder
data=`dirname $1`/`basename $memoviewer`.data       # data extracted from memoviewer folder
if [ data=. ]
then
backup=`dirname $data`/`basename $data`.back
else
backup=`dirname $data`/`basename $data`.data
fi

# 1. Backup the old data
echo "Save $data to $backup"
rm -rf $backup
mv $data $backup

# 2. Save memoviewer into data folder
bash $mypath/copyDataFromMain.sh $memoviewer $data
