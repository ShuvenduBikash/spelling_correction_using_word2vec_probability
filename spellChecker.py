import sys
import tkinter as tk
import numpy as np
import pandas as pd
import codecs

words = []
with codecs.open('D:\\SD14\\data\\Words\\unique_word_frequency\\output_data\\freq_lt_15.txt', mode='r', encoding='utf-8') as f:
    for line in f:
        words.append(line.split(' ')[0])

w_rank = {}
for i, word in enumerate(words):
    w_rank[word] = i

WORDS = w_rank

import re
from collections import Counter

# Finds all words in a sentence
def words(text): return re.findall(r'\w+', text.lower())

def P(word): 
    "Probability of `word`."
    # use inverse of rank as proxy
    # returns 0 if the word isn't in the dictionary
    return - WORDS.get(word, 0)

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    #       word itself   or 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'ঁংঃঅআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ঽািীুূৃৄেৈোৌ্ৎৗড়ঢ়য়'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correctSentence(text):
    words = text.split(' ')
    return ' '.join(correction(word) for word in words)
    

def extract_text():
    mtext = ment.get()
    correctedText = correctSentence(mtext)
    mlabel2.config(text = correctedText)
    return


gui = tk.Tk()
ment = tk.StringVar()

gui.geometry('900x450+500+300')
gui.title("Spell Checker")

mlabel = tk.Label(gui, text="Spell Chekcer V0.1", width=200)
mlabel.config(font=("Courier", 44))
mlabel.pack()

mEntry = tk.Entry(gui, textvariable = ment, width=70)
mEntry.config(font=("Courier", 15))
mEntry.pack()

mButton =tk.Button(gui, text='Check', command=extract_text)
mButton.config(font=("Courier", 18))
mButton.pack()

mlabel2 = tk.Label(gui, text='')
mlabel2.config(font=("Courier", 15))
mlabel2.pack()

gui.mainloop()