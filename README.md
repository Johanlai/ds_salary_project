# Data science project overview
- Built a webscrapper to collect over 1700 job listings from glassdoors (selenium)
- Engineered features from the listings to quantify company ratings and the value companies put on certain skills, such as python, aws, SQL, R, STATA
- Optimized Linear, Lasso, and Random Forest Regressors using GridsearchCV to reach the best model.

## Code and Resources Used
[Entire walkthrough **(Ken Jee)**](https://youtube.com/playlist?list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t)<br>
**Python version**: 3.9.13<br>
**Apps**: spyder, jupyter notebook, Anaconda<br>
**Packages**: pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle<br>
**For Web Framework Requirements**: `pip install -r requirements.txt`<br>
**Scraper Github**: https://github.com/arapfaik/scraping-glassdoor-selenium<br>
**Scraper Article**: https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905<br>
**Flask Productionization**: https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2<br>

## Webscrapping
Although benefitting from having an example project to work from, the Glassdoor scrapper was built for the US website and had to be completely overhauled. Website elements and functions (including pop-ups) were completely different.<br>
Scraped variables include:
- Company
- Job title
- Location
- Employees
- Estimated salary
- Company founded
- Company type
- Company industry
- Company sector
- Employee provided company ratings
- Company revenue

## Data cleaning
After scraping the data, it needed to be cleaned for anaylsis. The following changes were made:

- Merged multiple datasets (identicalled generated so a simple concat worked well)
- Identical listings were removed (there were thousands, Glassdoor would show same listings every few pages - possibly sponsored content)
- Parsed non-numeric data out of salary, and scaled to thousands
- Made columns for employer provided salary and hourly wages
- Removed observations without salary data
- Transformed founded date into age of company
- Made columns for if different skills were mentioned in the job description:
  - Python, R, STATA, SPSS, Excel, AWS, Spark, Jupyter
- Column for simplified job title and Seniority
- Column for description length
- Dropped some observations that had unique 'Company sector' since most were standardised apart from ~30

## EDA
The data was explored throug a selection of distribution plots, correlation analysis and pivot tables. A few highlights were extracted:<br><br>
Most salaries fell in the 40-70k range. The vertical straight lines are probably a result of converting hourly figures to annual salaries so there is a lot of exact matches.<br> 
![image](https://user-images.githubusercontent.com/65450101/217888826-9c3d1be6-48d9-45e5-8452-41230c84509a.png)<br>
There was high collinearity within the company ratings, which is one of the most consistent aspects of the dataset. This likely dimished the predictive reliability of the models.<br>
![image](https://user-images.githubusercontent.com/65450101/217881923-9077446a-c8db-462f-89b8-92df53414f44.png)<br>
Apparently some skills meant a lower salary than those without. In reality, some skills are probably more used by senior professionals or are more specialised.<br>
![image](https://user-images.githubusercontent.com/65450101/217882245-db0e76e4-9897-48e8-9744-a32072bb874f.png)<br>
Some outliers in overall company ratings from people who hate their employers but most seem satisfied.<br>
![image](https://user-images.githubusercontent.com/65450101/217882343-6b8d9d63-13d4-41a6-92b6-9ee9a9c88ae3.png)<br>
Finance professions, on average, seem pretty unhappy by most measures, business intelligence trumps most fields<br>
![image](https://user-images.githubusercontent.com/65450101/217882374-1c144393-1e38-466a-bfb4-6a11a78f2196.png)<br>
Most common words in the job descriptions - stop words may need amending<br>
![image](https://user-images.githubusercontent.com/65450101/217887695-5b6e7339-a2ea-4496-98b6-ce8a8a13d881.png)



### Model performance
First, the categorical variables were transformmed into dummy variables and the data split into train and test sets with a test set of 30%.<br>
Three models were used, with the linear regression being used as a baseline model and compared using mean absolute error.<br>
The Random Forest model outperformed the other approaches on the test and validation sets.<br>

Random Forest : MAE = 23.5<br>
Ridge Regression: MAE = 24.29<br>
Linear Regression: MAE = 29.52<br>

Due to the high multicollinearity, the errors are quite high.

