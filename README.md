# Job Scraper

A Python-based job scraper using Selenium to extract job postings from websites like Indeed. This scraper collects information such as job titles, company names, locations, and job links and saves it in a CSV file.


## Features

- Scrapes job postings from Indeed based on specified search criteria.
- Collects job titles, company names, job locations, and links.
- Saves the scraped data into a CSV file for later use.
- Uses Selenium for browsing and automating the extraction process.
- Runs in headless mode to avoid opening a browser window.


## Requirements

- Python 3.x
- Google Chrome browser
- ChromeDriver (matching the version of your Chrome browser)
- The following Python libraries:
  - `selenium`
  - `selenium-stealth`
  - `pandas`
  - `numpy`


## Installation

1. Clone the repository:
=> git clone https://github.com/D4V1ND/job_scraper

2. Install the required Python dependencies:
=> pip install -r requirements.text

3. Download the appropriate ChromeDriver for your version of Google Chrome.

4. Configure the chromedriver.exe path in the code.


## Usage

1. Open the Jobs_Scraper.py file and modify the scraper initialization with your preferred search (Example for indeed are provided)
2. Run the scraper:
=> python scraper.py
3. The scraper will start fetching job postings from the directed jobs website, navigating through the pages and extracting job details. Once finished, the data could be saved as a CSV file in the current directory.

## Output
The scraped data will be saved in a CSV file named <Website_name>-<day>-<month>-<year>
