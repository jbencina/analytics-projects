
# coding: utf-8

# In[ ]:

from bigquery import get_client
from time import sleep
import pandas as pd
import numpy as np
import io, os, pickle
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:

FILE_NAME = 'pitcher_data.p'

def get_bq_data():
    # Download the .json key from your Google Cloud account
    client = get_client(json_key_file='bq-query.json', readonly=True)
    
    query = """
    SELECT
        pitcherId,
        pitchTypeDescription,
      outcomeDescription,
        COUNT(pitchTypeDescription) throws
    FROM
        [bigquery-public-data:baseball.games_wide]
    WHERE
        atBatEventType = "PITCH"
    GROUP BY 
        pitcherId,
        pitchTypeDescription,
        outcomeDescription
    """

    job_id, _results = client.query(query)
    complete = False

    while not complete==True:
        print('Checking for job {JOB}...'.format(JOB=job_id))
        complete, row_count = client.check_job(job_id)
        sleep(1)

    print('Job complete - downloading...')
    results = client.get_query_rows(job_id)
    print('Downloaded {N} results...'.format(N=len(results)))
    
    with open(FILE_NAME, 'wb') as f:
        pickle.dump(results, f)
    return results
        
def get_data():
    if os.path.exists(FILE_NAME):
        print('Reading downloaded file...')
        with open(FILE_NAME, 'rb') as f:
            d = pickle.load(f)
        return pd.DataFrame.from_dict(d)
    else:
        print('Downloading from BQ...')
        d = get_bq_data()
        return pd.DataFrame.from_dict(d)

results = get_data()
results.head()


# In[ ]:

def plot_top_crossplot(data):
    get_ipython().magic('matplotlib inline')
    d = data.copy()
    
    # Group small outcomes into 'Other'
    outcome_other = d.groupby('outcomeDescription').agg({'throws': np.sum}).reset_index().sort_values(by='throws').tail(10)['outcomeDescription'].values
    d['outcomeDescription'] = d.apply(lambda x: 'Other' if x['outcomeDescription'] not in outcome_other 
                                            else x['outcomeDescription'], axis=1)
    
    # Remove three pitch types with little data
    d = d[~d['pitchTypeDescription'].isin(['Intentional Ball','Other','Pitchout'])]

    # Create a pivot from the sums
    d = d.groupby(['outcomeDescription','pitchTypeDescription']).agg({'throws': np.sum}).reset_index()
    d = d.pivot(index='outcomeDescription',columns='pitchTypeDescription', values='throws').fillna(0)
        
    # Convert values to % of each column (pitch type)
    data_sums = d.sum()
    d = d.apply(lambda x: x/data_sums, axis=1)
    
    # Create the plot
    plt.figure(figsize=(18,10))
    sns.set(font_scale=1.3)
    sns.set_style({'font.family':'Segoe UI'})
    sns.heatmap(d, robust=True, square=False, linewidths=0.01, linecolor='#666666',annot=True, fmt='.1%')
    plt.xlabel('\nPitch Type')
    plt.ylabel('Pitch Outcome')
    plt.title('Pitch Outcome % by Pitch Type - MLB 2016 Regular Season\nSource: Google BigQuery\n', fontsize=20, fontname='Segoe UI')
    plt.savefig('pitches-results.png')
    return

plot_top_crossplot(results)


# In[ ]:



