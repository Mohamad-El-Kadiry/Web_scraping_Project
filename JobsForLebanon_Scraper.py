import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from datetime import datetime
import os


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
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "srapi_wp_ajax_get_jobs_button")))

            if "disabled" in button.get_attribute("class") or button.get_attribute("disabled"):
                print("All jobs loaded. Exiting loop.")
                break

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            print("Clicking 'Load More Jobs' button...")
            button.click()
            time.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
            break


def scrape_JobsForLebanon_page(driver):
    jobs = []
    click_load_more(driver)  # Load all job listings

    job_elements = driver.find_elements(By.CLASS_NAME, "catalogue-job")

    for job in job_elements:
        try:
            job_type = job.find_element(By.CLASS_NAME, "catalogue-job-department-text").text.strip()
        except:
            job_type = "N/A"

        try:
            job_title = job.find_element(By.CLASS_NAME, "catalogue-job-title-text").text.strip()
        except:
            job_title = "N/A"

        try:
            job_location = job.find_element(By.CLASS_NAME, "catalogue-job-location-text").text.strip()
        except:
            job_location = "N/A"

        try:
            job_details = job.find_elements(By.CLASS_NAME, "job-meta")
            job_nature = " ".join([detail.text.strip() for detail in job_details if detail.text.strip()])
        except:
            job_nature = "N/A"

        try:
            job_link = job.get_attribute("data-href").strip()
        except:
            job_link = "N/A"

        # Append job data to the list
        jobs.append({
            "Job Type": job_type,
            "Job Title": job_title,
            "Location": job_location,
            "Job Nature": job_nature,
            "Job Link": job_link,
            "Scraped Date (DD-MM-YYYY)": datetime.now().strftime("%d-%m-%Y")  # Ensure date is recorded
        })

    return jobs


# Initialize WebDriver
driver = setup_driver()

url = "https://www.jobsforlebanon.com/search/?function=latest#results"
driver.get(url)

time.sleep(5)  # Wait for the page to load

# Scrape job data
new_data = scrape_JobsForLebanon_page(driver)

# Convert to DataFrame
df_new = pd.DataFrame(new_data)

# Check if CSV file exists
csv_file = "JobsForLebanon.csv"
if os.path.exists(csv_file):
    df_existing = pd.read_csv(csv_file, encoding="utf-8")

    # Ensure date column is correctly formatted before merging
    if "Scraped Date (DD-MM-YYYY)" not in df_existing.columns:
        df_existing["Scraped Date (DD-MM-YYYY)"] = ""

    df_combined = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates(subset=["Job Title", "Job Link"],
                                                                                      keep="last")
else:
    df_combined = df_new

# Ensure the Scraped Date column is NOT empty
df_combined["Scraped Date (DD-MM-YYYY)"].fillna(datetime.now().strftime("%d-%m-%Y"), inplace=True)

# Save updated data to CSV
df_combined.to_csv(csv_file, index=False, encoding="utf-8")

print("Scraping complete. Data saved to JobsForLebanon.csv")

# Close WebDriver
driver.quit()
