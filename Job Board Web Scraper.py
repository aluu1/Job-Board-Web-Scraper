from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pyautogui import *
import pyautogui as pya
import time
import datetime as date
import pyperclip as pyc
import os
import gspread
print('Import complete')
mousepos = pya.position()

#Target focus on browser
pya.moveTo(360, 424)
time.sleep(.1)
pya.mouseDown(button='left')
pya.mouseUp(button='left')
time.sleep(.1)
#Hotkey to copy URL
pya.hotkey('alt', 'd')
pya.hotkey('ctrl', 'c')
#Move cursor back to original position
pya.moveTo(mousepos)
print('Physical inputs complete')

url = pyc.paste()

if 'glassdoor' in url:
    website = 'Glassdoor'
elif 'indeed' in url:
    website = 'Indeed'

# Indeed xpaths
jobtitle_xpath = '//*[@id="viewJobSSRRoot"]/div[2]/div/div[4]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/h1/span'
jobtitle_xpath2 = '//*[@id="viewJobSSRRoot"]/div[2]/div/div[4]/div/div/div[1]/div[1]/div[3]/div[1]/div[1]/h1/span'
company_xpath = '//*[@id="viewJobSSRRoot"]/div[2]/div/div[4]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div'
company_xpath2 = '//*[@id="viewJobSSRRoot"]/div[2]/div/div[4]/div/div/div[1]/div[1]/div[3]/div[1]/div[2]/div/div/div/div[1]/div[1]'
salary_xpath = '//*[@id="salaryInfoAndJobType"]/span[1]'
salary_xpath2 = '//*[@id="salaryInfoAndJobType"]/span[1]'
salary_xpath3 = '//*[@id="salaryGuide"]/ul/li[2]'

# Glassdoor xpaths
jobtitle_xpath3 = '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]'
company_xpath3 = '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[1]/div'
salary_xpath4 = '//*[@id="PageContent"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[4]/span'
print('Xpath assignments complete')

browser = webdriver.Chrome()

browser.get(url)

time.sleep(6)
WebDriverWait(browser, 6)
print('Scraping...')
if website == 'Indeed':
    try:
        browser.find_element(By.XPATH, jobtitle_xpath)
        jobtitle_text = browser.find_element(By.XPATH, jobtitle_xpath).text;
    except:
        browser.find_element(By.XPATH, jobtitle_xpath2)
        jobtitle_text = browser.find_element(By.XPATH, jobtitle_xpath2).text;
    finally:
        print(jobtitle_text)

    try:
        browser.find_element(By.XPATH, company_xpath)
        company_text = browser.find_element(By.XPATH, company_xpath).text;
    except:
        browser.find_element(By.XPATH, company_xpath2)
        company_text = browser.find_element(By.XPATH, company_xpath2).text;
    finally:
        print(company_text)

    try:
        browser.find_element(By.XPATH, salary_xpath)
        salary_text = browser.find_element(By.XPATH, salary_xpath).text;
    except:
        try:
            browser.find_element(By.XPATH, salary_xpath2)
            salary_text = browser.find_element(By.XPATH, salary_xpath2).text;
        except:
            browser.find_element(By.XPATH, salary_xpath3)
            salary_text = browser.find_element(By.XPATH, salary_xpath3).text;
    finally:
        print(salary_text)

elif website == 'Glassdoor':
    try:
        browser.find_element(By.XPATH, jobtitle_xpath3)
        jobtitle_text = browser.find_element(By.XPATH, jobtitle_xpath3).text;
    except:
        print('glassdoor job title xpath failed')
    finally:
        print(jobtitle_text)    
    
    try:
        browser.find_element(By.XPATH, company_xpath3)
        company_text = browser.find_element(By.XPATH, company_xpath3).text;
        company_text = company_text[:-6] #Deletes the star rating
    except:
        print('glassdoor company name xpath failed')
    finally:
        print(company_text)

    try:
        browser.find_element(By.XPATH, salary_xpath4)
        salary_text = browser.find_element(By.XPATH, salary_xpath4).text;
    except:
        print('glassdoor salary xpath failed')
    finally:
        print(salary_text)
print('Scraping complete')

jobtitle_text = jobtitle_text.replace('/', '-') # Replaces '/' for file name
jobtitle_text = jobtitle_text.replace("\\", '-')

print('Creating folder...')

# Creates folder on desktop named 'Job Apps' if it does not exist
path = "C:/Users/" + os.getlogin() +"/Desktop/Job Apps/"
if not os.path.exists(path):
    os.mkdir(path)
# Creates job application folder in this format: Company Name - Job Title
fullpathname = path + str(company_text) + ' - ' + str(jobtitle_text)
os.mkdir(fullpathname)
print('Folder created')

# Date Applied
now = date.datetime.now()
today = now.strftime('%m/%d/%Y')

sa = gspread.service_account(filename = 'C:/Users/' + os.getlogin() + '/[file name].json')
sh = sa.open("Job Apps")
wks = sh.worksheet("Sheet1")

# Iterate to see which row is empty on Google Sheet
i = 1
while wks.cell(i,1).value != None:
     i = i + 1

print('Updating Google Sheet...')
# Populates Google Sheet row based on information extracted
wks.update_cell(i,1, i-1) #Row number
wks.update_cell(i,2, company_text) #Company Name
wks.update_cell(i,3, jobtitle_text) #Job title
wks.update_cell(i,4, today) #Today's date
wks.update_cell(i,6, website) #Website applied on name

if website == 'Indeed':
    wks.update_cell(i,7, salary_text)
elif website == 'Glassdoor':
    wks.update_cell(i,8, salary_text)

if website == 'Indeed':
    wks.update_cell(i,10, url) # If website is Indeed update column 10
elif website == 'Glassdoor':
    wks.update_cell(i,11, url) # If website is Glassdoor update column 11
print('Google Sheet updated')

print('Script Done')