# Parses ACS 1YR summary files into a single merged file. Produces a summary file as well.
# Columns are truncated down to the ones listed in headers.py

# Instructions
# 1. Use https://factfinder.census.gov/ to select 2016 ACS 1-year estimates & "Quick Table"
# 2. Download DP02, DP03, DP05 to /aff_download folder in script directory
# 3. Run script - output is saved as data_out.csv, data_out_scaled.csv, and headers_out.csv

import pandas as pd
import numpy as np
import glob
import re
from headers import FILE_HEADERS, HEADER_MAP

WORKING_DIR = 'aff_download'
WORKING_PREFIX = 'ACS_16_1YR'

def get_headers(name, include_geo=True):
    """Returns the variable names and friendly names for an ACS file"""

    file_headers =  FILE_HEADERS.get(name)

    if include_geo:
        headers = ['GEO.id','GEO.display-label']
        descriptions = ['Id','Label']
    else:
        headers, descriptions = [], []

    for v, t, n in file_headers:
        headers.append('{}_{}'.format(HEADER_MAP.get(t), v))
        descriptions.append(n)

    return headers, descriptions

def get_data_file(filename):
    """Parses an ACS data file"""

    file_type = re.findall('DP\d{2}', filename)[0]
    file_headers, short_names = get_headers(file_type)

    df = pd.read_csv(filename, skiprows=[1], encoding='iso-8859-1', usecols=file_headers)
    df.columns = short_names
    df = df.set_index(['Id','Label'])

    return df

def get_header_file(filename):
    """Parses an ACS metadata file"""

    file_type = re.findall('DP\d{2}', filename)[0]
    file_headers, header_names = get_headers(file_type, include_geo=False)
    

    df = pd.read_csv('{}/{}_{}_metadata.csv'.format(WORKING_DIR, WORKING_PREFIX, file_type), header=0, names=['Variable','LongDescription'], encoding='iso-8859-1')
    df = df[df.Variable.isin([v for v in file_headers])]

    df['ShortDescription'] = header_names
    df['File'] = file_type
    df = df.set_index(['File','Variable'])

    return df

def process_files():
    """Process all files in the data directory"""

    data_files = glob.glob('{}/{}*with_ann.csv'.format(WORKING_DIR, WORKING_PREFIX))

    final_data = pd.DataFrame()
    final_headers = pd.DataFrame()

    print('Processing {} files'.format(len(data_files)))
    for file in data_files:
        final_data = pd.concat([final_data, get_data_file(file)], axis=1)
        final_headers = pd.concat([final_headers, get_header_file(file)])

    final_data = final_data.replace('N', np.nan).astype(float)
    data_summary = final_data.describe().transpose().reset_index().rename(columns={'index': 'ShortDescription'})
    final_headers = final_headers.reset_index().merge(data_summary, on=['ShortDescription']).set_index(['File','Variable'])

    final_data.to_csv('data_out.csv')
    final_headers.to_csv('headers_out.csv')

    def scale(x):
        return (x - x.mean()) / x.std()

    final_data.apply(scale).to_csv('data_out_scaled.csv')
    print('Processing complete!')


process_files()