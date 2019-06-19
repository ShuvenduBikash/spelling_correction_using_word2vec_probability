from flask import Flask, jsonify
import re
import sys
import tkinter as tk
import numpy as np
import pandas as pd
import json
import codecs

app = Flask(__name__)
words = []
with codecs.open('D:\\SD14\\data\\Words\\unique_word_frequency\\output_data\\freq_lt_15.txt', mode='r',
				 encoding='utf-8') as f:
	for line in f:
		words.append(line.split(' ')[0])

w_rank = {}
for i, word in enumerate(words):
	w_rank[word] = i

WORDS = w_rank


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
	letters = 'ঁংঃঅআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ঽািীুূৃৄেৈোৌ্ৎৗড়ঢ়য়'
	splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	deletes = [L + R[1:] for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
	replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
	inserts = [L + c + R for L, R in splits for c in letters]
	return set(deletes + transposes + replaces + inserts)


def edits2(word):
	"All edits that are two edits away from `word`."
	return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def correctSentence(text):
	words = text.split(' ')
	return [correction(word) for word in words]


@app.route("/")
def hello():
	return jsonify({'about': 'Hello world'})


@app.route('/<sentence>', methods=['GET'])
def sentence_correction_request(sentence):
	words = sentence.split(' ')
	correctedWords = correctSentence(sentence)

	outputJson = {}
	for i in range(len(words)):
		data = {'index': i, 'verdict': 0 if words[i] == correctedWords[i] else 1, 'word': words[i],
				'candidates': correctedWords[i]}
		outputJson[words[i]] = data

	print(json.dumps(outputJson))
	return json.dumps(outputJson)


if __name__ == '__main__':
	app.run(debug=True)
