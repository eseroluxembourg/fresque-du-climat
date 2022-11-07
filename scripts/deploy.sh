#!/bin/bash
# production deployment
mypath=`dirname $0`
source=$1
destination=$2

# 0. Make a backup
# bash $mypath/backup.sh $destination

# 1. Copy data
bash $mypath/copyDataToMain.sh $source $destination

# 2. pull ...

# 3.
