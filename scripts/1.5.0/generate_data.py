import os
import sys
import csv
from typing import List
import json
import shutil
import language_utils

LANGUAGES_FILE = 'Languages.csv'
CARDS_RELATIONS = 'Relations Documentation_memo.csv'
CARDS_BACK_FILE = 'Cards - Documentation_memo.csv'




class Language:
    internal_id: int
    i18n_id: str
    language_fr: str
    language_en: str
    language_ln: str
    fresk_translation: str
    website_url: str
    cards_mode: str
    cards_print: bool
    cards_url: str
    cards_mini: bool
    cards_version: str

    def __init__(self, line=None, i18n=None):
        if line is not None:
            line = line.strip().split(';')
            line = [x.replace('"', '') for x in line]
            self.internal_id = int(line[0])
            self.i18n_id = line[1]
            self.language_fr = line[2]
            self.language_en = line[3]
            self.language_ln = line[4]
            self.fresk_translation = line[5]
            self.website_url = line[6]

        else:
            self.internal_id = -1
            self.i18n_id = i18n
            self.language_fr = ''
            self.language_en = ''
            self.language_ln = ''
            self.fresk_translation = ''
            self.website_url = ''
        self.cards_mode = ''
        self.cards_print = False
        self.cards_url= ''
        self.cards_mini = False
        self.cards_version = ''

    def __str__(self):
        return f'Language { self.correct_i18n }'

    @property
    def correct_i18n(self):
        if self.i18n_id not in language_utils.LANGUAGES_DICT.values():
            return language_utils.LANGUAGES_DICT[self.i18n_id]
        return self.i18n_id


    @staticmethod
    def load_from_file(texts_directory) -> List:
        languages_filename = os.path.join(texts_directory, LANGUAGES_FILE)
        f = open(languages_filename, 'r')
        lines = f.readlines()
        f.close()
        if lines[0].strip() != '"ID";"Code";"Language (FR)";"Language (EN)";"Language (LN)";"Title (LN)";"Web Site"':
            print(f'Error reading languages file { languages_filename } (first line changed)')
            sys.exit(1)
        languages = [Language(line) for line in lines[1:] if line.strip() != '']
        return languages

    @staticmethod
    def language(languages: List, language_id):
        for language in languages:
            if language_id == language.internal_id:
                return language
        return None

    def to_object(self):
        return {
            'code': self.correct_i18n,
            'language_fr': self.language_fr,
            'language_en': self.language_en,
            'language_local': self.language_ln,
            'fresk_translation': self.fresk_translation,
            'website_url': self.website_url,
        }


class Card:

    i18n_language: str
    card_num: int
    cardSet: int
    title: str
    wikiId: id
    wikiInternalName: str
    wikiUrl: str
    back_description: str
    explanation: str
    instagramCode: str
    videoYoutubeCode: str
    documentation: str

    def __init__(self, i18n_language, card_num, title, back_description, explanation):
        self.i18n_language = i18n_language
        self.card_num = card_num
        self.title = title
        self.back_description = back_description
        self.explanation = explanation
        
    @property
    def correct_i18n(self):
        if self.i18n_language not in language_utils.LANGUAGES_DICT.values():
            return language_utils.LANGUAGES_DICT[self.i18n_language]
        return self.i18n_language


    def to_object(self):
        return {
            'title': self.title,
            'backDescription': self.back_description,
            'explanation': self.explanation
        }

    @staticmethod
    def load_from_file(languages, texts_directory):
        cards = []
        with open(os.path.join(texts_directory, CARDS_BACK_FILE), newline='') as csvfile:
            description_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            header = next(description_reader)
            if header != 'Language ID;Code;Card ID;Title;Back text;Documentation text'.split(';'):
                print('Pas content !')

            for row in description_reader:
                cards.append(Card(
                    i18n_language = row[1],
                    card_num= int(row[2]),
                    title=row[3],
                    back_description=row[4],
                    explanation=row[5]
                ))
        return cards

    @staticmethod
    def cards_by_language(cards):
        result = dict()

        for card in cards:
            if card.correct_i18n not in result.keys():
                result[card.correct_i18n] = []
            result[card.correct_i18n].append(card)

        return result

    @staticmethod
    def cards_by_card_num(cards):
        result = dict()

        for card in cards:
            if card.card_num not in result.keys():
                result[card.card_num] = []
            result[card.card_num].append(card)

        return result

    
class Link:
    i18n_language: str
    from_num: int
    to_num: int
    explanation: str

    def __init__(self, i18n_language, from_num, to_num, explanation):
        self.i18n_language = i18n_language
        self.from_num = from_num
        self.to_num = to_num
        self.explanation = explanation

    @property
    def correct_i18n(self):
        if self.i18n_language not in language_utils.LANGUAGES_DICT.values():
            return language_utils.LANGUAGES_DICT[self.i18n_language]
        return self.i18n_language

    @property
    def link_id(self):
        return str(self.from_num) + '_' + str(self.to_num)

    def to_object(self):
        return {
            'explanation': self.explanation
        }

    @staticmethod
    def load_from_file(texts_directory):
        links = []
        with open(os.path.join(texts_directory, CARDS_RELATIONS), newline='') as csvfile:
            description_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            header = next(description_reader)
            if header != '"Language ID";"Code";"Cause ID";"Cause";"Consequence ID";"Consequence";"Translation"'.split(';'):
                print('Pas content !')

            for row in description_reader:
                links.append(Link(
                    i18n_language = row[1],
                    from_num= int(row[2]),
                    to_num=int(row[4]),
                    explanation=row[6]
                ))
        return links

    @staticmethod
    def links_by_language(links):
        result = dict()

        for link in links:
            if link.correct_i18n not in result.keys():
                result[link.correct_i18n] = []
            result[link.correct_i18n].append(link)

        return result

def init_local_directories():
    def _clean_local_dir(path, recreate=True):
        if os.path.isdir(path):
            print(f'\t> { os.path.basename(path) }')
            if os.path.exists(path):
                shutil.rmtree(path)
            if recreate:
                os.mkdir(path)
        else:
            if os.path.exists(path):
                os.remove(path)

    print('Clean local directories...')
    _clean_local_dir(os.path.join('src', 'i18n'))
    _clean_local_dir(os.path.join('src', 'data', 'langs.json'))
    

        
def generate_data(cards_directory, texts_directory, pdf_cards_info):    

    print(f'Updating data from { cards_directory } (cards) and { texts_directory } (texts)')

    init_local_directories()

    languages = Language.load_from_file(texts_directory)
    print(f'Languages loaded: { ", ".join([x.correct_i18n for x in languages ])}')
    
    print('Loading cards...')
    cards = Card.load_from_file(languages, texts_directory)
    cards_by_language = Card.cards_by_language(cards)

    print('Loading links...')
    links = Link.load_from_file(texts_directory)
    links_by_language = Link.links_by_language(links)

    all_languages = set(links_by_language.keys()).union(cards_by_language.keys()).union(pdf_cards_info.keys())
    missing_languages = all_languages - set([x.correct_i18n for x in languages])
    if len(missing_languages) > 0:
        print('Error, missing languages', missing_languages)
        for missing_language in missing_languages:
            languages.append(Language(i18n=missing_language))

    for k in range(len(languages)):
        print(languages[k].to_object())
        if languages[k].correct_i18n not in pdf_cards_info.keys():
            continue
        
        infos = pdf_cards_info[languages[k].correct_i18n]
        languages[k].cards_version = infos['version']
        languages[k].cards_mini = infos['mini']
        languages[k].cards_mode = infos['mode']
        languages[k].cards_print = infos['print']
        languages[k].cards_url = infos['url']
        languages[k].language_ln = infos['lang_label']

    langs_path = os.path.join('src', 'data', 'langs.json')
    print(f'\t> Dump { langs_path }')
    with open(langs_path, 'w') as f:
        results = []
        for language in languages:
            results.append(language.to_object())
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    for language_obj in languages:
        language = language_obj.correct_i18n
        path = os.path.join('src', 'i18n', language)
        if not os.path.exists(path):
            os.mkdir(os.path.join(path))

        print(f'\t> Dump cards: { language }')
        infos = {}
        if language in pdf_cards_info.keys():
            infos = {
                'mode': pdf_cards_info[language]['mode'],
                'print': pdf_cards_info[language]['print'],
                'url': pdf_cards_info[language]['url'],
                'mini': pdf_cards_info[language]['mini'],
                'version': pdf_cards_info[language]['version'],
            }
        with open(os.path.join(path, 'local.json'), 'w') as f:
            json.dump(infos, f, ensure_ascii=False, indent=4)

        if not os.path.exists(os.path.join(path, 'main.json')):
            with open(os.path.join(path, 'main.json'), 'w') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)


        print(f'\t> Dump cards: { language }')
        if language in cards_by_language.keys():
            result = {
                card.card_num: card.to_object() for card in cards_by_language[language]
            }
        else:
            print(f'\t No cards data found for: { language } ')
            result={}
        json.dump(result, 
            open(os.path.join(path, 'cards.json'), 'w'),
            ensure_ascii=False, indent=4)

        print(f'\t> Dump links: { language }')
        if language in links_by_language.keys():
            result = {
                link.link_id: link.to_object() for link in links_by_language[language]
            }
        else:
            print(f'\t No links data found for: { language } ')
            result = {}

        json.dump(result, 
            open(os.path.join(path, 'links.json'), 'w'),
            ensure_ascii=False, indent=4)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 main.py <cards_directory> <texts_directory>')
        sys.exit(1)
    
    cards_directory = sys.argv[1]
    texts_directory = sys.argv[2]
    generate_data(cards_directory, texts_directory)
    