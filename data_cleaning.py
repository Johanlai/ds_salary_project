# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 16:41:48 2023

@author: JHL
"""

import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt

#Read all the data in
data1 = pd.read_csv('data\glassdoor_jobs_data1.csv')
data2 = pd.read_csv('data\glassdoor_jobs_data2.csv')
data3 = pd.read_csv('data\glassdoor_jobs_dataanalyst.csv')
data4 = pd.read_csv('data\glassdoor_jobs_datascientist.csv')
data5 = pd.read_csv('data\glassdoor_jobs_findeveloper.csv')
data6 = pd.read_csv('data\glassdoor_jobs_market_risk.csv')
data7 = pd.read_csv('data\glassdoor_jobs_python.csv')
data8 = pd.read_csv('data\glassdoor_jobs_quant_developer.csv')
data9 = pd.read_csv('data\glassdoor_jobs_regression.csv')
data10 = pd.read_csv('data\glassdoor_jobs_econometrics.csv')
data11 = pd.read_csv('data\TEMP_glassdoor_jobs.csv')

# check the total length of the data
datas = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11]
sum([len(i) for i in datas])

# Merge the data together
df= pd.concat(datas)

#Remove duplicaes and reset the index since there weere duplicates from the merge
df = df.drop_duplicates().reset_index(drop=True)

# Replace all the -1s to be NaN
df[df==-1]=np.nan
df.replace('-1', np.nan,inplace=True)

# Some rows have too many missing fields
df.isnull().sum(axis=1).value_counts().sort_index()

# Remove any rows with more than 11 missing values
df.drop(index=df[df.isnull().sum(axis=1)>11].index, inplace=True)

# Remove any rows that are missing company names
df.drop(index=df[df['Company'].isnull()].index, inplace=True)

# Split the company ratings out from the company names
df[["Company", "comp_rate"]] = df['Company'].str.split('\n', expand=True)


########## SALARY #############
len(df[df['Salary'].isna()])
len(df[df['Salary estimate'].isnull()])

# Remove trailing salary information
df['Salary'] = df['Salary'].fillna(df['Salary estimate'])
df['Salary'].isna().sum()
df.drop(index=df[df['Salary'].isna()].index, inplace=True)

merge_salary = df['Salary']

# Dummy variable of employer estimated salary
df['em_provided_est'] = merge_salary.apply(lambda x: 1 if '(employer est.)' in str(x).lower() else 0)

# Clean up salaries
### hourly to annual
### range to average
merge_salary = merge_salary.apply(lambda x: str(x).replace('£','').split('(')[0])

def hourly(fig):
    return float(fig)*1950

def avg_range(x):
    return int((float(x.split()[0])+float(x.split()[2]))/2)

def thousand(x):
    return float(x)*1000

hourly_clean = merge_salary.apply(lambda x: hourly(x.split(' ')[0]) if '/hr' in x else x)

avg_per_hour_clean = hourly_clean.apply(lambda x: hourly(avg_range(x)) if 'per hour' in str(x).lower() else x)
clean_salary = avg_per_hour_clean.apply(lambda x: str(x).lower().replace(' /yr','').replace(',','').replace('k', '000'))
salary_cleaned = clean_salary.apply(lambda x: avg_range(x.strip()) if ' - ' in str(x) else x)
cleaned_salary = salary_cleaned.apply(lambda x: x if np.nan else float(x))

df['cleaned_salary'] = cleaned_salary

# Clean employees
employees = df['Employees'].apply(lambda x: str(x).replace(' Employees','').replace('+',''))
employees = employees.apply(lambda x: int(avg_range(x.strip())) if ' to '  in str(x) else x)
employees = employees.apply(lambda x: np.nan if 'unknown'  in str(x).lower() else x)
df['cleaned_employees'] = employees

# Company revenue
revenue = df['Company revenue'].apply(lambda x: str(x).replace(' (USD)','').replace('$','').replace('+ billion','000').replace('Less than ','').replace(' million ',' ').replace('1 million','1'))
revenue[revenue=='Unknown / Non-Applicable'] = np.nan
revenue = revenue.apply(lambda x: avg_range(str(x))*1000 if 'billion' in str(x) else avg_range(x) if 'million' in str(x) else x)
revenue.value_counts()
df['cleaned_revenue'] = revenue

# Founded
founded = df.Founded.apply(lambda x: x if x==np.nan else 2023-x)
founded.value_counts()
df['cleaned_founded'] = founded

# Check the other columns
df['Company type'].value_counts()
df['Company industry'].value_counts()
df['Company sector'].value_counts()

# python
df['python_yn'] = df.Description.apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()
# R
df['R_yn'] = df.Description.apply(lambda x: 1 if ' r ' in x.lower() else 0)
df.R_yn.value_counts()
# STATA
df['STATA_yn'] = df.Description.apply(lambda x: 1 if 'stata' in x.lower() else 0)
df.STATA_yn.value_counts()
# SPSS
df['SPSS_yn'] = df.Description.apply(lambda x: 1 if 'spss' in x.lower() else 0)
df.SPSS_yn.value_counts()
# Spark
df['spark_yn'] = df.Description.apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark_yn.value_counts()
# SQL
df['sql_yn'] = df.Description.apply(lambda x: 1 if 'sql' in x.lower() else 0)
df.sql_yn.value_counts()
# excel
df['excel_yn'] = df.Description.apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel_yn.value_counts()
# aws
df['aws_yn'] = df.Description.apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws_yn.value_counts()

git commit -m 'name_commit'
git push origin master


HELLOW TEsting
### END OF CLEAN
# (float(hourly_clean[1400].split()[0])+float(hourly_clean[1400].split()[2]))/2




hourly_clean = hourly_clean.apply(lambda x: str(x).replace(' /yr','').replace(',','').replace('k',''))

# ---------------
hourly_clean = merge_salary.apply(lambda x: x.split(' ') if '/hr' in str(x))

merge_salary = merge_salary.apply(lambda x: x.replace('£','').replace(' /hr (est.)','') if '/hr' in x)      
merge_salary.isna().sum()

minus_kd[minus_kd.isna()]
salary = df['Salary'].apply(lambda x: str(x).split('(')[0])
minus_kd = salary.apply(lambda x: x.replace('K','').replace('£',''))


1950*16
