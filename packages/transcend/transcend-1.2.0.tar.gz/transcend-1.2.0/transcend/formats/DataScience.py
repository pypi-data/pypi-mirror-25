import pandas as pd
import numpy as np
import datetime
import json
from config import datascience_format_options

from pandas.io.json import json_normalize


def raw_to_data_science(data, serviceURI):
    params = datascience_format_options[serviceURI]
    params['name'] = serviceURI
    params['data'] = data
    return RawToDataScience(**params).to_json()


# should be function and the class should be the already formatted object
class RawToDataScience(object):
    def __init__(self, data, name, now = None, dt_str_strip = '%Y-%m-%dT%H:%M:%S.%fZ',
                 date_str_strip = '%m/%d/%Y', collapse = [], col_to_type = {}, attributes = [],
                 getAttributes = {}, additional_details = ['updatedAt', 'createdAt', 'latestPull'],
                 try_dates = None):
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
        self.col_to_type = col_to_type
        
        # the list of attributes one can access
        self.attributes = attributes[:]
        
        # the list of attributes that can be queried at any given time
        self.getAttributes = getAttributes
        
        # the attributes to pull into the details attribute
        self.additional_details = additional_details[:]
        
        # the collumns to initially collapse
        self.collapse = collapse
        
        self.try_dates = try_dates
        
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
        for col in self.collapse:
            keys = self.allData[col].keys()
            for key in keys:
                self.allData[key] = self.allData[col][key]
            del self.allData[col]
        
            
        # standard attributes to dataframe
        for attr in self.attributes:
            setattr(self, attr, self.to_df(self.allData[attr], attr))
        
        # bunch together details
        details = pd.Series(self.allData['details'] if 'details' in  self.allData else {})
        for attr in self.additional_details:
            details[attr] = self.allData[attr]
        self.details = self.to_df(details, 'details')
        self.attributes.append('details')
    
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
        obj_type = type(json_object)
        
        # list of objects converted to df
        if obj_type == list:
            df = pd.DataFrame(json_object)
            
            # if not a list of objects, change the column name
            if len(json_object) > 0 and type(json_object[0]) != dict:
                df.columns = [name]
        
        # dict converted to series then to df
        elif obj_type == dict:
            df = pd.Series(json_object).to_frame()
            df.columns = [name]
            df = df.T
        
        # series converted to dataframe
        elif obj_type == pd.Series:
            df = json_object.to_frame().T
        else:
            raise TypeError('Unexpected type for json object %s' % obj_type)
        
        # set the index if it exists
        if index in df:
            df = df.set_index(index)
            
        if df.shape[0] == 0:
            return df
        else:
            df = json_normalize(json.loads(df.to_json(orient='records')))
            
            # convert datetimes and dates to datetime objects
            for col in filter(lambda x : x in self.col_to_type, df.columns):
                col_type = self.col_to_type[col]
                
                if self.try_dates:
                    for form in self.try_dates:
                        try:
                            df[col] = df[col].map(lambda x :  datetime.datetime.strptime(x, form) if pd.notnull(x) else np.nan)
                            break
                        except:
                            pass
                else:
                    if col_type == 'raw_datetime':  
                        df[col] = df[col].map(lambda x :  datetime.datetime.strptime(x, self.dt_str_strip) if pd.notnull(x) else np.nan)
                    elif col_type == 'raw_date':  
                        df[col] = df[col].map(lambda x :  datetime.datetime.strptime(x, self.date_str_strip) if pd.notnull(x) else np.nan)
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
        rawdata = self.allData[name]
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