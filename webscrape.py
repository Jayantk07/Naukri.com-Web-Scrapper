import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium import webdriver
import time
import os
import csv
import pandas as pd
from math import ceil
from datetime import date
import sys


#Create variables for different files and companies
global raw_csv_file 
dateTimeObj = date.today()
# Raw Data will be stored in the following file
raw_csv_file = os.getcwd()+"\\Data-Analyst_Job_Portal_Analysis"+str(dateTimeObj)+".csv"
print(raw_csv_file)
#Processed data will be stored in the following file
processed_csv_file = os.getcwd()+"\\Data-Analyst_Jobs"+str(dateTimeObj)+".csv"

# based on the below key words , search will be done on naukri.com
keywords = ["Data-Analyst"]
#The script will scrape the data Based on the below page_count variable.
page_count = 200

# Get the actual URLs with a list comprehension using the above list
# company_pages = ["https://www.naukri.com/"+keywords+"-jobs-in-hyderabad-secunderabad-secunderabad" for company in companies]
company_pages = ["https://www.naukri.com/"+keyword+"-jobs" for keyword in keywords]
print(company_pages)

#Get job title
def get_title(position):
    try:
        title=position.find_element_by_xpath('.//a[@class = "title fw500 ellipsis"]').text
        return title
    except:
        position=""
        

#Get company name
def get_companyname(position):
    try:
        company=position.find_element_by_xpath('.//a[@class = "subTitle ellipsis fleft"]').text
        return company
    except:
        company=""
        

# Get total expirence required for a particular position
def get_expirencerequired(position):
    try:
        expirence=position.find_element_by_xpath('.//li[@class = "fleft grey-text br2 placeHolderLi experience"]').text
        return expirence
    except:
        expirence=""
        

# Get expected salary
def get_salaryexpected(position):
    try:
        salary=position.find_element_by_xpath('.//li[@class = "fleft grey-text br2 placeHolderLi salary"]').text
        return salary
    except:
        salary=""
        

# Get location for that job vacancy
def get_location(position):
    try:
        location=position.find_element_by_xpath('.//li[@class = "fleft grey-text br2 placeHolderLi location"]').text
        return location
    except:
        location=""

        
# Get skills required for the job position
def get_skillsrequired(position):
    try:
        Skilldata = position.find_elements_by_xpath('.//ul[@class = "tags has-description"]')
        for individualSkills in Skilldata:
            skill = individualSkills.text.split("\n")
            return skill
    except:
        skill=""
        
        
#Get when job was posted 
def get_rquirementpublisheddate(position):
    try:
        date=position.find_element_by_xpath('.//div[@class = "type br2 fleft grey"]').text
        return date
    except:
         date=""         
         




#Here we do pagination --> go to every page and get the details
locationOfWebdriver = "E:/Downloads/Web Driver/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(locationOfWebdriver)

#Create a csv file. 
try:
    csv_file = open(raw_csv_file, 'w', encoding="UTF-8", newline="")
    writer = csv.writer(csv_file)
except Exception as e:
     sys.exit(str(e))

start = time.time()

print("********Data collection process has been started********")
#Create the column names in csv file
writer.writerow(['title', 'company', 'expirence', 'salary', 'location','skill','date'])
for page in company_pages:
    driver.get(page)
    time.sleep(3)
    print("=" * 50)  
    # Shows in terminal when a new airline is being scraped
    print("Scraping " + page)

    count = 1
    
    #Iterate the pages to get info
    while count <= page_count:
        newpage=page + "-" +str(count)
        print(newpage)
        driver.get(newpage)
        time.sleep(5)        
         # Find all the reviews:
        positions = driver.find_elements_by_xpath('//article[@class = "jobTuple bgWhite br4 mb-8"]')
        for position in positions:
            job_data={}
            title=get_title(position)
            company=get_companyname(position)
            expirence=get_expirencerequired(position)
            salary=get_salaryexpected(position)
            location=get_location(position)
            skills=get_skillsrequired(position)
            date=get_rquirementpublisheddate(position)
               
            job_data['title']=title
            job_data['company']=company
            job_data['expirence']=expirence
            job_data['salary']=salary
            job_data['location']=location
            job_data['skills']=skills
            job_data['date']=date
        
            #Write to csv file
            writer.writerow(job_data.values())
        count=count+1
            
        
print("********Data collection process has been ended********")    
csv_file.close() 
print('Time taken to collecting and write to CSV file : {} mins'.format(round((time.time() - start) / 60, 2)))