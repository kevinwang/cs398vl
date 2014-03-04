from nltk.corpus import PlaintextCorpusReader
import json
import csv

wordlists = PlaintextCorpusReader('', '../corpora/ofk.txt')

words = set(wordlists.words('../corpora/ofk.txt'))

towns = {}
counties = {}
countries = set()
with open('../corpora/Towns_List.csv') as csvfile:
    townreader = csv.reader(csvfile)
    for row in townreader:
        towns[row[0]] = row[1]
        counties[row[1]] = row[2]
        countries.add(row[2])

with open('../corpora/countries.txt') as countries_list:
    for country in countries_list:
        countries.add(country.rstrip())

# Patch up some holes
del towns['Battle']
del towns['Street']
del towns['Ware']
del towns['Derby']
del towns['Stone']
countries.remove('Guinea')
towns['London'] = 'Greater London'
towns['Stonehenge'] = 'Wiltshire'
counties['Camelot'] = 'England'
counties['Siberia'] = 'Russia'
counties['Paris'] = 'France'
countries.add('Indies')
countries.add('Flanders')

out_data = {'name': 'The World', 'children': []}

ofk_towns = set()
ofk_counties = set()
ofk_countries = set()

for w in words:
    if w in towns:
        ofk_towns.add(w)
        ofk_counties.add(towns[w])
        ofk_countries.add(counties[towns[w]])
    elif w in counties:
        ofk_counties.add(w)
        ofk_countries.add(counties[w])
    elif w in countries:
        ofk_countries.add(w)

# Add "America" because "American" shows up twice which is interesting
ofk_countries.add('America')

# Confound this infernal JSON structure!
for c in ofk_countries:
    out_data['children'].append({'name': c})

for c in ofk_counties:
    country_index = next(index for (index, d) in enumerate(out_data['children']) if d['name'] == counties[c])
    if 'children' not in out_data['children'][country_index]:
        out_data['children'][country_index]['children'] = []
    out_data['children'][country_index]['children'].append({'name': c})

for c in ofk_towns:
    country_index = next(index for (index, d) in enumerate(out_data['children']) if d['name'] == counties[towns[c]])
    county_index = next(index for (index, d) in enumerate(out_data['children'][country_index]['children']) if d['name'] == towns[c])
    if 'children' not in out_data['children'][country_index]['children'][county_index]:
        out_data['children'][country_index]['children'][county_index]['children'] = []
    out_data['children'][country_index]['children'][county_index]['children'].append({'name': c})

with open('data/data.json','w') as outfile:
     json.dump(out_data, outfile, sort_keys=True, indent=4, ensure_ascii=False)
