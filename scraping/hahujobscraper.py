from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from hahujobNormilizer import save_to_excel


def scrape_job_detail_page(sector_url , job_index):
    try:
        # Setup WebDriver options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.headless = True  # Set to False to see the browser
        options.add_argument("--window-size=1920,1000")
        options.add_argument("--disable-gpu")

        # Install and setup ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the sector webpage
        driver.get(sector_url)
        time.sleep(5)  # Let the page load completely

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.grid.grid-cols-1'))
        )

        # Scrape the desired data
        jobs = driver.find_elements(By.CSS_SELECTOR, 'div.grid.grid-cols-1 > div')

        if job_index >= len(jobs):
            print(f"Job index {job_index} is out of range for the current sector page.")
            driver.quit()
            return {}

        # Click the "Read More" button using JavaScript
        read_more_button = jobs[job_index].find_element(By.XPATH, ".//button[contains(., 'Read More')]")
        driver.execute_script("arguments[0].click();", read_more_button)

        time.sleep(5)
        # Ensure the full page is loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'mt-8 xl:mt-28')]"))
        )

        job_details = {}

        # Extract the new page URL after clicking "Read More"
        new_url = driver.current_url

        # Scrape job title
        job_title = driver.find_element(By.XPATH, "//h3[contains(@class, 'font-extrabold')]").text
        job_details['job_title'] = job_title

        # Scrape company name
        company_name = driver.find_element(By.XPATH, "//p[contains(@class, 'text-sm') and contains(@class, 'text-base')]").text
        job_details['company_name'] = company_name

        # Scrape location
        location = driver.find_element(By.XPATH, "//div[@title='Location']/p").text
        job_details['location'] = location

        # Scrape years of experience
        experience = driver.find_element(By.XPATH, "//div[@title='Years of Experience']/p").text
        job_details['experience'] = experience

        # Scrape job type
        job_type = driver.find_element(By.XPATH, "//div[@title='Job Type']/p").text
        job_details['job_type'] = job_type

        # Scrape posted date and deadline
        posted_date = driver.find_element(By.XPATH, "//p[@title='Posted Date']").text
        deadline_date = driver.find_element(By.XPATH, "//p[@title='Expiration Date']").text
        job_details['posted_date'] = posted_date
        job_details['application_deadline'] = deadline_date

        # Scrape job description
        job_description = driver.find_element(By.ID, "job_description").text
        job_details['job_description'] = job_description

        job_details['job_apply_url'] = new_url


        # Close the driver
        driver.quit()

        return job_details
    except Exception as e:
        print(f"Error fetching or scraping the job detail page: {e}")
        driver.quit()
        return {}



def scrape_sector_detail_page(url, retries=0):
    try:
        # Setup WebDriver options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.headless = False  # Set to True for headless mode
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

        for job_index, job in enumerate(jobs):
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

                job_details = scrape_job_detail_page(url, job_index)

                job = {
                    'job_title': title,
                    'company_name': company,
                    'job_location': location,
                    'experience': experience,
                    'job__type': job_type,
                    'positions': positions,
                    **job_details
                }

                print(f'Job ', job_details)

                job_list.append(job_details)

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
            driver.quit()
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
        for sector in sectors[:1]:
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

        save_to_excel(all_jobs)

    except Exception as e:
        print(f"Error fetching or scraping the web page: {e}")

# Call the function
scrape_web_page()
