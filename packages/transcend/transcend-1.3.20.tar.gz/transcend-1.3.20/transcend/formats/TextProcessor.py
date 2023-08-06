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

def data_science_to_text_processor(service, attr, keys, get_col):
    funcs = [text_to_sentences, text_to_words, text_to_words_rm_stop, text_to_nouns, text_to_noun_sentences]
    names = ['sentences', 'words', 'words-no-stop', 'nouns', 'sentences-nouns']
    params = datascience_format_options[service]
    valid_text = ['raw_string', 'raw_text', 'raw_enum', 'raw_username_string']
    text_keys = filter(lambda x : params['col_to_type'][x] in valid_text, keys)
    results = {}
    for key in text_keys:
        results[key] = {}
        series = get_col(key).fillna('')
        for name, func in zip(names, funcs):
            results[key][name] = series.astype(unicode).map(func)
    return results

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

