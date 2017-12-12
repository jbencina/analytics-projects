# Overview
Parses ACS 1YR summary files into a single merged file. This script takes 3 2016 ACS 1-yr
quick table files at the **county** level and extracts a subset of columns as defined in headers.py.
Each column is given a friendly name. The output of this script is:
- A consolidated data file
- A consolidated data file which is mean normalized
- A summary file which contains the original variable, ACS description,
short description, and summary statistics

Data can be accessed at BigQuery https://bigquery.cloud.google.com/dataset/jbencina-144002:census

A CSV copy of the data is also contained in the repo's zip file



# Instructions
1. Use https://factfinder.census.gov/ to select 2016 ACS 1-year estimates & "Quick Table"
2. Download DP02, DP03, DP05 to /aff_download folder in script directory
3. Run script - output is saved as data_out.csv, data_out_scaled.csv, and headers_out.csv
