from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,TimeoutException
from bs4 import BeautifulSoup
import time

dge_driver_path = "C:\\Users\\hp\\Downloads\\edgedriver\\msedgedriver.exe"
service = Service(executable_path=dge_driver_path)

options = Options()
options.add_argument('--headless') 
options.add_argument('--disable-gpu') 
options.add_argument('--window-size=1920x1080')

driver = webdriver.Edge(service=service, options=options)

result=[]

def extract_jobs():
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        job_result = soup.find_all('div', class_='table-td table-title')

        for job in job_result:
            job_result=job.find('div')
            if job_result:
                result.append(job_result)


try:
    driver.get('https://www.capgemini.com/careers/join-capgemini/job-search/?size=30')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'table-td'))
    )

    extract_jobs()
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@aria-label, "Load More about jobs")]'))  
            )
            if load_more_button.is_displayed():
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(2) 
                extract_jobs()
            else:
                print("Load More button is not visible. Ending data load.")
                break
            extract_jobs()
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            print("No more data to load or Load More button not found.")
            break 
finally:
    driver.quit()    
