from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time

from normalize_scraped_job import normalize_job_data

predefinedSectors = [
  "Accounting, Finance, and Insurance",
  "Administrative and Secretarial Services",
  "Advertising, Media Journalism and Public Relations",
  "Agriculture, Forestry, and Environmental Science",
  "Architecture, Design, and Construction",
  "Engineering and Technology",
  "Banking, Investment and Insurance",
  "Business and Management",
  "Law, Legal Services, and Public Administration",
  "Communications, Marketing, and Sales",
  "Human Resources, Recruitment, and Organizational Development",
  "Consultancy, Training and Education",
  "Creative Arts, Event Management and Entertainment",
  "Hospitality, Tourism, and Customer Service",
  "Product, Program, and Project Management",
  "Natural and Social Sciences",
  "Health and Wellness",
  "Retail, Wholesale, and Inventory Management",
  "Logistics, Supply Chain, and Transportation",
  "Manufacturing and Production",
  "Quality Assurance, Safety, and Compliance",
  "Product Development",
  "Unknown Sector"
];

category_urls = [
    "https://ethiojobs.net/jobs?search=Accounting+and+Finance&page=1",
    # "https://ethiojobs.net/jobs?search=Admin%2C+Secretarial%2C+and+Clerical&page=1",
    # "https://ethiojobs.net/jobs?search=Water+and+Sanitation&page=1",
    # "https://ethiojobs.net/jobs?search=Agriculture&page=1"
]


def scrape_jobs_by_category(category_url):
    driver = webdriver.Chrome()
    driver.get(category_url)
    WebDriverWait(driver, 120).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    jobs = []

    try:
        time.sleep(10)
        job_cards = WebDriverWait(driver, 120).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.jobcardcontainer .MuiPaper-root'))
        )
    except TimeoutException:
        print("No job cards found.")
        job_cards = []

    for card in job_cards:
        retry_count = 3
        while retry_count > 0:
            try:
                job_title = card.find_element(By.CSS_SELECTOR, 'p.MuiTypography-root.MuiTypography-body1.MuiTypography-alignLeft.mui-style-sz2p1p').text
                company_name = card.find_element(By.CSS_SELECTOR, 'p.MuiTypography-root a').text
                location = card.find_element(By.CSS_SELECTOR, '.MuiSvgIcon-root[data-testid="LocationCityIcon"] + p').text
                posted_date = card.find_element(By.CSS_SELECTOR, 'p.MuiTypography-root.MuiTypography-body1.mui-style-1vlcel7[style*="font-size: 12px; color: rgb(0, 0, 0); text-transform: none;"]').text
                job_url = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                deadline_elements = card.find_elements(By.CSS_SELECTOR, 'p.MuiTypography-root.MuiTypography-body1.mui-style-17n0xwk')
                deadline = "N/A"
                for elem in deadline_elements:
                    if "Deadline" in elem.text:
                        deadline = elem.text.replace("Deadline : ", "")
                        break

                job_details = scrape_job_details(job_url)

                jobs.append({
                    'job_title': job_title,
                    'company_name': company_name,
                    'location': location,
                    'posted_date': posted_date,
                    'job_url': job_url,
                    'deadline': deadline,
                    **job_details
                })
                break
            except StaleElementReferenceException:
                retry_count -= 1
                print("StaleElementReferenceException encountered. Retrying...")
            except NoSuchElementException as e:
                print(f"Error parsing job card: {e}")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

    driver.quit()
    return jobs

def scrape_job_details(job_url):
    driver = webdriver.Chrome()
    driver.get(job_url)
    WebDriverWait(driver, 120).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    job_details = {}

    try:
        current_url = driver.current_url
        if "404" in current_url or "statusCode=400" in current_url:
            print(f"404 Error: Page not found for URL: {job_url}")
            driver.quit()
            return job_details
        # Ensure specific elements are loaded
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-17sbmss'))
        )
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-pdximt'))
        )

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "sidebar"))
        )
        job_details['about_job'] = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-17sbmss').text
        job_details['about_you'] = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-pdximt').text
        job_details['required_skills'] = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 ul.MuiList-root.MuiList-padding').text
        job_details['how_to_apply'] = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-pdximt').text
        # Ensure the sidebar is fully loaded
        sidebar = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "sidebar"))
        )
        try:
            job_details['employment_type'] = sidebar.find_element(By.XPATH, ".//p[contains(text(), 'Employment Type')]/following-sibling::p").text
        except NoSuchElementException:
            job_details['employment_type'] = "N/A"
            print("Employment Type element not found")

        try:
            job_details['work_experience'] = sidebar.find_element(By.XPATH, ".//p[contains(text(), 'Work Experience')]/following-sibling::p").text
        except NoSuchElementException:
            job_details['work_experience'] = "N/A"
            print("Work Experience element not found")

        try:
            job_details['deadline'] = sidebar.find_element(By.XPATH, ".//p[contains(text(), 'Deadline')]/following-sibling::p").text
        except NoSuchElementException:
            job_details['deadline'] = "N/A"
            print("Deadline element not found")

        try:
            job_details['career_level'] = sidebar.find_element(By.XPATH, ".//p[contains(text(), 'Career Level')]/following-sibling::p").text
        except NoSuchElementException:
            job_details['career_level'] = "N/A"
            print("Career Level element not found")

        try:
            job_details['number_of_people_required'] = sidebar.find_element(By.XPATH, ".//p[contains(text(), 'Number of people required')]/following-sibling::p").text
        except NoSuchElementException:
            job_details['number_of_people_required'] = "N/A"
            print("Number of people required element not found")

        try:
            job_details['location_type'] = sidebar.find_element(By.XPATH, ".//p[contains(text(), 'Location Type')]/following-sibling::p").text
        except NoSuchElementException:
            job_details['location_type'] = "N/A"
            print("Location Type element not found")

    except NoSuchElementException as e:
        print(f"Error parsing job details: {e}")
    except TimeoutException as e:
        print(f"Timeout waiting for elements to load: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while parsing job details: {e}")

    driver.quit()
    return job_details

def main():

    all_jobs_by_category = []
    for i, category_url in enumerate(category_urls):
        print(f"\nScraping jobs from URL: {category_url}")
        jobs = scrape_jobs_by_category(category_url)

        all_jobs_by_category.append({
            "job_sector": predefinedSectors[i],
            "job_listing": jobs
        })

    for category in all_jobs_by_category:
        for job in category["job_listing"]:
            print(category)
            # normalize_job_data(job, category["job_sector"])

if __name__ == "__main__":
    main()
