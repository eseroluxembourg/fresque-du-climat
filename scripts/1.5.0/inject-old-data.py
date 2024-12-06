
import json

# links = 'db-data/links-fr.json'
# links = json.load(open(links, 'r'))
# print(links)

# f = open('src/i18n/fr-FR/links.json')
# new_links = json.load(f)
# f.close()
# print(new_links)

# for link in links:
#     key = str(link['fromNum']) + '_' + str(link['toNum'])
#     if link['explanation'] == '':
#         continue

#     if key not in new_links.keys():
#         print(link)
#     else:
#         old_explanation = new_links[key]['explanation']

#         if old_explanation == link['explanation']:
#             print('Already same')
#             continue

#         print('--------------------')
#         print('1. Database (db)')
#         print(old_explanation)
#         print('2. Memo')
#         print(link['explanation'])
#         x = input('Choose ? (db / memo)')
#         if x != 'db':
#             new_links[key]['explanation'] = link['explanation']

# with open('src/i18n/fr-FR/links.json', 'w') as f:
#     json.dump(new_links, f, ensure_ascii=False, indent=4)
#     # key = link[]

cards = 'db-data/cards-en.json'
cards = json.load(open(cards, 'r'))
print(cards)

f = open('src/i18n/en-GB/cards.json')
new_cards = json.load(f)
f.close()
print(new_cards)

for card in cards:
    key = str(card['cardNum'])

    if 'wikiUrl' not in new_cards[key].keys():
        new_cards[key]['wikiUrl'] = card['wikiUrl']
    if 'wikiId' not in new_cards[key].keys():
        new_cards[key]['wikiId'] = card['wikiId']
    if 'wikiInternalName' not in new_cards[key].keys():
        new_cards[key]['wikiInternalName'] = card['wikiInternalName']
    if 'videoYoutubeCode' not in new_cards[key].keys():
        new_cards[key]['videoYoutubeCode'] = card['videoYoutubeCode']
    if 'instagramCode' not in new_cards[key].keys():
        new_cards[key]['instagramCode'] = card['instagramCode']

    if card['explanation'] == '':
        continue

    if key not in new_cards.keys():
        print(card)
    else:
        old_explanation = new_cards[key]['explanation']

        if old_explanation == card['explanation']:
            print('Already same')
            continue

        print('--------------------')
        print('1. Database (db)')
        print(old_explanation)
        print('2. Memo')
        print(card['explanation'])
        x = input('Choose ? (db / memo)')
        if x != 'db':
            new_cards[key]['explanation'] = card['explanation']

with open('src/i18n/en-GB/cards.json', 'w') as f:
    json.dump(new_cards, f, ensure_ascii=False, indent=4)
    # key = card[]