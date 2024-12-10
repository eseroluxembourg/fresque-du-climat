#!/bin/bash
#cp -a "cards_svg_copy/*" "cards"
for l in $(echo en-GB de-DE) ; do
    for f in $(find "cards/$l" -name "*-back.svg" | sort) ; do
        #echo $f ;
        content=$(grep -P "<path .*?style=\"fill:url.*?/>" "$f" | sed 's/\//\\\//g' | sed 's/\"/\\\"/g')
        #echo ${content}
        #cat "$f" | sed "s/${content}//g"
        sed -i "s/${content}//g" "$f"
    done ;
done