from flask import Flask, render_template, url_for, request
import random
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import json
import re
from nltk.tag import CRFTagger

#################### Number Modification ####################
def num_mod(text):
  # Membagi kalimat menjadi token
  words = word_tokenize(text)

  # Mengubah angka yang terdapat dalam kalimat
  for i, word in enumerate(words):
      if word.isdigit():
          num = int(word)
          # Mendapatkan angka secara random antara (number/2) ~ (number*2)
          num = random.randint(int(num/2), int(num*2))
          words[i] = str(num)
  # Menggantikan angka awal menjadi angka baru yang sudah dimanipulasi
  text_modified = " ".join(words)

  return text_modified
#################### End of Number Modification ####################

#################### Synonym/Antonym Modification ####################
def load(filename):	
	with open(filename) as data_file:
		data = json.load(data_file)	
	return data

mydict = load('files/dict.json')

def getSynonym(word):
	if word in mydict.keys():
		return mydict[word]['sinonim']
	else:
		return []

def getAntonym(word):
	if word in mydict.keys():
		if 'antonim' in mydict[word].keys():
			return mydict[word]['antonim']
	return []

def preprocessing(text):
  lower_text = text.lower()
  return lower_text

def replace_synonyms(text):
    # Tokenize the input text
    tokens = re.findall(r'\b\w+\b', text)
  
    # Generate random and not repeated integer number
    num_tokens_to_replace = min(2, len(tokens))
    indices_to_replace = random.sample(range(len(tokens)), num_tokens_to_replace)
    for i in indices_to_replace:
        word = tokens[i]
        synonym_list = getSynonym(word)
        if not synonym_list:
            continue
        synonym = random.choice(synonym_list)
        text = re.sub(r'\b{}\b'.format(word), f'<span style="color:blue">{synonym}</span>',text)
    return text

def replace_antonyms(text):
    # Tokenize the input text
    tokens = re.findall(r'\b\w+\b', text)
  
    # Replace a random word with an antonym
    antonym_indices = [i for i in range(len(tokens)) if len(getAntonym(tokens[i])) > 0]

    # If there is no antonyms available in the dictionary, then return the original text.
    if len(antonym_indices) == 0:
        return text
    
    index_to_replace = random.choice(antonym_indices)
    antonyms = getAntonym(tokens[index_to_replace])
    # Replace with the first antonym in the list
    new_word = antonyms[0] 
    text = re.sub(r'\b{}\b'.format(tokens[index_to_replace]), f'<span style="color:red">{new_word}</span>', text)
    return text
#################### End of Synonym/Antonym Modification ####################

#################### Negation Modification ####################
negation_words = ['tidak', 'bukan', 'belum', 'tak', 'jangan']

def remove_negation_words(text):
    negation_pattern = r'\b(' + '|'.join(negation_words) + r')\b'
    text = re.sub(negation_pattern, '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
#################### End of Negation Modification ####################

#################### Coordination Modification ####################
def preprocessing_coord(text):
    tokenized = word_tokenize(text)
    return tokenized
#################### End of Coordination Modification ####################


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/coord', methods=['GET','POST'])
def coord():
    tokenized_sentences = []
    tagged_sentences = []
    result_sentences = []

    sentence = str(request.form.get('coord'))
    original_text = str(request.form.get('coord'))

    sentences = sentence.split('. ')

    for sentence in sentences:
        tokens = preprocessing_coord(sentence)
        tokenized_sentences.append(tokens)
        ct = CRFTagger()
        ct.set_model_file('files/all_indo_man_tag_corpus_model.crf.tagger')
        tagged_sentence = ct.tag(tokens)
        tagged_sentences.append(tagged_sentence)

    # Checking if the sentences has the Noun - CC - Noun rule. If Noun - CC - Noun sequence found, then the first Noun and CC will be removed from the sentence.
    for i in range(len(tagged_sentences)):
        tokens = tagged_sentences[i]
        j = 0
        sequence_found = False  # initialize flag
        while j < len(tokens) - 2:
            if tokens[j][1].startswith('N') and tokens[j+1][1] == 'CC' and tokens[j+2][1].startswith('N'):
                del tokens[j]
                del tokens[j]
                sequence_found = True  # set flag to True
            j += 1
        tagged_sentences[i] = tokens
        if sequence_found:
            modified_sentence = ' '.join([t[0].strip() for t in tokens])
            result_sentences.append(modified_sentence)
        else:
            result_sentences.append('The sentence has no [Noun - CC - Noun] sequence.')

    return render_template('coord_mod.html', new_sentence = result_sentences, original_text = original_text)

@app.route('/sinto', methods=['GET','POST'])
def sinto():
    sentence = str(request.form.get('sinto'))
    sentence = preprocessing(sentence)
    sentences = sentence.split('. ')

    orginal_text = str(request.form.get('sinto'))

    # Array to contain the result of synonym and antoym process
    synonym_result = []
    antonym_result = []

    for sentence in sentences:
        sinonim = replace_synonyms(sentence)
        synonym_result.append(sinonim)
        antonim = replace_antonyms(sentence)
        print(antonim)
        antonym_result.append(antonim)

    return render_template('sinto.html', synonym_result=synonym_result, antonym_result=antonym_result, original_text=orginal_text)

@app.route('/number', methods=['GET','POST'])
def number():
    sentence = str(request.form.get('number'))
    sentences = sentence.split('. ')
    new_sentence = []

    for text in sentences:
        if not any(char.isdigit() for char in text):
            new_sentence.append('No number found in the sentence.')
        else:
            text_modified = num_mod(text)
            new_sentence.append(text_modified)

    return render_template('number.html', new_sentence = new_sentence, original_text = sentence)

@app.route('/negation', methods=['GET','POST'])
def negation():
    sentence = str(request.form.get('negation'))
    sentences = sentence.split('. ')
    new_sentence = []
    
    for text in sentences:
        found_negation_word = False
        if any(re.search(r'\b{}\b'.format(word), text.lower()) for word in negation_words):
            found_negation_word = True
            
        if found_negation_word:
            text_modified = remove_negation_words(text)
            new_sentence.append(text_modified)
        else:
             new_sentence.append('The sentence has no negation word.')

    return render_template('negation.html', new_sentence = new_sentence, original_text = sentence)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

