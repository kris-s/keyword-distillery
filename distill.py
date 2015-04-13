import sys
import json
import requests
from bs4 import BeautifulSoup


def distillery_manager(mode=None):
    if mode == 'weigh':
        print 'Generating keyword weights.'
        keyword_list = load_keyword_list()
        generate_keyword_weights(keyword_list)

    elif mode == 'filter':
        generate_keyword_relationship_map()
        filter_non_related_keywords()

    elif mode == 'test':
        filter_non_related_keywords()

def load_keyword_list(filepath='data/keywords.json'):
    with open(filepath, 'r') as jsonfile:
        keyword_list = json.load(jsonfile)
    return keyword_list


def load_dataset(filepath='data/data.json'):
    with open(filepath, 'r') as jsonfile:
        dataset = json.load(jsonfile)
    return dataset


def generate_master_file_skeleton(keyword_list):
    master_skeleton = []
    for keyword in keyword_list:
        master_skeleton.append({'keyword': keyword['keyword'],
                                'weight': keyword['weight'],
                                'related_data': []})
    return master_skeleton


def generate_keyword_density(dataset, keyword):
    word_count = 0.0
    try:
        keyword = keyword.replace('+', ' ')
        word_count = float(dataset.count(keyword))
    except:
        print 'Error generating density.'
    return word_count


def generate_keyword_weights(keyword_list):
    """
    Word weight is the inverse of the number of articles returned by Bing.
    I tried Google Scholar initially but Google doesn't allow search crawling.

    Weighting the words in this way allows finer refinement of keyword relations,
    If an uncommon word appears frequently in two data sets, those data sets are
    more strongly related than if a common word appeared with the same frequency.

    This will take time to complete, 475 keyword terms took roughly three minutes.

    :param array of keywords:
    :return array of dictionaries:
    """
    bing_url_root = 'http://www.bing.com/search?q='
    weighted_keyword_list = []

    for keyword in keyword_list:
        try:
            keyword = keyword.replace(' ', '+')
            bing_result = requests.get(bing_url_root + keyword)
            soup = BeautifulSoup(bing_result.content)
            results_count = soup.find('div', id='b_tween')
            weight = str(results_count)
            weight = weight[(weight.find("\"sb_count\""))+11:weight.find(" results")]
            weight = weight.replace(',', '')
            weight = 1.0 / float(weight)
            weight_object = {'keyword': keyword,
                             'weight': weight}
            weighted_keyword_list.append(weight_object)
            print '{}: {}'.format(keyword, weight)
        except:
            print 'Error creating weight.'

    weighted_keyword_list = sorted(weighted_keyword_list,
                                   key=lambda k: k['weight'],
                                   reverse=True)

    with open('data/weighted_keywords.json', 'w') as jsonfile:
        jsonfile.write(json.dumps(weighted_keyword_list,
                                  sort_keys=True,
                                  indent=4,
                                  separators=(',', ': ')))

    return weighted_keyword_list


def update_master_relationship_map(density, meta_data, keyword, keyword_relation_map):
    meta_data['relation_weight'] = density

    for data in keyword_relation_map:
        if data['keyword'] == keyword:
            data['related_data'].append(meta_data)


def generate_keyword_relationship_map():
    weighted_keyword_list = load_keyword_list(filepath='data/weighted_keywords.json')
    comparison_dataset = load_dataset()
    comparison_dataset_length = len(comparison_dataset['dataset'])
    keyword_relation_map = generate_master_file_skeleton(weighted_keyword_list)
    count = 1

    for data_chunk in comparison_dataset['dataset']:
        print 'Scanning chunk {} of {}.'.format(count, comparison_dataset_length)
        meta_data = {'id': data_chunk['identifier'][data_chunk['identifier'].find('/views/')+7:],
                     'title': data_chunk['title'],
                     'relation_weight': None}

        for urls in data_chunk['distribution']:
            if urls['mediaType'] == u'application/json':
                target_url = urls['downloadURL']
                if 'https' in target_url:
                    target_url = target_url.replace('https', 'http')

        target_data = requests.get(target_url)

        for keyword in weighted_keyword_list:
            relationship_chunk = {'keyword': keyword['keyword'],
                                  'related_data': []}
            density = generate_keyword_density(target_data.content, keyword['keyword'])
            if density > 0.0:
                density /= len(target_data.content)
                update_master_relationship_map(density,
                                               meta_data,
                                               keyword['keyword'],
                                               keyword_relation_map)
        count += 1

    with open('data/keyword_relationship_map.json', 'w') as jsonfile:
            jsonfile.write(json.dumps(keyword_relation_map,
                                      sort_keys=True,
                                      indent=4,
                                      separators=(',', ': ')))

def filter_non_related_keywords():
    unfiltered = load_dataset(filepath='data/filtered_keyword_relationship_map_hawaii.json')
    filtered = []
    for keyword in unfiltered:
        if (len(keyword['related_data']) > 0):
            for dataset in keyword['related_data']:
                dataset['relation_score'] = keyword['weight'] * dataset['relation_weight']
            filtered.append(keyword)

    for keyword in filtered:
        keyword['related_data'] = sorted(keyword['related_data'],
                                         key=lambda k: k['relation_score'],
                                         reverse=True)

    with open('data/filtered_keyword_relationship_map.json', 'w') as jsonfile:
            jsonfile.write(json.dumps(filtered,
                                      sort_keys=True,
                                      indent=4,
                                      separators=(',', ': ')))

if len(sys.argv) != 2:
    print '\nCommands:'
    print '  weigh: python distill.py weigh'
    print ' filter: python distill.py filter\n'
    exit()

if sys.argv[1] == 'weigh':
    distillery_manager(mode='weigh')

elif sys.argv[1] == 'filter':
    distillery_manager(mode='filter')

elif sys.argv[1] == 'test':
    distillery_manager(mode='test')

else:
    print '\nCommands:'
    print '  weigh: python distill.py weigh'
    print ' filter: python distill.py filter\n'
    exit()
