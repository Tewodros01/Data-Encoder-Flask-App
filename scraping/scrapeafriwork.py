import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pyperclip

from normalizeafriwork import normalize_and_save_jobs

def login(driver, email, password):
    driver.get("https://afriworket.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username or Email"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Username or Email"]').send_keys(email)
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    WebDriverWait(driver, 10).until(EC.url_changes("https://afriworket.com/login"))
    print("Logged in successfully")

def select_account(driver):
    driver.get("https://afriworket.com/company-type?login=true")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".botornew")))
    try:
        job_seeker_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="radio"]#job-seeker'))
        )
        job_seeker_radio.click()
        choose_account_button = driver.find_element(By.CSS_SELECTOR, 'button[type="buton"]')
        driver.execute_script("arguments[0].removeAttribute('disabled')", choose_account_button)
        choose_account_button.click()
        WebDriverWait(driver, 10).until(EC.url_changes("https://afriworket.com/company-type?login=true"))
        print("Account selected successfully")
    except Exception as e:
        print(f"Error selecting account: {e}")

# Function to scrape sectors and job types
def scrape_filters(driver):
    filters = {'sectors': [], 'job_types': []}

    # Click "see more" buttons to reveal all filters
    see_more_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'see more')]")
    for button in see_more_buttons:
        button.click()
        time.sleep(1)

    # Scrape sectors
    sector_checkboxes = driver.find_elements(By.XPATH, "//h6[contains(text(), 'Sectors')]/following-sibling::div//input[@type='checkbox']")
    for checkbox in sector_checkboxes:
        sector = checkbox.get_attribute('value')
        filters['sectors'].append(sector)

    # Scrape job types
    job_type_checkboxes = driver.find_elements(By.XPATH, "//h6[contains(text(), 'Job Type')]/following-sibling::div//input[@type='checkbox']")
    for checkbox in job_type_checkboxes:
        job_type = checkbox.get_attribute('value')
        filters['job_types'].append(job_type)

    return filters

# Function to scrape job detail based on job element
def scrape_job_details(driver):
    job_details = {}
    try:
        # Ensure the sidebar is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".single-job.ant-drawer.ant-drawer-right.ant-drawer-open")))

        sidebar = driver.find_element(By.CSS_SELECTOR, ".single-job.ant-drawer.ant-drawer-right.ant-drawer-open")

        # Locate the job description using a specific selector
        description_element = sidebar.find_element(By.CSS_SELECTOR, "div[style='word-break: break-all; white-space: pre-line;']")
        job_description = description_element.text.strip()

# Extract job info
        job_info_elements = sidebar.find_elements(By.CSS_SELECTOR, "div.grid.grid-cols-1.gap-2.md\\:gap-4 div.my-3.capitalize")
        job_info = {}
        for element in job_info_elements:
            key_element = element.find_element(By.CSS_SELECTOR, "span.font-medium")
            value_element = element.find_element(By.CSS_SELECTOR, "span:not(.font-medium)")
            key = key_element.text.replace(":", "").strip()
            value = value_element.text.strip()
            job_info[key] = value

         # Format job info as a single string
        job_info_string = "\n".join([f"{key}: {value}" for key, value in job_info.items()])

        # Combine job description and job info
        combined_job_description = f"{job_description}\n\n{job_info_string}"
        job_details['job_description'] = combined_job_description

        print(f"Job Description",combined_job_description )
        # Extract skills
        skills_elements = sidebar.find_elements(By.CSS_SELECTOR, "div.flex.flex-wrap div span.ant-tag")
        skills = [element.text.strip() for element in skills_elements]
        job_details['skills'] = skills

        print(f"Skills", skills)

        share_button = sidebar.find_element(By.CSS_SELECTOR, ".mdi-share")
        driver.execute_script("arguments[0].click();", share_button)

        time.sleep(2)
        # Click the copy button
        copy_button = sidebar.find_element(By.CSS_SELECTOR, ".mdi-content-copy")
        driver.execute_script("arguments[0].click();", copy_button)

        # Get the URL from the clipboard
        time.sleep(1)  # Wait for clipboard to update
        job_details['apply_url'] = pyperclip.paste()

        time.sleep(2)
        driver.execute_script("arguments[0].click();", share_button)
        time.sleep(2)

    except NoSuchElementException as e:
        print(f"Error scraping job details: {e}")
    return job_details

# Function to scrape job listings based on filters
def scrape_jobs(driver, sector, job_type):
    # Apply filters
    sector_checkbox = driver.find_element(By.CSS_SELECTOR, f"input[value='{sector}']")
    job_type_checkbox = driver.find_element(By.CSS_SELECTOR, f"input[value='{job_type}']")

    driver.execute_script("arguments[0].click();", sector_checkbox)
    driver.execute_script("arguments[0].click();", job_type_checkbox)

    # Click the filter button
    filter_button_selector = ".bg-primary.my-4.rounded.px-4.py-1.text-sm.text-white:not(.cursor-not-allowed)"
    try:
        filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, filter_button_selector)))
        driver.execute_script("arguments[0].click();", filter_button)
        print("Filter button clicked")
    except TimeoutException as e:
        print("Filter button not found or not clickable:", e)
    # filter_button = driver.find_element(By.CSS_SELECTOR, "button.bg-primary")
    # driver.execute_script("arguments[0].click();", filter_button)
    time.sleep(2)

    # Scrape jobs
    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='tabpanel'] div.cursor-pointer")
    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, "h3").text
        job_company = job_element.find_elements(By.CSS_SELECTOR, "div.job-footer")[0].text
        post_date = job_element.find_elements(By.CSS_SELECTOR, "div.job-footer")[1].text
        job_location = job_element.find_elements(By.CSS_SELECTOR, "div.job-footer")[2].text
        job_description = job_element.find_element(By.CSS_SELECTOR, "p span[id^='description']").text

        # Handling experience level
        experience_level_elements = job_element.find_elements(By.CSS_SELECTOR, "div.flex.flex-col > span.font-medium")
        if len(experience_level_elements) > 1:
            experience_level = experience_level_elements[1].text.strip()
        else:
            experience_level = "Not specified"

        # Handling salary
        salary_elements = job_element.find_elements(By.CSS_SELECTOR, "div.flex.flex-col > span.font-medium.text-primary")
        if salary_elements:
            salary = salary_elements[0].text.strip()
        else:
            salary = "Not specified"

        # Handling application deadline
        deadline_elements = job_element.find_elements(By.XPATH, ".//span[contains(text(),'Deadline')]")
        if deadline_elements:
            application_deadline = deadline_elements[0].text.replace("Deadline: ", "").strip()
        else:
            application_deadline = "Not specified"

        job_type = job_element.find_element(By.CSS_SELECTOR, ".skill-chip.capitalize").text

        job_element.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".single-job.ant-drawer.ant-drawer-right.ant-drawer-open")))
        job_details = scrape_job_details(driver)

        jobs.append({
            'job_title': job_title,
            'company_name': job_company,
            'location': job_location,
            'job_description': job_description,
            'skills': job_details.get('skills', ''),
            'experience_level': experience_level,
            'salary': salary,
            'application_deadline': application_deadline,
            'job_type': job_type,
            'post_date': post_date,
            'job_apply_url': job_details.get('apply_url', 'Not specified'),
            'job_description': job_details.get('job_description', job_description)
        })

        # Click the back button to close the right sidebar
        back_button = driver.find_element(By.CSS_SELECTOR, "div.drawer-header-title h3.text-primary")
        driver.execute_script("arguments[0].click();", back_button)
    # Reset filters
    driver.execute_script("arguments[0].click();", sector_checkbox)
    driver.execute_script("arguments[0].click();", job_type_checkbox)
    time.sleep(2)

    return jobs

def main():
    email = "tekilzegiyorgis@gmail.com"  # Add your email here
    password = "P@ssw0rd!!"

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = False  # Run in headless mode for debugging, set to False
    options.add_argument("--window-size=1920,1000")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        login(driver, email, password)
        select_account(driver)
        # Scrape filters
        filters = scrape_filters(driver)
        all_jobs = []
        # Scrape jobs for each sector and job type
        for sector in filters['sectors'][:2]:
            for job_type in filters['job_types'][:2]:
                jobs = scrape_jobs(driver, sector, job_type)
                all_jobs.append({'sector': sector, 'jobtype': job_type, 'joblist': jobs})
                print(f"All Job: {all_jobs}")
    finally:
        driver.quit()

    # Save results to JSON
    normalize_and_save_jobs(all_jobs)

if __name__ == "__main__":
    main()
