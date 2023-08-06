import pandas as pd
import numpy as np
import datetime
import json

import nltk
nltk.data.path.append('/var/task/nltk_data/')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
s=set(stopwords.words('english'))


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
text_to_words_rm_stop = lambda text: [x.lower() for x in filter(lambda w: not w in s, flatten(text_to_tokenized_reports(text))) if x.isalpha()]


# gets all of the words in a series of a list of words
get_all_words = lambda series: list(set(flatten(list(series.values))))

def split_to_discrete_word_matrix(df, now = None, indexes = ['created_time'], keys = ['name'], name = None, func = text_to_words):
    if now is None:
        now = datetime.datetime.now()

    df = df.copy()
    
    found = False
    for ind in indexes:
        if ind in df:
            df[ind] = df[ind].bfill()
            df = df.set_index(ind)
            found = True
            break
    if not found:
        df.index = [now for _ in list(df.index)]
            
    all_words = set()

    good_keys = [key + '__words' for key in keys]
    for key in keys:
        df[key + '__words'] = df[key].fillna('').apply(func)
        all_words = all_words.union(set(get_all_words(df[key + '__words'])))

    all_words = map(unicode, sorted(list(all_words)))
    return df[good_keys], all_words

def data_science_to_text_processor(data, name):
    return DataScienceToTextProcessor(data, name, func = text_to_words_rm_stop).to_json()   

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
            base += '|- %s__allwords\n' % attr
        return base
    
    def text_process(self):
        valid_text = ['raw_string', 'raw_text', 'raw_enum', 'raw_username_string']
        text_keys = set(filter(lambda x : self.col_to_type[x] in valid_text, self.col_to_type.keys()))
        def build_params(attr):
            df =  getattr(self, attr)
            df.columns
            return {
                'df' : df,
                'name' : '%s.%s' % (self.name, attr),
                'keys' : list(filter(lambda x : x in text_keys, list(df.columns))),
                'func' : self.func,
                'indexes' : datascience_format_options[self.name]['indexes'],
                'now' : self.now
                
            }
        for attr in self.attributes:
            params = build_params(attr)
            df, all_words = split_to_discrete_word_matrix(**params)
            setattr(self, '%s__words' % attr, df)
            setattr(self, '%s__allwords' % attr, all_words)
    
    def to_json(self):
        base = super(DataScienceToTextProcessor, self).to_json()
        base['textProcesserAttributes'] = {}
        for attr in self.attributes:
            df = getattr(self, '%s__words' % attr)
            all_words = getattr(self, '%s__allwords' % attr)
            df['__index__'] = df.index
            base['textProcesserAttributes']['%s__words' % attr] = json.loads(df.to_json(orient='records'))
            base['textProcesserAttributes']['%s__allwords' % attr] = all_words
        return base

class TextProcessor(DataScience):
    def __init__(self, data, name, alpha = 0):
        super(TextProcessor, self).__init__(data, name)
        self.alpha = alpha
        self.textProcesserAttributes = self.allData['textProcesserAttributes'].keys()
        self.expand_to_sparse()

    def expand_to_sparse(self):

        for attr in self.attributes:
            df =  self.to_df(self.allData['textProcesserAttributes']['%s__words' % attr], attr, index = '__index__')
            all_words = self.allData['textProcesserAttributes']['%s__allwords' % attr]
            counts_df = pd.DataFrame(self.alpha, index = df.index, columns = all_words)
            full_df = pd.concat([df, counts_df], axis = 1)

            keys = list(df.columns)
            weights = [1 for _ in keys]
            zipped = zip(keys, weights)
            def word_list_to_counts(row):
                for key, weight in zipped:
                    for word in row[key]:
                        try:
                            row[word] += weight
                        except:
                            print word
                return row
            full_df = full_df.apply(word_list_to_counts, axis = 1)
            setattr(self, '%s__words' % attr, full_df.ix[:, len(keys):])
    
    def to_string(self):
        base = super(TextProcessor, self).to_string()
        base += '--------- TEXT PROCESSOR ---------\n'
        for attr in self.attributes:
            base += '|- %s__words\n' % attr
        return base
    
    def to_json(self):
        base = super(TextProcessor, self).to_json()
        base['textProcesserAttributes'] = {}
        for attr in self.attributes:
            base['textProcesserAttributes'][attr] = getattr(self, '%s__words' % attr).to_json(orient='records')
        return base

