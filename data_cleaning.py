# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:49:29 2024

@author: DELL
"""

import pandas as pd 

df = pd.read_csv('glassdoor_jobs.csv')

#parsing of salary ( retaining only relevant figures )
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0) #adding a column for hourly salary
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0) #adding a column for emplyer provided salary

df = df[df['Salary Estimate'] != '-1'] #removing data with irrelevant salary
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]) #removing text 'Glassdoor Estimates' from salary column
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$','')) #remove currency symbol

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#adding a field corresponding to company name, no ratings
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3], axis = 1)

#adding a field corresponding to the state where the job is  
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1) #if headquarters of the company and the respective job location are the same, assign 1 else 0

#age of company 
df['age'] = df.Founded.apply(lambda x: x if x <1 else 2020 - x) #current year - founding year


#parsing of job description( eg : python, etc.)

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 
#r studio 
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

#spark 
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()

#aws 
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()

#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

#math
df['math'] = df['Job Description'].apply(lambda x: 1 if 'math' in x.lower() else 0)
df.excel.value_counts()

#engineering
df['engineering'] = df['Job Description'].apply(lambda x: 1 if 'engineering' in x.lower() else 0)
df.excel.value_counts()

#excel
df['data analysis'] = df['Job Description'].apply(lambda x: 1 if 'data analysis' in x.lower() else 0)
df.excel.value_counts()

#excel
df['AI'] = df['Job Description'].apply(lambda x: 1 if 'artificial intelligence' in x.lower() else 0)
df.excel.value_counts()

df.columns

df_out = df.drop(['Unnamed: 0'], axis =1)

df_out.to_csv('salary_data_cleaned.csv',index = False)