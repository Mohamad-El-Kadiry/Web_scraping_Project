import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # Corrected import
from selenium.webdriver.support import expected_conditions as EC  # Corrected import


def setup_driver():
    options = Options()

    options.add_argument("--headless")  # Run browser in headless mode (no GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")  # Random UserAgent

    service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)


def click_load_more(driver):
    wait = WebDriverWait(driver, 10)  # Corrected: Create WebDriverWait instance

    while True:
        try:
            # Find the button
            button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "srapi_wp_ajax_get_jobs_button")))

            # Check if the button is disabled
            if "disabled" in button.get_attribute("class") or button.get_attribute("disabled"):
                print("All jobs loaded. Exiting loop.")
                break

            # Scroll to the button
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

            # Click the button
            print("Clicking 'Load More Jobs' button...")
            button.click()

            # Wait for 3 seconds for new jobs to load
            time.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
            break


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pandas as pd
from selenium.webdriver.common.by import By

def scrape_JobsForLebanon_page(driver):
    jobs = []

    # Click "Load More Jobs" until all jobs are loaded
    click_load_more(driver)

    # Locate all job cards on the page
    job_elements = driver.find_elements(By.CLASS_NAME, "catalogue-job")

    for job in job_elements:
        try:
            # Extract job type (Education, IT, etc.)
            job_type = job.find_element(By.CLASS_NAME, "catalogue-job-department-text").text.strip()
        except:
            job_type = "N/A"

        try:
            # Extract job title
            job_title = job.find_element(By.CLASS_NAME, "catalogue-job-title-text").text.strip()
        except:
            job_title = "N/A"

        try:
            # Extract job location (Remote or City, Country)
            job_location = job.find_element(By.CLASS_NAME, "catalogue-job-location-text").text.strip()
        except:
            job_location = "N/A"

        try:
            # Extract job nature (Part-time, Full-time, etc.)
            job_details = job.find_elements(By.CLASS_NAME, "job-meta")
            job_nature = " ".join([detail.text.strip() for detail in job_details if detail.text.strip()])
        except:
            job_nature = "N/A"

        try:
            # Extract job link from the "data-href" attribute
            job_link = job.get_attribute("data-href").strip()
        except:
            job_link = "N/A"

        # Append job data to the list
        jobs.append({
            "Job Type": job_type,
            "Job Title": job_title,
            "Location": job_location,
            "Job Nature": job_nature,
            "Job Link": job_link
        })

    # Convert job data into a Pandas DataFrame
    df = pd.DataFrame(jobs)

    # Save to CSV file
    df.to_csv("JobsForLebanon.csv", index=False, encoding='utf-8')

    return jobs


# Initialize WebDriver
driver = setup_driver()

url = "https://www.jobsforlebanon.com/search/?function=latest#results"
driver.get(url)

time.sleep(5)  # Wait for the page to load

results= scrape_JobsForLebanon_page(driver)

df =pd.DataFrame(results)
df.to_csv("JobsForLebanon.csv", index = False, encoding= 'utf-8')