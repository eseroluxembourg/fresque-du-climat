import json
import os
import sys


sets = json.load(open('data/cards/cards.json', 'r'))
card_sets = {}
for card in sets:
    card_sets[card['cardNum']] = card['cardSet']

links = json.load(open('data/cards/links.json', 'r'))
links_status = {}
for link in links:
    links_status[(int(link['fromNum']), int(link['toNum']))] = link['status']

langs = json.load(open('data/i18n/langs.json', 'r'))
for lang in langs:
    break
    filename = f'src/i18n/{lang["code"]}/cards.json'
    with open(filename, 'r') as f:
        cards = json.load(f)


    for card_num, card in cards.items():
        folder = f'data/i18n/cards/{card_num}'
        if not os.path.exists(folder):
            os.mkdir(folder)
        card_num = int(card_num)
        card_filename = f'data/i18n/cards/{card_num}/{lang["code"]}.md'

        with open(card_filename, 'w') as f:
            f.write('---\n')
            f.write(f'title: "{ card["title"] }"\n')
            f.write(f'backDescription: "{ card["backDescription"] }"\n')
            if "wikiUrl" in card:
                f.write(f'wikiUrl: "https://fresqueduclimat.org/{ card["wikiUrl"] }"\n')
            if "videoYoutubeCode" in card:
                f.write(f'youtubeCode: "{ card["videoYoutubeCode"] }"\n')
            if "instagramCode" in card:
                f.write(f'instagramCode: "{ card["instagramCode"] }"\n')
            f.write(f'set: { card_sets[card_num] }\n')
            f.write(f'cardNum: { card_num }\n')
            # f.write(f'version: { "todo" }\n')
            f.write('---\n')
            f.write(f'{ card["explanation"] }\n')

for lang in langs:
    filename = f'src/i18n/{lang["code"]}/links.json'
    with open(filename, 'r') as f:
        links = json.load(f)


    for link_id, link in links.items():

        folder = f'data/i18n/links/{link_id}'
        if not os.path.exists(folder):
            os.mkdir(folder)
        card_filename = f'data/i18n/links/{link_id}/{lang["code"]}.md'
        from_num, to_num = [int(x) for x in link_id.split('_')]
        if (from_num, to_num) not in links_status:
            print(f'Warning: link {from_num}, {to_num} is not in links.json (see { link })')
            continue
        with open(card_filename, 'w') as f:
            f.write('---\n')

            f.write(f'linkId: "{ link_id }"\n')
            f.write(f'fromCardId: { from_num }\n')
            f.write(f'toCardId: { to_num }\n')
            f.write(f'status: { links_status[(from_num, to_num)] }\n')
            f.write('---\n')

            f.write(f'{ link["explanation"] }\n')