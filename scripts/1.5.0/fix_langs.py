# Small script to fix the list of langs

import os
import json

cards = 'public/cards'
i18n = 'src/i18n'

cards_langs = set(os.listdir(cards))
i18n_langs = set(os.listdir(i18n))

new_langs = i18n_langs - cards_langs

print('Missing cards', new_langs)
print('Missing i18n', cards_langs - i18n_langs)

json_d = json.load(open('src/data/langs.json'))
json_langs = set(x['code'] for x in json_d)

print('In json but not in cards ', json_langs - cards_langs )
print('In cards but not in json ', cards_langs - json_langs )