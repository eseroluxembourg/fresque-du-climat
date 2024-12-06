
from download_pdf_cards import download_all_pdfs
from generate_cards_from_pdf import extract
from generate_data import generate_data

import os
import json

if __name__ == '__main__':
    
    print('------------------------')
    print('| 1. Download all pdfs |')
    print('------------------------')
    pdfs_folder = download_all_pdfs()

    all_langs = set()
    
    print('-------------------------------')
    print('| 2. Generate cards from pdfs |')
    print('-------------------------------')
    pdfs = [x for x in os.listdir(pdfs_folder) if x.endswith('.pdf')]
    print('Extract { } pdfs')
    k = 0
    for pdf in pdfs:
        lang = pdf[:-4]
        all_langs.add(lang)
        print(f'{ k } / { len(pdfs) } done. Current: { pdf }')
        extract(os.path.join(pdfs_folder, pdf), force_ignore=True)
        k += 1

    pdf_cards_info = {}
    cards_files = [x for x in os.listdir(pdfs_folder) if x.endswith('.json')]
    for card_file in cards_files:
        data = json.load(open(os.path.join(pdfs_folder, card_file), 'r'))
        pdf_cards_info[card_file[:-5]] = data

    print('------------------------------------')
    print('| 3. Generate i18n files from pdfs |')
    print('------------------------------------')

    generate_data(os.path.join('db-data', 'Cards'), os.path.join('db-data', 'Texts'), pdf_cards_info)