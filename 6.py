from flask import Flask, redirect, render_template, request, Response
import requests
from typing import List
import json
import nltk

app = Flask(__name__)


def text_into_sentences(file: str) -> List[str]:
    with open(file, 'rt', encoding='cp1251') as in_file:
        sentence_list = []
        for line in in_file:
            sentence_list += nltk.sent_tokenize(line)
        return sentence_list


def find_sentences(sentences: List[str], size: int, word: str) -> List[str]:
    sentence_list = []
    for sent in sentences:
        if size == 0:
            break
        lower_sent = sent.lower()
        word = word.lower()
        if word in lower_sent:
            sentence_list.append(sent)
            size -= 1
    return sentence_list


def find_sentences2(sentences: List[str], _from: int, _to: int, word: str) -> List[str]:
    sentence_list = []
    counter = 1
    for sent in sentences:
        if counter > _to:
            break
        lower_sent = sent.lower()
        word = word.lower()
        if word in lower_sent:
            if counter >= _from:
                sentence_list.append(sent)
            counter += 1
    return sentence_list


@app.route('/')
def redirected():
    return redirect('/search')


@app.route('/search')
def hello():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def func():
    count = int(request.form.get('count'))
    word = str(request.form.get('word'))
    sentences = text_into_sentences('Harry Potter and the Sorcerer.txt')
    sentences = find_sentences(sentences, count, word)
    return render_template('rez.html', data=sentences, kek=word)


@app.route('/request', methods=['POST'])
def function():
    data = request.json
    word = data['word']
    _from = data['from']
    _to = data['to']
    sentences = text_into_sentences('Harry Potter and the Sorcerer.txt')
    sentences = find_sentences2(sentences, _from, _to, word)
    dict = {
        "examples": sentences,
        "examples_count": len(sentences),
        "from": _from,
        "to": _to,
        "word": word
    }
    return dict


if __name__ == '__main__':
    app.run()
