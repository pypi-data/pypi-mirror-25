#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: leslie
# date: 2017-08-24
# email: 249893977@qq.com

import string,re
from collections import defaultdict


if __name__ == '__main__':
	text1 = '#楚乔传# #赵丽颖快乐大本营# @赵丽颖 replay [心][心][心]#鹿晗# @M鹿M 140.611 快乐//@Yusunly:赵丽颖[心][心]'
	preprocess(text1)



keywords = set(['周一见',
                '拜托了冰箱','拜冰','冰箱字幕君','冰箱贴','何炅',
                '冰箱贴','王嘉尔','冰箱贴们','冰箱家族','开冰箱有好料',
                '何尔萌','超强音浪','无乐不作','音浪小分队',
                '无与伦比的发布会','无与伦比','何洁','快乐大本营',
                '音乐大师课','音乐大师','北京卫视','音乐大师',
                '四川卫视','吃光全宇宙','姐姐好饿'])

def preprocess(text):
    if type(text) is not str or len(text) == 0:
        return ''
    
    content = text
    content = clean_url(content)
    content = clean_topic(content)
    content = clean_emotion(content)
    content = clean_at(content)
    content = clean_keywords(content)
    content = clean_digit(content)
    content = clean_eng_words(content)
    content = clean_eng_punc(content)
    content = clean_cn_punc(content)
    content = clean_space(content)
    
    return content
    


regex_topic = re.compile('#.+?#')
def clean_topic(text):
    return re.sub(regex_topic, ' ', text)

def extract_topic(text, sep = '|'):
    m = regex_topic.findall(text)
    if len(m) > 0:
        return sep.join(m)
    else:
        return ''

regex_emotion = re.compile('\[[^\] ]{1,8}\]')
def extract_emotion(text, sep = '|'):
    m = regex_emotion.findall(text)
    if len(m) > 0:
        return sep.join(m)
    else:
        return ''

def clean_emotion(text):
    return re.sub(regex_emotion, ' ', text)

# TODO：这个正则有bug。 add by leslie @20170829
regex_url = re.compile(r'(https?:\/\/(w{3}\.)?)?\w+\.[a-zA-Z]+(\.[a-zA-Z]+)*(:\d{1,5})?(\/\w*)*(\??(.+=.*)?(&.+=.*)?)?')
def clean_url(text):
    return re.sub(regex_url, ' ', text)

regex_eng_punc = re.compile('[%s]' % re.escape(string.punctuation))
def clean_eng_punc(text):
    return re.sub(regex_eng_punc, ' ', text)

cn_punctuation = '+——！，。？、~@#￥ˊˋ?%……&*（）：；《》“”»〔〕-【】\u200b〃ゞ∠※▽ノ●зε●☆≧≦③'
regex_cn_punc = re.compile('[\s+{}]'.format(re.escape(cn_punctuation)))
def clean_cn_punc(text):
    return re.sub(regex_cn_punc, ' ', text)

def clean_space(text):
    return re.sub('\s+', '', text)

regex_keywords = re.compile('|'.join(list(keywords)))
def clean_keywords(text):
    return re.sub(regex_keywords, ' ', text)

regex_at = re.compile(r'@[^: 。]+')
regex_at2 = re.compile(r'@[^ ]+$')
regex_reat = re.compile(r'//@[^:]+:')
def clean_at(text):
    text = re.sub(regex_reat, ' ', text)
    text = re.sub(regex_at, ' ', text)
    #text = re.sub(regex_at2, ' ', text)
    
    return text
    
regex_digits = re.compile(r'[\d\.]+')
def clean_digit(text):
    return re.sub(regex_digits, ' ', text)


# TODO: 生僻字，英文单词，特殊符号

#英文
regex_character = re.compile(r'[A-Za-z]+')
def clean_eng_words(text):
    return re.sub(regex_character, ' ', text)

def clean_unusual_words(text):
    pass

def clean_special_punc(text):
    pass

