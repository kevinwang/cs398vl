from __future__ import division
from nltk.corpus import PlaintextCorpusReader
import enchant
from collections import defaultdict
import operator
import matplotlib.pyplot as plt
import csv
import json
from colorsys import hsv_to_rgb

reader = PlaintextCorpusReader('', '.*\.txt')
d = enchant.Dict('en_GB')
titles = {
        'finnegans_wake.txt': 'Finnegans Wake',
        'ulysses.txt': 'Ulysses',
        'ofk.txt': 'The Once and Future King'
        }

def get_words(filename):
    return [w.lower() for w in reader.words(filename) if w.isalpha()]

def percent_english(filename):
    words = [w for w in reader.words(filename) if w.isalpha()]
    return sum(d.check(word) for word in words) / len(words)

def num_unique_words(words):
    return len(set(words))

def longest_words(words, limit=10):
    return sorted(set(words), key=len, reverse=True)[:limit]

def lexical_novelty(words):
    word_set = set()
    novelty_distribution = []
    num_new = 0
    for i, word in enumerate(words):
        if word not in word_set:
            word_set.add(word)
            num_new += 1
        if i != 0 and i % 1000 == 0:
            novelty_distribution.append(num_new / 1000)
            num_new = 0
    return novelty_distribution

def print_info(filename):
    print filename
    print '-' * len(filename)

    words = get_words(filename)
    print 'Word count: %d' % len(words)
    print 'Unique words: %d' % num_unique_words(words)
    print 'Percent English: %.2f%%' % (percent_english(filename) * 100)

    sents = reader.sents(filename)
    print 'Average sentence length: %.2f words' % (sum(len(sent) for sent in sents) / len(sents))

    print 'Longest words'
    for i, word in enumerate(longest_words(words)):
        print str(i + 1) + '\t' + word

    print 'Lexical novelty'
    novelty = lexical_novelty(words)
    #plt.plot(novelty)
    #plt.ylabel('Novelty')
    #plt.ylim(0, 1)
    #plt.show()
    print novelty

def write_word_counts(outfile):
    with open(outfile, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')
        writer.writerow(['Title', 'Total words', 'Unique words'])
        for filename in ['finnegans_wake.txt', 'ulysses.txt', 'ofk.txt']:
            words = get_words(filename)
            writer.writerow([titles[filename], len(words), num_unique_words(words)])

def write_english_percentages(outfile):
    out_data = []
    for filename in ['finnegans_wake.txt', 'ulysses.txt', 'ofk.txt']:
        english_percentage = percent_english(filename)
        out_data.append({
            'title': titles[filename],
            'sects': [
                {'name': 'English', 'percent': english_percentage},
                {'name': 'Non-English', 'percent': 1 - english_percentage}
                ]
            })
    with open(outfile, 'w') as file:
        json.dump(out_data, file, sort_keys=True, indent=4, ensure_ascii=False)

def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

def generate_novelty_heatmaps(outfile):
    with open(outfile, 'w') as file:
        max_novelties = []
        novelties = {}
        for filename in ['finnegans_wake.txt', 'ulysses.txt', 'ofk.txt']:
            words = get_words(filename)
            novelty = lexical_novelty(words)
            max_novelties.append(max(novelty))
            novelties[filename] = novelty

        max_novelty = max(max_novelties)
        for filename in ['finnegans_wake.txt', 'ulysses.txt', 'ofk.txt']:
            file.write('<h3>' + titles[filename] + '</h3>\n')
            file.write('<div class="sent" style="padding-bottom:40px">\n')
            for chunk in novelties[filename]:
                chunk_normalized = chunk / max_novelty
                color = rgb_to_hex(hsv_to_rgb((1 - chunk_normalized) / 3, 1, 255))
                file.write('  <div class="sentbar" style="height:40px;background:%s;width:4px;float:left;" title="%.1f%%"></div>\n' % (color, chunk * 100))
            file.write('</div>\n')

#write_word_counts('data/wc.csv')
#write_english_percentages('data/english.json')
generate_novelty_heatmaps('data/novelty.html')

#print_info('finnegans_wake.txt')
#print
#print_info('ulysses.txt')
#print
#print_info('ofk.txt')
