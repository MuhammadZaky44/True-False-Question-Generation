# -*- coding: utf-8 -*-
"""Sino-Anto NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h10BjtKNszgUQMMbOWl-XkXqujQdyeF1
"""

import random
import json
import re
# from google.colab import drive
# drive.mount('/content/gdrive')
# !cp '/content/gdrive/My Drive/Tugas_Akhir/dict.json' dict.json

# ==================================================
# Membaca dictionary dari json
# ==================================================
def load(filename):	
	with open(filename) as data_file:
		data = json.load(data_file)	

	return data

# load dictionary
mydict = load('files/dict.json')

# ==================================================
# Mencari sinonim dari suatu kata
# ==================================================
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

# ==================================================
# Mengubah kata awal menjadi sinonimnya
# ==================================================

def replace_synonyms(text):
    # Tokenize the input text
    tokens = re.findall(r'\b\w+\b', text)
    print('tokens:', tokens)
    print('\n')
    # print('Panjang tokens: ', len(tokens))
    # Generate random and not repeated integer number
    num_tokens_to_replace = min(2, len(tokens))
    indices_to_replace = random.sample(range(len(tokens)), num_tokens_to_replace)
    for i in indices_to_replace:
        word = tokens[i]
        synonym_list = getSynonym(word)
        if not synonym_list:
            continue
        synonym = random.choice(synonym_list)
        text = re.sub(r'\b{}\b'.format(word), synonym, text)
    return text

def replace_antonyms(text):
    # Tokenize the input text
    tokens = re.findall(r'\b\w+\b', text)
  
    # Replace words with antonyms
    for i in range(len(tokens)):
        antonyms = getAntonym(tokens[i])
        if len(antonyms) > 0:
            new_word = antonyms[0] # Replace with the first antonym in the list
            text = re.sub(r'\b{}\b'.format(tokens[i]), new_word, text)
            break
    return text


sentence = 'Di suatu sekolah dasar sedang terdapat hari yang penting. Hari di mana pemenang lomba Agustusan akan diumumkan. Saat itu para siswa kelas 2 SD pergi keluar kelas sambil berlarian mencari tempat untuk mendengarkan pengumuman lomba. Tentunya mereka berharap menjadi pemenangnya. Para pemenang lomba Agustusan akan mendapatkan hadiah yang menarik yang telah disiapkan oleh panitia lomba. Begitu pula dengan Zahra, ia sangat antusias dan bersemangat mendengarkan pengumuman dari guru.'
sentence = preprocessing(sentence)
sentences = sentence.split('. ')

print('----------------Sinonim----------------')
for sentence in sentences:
  sinonim = replace_synonyms(sentence)
  print('Hasil proses: ', sinonim)
  print('\n\n')

print('----------------Antonim----------------')
for sentence in sentences:
  antonim = replace_antonyms(sentence)
  print('Hasil proses: ', antonim)
  print('\n\n')