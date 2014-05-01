from __future__ import division
from nltk.corpus import PlaintextCorpusReader
import enchant
from collections import defaultdict
import operator
import matplotlib.pyplot as plt
import csv

reader = PlaintextCorpusReader('', '.*\.txt')
d = enchant.Dict('en_GB')
titles = {
        'finnegans_wake.txt': 'Finnegans Wake',
        'ulysses.txt': 'Ulysses',
        'ofk.txt': 'Once and Future King'
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

def write_word_counts(filename):
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')
        writer.writerow(['Title', 'Total words', 'Unique words'])
        for filename in ['finnegans_wake.txt', 'ulysses.txt', 'ofk.txt']:
            words = get_words(filename)
            writer.writerow([titles[filename], len(words), num_unique_words(words)])

write_word_counts('data/wc.csv')

#print_info('finnegans_wake.txt')
#print
#print_info('ulysses.txt')
#print
#print_info('ofk.txt')
