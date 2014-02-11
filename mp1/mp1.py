from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.stem import PorterStemmer
from operator import itemgetter
from scipy.stats import linregress
import json

wordlists = PlaintextCorpusReader('', '../corpora/ofk_ch[1234]\.txt')
stopwords_set = set(stopwords.words('english'))
all_words = []
freqs = []
ch_lens = []

for i in xrange(1, 5):
    words = wordlists.words('../corpora/ofk_ch' + str(i) + '.txt')
    words = [w.lower() for w in words]
    words = [w for w in words if w.isalpha()]
    words = [w for w in words if not w in stopwords_set]
    words = [PorterStemmer().stem(w) for w in words]
    all_words += words
    ch_lens.append(len(words))
    freq = FreqDist(words)
    freqs.append(freq)
    print freq

all_freq = FreqDist(all_words)

slopes = []
x = [1, 2, 3, 4]
for w in all_freq:
    y = [float(freqs[0][w])/ch_lens[0],
            float(freqs[1][w])/ch_lens[1],
            float(freqs[2][w])/ch_lens[2],
            float(freqs[3][w])/ch_lens[3]]
    slope = linregress(x, y)[0]
    slopes.append({'word': w, 'slope': slope})

slopes_sorted = sorted(slopes, key=itemgetter('slope'), reverse=True)

out_data = slopes_sorted[:20] + slopes_sorted[-20:]
for w in out_data:
    w['freqs'] = [{'ch': 1, 'freq': float(freqs[0][w['word']])/ch_lens[0]},
            {'ch': 2, 'freq': float(freqs[1][w['word']])/ch_lens[1]},
            {'ch': 3, 'freq': float(freqs[2][w['word']])/ch_lens[2]},
            {'ch': 4, 'freq': float(freqs[3][w['word']])/ch_lens[3]}]

with open('data.json','w') as outfile:
     json.dump(out_data, outfile, sort_keys=True, indent=4, ensure_ascii=False)
