# -*- coding: utf-8 -*-
"""Negation Modification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FEdfEPoNMSTiOCr7_OHPmR8ruPDZ-U0q
"""

import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

negation_words = ['tidak', 'bukan', 'belum', 'tak', 'jangan']

def remove_negation_words(text):
    negation_pattern = r'\b(' + '|'.join(negation_words) + r')\b'
    text = re.sub(negation_pattern, '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

sentence = "Saya bukan seseorang yang pintar yang belum sering belajar."
new_sentence = remove_negation_words(sentence)
print(new_sentence)