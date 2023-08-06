import pandas as pd
import numpy as np
import datetime
import json



import nltk
nltk.data.path.append('/var/task/nltk_data/')
from nltk.tokenize import word_tokenize

from textblob import TextBlob
from DataScience import DataScience
from config import datascience_format_options


# flatten a list of lists into a list
flatten = lambda l: [item for sublist in l for item in sublist]

# convert raw text into sentences
text_to_sentences = lambda text: flatten(map(nltk.sent_tokenize, filter(lambda x : x != '', text.split('\n'))))

# convert raw text to tokenized report of words and punctuation
text_to_tokenized_reports = lambda text: [word_tokenize(sentence) for sentence in text_to_sentences(text)] 

# convert raw text to list of list of nouns
text_to_noun_sentences = lambda text: [list(TextBlob(sentence).noun_phrases) for sentence in text_to_sentences(text)]

# convert raw text to list of nouns
text_to_nouns = lambda text: flatten(text_to_noun_sentences(text))

# convert raw text to list of words
text_to_words = lambda text: [x.lower() for x in flatten(text_to_tokenized_reports(text)) if x.isalpha()]

# gets all of the words in a series of a list of words
get_all_words = lambda series: list(set(flatten(list(series.values))))

def split_to_discrete_word_matrix(df, indexes = ['created_time'], keys = ['name'], weights = None, name = None, func = text_to_words, alpha = 0):
    if weights is None:
        weights = [1 for _ in keys]
    df = df.copy()
    
    for ind in indexes:
        if ind in df:
            df[ind] = df[ind].bfill()
            df = df.set_index(ind)
            break
            
    all_words = set()

    good_keys = [key + '__words' for key in keys]
    for key in keys:
        df[key + '__words'] = df[key].fillna('').apply(func)
        all_words = all_words.union(set(get_all_words(df[key + '__words'])))

    all_words = map(unicode, sorted(list(all_words)))
    counts_df = pd.DataFrame(alpha, index = df.index, columns = all_words)
    full_df = pd.concat([df[good_keys].copy(), counts_df], axis = 1)

    zipped = zip(keys, weights)
    def word_list_to_counts(row):
        for key, weight in zipped:
            for word in row[key + '__words']:
                try:
                    row[word] += weight
                except:
                    print word
        return row
    full_df = full_df.apply(word_list_to_counts, axis = 1)
    return full_df[full_df.columns[len(keys):]]

class DataScienceToTextProcessor(DataScience):
    def __init__(self, data, name, func = text_to_words):
        super(DataScienceToTextProcessor, self).__init__(data, name)
        self.func = func
        self.text_process()
    
    def to_string(self):
        base = super(DataScienceToTextProcessor, self).to_string()
        base += '--------- TEXT PROCESSOR ---------\n'
        for attr in self.attributes:
            base += '|- %s__words\n' % attr
        return base
    
    def text_process(self):
        text_keys = set(filter(lambda x : self.col_to_type[x] == 'raw_string' or self.col_to_type[x] == 'raw_text', self.col_to_type.keys()))
        def build_params(attr):
            df =  getattr(self, attr)
            df.columns
            return {
                'df' : df,
                'name' : '%s.%s' % (self.name, attr),
                'keys' : list(filter(lambda x : x in text_keys, list(df.columns))),
                'func' : self.func,
                'indexes' : ['created_time', 'start_time']
                
            }
        for attr in self.attributes:
            params = build_params(attr)
            setattr(self, '%s__words' % attr, split_to_discrete_word_matrix(**params))
    
    def to_json(self):
        base = super(DataScienceToTextProcessor, self).to_json()
        base['textProcessAttributes'] = {}
        for attr in self.attributes:
            base['textProcessAttributes'][attr] = getattr(self, '%s__words' % attr).to_json(orient='records')
        return base

class TextProcessor(DataScience):
    def __init__(self, data, name, func = text_to_words):
        super(TextProcessor, self).__init__(data, name)
        self.func = func

        for attr in data['textProcessAttributes'].keys():
            setattr(self, '%s__words' % attr, self.to_df(data['textProcessAttributes'][attr], attr))
    
    def to_string(self):
        base = super(TextProcessor, self).to_string()
        base += '--------- TEXT PROCESSOR ---------\n'
        for attr in self.attributes:
            base += '|- %s__words\n' % attr
        return base
    
    def to_json(self):
        base = super(TextProcessor, self).to_json()
        base['textProcessAttributes'] = {}
        for attr in self.attributes:
            base['textProcessAttributes'][attr] = getattr(self, '%s__words' % attr).to_json(orient='records')
        return base

