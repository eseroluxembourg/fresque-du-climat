import sys
import subprocess
import os
import shutil
import language_utils
from alive_progress import alive_bar
import threading
NB_THREADS = 12
from compress_svg import compress
from math import ceil

def split_pdf(language, pdf_filename):
    print(f'1. Split pdf { pdf_filename }')
    os.mkdir(os.path.join(language, 'pdf'))
    # for k in range(1, 88):
    #     subprocess.call(f'pdftk { pdf_filename } cat { k } output {language}/{k}.pdf', shell=True)
    command = f'pdfseparate { pdf_filename} { language }/%d.pdf'
    subprocess.call(command, shell=True)

    fronts = [ (3, 'front-1'), (5, 'front-5'), (7, 'front-7'), (9, 'front-13'), (11, 'front-21'), (13, 'front-18'), (15, 'front-22'), (17, 'front-2'), (19, 'front-3'), (21, 'front-4'), (23, 'front-6'), (25, 'front-8'), (27, 'front-9'), (29, 'front-11'), (31, 'front-12'), (33, 'front-24'), (35, 'front-10'), (37, 'front-14'), (39, 'front-15'), (41, 'front-16'), (43, 'front-17'), (45, 'front-19'), (47, 'front-20'), (49, 'front-23'), (51, 'front-25'), (53, 'front-26'), (55, 'front-27'), (57, 'front-34'), (59, 'front-29'), (61, 'front-30'), (63, 'front-33'), (65, 'front-28'), (67, 'front-31'), (69, 'front-32'), (71, 'front-35'), (73, 'front-36'), (75, 'front-37'), (77, 'front-38'), (79, 'front-39'), (81, 'front-40'), (83, 'front-41'), (85, 'front-42') ]
    
    backs = [ (4, 'back-1'), (6, 'back-5'), (8, 'back-7'), (10, 'back-13'), (12, 'back-21'), (14, 'back-18'), (16, 'back-22'), (18, 'back-2'), (20, 'back-3'), (22, 'back-4'), (24, 'back-6'), (26, 'back-8'), (28, 'back-9'), (30, 'back-11'), (32, 'back-12'), (34, 'back-24'), (36, 'back-10'), (38, 'back-14'), (40, 'back-15'), (42, 'back-16'), (44, 'back-17'), (46, 'back-19'), (48, 'back-20'), (50, 'back-23'), (52, 'back-25'), (54, 'back-26'), (56, 'back-27'), (58, 'back-34'), (60, 'back-29'), (62, 'back-30'), (64, 'back-33'), (66, 'back-28'), (68, 'back-31'), (70, 'back-32'), (72, 'back-35'), (74, 'back-36'), (76, 'back-37'), (78, 'back-38'), (80, 'back-39'), (82, 'back-40'), (84, 'back-41'), (86, 'back-42') ]

    all_cards = set(f'front-{k}' for k in range(1, 43)).union(set(f'back-{k}' for k in range(1, 43)))
    missing_cards =  all_cards - set([x[1] for x in fronts + backs])
    if len(missing_cards) > 0:
        print('Missing cards ', missing_cards)
        sys.exit(1)

    for (index, old_name) in fronts + backs:
        tmp = old_name.split('-')
        new_name = tmp[1] + '-' + tmp[0]
        os.rename(
            os.path.join(language, str(index) + '.pdf'),
            os.path.join(language, 'pdf', new_name + '.pdf')
        )
    os.remove(os.path.join(language, '87.pdf'))
    os.remove(os.path.join(language, '88.pdf'))
    os.remove(os.path.join(language, '2.pdf'))
    os.remove(os.path.join(language, '1.pdf'))
    # for k in {1..88}; do pdftk cards.pdf cat $k output $k.pdf; done

def export_svg(language):
    print(f'2. Export svg { language }')
    svg_dir = os.path.join(os.path.join(language, 'bad_svg'))
    pdf_dir = os.path.join(language, 'pdf')
    pdf_filenames = [x for x in os.listdir(pdf_dir) if x.endswith('.pdf')]
    if os.path.exists(svg_dir):
        shutil.rmtree(svg_dir)
    os.mkdir(svg_dir)

    def _export_filenames(pdf_filenames, bar):
        for pdf_filename in pdf_filenames:
            command = f'inkscape {os.path.join(pdf_dir, pdf_filename)} --export-filename { os.path.join(svg_dir, pdf_filename[:-4] + ".svg") }'
            subprocess.call(command, shell=True)

            svg_path = os.path.join(svg_dir, pdf_filename[:-4] + ".svg")
            with open(svg_path, 'r') as f:
                content = f.read()
            
            with open(svg_path, 'w') as f:
                f.write(content.replace('ArialMT', 'Arial'))
            bar()


    with alive_bar(len(pdf_filenames)) as bar:   
        nb_files_by_thread = ceil(len(pdf_filenames)/NB_THREADS)
        threads = []
        for k in range(NB_THREADS):
            threads.append(threading.Thread(target=_export_filenames, args=(pdf_filenames[k*nb_files_by_thread: min(len(pdf_filenames), (k+1)*nb_files_by_thread)], bar)))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

def compress_svg(language):
    def _folder_weight(path):
        size = 0
        for ele in os.scandir(path):
            size += os.path.getsize(ele)
        return size

    print('3. Compress svg')
    svg_dir = os.path.join(language, 'bad_svg')
    svg_compressed_dir = os.path.join(os.path.join(language, 'svg'))
    if os.path.exists(svg_compressed_dir):
        shutil.rmtree(svg_compressed_dir)
    os.mkdir(svg_compressed_dir)
    svg_filenames = [x for x in os.listdir(svg_dir) if x.endswith('.svg')]
    
    def _compress_svgs(svg_filenames, bar):
        for svg_filename in svg_filenames:
            bar.text = f'Compress { svg_filename }'
            compressed_svg = compress(os.path.join(svg_dir, svg_filename[:-4] + '.svg'))
            os.rename(compressed_svg, os.path.join(svg_compressed_dir, svg_filename))
            shutil.rmtree(os.path.dirname(compressed_svg))

            bar()

    with alive_bar(len(svg_filenames)) as bar:   
        nb_files_by_thread = ceil(len(svg_filenames)/NB_THREADS)
        threads = []
        for k in range(NB_THREADS):
            threads.append(threading.Thread(target=_compress_svgs, args=(svg_filenames[k*nb_files_by_thread: min(len(svg_filenames), (k+1)*nb_files_by_thread)], bar)))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    original_size = round(_folder_weight(svg_dir)/1000000, 2)
    new_size = round(_folder_weight(svg_compressed_dir)/1000000, 2)
    print(f'\t> { original_size } Mo --> { new_size } Mo')

def export_png(language):
    print('4. Export png')
    pdf_dir = os.path.join(language,'pdf')
    pdf_filenames = [x for x in os.listdir(pdf_dir) if x.endswith('.pdf')]

    default_dir = os.path.join(language, 'default')
    if os.path.exists(default_dir):
        shutil.rmtree(default_dir)
    os.mkdir(default_dir)

      
    def _export_defaults(pdf_filenames, bar):
        for pdf_filename in pdf_filenames:
            bar()
            bar.text = f'Export { pdf_filename }'

            if 'back' in pdf_filename:
                png_bis = os.path.join(default_dir, pdf_filename[:-4] + '-bis.png')
                command = f'convert -density 150 { pdf_dir }/{ pdf_filename } -quality 100 -resize 600 { png_bis }'
                subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
                
                command = f'convert -density 150 { png_bis }  -depth 8 -quality 90  { png_bis }'
                subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

                command = f'pngquant { png_bis } --speed 1 --output { png_bis[:-len("-bis.png")]}.png'
                subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
                os.remove(png_bis)

            else:
                jpg_export = os.path.join(default_dir, pdf_filename[:-4] + '.jpg')
                command = f'convert -density 150 { pdf_dir }/{ pdf_filename } -quality 100 -resize 600 { jpg_export }'
                subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
                
                command = f'jpegoptim --max 75 { jpg_export}'
                subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

    print(f'  4.1 Export back pdf to png / front pdf to jpg')
    with alive_bar(len(pdf_filenames)) as bar:   
        nb_files_by_thread = ceil(len(pdf_filenames)/NB_THREADS)
        threads = []
        for k in range(NB_THREADS):
            threads.append(threading.Thread(target=_export_defaults, args=(pdf_filenames[k*nb_files_by_thread: min(len(pdf_filenames), (k+1)*nb_files_by_thread)], bar)))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
 

    print(f'  4.2 Export png to webpp')
    with alive_bar(len(pdf_filenames)*4) as bar:   
        for size in [125, 250, 450, 600]:
            webd_dir = os.path.join(language, str(size))
            if os.path.exists(webd_dir):
                shutil.rmtree(webd_dir)
            os.mkdir(webd_dir)

            for pdf_filename in pdf_filenames:
                extension = '.png' if 'back' in pdf_filename else '.jpg'
                command = f'convert { os.path.join(default_dir, pdf_filename[:-4] + extension) } -resize { size }x{ size } -quality 90 { os.path.join(webd_dir, pdf_filename[:-4])}.webp'
                subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
                bar()


def extract(pdf_filename, force_ignore=False):
    language = os.path.basename(pdf_filename)[:-4]
    if language not in language_utils.LANGUAGES_DICT.values():
        language = language_utils.LANGUAGES_DICT[language]

    output_dir = os.path.join('public', 'cards', language)
    if os.path.exists(output_dir):
        print(f'output_dir already exists.')
        if force_ignore: return
        x = input('Continue ? (yes/no):   ')
        if x != 'yes':
            print('Skip')
            return
        
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    
    split_pdf(output_dir, pdf_filename)
    export_svg(output_dir)
    compress_svg(output_dir)

    export_png(output_dir)

    shutil.rmtree(os.path.join(output_dir, 'pdf'))
    shutil.rmtree(os.path.join(output_dir, 'bad_svg'))


if __name__ == '__main__':

    if os.path.isdir(sys.argv[1]):
        pdfs = [x for x in os.listdir(sys.argv[1]) if x.endswith('.pdf')]
        print('Extract { } pdfs')
        k = 0
        for pdf in pdfs:
            print(f'{ k } / { len(pdfs) } done. Current: { pdf }')
            extract(os.path.join(sys.argv[1], pdf))
            k += 1
    else:
        pdf_filename = sys.argv[1]
        
        extract(pdf_filename)