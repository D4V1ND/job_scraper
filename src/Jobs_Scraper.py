from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import numpy as np
from selenium_stealth import stealth
import pandas as pd
from datetime import datetime
import re

class job_scraper:
    """
    A Job scraper that extracts job postings from job websites like indeed using Selenium
    """
    def __init__(self, website, driver_path, container_xpath, title_xpath, link_xpath, company_xpath, location_xpath, csv_save):
        """
        Initializes the job scraper.

        website         : The URL of the job website, that is to be scraped,
        driver_path     : Path to the executable Chrome Webdriver,
        container_xpath : XPATH for the job container elements,
        title_xpath     : XPATH for job titles,
        link_xpath      : XPATH for job links,
        company_xpath   : XPATH for company names,
        location_xpath  : XPATH for job locations     
        csv_save        : True for saving scraped data in a csv file
        """
        self.website = website
        self.driver_path = driver_path
        self.options = self._set_chrome_options()
        self.driver = self._init_driver()
        self.container_xpath = container_xpath
        self.title_xpath = title_xpath
        self.link_xpath = link_xpath
        self.company_xpath = company_xpath
        self.location_xpath = location_xpath
        self.csv_save = csv_save

    def _set_chrome_options(self):
        options1 = Options()
        options1.add_argument("--headless")  # Run in headless mode
        options1.add_argument("--window-size=1920,1080")  # Fix window size
        options1.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36") #Add User-Agent
        options1.add_argument("--disable-blink-features=AutomationControlled") #To avoid being detected as a bot
        return options1
    
    def _init_driver(self):
        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=self.options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
        )
        return driver
    
    def accept_cookie(self, button):
        try:
            wait = WebDriverWait(self.driver, 60) 
            accept = wait.until(EC.element_to_be_clickable((By.XPATH, button))) #Wait until the cookie button is clickable (maximal 60 seconds)
            ActionChains(self.driver).move_to_element(accept).click().perform()
        except Exception as e:
            print(f"Error  : {e}")

    def next_page(self, page_button):
        try:
            wait = WebDriverWait(self.driver, 38)
            next = wait.until(EC.element_to_be_clickable((By.XPATH, page_button)))
            ActionChains(self.driver).move_to_element(next).click().perform()
            print(f"Navigating to the next page...") 
        except Exception as e:
            print(f"Error : {e}")

    def count_page(self, count_button):
        page_container = self.driver.find_elements(By.XPATH, count_button)
        HTML_label = list(map(lambda x : x.get_attribute("outerHTML"), page_container))
        return list(map(lambda x : x.isnumeric(), list(map(lambda x: x.text, page_container)))).count(True)

    def get_job(self):
        job_list = list()
        for _ in range(3): 
            try:
                x_container = self.driver.find_elements(By.XPATH, self.container_xpath)
                for x in x_container:
                    try:
                        job_title = x.find_element(By.XPATH, self.title_xpath).text
                        job_link = x.find_element(By.XPATH, self.link_xpath).get_attribute("href")
                        company_name = x.find_element(By.XPATH, self.company_xpath).text
                        job_location = x.find_element(By.XPATH, self.location_xpath).text
                        job_list.append({"Title": job_title, 
                                        "Company": company_name,
                                        "location": job_location,
                                        "link": job_link})

                    except Exception as e:
                        print(f"Error fetching job details: {e}")
                break
            except StaleElementReferenceException:
                print("Stale Element not found : Retrying...")
        return job_list
    
    def save_to_csv(self, job_list):
        try:
            time_now = datetime.now()
            day = time_now.strftime("%d")
            month = time_now.strftime("%m")
            year = time_now.strftime("%Y")
            web_name = re.findall("(?<=\.).*(?=\.com)", self.website)
            file_name = f'{web_name[0]}-{day}-{month}-{year}.csv'
            df = pd.DataFrame(job_list)
            df.to_csv(file_name, index=False, encoding='utf-8')
            print(f"Data has been written to {file_name}")
        except Exception as e:
            print(f"Error : {e}")
    
    def run(self):
        self.driver.get(self.website)
        self.accept_cookie("//button[contains(text(), 'Alle Cookies')]")
        ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH, "//button[contains(text(), 'Alle Cookies')]")).perform()
        job_list = list()
        for i in range(self.count_page("//li[@class='css-1v1l206 eu4oa1w0']/a")):
            time.sleep(np.random.randint(5))
            if(self.driver.find_elements(By.XPATH, "//main[@class='error']") != []):
                continue
            self.next_page(f"//li[@class='css-1v1l206 eu4oa1w0']/a[contains(text(), '{i+1}' )]")
            container = self.get_job()
            WebDriverWait(self.driver, 10)
            job_list = job_list + container
        if(self.csv_save == True):
            self.save_to_csv(job_list)
        self.driver.quit()
        print(job_list)

#Configure the chromedriver.exe path here
path_to_chromedriver = ""
indeed_scraper = job_scraper("https://de.indeed.com/Jobs?q=werkstudent+informatik&l=m%C3%BCnchen&radius=50&vjk=3e48b496ee7d94a8",
                             path_to_chromedriver,
                             "//tr/td[@class='resultContent css-lf1alc eu4oa1w0'][div[h2]]",
                             ".//h2/a/span[contains(text(), 'Werkstudent')]",
                             ".//h2/a",
                             ".//div/div/span[@data-testid='company-name']",
                             ".//div/div[@data-testid='text-location']", True
                             )

indeed_scraper.run()
