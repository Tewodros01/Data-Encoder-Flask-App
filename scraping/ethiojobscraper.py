import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time

from normalize_scraped_job import normalize_job_data
from ethiojobNormilizer import save_to_excel

predefinedSectors = [
  "Accounting and Finance",
  "Admin, Secretarial and Clerical",
  "Agriculture",
  "Architecture and Construction",
  "Automotive",
  "Banking and Insurance",
  "Business and Administration",
  "Business Development",
  "Communications, PR and Journalism",
  "Consultancy and Training",
  "Creative Arts",
  "Customer Service",
  "Development and Project Management",
  "Economics",
  "Education",
  "Engineering",
  "Environment and Natural Resource",
  "Event Management",
  "Manufacturing",
  "Health Care",
  "Hotel and Hospitality",
  "Human Resource and Recruitment",
  "Information Technology",
  "Legal",
  "Logistics, Transport and Supply Chain",
  "Management",
  "Natural Sciences",
  "Pharmaceutical",
  "Purchasing and Procurement",
  "Quality Assurance",
  "Research and Development",
  "Retail, Wholesale and Distribution",
  "Sales and Marketing",
  "Security",
  "Social Sciences and Community",
  "IT, Computer Science and Software Engineering",
  "Telecommunications",
  "Warehouse, Supply Chain and Distribution",
  "Water and Sanitation"
]

category_urls = [
    "https://ethiojobs.net/jobs?search=Accounting+and+Finance&page=1",
    # "https://ethiojobs.net/jobs?search=Admin%2C+Secretarial%2C+and+Clerical&page=1",
    # "https://ethiojobs.net/jobs?search=Agriculture&page=1",
    # "https://ethiojobs.net/jobs?search=Architecture+and+Construction&page=1",
    # "https://ethiojobs.net/jobs?search=Automotive&page=1",
    # "https://ethiojobs.net/jobs?search=Banking+and+Insurance&page=1",
    # "https://ethiojobs.net/jobs?search=Business+and+Administration&page=1",
    # "https://ethiojobs.net/jobs?search=Business+Development&page=1",
    # "https://ethiojobs.net/jobs?search=Communications%2C+Media+and+Journalism&page=1",
    # "https://ethiojobs.net/jobs?search=Consultancy+and+Training&page=1",
    # "https://ethiojobs.net/jobs?search=Creative+Arts&page=1",
    # "https://ethiojobs.net/jobs?search=Customer+Service&page=1",
    # "https://ethiojobs.net/jobs?search=Development+and+Project+Management&page=1",
    # "https://ethiojobs.net/jobs?search=Economics&page=1",
    # "https://ethiojobs.net/jobs?search=Education&page=1",
    # "https://ethiojobs.net/jobs?search=Engineering&page=1",
    # "https://ethiojobs.net/jobs?search=Environment+and+Natural+Resource&page=1",
    # "https://ethiojobs.net/jobs?search=Event+Management&page=1",
    # "https://ethiojobs.net/jobs?search=FMCG+and+Manufacturing&page=1",
    # "https://ethiojobs.net/jobs?search=Health+Care&page=1",
    # "https://ethiojobs.net/jobs?search=Hotel+and+Hospitality&page=1",
    # "https://ethiojobs.net/jobs?search=Human+Resource+and+Recruitment&page=1",
    # "https://ethiojobs.net/jobs?search=IT%2C+Computer+Science+and+Software+Engineering&page=1",
    # "https://ethiojobs.net/jobs?search=Legal&page=1",
    # "https://ethiojobs.net/jobs?search=Logistics%2C+Transport+and+Supply+Chain&page=1",
    # "https://ethiojobs.net/jobs?search=Management&page=1",
    # "https://ethiojobs.net/jobs?search=Natural+Sciences&page=1",
    # "https://ethiojobs.net/jobs?search=Pharmaceutical&page=1",
    # "https://ethiojobs.net/jobs?search=Purchasing+and+Procurement&page=1",
    # "https://ethiojobs.net/jobs?search=Quality+Assurance&page=1",
    # "https://ethiojobs.net/jobs?search=Research+and+Development&page=1",
    # "https://ethiojobs.net/jobs?search=Retail%2C+Wholesale+and+Distribution&page=1",
    # "https://ethiojobs.net/jobs?search=Sales+and+Marketing&page=1",
    # "https://ethiojobs.net/jobs?search=Security&page=1",
    # "https://ethiojobs.net/jobs?search=Social+Sciences+and+Community+Service&page=1",
    # "https://ethiojobs.net/jobs?search=Technology&page=1",
    # "https://ethiojobs.net/jobs?search=Telecommunications&page=1",
    # "https://ethiojobs.net/jobs?search=Warehouse%2C+Supply+Chain+and+Distribution&page=1",
    # "https://ethiojobs.net/jobs?search=Water+and+Sanitation&page=1"
]


def scrape_jobs_by_category(category_url):
    driver = webdriver.Chrome()
    driver.get(category_url)

    try:
        # Wait for the page to fully load
        WebDriverWait(driver, 120).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        # Additional wait to handle splash screen or dynamic loading elements
        time.sleep(10)
        # Wait until the specific job container div is present
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.mui-style-isbt42'))
        )
    except TimeoutException:
        print("Page load timed out.")
        driver.quit()
        return []

    jobs = []

    try:
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
                print(f"Error parsing job card retry")
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

        # Wait for specific elements to load
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p'))
        )

        about_job = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-17sbmss').text
        about_you = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-pdximt').text
        required_skills = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 ul.MuiList-root.MuiList-padding').text
        how_to_apply = driver.find_element(By.CSS_SELECTOR, 'div.MuiGrid-item.MuiGrid-grid-xs-12 p.MuiTypography-root.MuiTypography-body1.mui-style-pdximt').text

        job_details["job_description"] = f"about_job: {about_job}\nabout_you: {about_you}\nrequired_skills: {required_skills}\nhow_to_apply: {how_to_apply}"
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

        # try:
        #     job_details['deadline'] = sidebar.find_element(By.XPATH, ".//p[contains(text(), 'Deadline')]/following-sibling::p").text
        # except NoSuchElementException:
        #     job_details['deadline'] = "N/A"
        #     print("Deadline element not found")

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

    print(f"All Job Listings: {json.dumps(all_jobs_by_category, indent=4)}")

    save_to_excel(all_jobs_by_category)

if __name__ == "__main__":
    main()
