import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Selenium WebDriver (Make sure chromedriver is in your PATH)
driver = webdriver.Chrome()

# URL of the job list
url = "https://www.behance.net/joblist?tracking_source=nav20"

# Open the webpage
driver.get(url)

# Wait for the dynamic content to load
time.sleep(5)  # Adjust time if necessary

# Initialize a list to store job details
job_listings = []

# Function to scrape job details from the modal
def scrape_job_details():
    modal_html = driver.page_source
    modal_soup = BeautifulSoup(modal_html, 'html.parser')

    job_detail = {}
    job_detail['title'] = modal_soup.select_one('.JobDetailContent-headerTitle-rlk').text.strip()
    job_detail['company'] = modal_soup.select_one('.JobDetailContent-companyNameLink-EUx').text.strip()
    job_detail['location'] = modal_soup.select_one('.JobDetailContent-companyEmDash-Hkf').next_sibling.strip()
    job_detail['description'] = modal_soup.select_one('.JobDetailContent-jobContent-Nga').text.strip()

    details = modal_soup.select('.JobDetailContent-detailItem-nks')
    for detail in details:
        title = detail.select_one('.JobDetailContent-detailTitle-MCn').text.strip()
        text = detail.select_one('.JobDetailContent-detailText-Fmk').text.strip()
        job_detail[title] = text

    return job_detail

# Get all job cards
job_cards = driver.find_elements(By.CSS_SELECTOR, '.JobCard-jobCard-mzZ')

for index, card in enumerate(job_cards):
    # Scroll the job card into view
    driver.execute_script("arguments[0].scrollIntoView(true);", card)
    time.sleep(1)  # Ensure the scroll action completes

    # Use JavaScript to click the job card with retries
    retries = 3
    for attempt in range(retries):
        try:
            # More specific click to avoid intercepted clicks
            link = card.find_element(By.CSS_SELECTOR, '.JobCard-jobCardLink-Ywm')
            driver.execute_script("arguments[0].click();", link)
            break
        except Exception as e:
            print(f"Retry {attempt + 1} clicking card due to error: {e}")
            time.sleep(1)
    else:
        print(f"Failed to click card after {retries} retries.")
        continue

    # Wait for the modal to appear
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.JobDetailContent-jobDetailContainer-LyM')))
    except Exception as e:
        print(f"Error waiting for modal: {e}")
        continue

    # Scrape job details from the modal
    job_details = scrape_job_details()
    job_listings.append(job_details)

    # Close the modal
    try:
        close_button = driver.find_element(By.CSS_SELECTOR, '.UniversalPopup-closeButton-gx_')
        driver.execute_script("arguments[0].click();", close_button)
    except Exception as e:
        print(f"Error closing modal: {e}")
        continue

    # Wait for the modal to close
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '.JobDetailContent-jobDetailContainer-LyM')))

    # Add a short wait to ensure stability
    time.sleep(1)

# Print the job listings
for job in job_listings:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Description: {job['description']}")
    for key, value in job.items():
        if key not in ['title', 'company', 'location', 'description']:
            print(f"{key}: {value}")
    print("------")

# Close the browser
driver.quit()
