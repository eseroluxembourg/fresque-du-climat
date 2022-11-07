import sys
import subprocess
from bs4 import BeautifulSoup
import base64
import os
import re
import cv2
from alive_progress import alive_bar
import shutil

import numpy as np
import matplotlib.pyplot as plt

import uuid


def compress(filename):
    tmp_compress = str(uuid.uuid4())
    os.mkdir(tmp_compress)
    def _export_to_png(svg_string, png_filename):
        with open('tmp_svg.svg', 'w') as f:
            f.write(svg_string)
        
        command = f'inkscape -w { 800 } "tmp_svg.svg" -o "{png_filename}"'
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

    def _compare_images(reference_png, png_filename):
        reference =  cv2.imread(reference_png, cv2.IMREAD_UNCHANGED)
        compare =  cv2.imread(png_filename, cv2.IMREAD_UNCHANGED)
        diff = reference == compare
        diff = diff.reshape((-1, 1, 1))
        ratio = sum(diff) / len(diff)
        ratio = ratio[0][0]
        return ratio

    def _extract_image(svg_filename, image_id):
        command = f'inkscape { svg_filename } --export-id="{image_id}" -o "{tmp_compress}/selected_image{ image_id }.png"'
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
        img = cv2.imread(os.path.join(tmp_compress, 'selected_image' + image_id + 'png'), cv2.IMREAD_UNCHANGED)
        w = img.shape[0]
        h = img.shape[1]

        return (w, h)

    def _recompute_image(svg_filename, image_id):

        command = f'inkscape { svg_filename } --export-id="{image_id}" -o "{tmp_compress}/reference_{ image_id }.png"'
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result_size = os.path.getsize(f"{tmp_compress}/reference_{ image_id }.png")
        if result_size < 1000:
            return None

        soup = BeautifulSoup(open(svg_filename, 'r').read(), 'xml')

        image = soup.find('svg:image', {"id": image_id })
        base64_image = image['xlink:href']
        prefix = 'data:image/png;base64,'
        base64_image = base64_image[len(prefix):]

        png_filename = "extracted_" + str(image_id) + '.png'
        with open(os.path.join(tmp_compress, png_filename), "wb") as f:
            f.write(base64.b64decode(base64_image))

        actual_size = cv2.imread(os.path.join(tmp_compress, png_filename)).shape
        reference_png = cv2.imread(os.path.join(tmp_compress, f'reference_{image_id}.png'))
        target_size = reference_png.shape

        ratio = round(target_size[0]/actual_size[0]*100,2)
        command = f'convert {tmp_compress}/{png_filename} -resize {ratio}% {tmp_compress}/{png_filename}'
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)


        resized_image = cv2.imread(os.path.join(tmp_compress, png_filename))
        height = min(resized_image.shape[1], reference_png.shape[1]) 

        # resized_image = resized_image[:, :height, :]
        # reference_png = reference_png[:, :height, :]
        
        # diff_r = np.abs(reference_png[:,:,0] - reference_png[:,:,0]) == 0
        # diff_g = np.abs(resized_image[:,:,1] - reference_png[:,:,1]) == 0
        # diff_b = np.abs(resized_image[:,:,2] - reference_png[:,:,2]) == 0

        diff_r = reference_png[:,:,0] != reference_png[:,:,0]
        diff_g = resized_image[:,:,1] != reference_png[:,:,1]
        diff_b = resized_image[:,:,2] != reference_png[:,:,2]

        diff = np.where(resized_image != reference_png)
        nb_diff = len(diff[0])
        ratio_diff = nb_diff / (resized_image.shape[0]*resized_image.shape[1]*resized_image.shape[2])

        if False:#ratio_diff > 0.98:
            rgba_img = cv2.cvtColor(resized_image, cv2.COLOR_RGB2RGBA)

            # 0 ssi au moins 1 px est différent
            rgba_img[:,:,3] = 255*diff_r*diff_g*diff_b
            # # rgba_img[:,:,0] = img[:,:,0]
            cv2.imwrite('{tmp_compress}/rgba_' + image_id + '.png', rgba_img)
            png_filename = 'rgba_' + image_id + '.png'

            output_png = os.path.join(tmp_compress, 'final_' + image_id + '.png')
            if os.path.exists(output_png):
                os.remove(output_png)
            
            command = "pngquant {tmp_compress}/{} --output {}".format(png_filename, output_png)
            print(command)
            outcode = subprocess.call(command, shell=True)
            print('ooutcode', outcode)
            
            return output_png
        else:

            cv2.imwrite(f'{tmp_compress}/masked_' + image_id + '.png', resized_image)

            command = f'convert {tmp_compress}/masked_{image_id}.png {tmp_compress}/masked_{image_id}.jpg'
            subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

            command = f'jpegoptim --max 75 {tmp_compress}/masked_{image_id}.jpg'
            subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

            return os.path.join(tmp_compress, 'masked_' + image_id + '.jpg')
    

    card = os.path.basename(filename)[:-4]
    svg_filename = filename[:-3] + 'svg'
    
    soup = BeautifulSoup(open(svg_filename, 'r').read(), 'xml')
    images = list(soup.find_all('svg:image'))
    for image in images:
        recomputed_img = _recompute_image(svg_filename, image['id'])
        if recomputed_img is None: continue

        with open(recomputed_img, "rb") as nf:

            prefix = 'data:image/jpeg;base64,' if recomputed_img.endswith('jpg') else 'data:image/png;base64,'
            new_image = prefix + base64.encodebytes(nf.read()).decode('utf8')

            soup.find('svg:image', {"id": image['id'] })['xlink:href'] = new_image

    with open(os.path.join(tmp_compress, 'compressed_svg.svg'), 'w') as f:
        strsoup = str(soup)
        strsoup = strsoup.replace("svg:", "")
        prefix = card

        regex_id = r'id="([^"]*)'
        subst_id = r'id="{}_\1'.format(prefix)
        strsoup = re.sub(regex_id, subst_id, strsoup)

    #     # # You can manually specify the number of replacements by changing the 4th argument
        # f.write(strsoup)
        regex_id = r'\(#(\D+\d+)\)'
        subst_id = r'(#{}_\1)'.format(prefix)
        strsoup = re.sub(regex_id, subst_id, strsoup)

        # You can manually specify the number of replacements by changing the 4th argument
        f.write(strsoup)
        #     # if result:
        #     #     print(result)
        #     file.write(strsoup)

        
    return os.path.join(tmp_compress, 'compressed_svg.svg')
        
if __name__ == '__main__':
    compress(sys.argv[1])
        