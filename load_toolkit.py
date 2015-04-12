import csv
import json
import requests


def load_treasure_csv(filepath='data/treasure.csv'):
    data_object = []
    with open(filepath, 'r') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in content:
            data_object.append(row)

    return data_object


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


def generate_existing_keyword_set(data_object):
    keyword_set = set()
    for i in range(1, len(data_object)):
        if ';' in data_object[i][6]:
            keywords = data_object[i][6].split(';')
            for word in keywords:
                keyword_set.add(word)

    return keyword_set


for data_set in keyword_relations:
    if len(data_set['keyword_relations']) > 0:
        for relationship in data_set['keyword_relations']:
            print '{} is related to {} by keyword: {}'.format(data_set['title'],
                                                              relationship.values()[0],
                                                              relationship.keys()[0])


def filter_keyword_set(keyword_set):
    keyword_array = []

    for word in keyword_set.copy():
        if len(word) < 4:
            keyword_set.remove(word)

    for word in keyword_set:
        keyword_array.append(word.lower())

    return keyword_array


def write_existing_keywords_json(keyword_array):
    with open('data/existing_keywords.json', 'w') as jsonfile:
        jsonfile.write(json.dumps(keyword_array,
                                  sort_keys=True,
                                  indent=4,
                                  separators=(',', ': ')))


data_object = load_treasure_csv()
keyword_set = generate_existing_keyword_set(data_object)
keyword_array = filter_keyword_set(keyword_set)
keyword_array.sort()
write_existing_keywords_json(keyword_array)

print '*---*\nCreated existing_keywords.json with {} keywords.\n*---*'.format(len(keyword_array))
