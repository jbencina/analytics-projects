import pickle
import os
import urllib.request as req
import numpy as np
import pandas as pd

def load_hurdat2_data(hurdat_file):  
    base_url = 'http://www.nhc.noaa.gov/data/hurdat/{}'.format(hurdat_file)
    filedir = 'cache'
    filename = '{}/hurdat2.p'.format(filedir)
    
    # Load from cache if file already exists
    if os.path.isfile(filename):
        print('Reading cached HURDAT2')
        with open(filename, 'rb') as f:
            return pickle.load(f)
        
    with req.urlopen(base_url) as response:
        print('Downloading HURDAT2 file - {}'.format(hurdat_file))
        data = response.read().decode('utf-8').split('\n')[:-1]

    print('Processing HURDAT2')
    # Create headers per http://www.nhc.noaa.gov/data/hurdat/hurdat2-format-atlantic.pdf
    headers = [
        'code','name','date','time','record_identifier','storm_status','latitude','longitude','max_wind',
        'min_pressure'
    ]
    
    # Create headers for the 3 wind speeds x 4 quadrent columns
    for w in ['34','50','64']:
        for q in ['ne','se','sw','nw']:
            headers.append('wind_{}kt_{}'.format(w, q))
    
    # Loop through each row, when encountering a header row, pull out the storm code and name
    # Strip out newline delimiter at end
    storm_data = []
    for k,v in enumerate(data):
        row_split = v.split(',')
        
        if len(row_split) == 4:
            storm_code = row_split[0].strip()
            storm_name = row_split[1].strip()
        else:
            data_row = '{},{},{}'.format(storm_code, storm_name, v).split(',')[:-1]
            storm_data.append(data_row)
            
    df = pd.DataFrame(storm_data, columns=headers).set_index('code')
    df = df.apply(lambda x: x.str.strip())
      
    # Convert date-time to single pandas column
    df['datetime'] = pd.to_datetime(df.date + df.time, format='%Y%m%d%H%M')
    df.drop(['date','time'], axis=1, inplace=True)
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    
    # Add an ordinal ranking for the storm status
    storm_status = ['DB','WV','LO','EX','SD','SS','TD','TS','HU']
    df['status_rank'] = df['storm_status'].apply(lambda x: storm_status.index(x))
        
    # Lat/lon to decimal values
    def convert_geo(x):
        sign = -1 if x[-1] in ['S','W'] else 1
        
        return float(x[:-1]) * sign
        
    # Convert coordinates from N/W string
    df['latitude'] = df['latitude'].apply(convert_geo)
    df['longitude'] = df['longitude'].apply(convert_geo)
    

    # Convert columns to numeric remove -999 or -99
    for col in [c for c in df.columns if c.split('_')[0] in ['max','min','wind']]:
        df[col] = pd.to_numeric(df[col]).replace([-99,-999], np.NaN)
        
    # Add hurricane wind category
    def wind_category(x):
        if x>=137:
            return 5
        elif x>=113:
            return 4
        elif x>=96:
            return 3
        elif x>=83:
            return 2
        elif x>=64:
            return 1
        else:
            return np.NaN
        
    df['status_cat'] = df['max_wind'].apply(wind_category)
        
    # Calculate peak values and join back to main
    df_agg = df.groupby('code')[[c for c in df.columns if c.split('_')[0] in ['max','wind','status']]].max()
    df_agg['min_pressure'] = df.groupby('code')['min_pressure'].min()
    
    df_agg.columns = ['agg_{}'.format(c) for c in df_agg.columns]
    df = df.merge(df_agg, left_index=True, right_index=True).reset_index()

    for w in ['34','50','64']:
        cols = [c for c in df.columns if 'agg_wind_{}kt_'.format(w) in c]
        df['agg_maxwind_{}kt_tot'.format(w)] = df[cols].max(axis=1)
           
    # Cache the merged file 
    if not os.path.exists(filedir):
        os.makedirs(filedir)
        
    with open(filename, 'wb') as f:
        pickle.dump(df, f)
    
    print('HURDAT2 Complete')
    return df


def load_ersst_data(year_start, year_end, bounding_box=None, use_cache=True):
    # Download latest Extended Reconstructed Sea Surface Temperature (ERSST) data
    base_url = 'https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/ascii/ersst.v5.{}.asc'
    filedir = 'cache'
    filename = '{}/ersst.p'.format(filedir)
    
    # Load from cache if file already exists
    if os.path.isfile(filename) and use_cache:
        print('Reading cached ERSST. Warning: Parameters ignored.')
        with open(filename, 'rb') as f:
            return pickle.load(f)
    
    print('Downloading ERSST data')
    
    temps = pd.DataFrame()
    
    # Each observation point is repeated 12 times - assuming full year file
    months = [item for item in range(1,13) for _ in range(180)] 
    
    # Loop for each year
    for yr in range(year_start, year_end+1):
        print('Downloading year {}'.format(yr))
        
        with req.urlopen(base_url.format(yr)) as response:
            content = response.read().decode('utf-8')
            
            # Split text file by newline delimiter and create columns by consecutive whitespaces
            lines = content.split('\n')
            new_data = pd.DataFrame([c.split() for c in lines if len(c.split())>0])
            
            # Convert columns to numeric remove -9999; Change temp to whole C degrees
            for col in new_data.columns:
                new_data[col] = pd.to_numeric(new_data[col]).replace(-9999, np.NaN) / 100.0

            # Concatenate with previous year
            new_data['year'] = yr
            new_data['month'] = months
            temps = pd.concat([temps, new_data], ignore_index=True, axis=0)

    print('Processing ERSST data')      
    # Define rows (longitude) and columns (latitude) 
    # based on the specs https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/ascii/Readme
    cols = [lat for lat in range(-88, 90, 2)] + ['year','month']
    rows = [lon for lon in range(0, 360, 2)] * (year_end - year_start + 1) * 12
    
    temps.columns = cols
    temps['lon'] = rows
    
    # Bounding box should be two tuples, top left and bottom right point. Note that latitude goes from -88 to +88
    # as expected, but longitude increases from 0 to 358 EASTWARD. A range like 250-360 would roughly cover the Northern
    # Atlantic
    
    if bounding_box is not None:
        filter_lat = [c for c in range(-88, 90, 2) if (c<=bounding_box[0][0]) and (c>=bounding_box[1][0])] + ['year','month']
        filter_lon = [c for c in range(0, 360, 2) if (c>=bounding_box[0][1]) and (c<=bounding_box[1][1])]
    
        temps = temps[temps['lon'].isin(filter_lon)][filter_lat]

    # Cache the merged file 
    if not os.path.exists(filedir):
        os.makedirs(filedir)
        
    with open(filename, 'wb') as f:
        pickle.dump(temps, f)

    print('ERSST Complete')
    return temps
