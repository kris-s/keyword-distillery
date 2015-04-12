import csv
import json
import requests

data_object = []
keyword_relations = []


def load_treasure_csv(filepath='data/treasure.csv'):
    with open(filepath, 'r') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in content:
            data_object.append(row)

def generate_treasure_hunt_json():
    json_skeleton = {}
    for i in range(1, len(data_object)):
        try:
            content = requests.get(data_object[i][9]).json()
            json_skeleton = {data_object[i][5]: content}
        except:
            print 'Item number {} request failed.'.format(i)

    with open('data/treasure.json', 'w') as jsonfile:
        jsonfile.write(json.dumps(json_skeleton,
                                  sort_keys=True,
                                  indent=4,
                                  separators=(',', ': ')))

def generate_existing_keyword_set():
    keyword_set = set()
    for i in range(1, len(data_object)):
        relation = {'title': data_object[i][5],
                    'keyword_relations': []}

        keywords_i = data_object[i][6]
        for j in range(1, len(data_object)):
            if i != j and data_object[i][5] != data_object[j][5]:
                keywords_j = data_object[j][6]
                if ';' in keywords_i and ';' in keywords_j:
                    keywords_i = keywords_i.split(';')
                    keywords_j = keywords_j.split(';')
                    for word in keywords_i:
                        if word in keywords_j:
                            r = {word: data_object[j][5]}
                            relation['keyword_relations'].append(r)
                            keyword_set.add(word)

        keyword_relations.append(relation)

for data_set in keyword_relations:
    if len(data_set['keyword_relations']) > 0:
        for relationship in data_set['keyword_relations']:
            print '{} is related to {} by keyword: {}'.format(data_set['title'],
                                                              relationship.values()[0],
                                                              relationship.keys()[0])

print 'done!'