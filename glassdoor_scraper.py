from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from tqdm.auto import tqdm
from time import sleep
tqdm._instances.clear()

def get_jobs(keyword, num_jobs, path, slp_time, verbose):
    
    pbar = tqdm(total=num_jobs)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1320, 1000)
    
    url = 'https://www.glassdoor.co.uk/Job/london-england-jobs-SRCH_IL.0,14_IC2671300.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=London%252C%2520England&context=Jobs&dropdown=0'
    driver.get(url)

    # Close the pop ups
    time.sleep(slp_time)
    driver.find_element(By.CLASS_NAME, 'eigr9kq4').click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'modal_closeIcon-svg'))).click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
   
    # Search for keyword
    key_search = driver.find_element(By.ID,'sc.keyword')
    key_search.send_keys(keyword)
    key_search.send_keys(Keys.RETURN)

    jobs = []
    while len(jobs)<num_jobs:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'e1rrn5ka4')))
        time.sleep(slp_time)
        job_buttons = driver.find_elements(By.CLASS_NAME, 'e1rrn5ka4')
        for i in job_buttons:
            if len(jobs)>num_jobs:
                break
            time.sleep(slp_time)
            try:
                driver.find_element(By.CSS_SELECTOR, '#JDCol > div > div.css-17bh0pp.erj00if0 > button')
            except:
                pass
            try:
                driver.execute_script("arguments[0].click();", i)
            except:
                break
            time.sleep(slp_time)
            ## added this as getting error where the page doesnt load and throws an error page to manually retry search
            # This checks for the error first
            try:
                driver.find_element(By.CSS_SELECTOR, '#JDCol > div > div.css-17bh0pp.erj00if0 > button')
            except:
                pass
                #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'e1tk4kwz1')))
            try:
                company = driver.find_element(By.CLASS_NAME, 'e1tk4kwz1').text
            except NoSuchElementException:
                company = -1
            try:
                location = driver.find_element(By.CLASS_NAME,'e1tk4kwz5').text
            except NoSuchElementException:
                location = -1
            try:
                job_title = driver.find_element(By.CLASS_NAME,'e1tk4kwz4').text
            except NoSuchElementException:
                job_title = -1
            try:
                salary = driver.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li[1]/div[2]/div[3]/div[1]/span').text
            except NoSuchElementException:
                salary = -1
            try:
                salary_estimate = driver.find_element(By.CLASS_NAME,'e2u4hf13').text
            except NoSuchElementException:
                salary_estimate = -1

            try:
                title = driver.find_elements(By.CLASS_NAME,'e1pvx6aw1')
                var = driver.find_elements(By.CLASS_NAME,'e1pvx6aw2')
                comp_info = {}
                for i,x in zip(title,var):
                    comp_info[i.text] = x.text    
                try:
                    num_employees = comp_info['Size']
                except:
                    num_employees = -1
                try:
                    founded = comp_info['Founded']
                except:
                    founded = -1
                try:
                    company_type = comp_info['Type']
                except:
                    company_type = -1
                try:
                    company_industry = comp_info['Industry']
                except:
                    company_industry = -1
                try:
                    company_sector = comp_info['Sector']
                except:
                    company_sector = -1
                try:
                    company_revenue = comp_info['Revenue']
                except:
                    company_revenue = -1
            except:
                num_employees = -1
                founded = -1
                company_type = -1
                company_industry = -1
                company_sector = -1
                company_revenue = -1
                
            try:
                review = driver.find_elements(By.CLASS_NAME,'erz4gkm1')
                ratings = {}
                for i,e in list(zip(review[::2], review[1::2])):
                    ratings[i.text] = e.text
                try:
                    career_opp_rat = ratings['Career Opportunities']
                except:
                    career_opp_rat = -1
                try:
                    comp_rate = ratings['Comp & Benefits']
                except:
                    comp_rate = -1
                try:
                    culture_rate = ratings['Culture & Values']
                except:
                    culture_rate = -1
                try:
                    mngmt_rate = ratings['Senior Management']
                except:
                    mngmt_rate = -1
                try:
                    worklife_rate = ratings['Work/Life Balance']
                except:
                    worklife_rate = -1
            except:
                career_opp_rat = -1
                comp_rate = -1
                culture_rate = -1
                mngmt_rate = -1
                worklife_rate = -1
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#JobDescriptionContainer > div.css-t3xrds.e856ufb4'))).click()
                time.sleep(slp_time)
                description = driver.find_element(By.ID,'JobDescriptionContainer').text
            except:
                description = -1
                
            jobs.append({
            'Company' : company,
            'Job title' : job_title,
            'Location': location,
            'Salary': salary,
            'Salary estimate': salary_estimate,
            'Employees': num_employees,
            'Founded': founded,
            'Company type': company_type,
            'Company industry': company_industry,
            'Company sector': company_sector,
            'Company revenue': company_revenue,
            'Career opportunities': career_opp_rat,
            'Comp & Benefits': comp_rate,
            'Culture & Values': culture_rate,
            'Senior Management': mngmt_rate,
            'Work/Life Balance': worklife_rate,
            'Description': description
            })
            
            if verbose:
                print("company: {}".format(company))
                print("job_title: {}".format(job_title))
                print("location: {}".format(location))
                print("salary: {}".format(salary))
                print("salary_estimate: {}".format(salary_estimate))
                print("employees: {}".format(num_employees))
                print("founded: {}".format(founded))
                print("company_type: {}".format(company_type))
                print("company_industry: {}".format(company_industry))
                print("company_sector: {}".format(company_sector))
                print("company_revenue: {}".format(company_revenue))
                print("Career opportunities: {}".format(career_opp_rat))
                print("Comp & Benefits: {}".format(comp_rate))
                print("Culture & Values: {}".format(culture_rate))
                print("Senior Management: {}".format(mngmt_rate))
                print("Work/Life Balance: {}".format(worklife_rate))
            else:
                if len(jobs)%30==0:
                    pd.DataFrame(jobs).to_csv('TEMP_glassdoor_jobs.csv', index = False)
            pbar.update(1)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#MainCol > div.tbl.fill.px.my.d-flex > div > div.pageContainer > button.nextButton.css-1hq9k8.e13qs2071 > span > svg'))).click()
        except:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
    return pd.DataFrame(jobs)
      