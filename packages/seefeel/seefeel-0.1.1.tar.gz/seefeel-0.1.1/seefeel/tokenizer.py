#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: leslie
# date: 2017-08-24
# email: 249893977@qq.com

from collections import defaultdict
import jieba
import os

get_module_res = lambda *res: open(os.path.normpath(os.path.join(
                            os.getcwd(), os.path.dirname(__file__), *res)), mode = 'r', encoding='utf-8')

STOP_WORDS_PATH = 'stop_words.txt'


def stop_words():
    words = [ line.strip() for line in get_module_res(STOP_WORDS_PATH)]
    return set(words)

stop_words = stop_words()
print('Loading {} stopwords. '.format(len(stop_words)))


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def ngram_tokenizer_and_filter_stopwords(text, ngram = 2):
    return filter(lambda x: x not in stop_words and len(x) > 1 and check_contain_chinese(x), ngram_tokenizer(text, ngram))

def tokenize_and_filter_stopwords(text):
    if type(text) is str:
        return filter(lambda x: x not in stop_words , jieba.cut(text))
    else:
        return []


def bigram_tokenizer(text):
    words = list(jieba_tokenizer(text))
    rst = []
    if len(words) > 1:
        for i in range(len(words) - 1):
            rst.append(words[i] + words[i + 1])
    else:
        rst = words
            
    return rst


# 生成ngram, 建议最大5
def ngram_tokenizer(text, ngram = 2):
    words = list(jieba_tokenizer(text))
    rst = []
    rst.extend(words)
    
    for i in range(1, ngram):
        ngram = []
        for j in range(len(words) - i):
            gram_word = ""
            for k in range(i + 1):
                gram_word += words[j + k]
            ngram.append(gram_word)
            
        rst.extend(ngram)
    return rst



def jieba_tokenizer(text):
    return filter(lambda x: len(x.strip()) > 0 , jieba.cut(text))