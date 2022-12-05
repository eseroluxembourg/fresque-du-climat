from bs4 import BeautifulSoup
import urllib
import urllib.request
import pickle
import language_utils
import os
import shutil
import json
import lxml
from alive_progress import alive_bar

DOWNLOAD_FOLDER = 'download'
ORDER_THE_CARDS_URL = 'https://climatefresk.org/orderthecards/'

PDF_FOLDERS = 'cards-pdfs'

def download_pdf(pdf_url):
    pdf_filename = pdf_url.split('/')[-1]
    path = os.path.join(DOWNLOAD_FOLDER, pdf_filename)
    if os.path.exists(path): return path
    urllib.request.urlretrieve(pdf_url, path)
    return path

def parse_order_the_cards():
    def _parse_pdf_info(label, url):
        label = label.strip()
        mode = ''
        if label.startswith('Adult') or label.startswith('Jeu adulte'):
            mode = 'adult'
        elif  label.startswith('Kid') or label.startswith('Jeu enfant'):
            mode = 'kid'
        elif label.startswith('Expert'):
            mode = 'expert'
        else:
            print(f'Unknown mode for { label }')

        version = label.split(' ')[-1]
        version = version if '.' in version else ''

        return {
            'label': label,
            'mode': mode,
            'print': 'ready to print' in label or 'imprimable' in label,
            'version': version,
            'mini': 'mini' in label,
            'url': url
        }

    def _parse_language_code(url):
        
        splitted = url.split('/')[-1].split('-')
        
        for k in range(len(splitted)-1):
            if (len(splitted[k]) >= 2 or len(splitted[k]) <= 4) and (len(splitted[k + 1]) >= 2 or len(splitted[k + 1]) <= 4):
                candidate = splitted[k] + '-' + splitted[k + 1]
                if candidate in language_utils.LANGUAGES_DICT.keys():
                    return language_utils.LANGUAGES_DICT[candidate]
                    
        for k in range(len(splitted)-1):
            candidate = splitted[k]
            if candidate in language_utils.LANGUAGES_DICT.keys():
                return language_utils.LANGUAGES_DICT[candidate]
        return None


    page = urllib.request.urlopen(ORDER_THE_CARDS_URL)
    soup = BeautifulSoup(page, 'lxml')

    accordion_items = soup.find_all(class_='elementor-accordion-item')

    pdf_urls = {}
    for item in accordion_items:
        lang = item.find('a', class_='elementor-accordion-title')
        lang = lang.text.split('|')[0].strip()
        hrefs = [x for x in item.find_all('a') if x['href'].endswith('.pdf')]
        if len(hrefs) == 0:
            continue

        pdfs= []
        all_pdfs_i18n_code = None
        for href in hrefs:
            url = href['href']
            i18n_code = _parse_language_code(url)
            if not i18n_code:
                print('Unable to decode language code for url: ', url)
            elif all_pdfs_i18n_code and all_pdfs_i18n_code != i18n_code:
                print(f'{ i18n_code } found instead of previously found { all_pdfs_i18n_code }')
                print(lang)
                print(hrefs)
            
            all_pdfs_i18n_code = i18n_code
            label = href.text
            pdfs.append(_parse_pdf_info(label, url))

        if all_pdfs_i18n_code is None:
            print('Unable to decode languge code for lang: ', lang)
            continue

        pdf_urls[all_pdfs_i18n_code] = {
            'lang_label': lang,
            'pdfs': pdfs 
        }
    return pdf_urls

def download_all_pdfs():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)

    if not os.path.exists(PDF_FOLDERS):
        os.mkdir(PDF_FOLDERS)
    pdf_urls = parse_order_the_cards()
    
    f = open('pdf_urls.pkl', 'wb')
    pickle.dump(pdf_urls, f)

    pdf_urls = pickle.load(open('pdf_urls.pkl', 'rb'))

    for lang, values in pdf_urls.items():
        lang_label = values['lang_label']
        pdfs = values['pdfs']
        print(f'Lang { lang } - { lang }:')
        for pdf in pdfs:
            if pdf['mode'] != 'adult' or  pdf['print'] or pdf['mini']:
                continue
            pdf_path = download_pdf(pdf["url"])
            shutil.copy(pdf_path, os.path.join(PDF_FOLDERS, lang + '.pdf'))
            with open (os.path.join(PDF_FOLDERS, lang + '.json'), 'w') as f:
                json.dump({
                    'mode': pdf['mode'],
                    'lang': lang,
                    'lang_label': lang_label,
                    'print': pdf['print'],
                    'url': pdf['url'],
                    'mini': pdf['mini'],
                    'version': pdf['version']
                }, f)

            
            print(f'\t { pdf["version"] } - { pdf["url"] }')

    return PDF_FOLDERS

if __name__ == '__main__':
    download_all_pdfs()

    # print(f'Found pdfs on { ORDER_THE_CARDS_URL }')
    # print(pdf_urls)

    