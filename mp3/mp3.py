import nltk
import cPickle

content = open('../corpora/ofk.txt', 'r').read()

def extract_persons(text):
    persons = set()
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node') and chunk.node == 'PERSON':
                person = ' '.join(c[0] for c in chunk.leaves())
                persons.add(person)
                print person
    return persons

#characters = extract_persons(content)

#characters = set()
#with open('characters.txt', 'r') as file:
    #for line in file:
        #characters.add(line.strip())
#cPickle.dump(characters, open('characters.p', 'wb'))

characters = cPickle.load(open('characters.p', 'rb'))
print characters
