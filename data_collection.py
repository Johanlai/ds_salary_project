# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:49:49 2023

@author: JHL
"""

import glassdoor_scraper as gs
import pandas as pd

path = r"C:\Users\44756\Documents\ds_salary_project\chromedriver"
slp_time = 2
save = 
# Data analyst
df = gs.get_jobs('Data analyst', 1, path, slp_time, False)
df.to_csv('data/glassdoor_jobs_data_analyst.csv', index = False)
# Quant developer
df = get_jobs('Quantitative developer', 500, path, slp_time, False)
df.to_csv('data/glassdoor_jobs_quant_developer.csv', index = False)
# Python
df = get_jobs('Python', 500, path, slp_time, False)
df.to_csv('data/glassdoor_jobs_Python.csv', index = False)
# Market risk
df = get_jobs('market risk', 500, path, slp_time, False)
df.to_csv('data/glassdoor_jobs_market_risk.csv', index = False)
# Finance developer
df = get_jobs('Finance developer', 500, path, slp_time, False)
df.to_csv('data/glassdoor_jobs_findeveloper.csv', index = False)
# Regression
df = get_jobs('regression', 500, path, slp_time, False)
df.to_csv('data/glassdoor_jobs_regression.csv', index = False)
# Econometrics
df = get_jobs('econometrics', 500, path, slp_time, False)
df.to_csv('data/glassdoor_jobs_econometrics.csv', index = False)