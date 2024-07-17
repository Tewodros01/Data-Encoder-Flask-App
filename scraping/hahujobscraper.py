from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_sector_detail_page(url, retries=0):
    try:
        # Setup WebDriver options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.headless = True  # Run in headless mode
        options.add_argument("--window-size=1920,1000")
        options.add_argument("--disable-gpu")

        # Install and setup ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the webpage
        driver.get(url)

        # Wait for the main job container to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.grid.grid-cols-1'))
        )

        # Scrape the desired data
        jobs = driver.find_elements(By.CSS_SELECTOR, 'div.grid.grid-cols-1 > div')
        job_list = []

        for job in jobs:
            try:
                title_element = job.find_element(By.CSS_SELECTOR, 'div.text-center.md\\:text-start > h3')
                company_element = job.find_element(By.CSS_SELECTOR, 'div.flex.flex-col.items-center.justify-start > p')
                location_element = job.find_element(By.XPATH, ".//div[contains(@title, 'Location')]/p")
                experience_element = job.find_element(By.XPATH, ".//div[contains(@title, 'Years of Experience')]/p")
                type_element = job.find_element(By.XPATH, ".//div[contains(@title, 'Job Type')]/p")
                positions_element = job.find_element(By.XPATH, ".//div[contains(@title, 'Number of Positions')]/p")

                title = title_element.text
                company = company_element.text
                location = location_element.text
                experience = experience_element.text
                job_type = type_element.text
                positions = positions_element.text

                # Click the "Read More" button using JavaScript
                read_more_button = job.find_element(By.XPATH, ".//button[contains(., 'Read More')]")
                driver.execute_script("arguments[0].click();", read_more_button)

                # Wait for the detailed job description to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div#job_description'))
                )

                # Scrape the detailed job description
                job_description_element = driver.find_element(By.CSS_SELECTOR, 'div#job_description')
                job_description = job_description_element.text

                job_list.append({
                    'Title': title,
                    'Company': company,
                    'Location': location,
                    'Experience': experience,
                    'Type': job_type,
                    'Positions': positions,
                    'Job Description': job_description
                })

                # Navigate back to the sector page
                driver.back()

                # Wait for the main job container to load again
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.grid.grid-cols-1'))
                )

            except Exception as e:
                print(f"Error extracting job details: {e}")

        # Close the driver
        driver.quit()

        return job_list
    except Exception as e:
        print(f"Error fetching or scraping the web page: {e}")
        if retries < 3:
            print("Retrying...")
            time.sleep(5)
            return scrape_sector_detail_page(url, retries + 1)
        else:
            print("Max retries reached. Exiting.")
            return []

def scrape_web_page():
    try:
        url = "https://hahu.jobs"

        # Setup WebDriver
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.headless = False  # Run in headless mode for debugging, set to True
        options.add_argument("--window-size=1920,1000")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the webpage
        driver.get(url)

        # Add a delay to allow the page to load
        time.sleep(5)

        # Scrape the desired data
        sectors = driver.find_elements(By.CSS_SELECTOR, 'section#sectors div.grid > div')

        job_sectors = []
        for sector in sectors:
            try:
                link_element = sector.find_element(By.TAG_NAME, 'a')
                title_element = sector.find_element(By.CSS_SELECTOR, 'div.text-center > p.font-body')
                open_positions_element = sector.find_element(By.CSS_SELECTOR, 'div.text-secondary > p')

                title = title_element.text
                open_positions = open_positions_element.text
                link = link_element.get_attribute('href')

                print(f"Sector: {title}, Open Positions: {open_positions}, Link: {link}")

                job_sectors.append({
                    "sector_name": title,
                    "sector_url": link,
                })
            except Exception as e:
                print(f"Error extracting sector details: {e}")

        all_jobs = []
        for sector in job_sectors[:1]:
            # Scrape details for each sector
            job_list = scrape_sector_detail_page(sector["sector_url"])
            all_jobs.append({
                "sector_name": sector["sector_name"],
                "sector_url": sector["sector_url"],
                "job_list": job_list
            })

        print(f"All Job With Sector: {all_jobs}")

        # Close the driver
        driver.quit()

    except Exception as e:
        print(f"Error fetching or scraping the web page: {e}")

# Call the function
scrape_web_page()
