#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 21:50:49 2018

@author: Razander
"""
# -----------------------------
# --- Twitter scrapper v0.0 --- 
# -----------------------------
# Goals:
# 1. scrape twitter for tickers that are mentioned together
# 2. scrape twitter for sentiment metrics on specific tickers
#   2.1 possibly extend this to other social media platforms (Facebook, instagram,...)
#       (Or, even have a bot crawler scrape news websites)

import csv
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import bigrams 
from collections import Counter
import re
import operator 
import string
import math
import matplotlib.pyplot as plt
from collections import defaultdict

date = 'Apr_05_2018'
fname = 'TwitterData/TD-'+date+'.json'
#fname = 'twitterData.json'

#Tweet text tokenizing
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r'(?:\$[\w_]+)', # $ stock ticker tags
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    s = s.lower() #force all to be lowercase to remove duplicate upper/lowercase tickers
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

     
# -- remove stop words -- 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via','RT','The','…','👉','👈','🔥','🚀']
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        #try:
        #print(type(line))
        tweet = json.loads(line)
        #except ValueError:
            #print('Json loads error')
        # Create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text']) if term not in stop]
        # Count words that are frequenctly together
        terms_bigram = bigrams(terms_all)
        # Update the counter
        count_all.update(terms_bigram)
    # Print the first 5 most frequent words
    print(count_all.most_common(8))
    
# -- Additional filters --

# Count terms only once, equivalent to Document Frequency
#terms_single = set(terms_all)
#count_single = Counter(terms_single)
#print('single terms: ',terms_single)
#print('single terms: ',count_single.most_common(top))

# Count hashtags only
#terms_hash = [term for term in preprocess(tweet['text']) 
#              if term.startswith('#')]
#count_hash = Counter(terms_hash)
#print('hash tags: ',count_hash.most_common(top))

# Count $ only
with open(fname, 'r') as f:
    count_dollar = Counter()
    for line in f:
        try:
            tweet = json.loads(line)
        except ValueError:
            print('Json loads error')
        terms_dollar = [term for term in preprocess(tweet['text']) 
              if term.startswith('$')]
        count_dollar.update(terms_dollar)
print('$ sign: ',count_dollar.most_common(5))

with open(fname, 'r') as f:
    count_only = Counter()
    for line in f:
        try:
            tweet = json.loads(line)
        except ValueError:
            print('Json loads error')
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text']) 
              if term not in stop and
              not term.startswith(('#', '@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs
        count_only.update(terms_only)
print('no #, @', count_only.most_common(5))


# -- Co-occurences --
# remember to include the other import from the previous post
 
com = defaultdict(lambda : defaultdict(int))
 
# f is the file pointer to the JSON data set
with open(fname, 'r') as f:
    for line in f: 
        #print(type(line))
        #try:
        tweet = json.loads(line)
        #except ValueError:
            #print('Json loads error')
        #find sentiment of only $ stock values
        #terms_only = [term for term in preprocess(tweet['text']) 
              #if term.startswith('$')]
        #original method
        terms_only = [term for term in preprocess(tweet['text']) 
                      if term not in stop and
                      not term.startswith(('#', '@'))]
 
        # Build co-occurrence matrix
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1 
                    
#extract top most common co-occurences
top = 5
com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:top]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:top])

# -- Search for a word's most common co-occurences --
search_word = '$AAPL' # pass a term as a command-line argument
count_search = Counter()
with open(fname, 'r') as f:
    for line in f:
        try:
            tweet = json.loads(line)
        except ValueError:
            print('Json loads error')
        terms_only = [term for term in preprocess(tweet['text']) 
                      if term not in stop 
                      and not term.startswith(('#', '@'))]
        if search_word in terms_only:
            count_search.update(terms_only)
print("Co-occurrence for %s:" % search_word)
print(count_search.most_common(20))


# -- Sentiment Analysis --
# n_docs is the total n. of tweets
n_docs = sum(1 for line in open(fname))
p_t = {}
p_t_com = defaultdict(lambda : defaultdict(int))
 
for term, n in count_only.items():
    p_t[term] = n / n_docs
    for t2 in com[term]:
        p_t_com[term][t2] = com[term][t2] / n_docs

# ---------------------------------------------------------------------
# -- consider suppor vector machine learning to better catagorize
# -- good and bad words
# ---------------------------------------------------------------------

positive_vocab = [
    'good', 'nice', 'great', 'awesome', 'outstanding',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
    'high','rising','buy','+','new','bull','up','fresh','trending'
]
negative_vocab = [
    'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
    'down','low','falling','sell','-','bear','drop','fiasco'
]

pmi = defaultdict(lambda : defaultdict(int))
for t1 in p_t:
    for t2 in com[t1]:
        denom = p_t[t1] * p_t[t2]
        pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)
 
semantic_orientation = {}
for term, n in p_t.items():
    positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
    negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
    semantic_orientation[term] = positive_assoc - negative_assoc


semantic_sorted = sorted(semantic_orientation.items(), 
                         key=operator.itemgetter(1), 
                         reverse=True)
#export semantic_sorted


#There may be different semantic levels for lower and upper case $tickers
# BE CAREFULL!
top_pos = semantic_sorted[:10]
print('\n\ntop semantic results\n',top_pos)
top_neg = semantic_sorted[-10:]
print('\n\nworst semantic result\ns',top_neg)

# Filer for stocks (e.g. '$')
stock_sentiment = [key for key in semantic_orientation.keys()
              if key.startswith('$')]

#get those semantic orientation values
sent = []
stock = []
for ind,s in enumerate(stock_sentiment):
    if semantic_orientation[s] != 0:
        stock.append(s)
        sent.append(semantic_orientation[s])


#filter out zeros

plt.scatter(stock[:15],sent[:15])
plt.title('stock sentiment != 0')
plt.xlabel('stocks')
plt.ylabel('sentiment')
plt.show()

plt.hist(sent,10)
plt.xlabel('sentiment')
plt.ylabel('frequency')
plt.show()

#write data to file
fname = 'TwitterData/TwitterSentiment-'+date+'.txt'

with open(fname, 'a') as f:
    f.write(date)
    for s in stock_sentiment:
        f.write(s)
        f.write(str(semantic_orientation[s]))
    f.write('\n')


with open(fname, 'w', newline='') as csvfile:
    w = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    w.writerow(['Date','Stock','Sentiment'])
    for s in stock_sentiment:
        w.writerow([date,s,semantic_orientation[s]])
