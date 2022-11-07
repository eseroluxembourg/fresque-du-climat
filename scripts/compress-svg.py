import sys
import subprocess
from bs4 import BeautifulSoup
import base64
import os
import re

filename = sys.argv[1]
card = os.path.basename(filename)[:-4]
svg_filename = filename[:-3] + 'svg'
svg_filename_bis = filename[:-4] + "-bis.svg"
#        command = 'inkscape --batch-process --verb com.klowner.filter.apply_transform {} -o {} '.format(svg_filename, svg_filename_bis)
#        subprocess.call(command, shell=True)
#        svg_filename = svg_filename_bis
#        command = "inkscape -z {} --export-plain-svg={}".format(filename, svg_filename)
#        subprocess.call(command, shell=True)

soup = BeautifulSoup(open(svg_filename, 'r').read(), 'xml')

#        txts = soup.find_all('svg:text')
#        for txt in txts:
#            txt.extract()


# style = BeautifulSoup("\
# <style>\
# @font-face {\
#     font-family: 'ArialMT';\
#     src: url('/fonts/arialmt.ttf') format('truetype');\
#     font-weight: normal;\
#     font-style: normal;\
# }\
# </style>", "xml")
# soup.find("svg").insert(0, style)
# Prefix all ids

images = list(soup.find_all('svg:image'))

bigger_img_index = 0
for k in range(len(images)):
#            if len(images[k]['xlink:href']) > len(images[bigger_img_index]['xlink:href']):
#                bigger_img_index = k
    
    image = images[k]
    imageid = image['id']
    base64_image = image['xlink:href']
    prefix = 'data:image/png;base64,'
    base64_image = base64_image[len(prefix):]
    #print(base64_image)
    png_filename = filename[:-4] + "-" + str(k) + '.png'
    print("En cours de traitement: ", png_filename)            
    with open(png_filename, "wb") as f:
        f.write(base64.b64decode(base64_image))
        output = png_filename[:-4] + '-compressed.png'
        if os.path.exists(output):
            os.remove(output)
        command = "pngquant {} --output {}".format(png_filename, output)
        outcode = subprocess.call(command, shell=True)
        if outcode != 25:
            with open(output, "rb") as nf:
                new_image = prefix + base64.encodebytes(nf.read()).decode('utf8')
                soup.find('svg:image', {"id": imageid })['xlink:href'] = new_image
        else:
            print("Error :(")
        if os.path.exists(output):
            os.remove(output)
        if os.path.exists(png_filename):
            os.remove(png_filename)
with open(svg_filename[:-4] + ".svg", "w") as file:
    strsoup = str(soup)
    strsoup = strsoup.replace("svg:", "")
    prefix = card

    regex_id = r'id="([^"]*)'
    subst_id = r'id="{}_\1'.format(prefix)

    # You can manually specify the number of replacements by changing the 4th argument
    strsoup = re.sub(regex_id, subst_id, strsoup)

    regex_id = r'\(#(\D+\d+)\)'
    subst_id = r'(#{}_\1)'.format(prefix)

    # You can manually specify the number of replacements by changing the 4th argument
    strsoup = re.sub(regex_id, subst_id, strsoup)
    # if result:
    #     print(result)
    file.write(strsoup)
    

    