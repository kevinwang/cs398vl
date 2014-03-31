import nltk
import re
import json

def extract_persons(text):
    """Returns a set of all person names found in text"""
    persons = set()
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node') and chunk.node == 'PERSON':
                person = ' '.join(c[0] for c in chunk.leaves())
                persons.add(person)
                print person
    return persons

#characters = extract_persons(content)

def load_characters(filename):
    """Load list of characters from file"""
    with open(filename, 'r') as file:
        return [character.strip() for character in file]

def generate_adjacency_matrix(paras, characters):
    """
    Generates a weighted adjacency matrix where edge weights represent
    number of paragraphs with co-occurrences
    """
    # Creates a dictionary where the keys are characters and the values are the
    # indices of the paragraphs in which that character has appeared.
    occurrences = {character: set([i for i, para in enumerate(paras) if character in para]) for character in characters}

    adjacency_matrix = [[0] * len(characters) for i in characters]
    for i, char_a in enumerate(characters):
        for j, char_b in enumerate(characters):
            adjacency_matrix[i][j] = len(occurrences[char_a].intersection(occurrences[char_b])) # Yeah sets!
    return adjacency_matrix

content = open('../corpora/ofk.txt', 'r').read()
paras = re.split('\n\n', content)
characters = load_characters('characters.txt')

adjacency_matrix = generate_adjacency_matrix(paras, characters)

out_data = {}
out_data['nodes'] = [{'name': character} for character in characters]
out_data['links'] = [{'source': i, 'target': j, 'sentiment': 0, 'value': adjacency_matrix[i][j]} for i in range(len(characters)) for j in range(i + 1) if adjacency_matrix[i][j] != 0]

with open('data/data.json','w') as outfile:
     json.dump(out_data, outfile, sort_keys=True, indent=4, ensure_ascii=False)
