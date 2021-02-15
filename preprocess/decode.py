import pandas as pd
import numpy as np


def judge(x):
    try:
        if '.' in x:
            return 'rate'
        elif ':' in x:
            return 'decrease'
        else:
            return 'fixed'
    except:
        return x


def process(x, flag):
    if x['discount_type'] == 'decrease':
        if flag =='pre':
            return x['Discount_rate'].split(':')[0]
        elif flag ==  'post':
            return x['Discount_rate'].split(':')[1]
    if x['discount_type'] == 'rate':
        return float(x['Discount_rate'])
    return np.nan


def preprocess_discount_rate(df):
    df['discount_type']=df['Discount_rate'].apply(lambda x: judge(x))
    df['rate_dis']=df['pre_dis']=df['post_dis']=np.nan
    idx = df[df['discount_type']=='decrease'].index
    if len(idx)>0:
        df['pre_dis'].loc[idx] = df.loc[idx].apply(lambda x: process(x,'pre'),axis=1)
        df['post_dis'].loc[idx]= df.loc[idx].apply(lambda x: process(x,'post'),axis=1)
    idx = df[df['discount_type']=='rate'].index
    if len(idx)>0:
        df['rate_dis'].loc[idx]= df.loc[idx].apply(lambda x: process(x,'rate'),axis=1)
    return