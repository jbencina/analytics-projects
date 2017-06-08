
# coding: utf-8

# In[1]:

from bigquery import get_client
from time import sleep
import pandas as pd
import numpy as np
import io, os, pickle
import matplotlib.pyplot as plt
import seaborn as sns


# In[4]:

FILE_NAME = 'batter_data.p'

def get_bq_data():
    # Download the .json key from your Google Cloud account
    client = get_client(json_key_file='bq-query.json', readonly=True)
    
    query = """
    #standardSQL
    SELECT
      startingBalls,
      startingStrikes,
      hitterPitchCount,
      SUM(isHit) hits,
      SUM(isStrike) strikes,
      SUM(isBall) balls,
      COUNT(*) pitches
    FROM
    (SELECT
      startingBalls,
      startingStrikes,
      hitterPitchCount,
      IF(SUBSTR(outcomeId,1, 1)='a', 1, 0) isHit,
      IF(SUBSTR(outcomeId,1, 1)='k', 1, 0) isStrike,
      IF(SUBSTR(outcomeId,1, 1)='b', 1, 0) isBall
    FROM
      `bigquery-public-data.baseball.games_wide`
    WHERE
      atBatEventType='PITCH') q
    GROUP BY
      startingBalls,
      startingStrikes,
      hitterPitchCount
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


# In[17]:

def calc_percentages(data):
    d = data.groupby(['startingBalls','startingStrikes']).sum().reset_index()
    del d['hitterPitchCount']
    d['balls'] = d['balls'] / d['pitches']
    d['hits'] = d['hits'] / d['pitches']
    d['strikes'] = d['strikes'] / d['pitches']
    d['other'] = 1 - d['balls'] - d['hits'] - d['strikes']
    d = d[d['pitches']>10]
    return d

results_pct = calc_percentages(results)
results_pct.head(10)


# In[114]:

def graph_data(data):
    vmax = data[['hits','balls','strikes']].values.max()
    dh = data.pivot(index='startingBalls', columns='startingStrikes', values='hits').sort_index(ascending=False)
    db = data.pivot(index='startingBalls', columns='startingStrikes', values='balls').sort_index(ascending=False)
    ds = data.pivot(index='startingBalls', columns='startingStrikes', values='strikes').sort_index(ascending=False)
    
    get_ipython().magic('matplotlib inline')
    fig, ax = plt.subplots(1, 3, figsize=(16,6))
    sns.set(font_scale=1.3)
    sns.set_style({'font.family':'Segoe UI'})
    fig.suptitle("% Likelihood of Hit, Ball, or Strike on Next Pitch By Pitch Count\nSource: Google BigQuery - 2016 MLB Regular Season")
    
    sns.heatmap(dh, ax=ax[0], vmin=0, vmax=vmax, annot=True, fmt='.1%', cbar=False, linewidths=0.01, linecolor='#666666')
    sns.heatmap(db, ax=ax[1], vmin=0, vmax=vmax, annot=True, fmt='.1%', cbar=False, linewidths=0.01, linecolor='#666666')
    sns.heatmap(ds, ax=ax[2], vmin=0, vmax=vmax, annot=True, fmt='.1%', cbar=False, linewidths=0.01, linecolor='#666666')
    
    
    ax[0].set_title("Hits")
    ax[1].set_title("Balls")
    ax[2].set_title("Strikes")
    
    ax[0].set_ylabel('Ball Count')
    ax[1].set_ylabel('')
    ax[2].set_ylabel('')
    
    for i in range(3):
        ax[i].set_xlabel('Strike Count')
 
    fig.subplots_adjust(top=0.8)
    plt.savefig('batting-results.png')
graph_data(results_pct)


# In[ ]:



