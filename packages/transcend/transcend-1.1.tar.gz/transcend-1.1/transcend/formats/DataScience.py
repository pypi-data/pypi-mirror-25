import pandas as pd
import numpy as np
import datetime
import json
from config import datascience_format_options


class DataScience(object):
    def __init__(self, data, name, now = None, dt_str_strip = '%Y-%m-%dT%H:%M:%S.%fZ', date_str_strip = '%m/%d/%Y'):
        '''
            Initialize a dataset object
        '''
        # the raw data
        self.allData = data
        
        # the time to use as the current time
        self.now = datetime.datetime.now() if now is None else now
        
        # the name of the service
        self.name = name
        
        # the format for datetime strings
        self.dt_str_strip = dt_str_strip
        
        # the format for date strings
        self.date_str_strip = date_str_strip
        
        # the mapping of column name to data type
        self.col_to_type = datascience_format_options[name]['col_to_type']
        
        # the list of attributes one can access
        self.attributes = data['attributes'].keys()
        
        # the list of attributes that can be queried at any given time
        self.getAttributes = datascience_format_options[name]['getAttributes'] if 'getAttributes' in datascience_format_options[name] else {}
        
        # pre process the object
        self.pre_process()
    
    def get(self, attr, date = None):
        '''
            Returns a dateframe for the attribute closest to the date in question
        '''
        return self.getAttributeHelper(attr,  date)
    
    def getAll(self, attr):
        '''
            Returns all of the data for the attribute
        '''
        return self.allData[attr]
        
    def pre_process(self):
            
        # standard attributes to dataframe
        for attr in self.attributes:
            setattr(self, attr, self.to_df(self.allData['attributes'][attr], attr))
        
    def to_json(self):
        response = {
            'attributes' : {},
            'getAttributes' : {}
        }

        for attr in self.attributes:
            response['attributes'][attr] = getattr(self, attr).to_json(orient='records') 
        for attr in self.getAttributes:
            response['getAttributes'][attr] = self.getAll(attr) 

        return response
            
    def to_string(self):
        '''
            Convert the service object to string and show 
            the attributes
        '''
        # indicate name of the model
        base = 'Transcend Service Model:\n' 
        base += '|- name: %s\n' % self.name
        
        # add raw data
        base += '|- allData #raw json data\n'
        
        # append attributes
        for attr in self.attributes:
              base += '|- %s\n' % attr
        
        # append get attributes
        for attr in self.getAttributes.keys():
              base += '|- get(\'%s\', datetime.datetime.now())\n' % (attr)
        return base
    
    def to_df(self, json_object, name, index = '_id'):
        '''
            Convert a json object to a dataframe
            
            json_object must be of type list, dict or pd.Series
        '''
        df = pd.DataFrame(json.loads(json_object))

        # set the index if it exists
        if index in df:
            df = df.set_index(index)
            
        if df.shape[0] == 0:
            return df
        else:
    
            # convert datetimes and dates to datetime objects
            for col in filter(lambda x : x in self.col_to_type, df.columns):
                col_type = self.col_to_type[col]
                
                if col_type == 'raw_datetime' or col_type == 'raw_date':
                    df[col] = pd.to_datetime(df[col],unit='ms')
            return df
        
    def __str__(self):
        return self.to_string()
    
    def __repr__(self):
        return self.to_string()

    def getAttributeHelper(self, name, date):
        '''
            Returns the latest pull if date is none,
            else finds the pull closest but after the date
        '''
        rawdata = self.allData['getAttributes'][name]
        key = self.getAttributes[name]
        if date is None:
            return self.to_df(rawdata[0][key], name)
        
        df = pd.DataFrame(rawdata)
        df.index = df['timePulled'].map(lambda x :  datetime.datetime.strptime(x, self.dt_str_strip))
        def nearest(items, pivot):
            return min(items, key=lambda x: pivot - x if x < pivot else 1e11)
        nearest_key = nearest(df.index, date)
        if nearest_key > date:
            print('no data from that time')
        else:
            print('closest date %s' % nearest_key)
            return self.to_df(df.ix[nearest_key, key], name)
        
    def get_all_col_keys(self):
        '''
            Get a list of all column headers for the service object
            attributes
        '''
        all_col_keys = set()
        for attr in self.attributes:
            all_col_keys = all_col_keys.union(set(getattr(self, attr).columns))
        for attr in self.getAttributes.keys():
            all_col_keys = all_col_keys.union(set(self.get(attr, self.now).columns))
        return sorted([str(x) for x in list(all_col_keys)])