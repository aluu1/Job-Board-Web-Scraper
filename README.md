# Job-Board-Web-Scraper

The purpose of this web scraper is to help jobseekers automate the tracking of jobs that they have applied to. This script will only work on Indeed and Glassdoor.

What this script does:
1. Copies a job posting's position name, company name, current date (date applied), website name, salary, and URL onto a Google Sheet.
2. Creates a folder on user's desktop named 'Job Apps' if this folder does not exist.
3. Creates a folder to store a resume for each job in the 'Job Apps' folder with the format: 'Company Name - Position Name'

How to use:
1. Find any job on Indeed or Glassdoor
2. Open view the job (Indeed URL should be 'https://www.indeed.com/viewjob...', Glassdoor URL should be 'https://www.glassdoor.com/job-listing/...')
3. Move the job posting browser window on the left side of the main monitor.
4. Run the script and wait about 10 seconds.

How the script works:
1. The cursor will be moved to the left side of the screen, click to focus on the browser window, copy the current URL, checks the URL for 'Glassdoor' or 'Indeed,' and will assign the xpath variables accordingly.
2. Selenium will open a separate Chrome webdriver instance of the copied URL and scrape the text from the xpaths of the position name, company name, and salary.
3. OS will create the nested job folders on the desktop for each job posting to store resumes.
4. GSpread will check for the next vacant row and populate the row will the extracted information from the job posting.

Libraries used:
Selenium, GSpread, Datetime, Time, Pyautogui, OS, Pyperclip
