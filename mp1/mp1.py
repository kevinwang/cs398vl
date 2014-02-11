from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.stem import PorterStemmer
from operator import itemgetter
from scipy.stats import linregress
import json

wordlists = PlaintextCorpusReader('', '../corpora/ofk_ch[1234]\.txt')
stopwords_set = set(stopwords.words('english'))
all_words = set()
freqs = []

for i in xrange(1, 5):
    words = wordlists.words('../corpora/ofk_ch' + str(i) + '.txt')
    words = [w.lower() for w in words]
    words = [w for w in words if w.isalpha()]
    words = [w for w in words if not w in stopwords_set]
    words = [PorterStemmer().stem(w) for w in words]
    all_words.update(words)
    freq = FreqDist(words)
    freqs.append(freq)
    print freq

slopes = []
x = [1, 2, 3, 4]
for w in all_words:
    y = [freqs[0].freq(w), freqs[1].freq(w), freqs[2].freq(w), freqs[3].freq(w)]
    slope = linregress(x, y)[0]
    slopes.append({'word': w, 'slope': slope})

slopes_sorted = sorted(slopes, key=itemgetter('slope'), reverse=True)

out_data = slopes_sorted[:20] + slopes_sorted[-20:]
for w in out_data:
    w['freqs'] = [{'ch': 1, 'freq': freqs[0].freq(w['word'])},
            {'ch': 2, 'freq': freqs[1].freq(w['word'])},
            {'ch': 3, 'freq': freqs[2].freq(w['word'])},
            {'ch': 4, 'freq': freqs[3].freq(w['word'])}]

with open('data.json','w') as outfile:
     json.dump(out_data, outfile, sort_keys=True, indent=4, ensure_ascii=False)
