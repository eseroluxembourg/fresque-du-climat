#!/bin/bash
OUTPUT_FILE="var/log/esero_server_out.log"
ERROR_FILE="var/log/esero_server_out.log"
touch $OUTPUT_FILE
touch $ERROR_FILE
npm run lsc >$OUTPUT_FILE 2>$ERROR_FILE
