# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:49:49 2023

@author: JHL
"""

import glassdoor_scraper as gs
import pandas as pd

path = r"C:\Users\44756\Documents\ds_salary_project\chromedriver"
slp_time = 2
num_jobs = 1500
keyword = 'Data analyst'

df = gs.get_jobs(keyword, num_jobs, path, slp_time, False)

df.to_csv('glassdoor_jobs.csv', index = False)