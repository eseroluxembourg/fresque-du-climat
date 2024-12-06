
for local in $(ls ./public/cards)
do
    if [ -d "./public/cards/$local" ];
    then
        rm -r ./public/cards/$local/125
        rm -r ./public/cards/$local/250
        rm -r ./public/cards/$local/450
        rm -r ./public/cards/$local/600
        rm -r ./public/cards/$local/default
        rm -r ./public/cards/$local/svg

        mkdir ./public/cards/$local/svg
        for card in $(ls ./public/cards/$local/pdf) 
        do
            inkscape ./public/cards/$local/pdf/${card%.*}.pdf --export-filename ./public/cards/$local/svg/${card%.*}.svg;
            python3 scripts/compress-svg.py  ./public/cards/$local/svg/${card%.*}.svg
        done

        mkdir ./public/cards/$local/default
        for card in $(ls ./public/cards/$local/pdf) 
        do
            convert -density 150 ./public/cards/$local/pdf/${card%.*}.pdf -quality 100 -resize 600 ./public/cards/$local/default/${card%.*}-bis.png
            convert ./public/cards/$local/default/${card%.*}-bis.png -depth 8 -quality 90 ./public/cards/$local/default/${card%.*}-bis.png
            pngquant ./public/cards/$local/default/${card%.*}-bis.png --speed 1 --posterize 4 --output ./public/cards/$local/default/${card%.*}.png
            rm ./public/cards/$local/default/${card%.*}-bis.png
        done

        mkdir ./public/cards/$local/125
        mkdir ./public/cards/$local/250
        mkdir ./public/cards/$local/450
        mkdir ./public/cards/$local/600
        for card in $(ls ./public/cards/$local/pdf) 
        do
            convert ./public/cards/$local/default/${card%.*}.png -resize 125x125 -quality 90 ./public/cards/$local/125/${card%.*}.webp
            convert ./public/cards/$local/default/${card%.*}.png -resize 250x250 -quality 90 ./public/cards/$local/250/${card%.*}.webp
            convert ./public/cards/$local/default/${card%.*}.png -resize 450x450 -quality 90 ./public/cards/$local/450/${card%.*}.webp
            convert ./public/cards/$local/default/${card%.*}.png -resize 600x600 -quality 90 ./public/cards/$local/600/${card%.*}.webp
        done
    fi
done