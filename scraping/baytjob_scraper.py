import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

from normilizbaytjob import save_to_excel

# Chrome options setup
options = Options()
options.add_argument('--disable-dev-shm-usage')

# Function to handle HTTP errors and retry requests
MAX_RETRIES = 3
INITIAL_BACKOFF_DELAY = 1  # 1 second

def handle_http_error(error, retries):
    if isinstance(error, requests.exceptions.RequestException):
        if error.response.status_code == 429 and retries < MAX_RETRIES:
            backoff_delay = (2 ** retries) * INITIAL_BACKOFF_DELAY
            print(f"Rate limited. Retrying in {backoff_delay} seconds...")
            time.sleep(backoff_delay)
            return True
        elif error.response.status_code == 404:
            print("404 Not Found Error:", error)
            return False
        else:
            raise error
    return False

# Define Job and SubSector classes
class Job:
    def __init__(self, job_title=None,  job_description=None,company_name=None, location=None,
                 experience=None, posting_date=None, easyApply=None, jobLocation=None,
                 job_type=None, companyIndustry=None, jobRole=None, employmentType=None,
                 monthlySalaryRange=None, numberOfVacancies=None, skillsRequired=None,
                 detailUrl=None):
        self.job_title = job_title
        self.job_description = job_description
        self.company_name = company_name
        self.location = location
        self.experience = experience
        self.posting_date = posting_date
        self.easyApply = easyApply
        self.jobLocation = jobLocation
        self.job_type = job_type
        self.companyIndustry = companyIndustry
        self.jobRole = jobRole
        self.employmentType = employmentType
        self.monthlySalaryRange = monthlySalaryRange
        self.numberOfVacancies = numberOfVacancies
        self.skillsRequired = skillsRequired
        self.detailUrl = detailUrl

class SubSector:
    def __init__(self, name, count, subSectorUrl, jobList=[]):
        self.name = name
        self.count = count
        self.subSectorUrl = subSectorUrl
        self.jobList = jobList

# Function to scrape job details
def scrape_job_detail(jobDetailUrl, retries=0):
    try:
        print("Job Detail Url:", jobDetailUrl)
        response = requests.get(jobDetailUrl)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        job = Job(
            job_title=soup.select_one("#job_title").text.strip() if soup.select_one("#job_title") else None,
            company_name=soup.select_one(".media-list .is-black span").text.strip() if soup.select_one(".media-list .is-black span") else None,
            posting_date=soup.select_one(".t-small.t-mute span").text.strip() if soup.select_one(".t-small.t-mute span") else None,
            monthlySalaryRange=soup.select_one(".icon.is-salaries + b").text.strip() if soup.select_one(".icon.is-salaries + b") else None,
            job_description=soup.select_one("h2.h5:contains('Job Description')").find_next("div").text.strip() if soup.select_one("h2.h5:contains('Job Description')") else None,
            skillsRequired=soup.select_one("h2.h5:contains('Skills')").find_next("div").text.strip() if soup.select_one("h2.h5:contains('Skills')") else None,
            companyIndustry=soup.select_one("dt:contains('Company Industry')").find_next("dd").text.strip() if soup.select_one("dt:contains('Company Industry')") else None,
            employmentType=soup.select_one("dt:contains('Employment Type')").find_next("dd").text.strip() if soup.select_one("dt:contains('Employment Type')") else None,
            numberOfVacancies=soup.select_one("dt:contains('Number of Vacancies')").find_next("dd").text.strip() if soup.select_one("dt:contains('Number of Vacancies')") else None,
            detailUrl=jobDetailUrl,
            job_type= soup.select_one("dt:contains('Employment Type')").find_next("dd").text.strip() if soup.select_one("dt:contains('Employment Type')") else None,

        )

        print("Job Type In Job Detail", job.job_type)
        print("Job Company Name In Job Detail", job.company_name)
        print("Job Title In Job Detail", job.job_title)
        print("Job Description In Job Detail", job.job_description)
        print("Job Employment Type In Job Detail", job.employmentType)
        print("Job Experience In Job Detail", job.experience)
        print("Job Skill Required In Job Detail", job.skillsRequired)
        print("Job Company Industry  In Job Detail", job.companyIndustry)
        print("Job Company Easy Apply  In Job Detail", job.easyApply)
        print("Job Location  In Job Detail", job.jobLocation)
        print("Job Role  In Job Detail", job.jobRole)


        return job
    except requests.RequestException as error:
        print("Error fetching or scraping job detail:", error)
        if retries < MAX_RETRIES:
            return scrape_job_detail(jobDetailUrl, retries + 1)
        else:
            return Job(detailUrl=jobDetailUrl)

def scrape_sub_sector_detail(subSectorUrl, retries=0):
    try:
        baseUrl = "https://www.bayt.com"
        fullUrl = urljoin(baseUrl, subSectorUrl)
        print("Full URL:", fullUrl)

        options = Options()
        options.headless = True  # Run headless Chrome
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(fullUrl)

        # Wait for the sidebar to be visible
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "jsMainClusterContainer"))
        )

        # Extract the "Work from Home" filter URL
        work_from_home_input = driver.find_element(By.ID, "remote_working_type")
        filter_url = work_from_home_input.get_attribute("onchange").split("AjaxUrlHandler.goTo('")[1].split("')")[0]
        filter_url = urljoin(baseUrl, filter_url)
        print("Filter URL:", filter_url)

        # Navigate to the filtered URL
        driver.get(filter_url)

        # Wait for the job listings to be visible
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#results_inner_card li[data-js-job]"))
        )

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        print("Response:", soup)

        # Check if there are job listings available
        no_jobs_message = soup.select_one("#results_inner_card li.card p")
        if no_jobs_message and "Sorry, we found no jobs matching your search criteria." in no_jobs_message.text:
            print("No jobs found for the selected criteria.")
            return []

        jobList = []

        for element in soup.select("#results_inner_card li[data-js-job]"):
            job_title = element.select_one("h2 a").text.strip() if element.select_one("h2 a") else ""
            company_name = element.select_one(".u-stretch b").get("title").strip() if element.select_one(".u-stretch b") else ""
            jobLocation = element.select_one(".t-mute").text.strip() if element.select_one(".t-mute") else ""
            job_description = element.select_one(".m10t.t-small").text.strip() if element.select_one(".m10t.t-small") else ""
            experience = element.select_one("ul.list li[data-automation-id='id_careerlevel']").text.strip() if element.select_one("ul.list li[data-automation-id='id_careerlevel']") else ""
            posting_date = element.select_one("[data-automation-id='job-active-date']").text.strip() if element.select_one("[data-automation-id='job-active-date']") else ""
            easyApply = "Easy apply" in element.select_one("a.btn.is-small").text if element.select_one("a.btn.is-small") else False
            jobDetailUrl = element.select_one("h2 a").get("href") if element.select_one("h2 a") else ""

            job = Job(
                job_title=job_title,
                company_name=company_name,
                jobLocation=jobLocation,
                job_description=job_description,
                experience=experience,
                posting_date=posting_date,
                easyApply=easyApply,
                detailUrl=urljoin(baseUrl, jobDetailUrl) if jobDetailUrl else "",
            )

            print("Job Detail Url:", job.detailUrl)
            print("Job Type:", job.job_type)

            detailPageData = scrape_job_detail(job.detailUrl, 0)
            if detailPageData:
                job.__dict__.update(detailPageData.__dict__)
            jobList.append(job)


        return jobList
    except Exception as error:
        print(f"Error: {error}")
        if handle_http_error(error, retries):
            return scrape_sub_sector_detail(subSectorUrl, retries + 1)
        else:
            print("Error fetching or scraping sub-sector detail page:", error)
            return []
# Example call
# Main scraping function
def scrape_web_page():
    try:
        url = "https://www.bayt.com/en/international/jobs/sectors/"
        jobSectors = fetch_data_with_retry(url)
        return {
            "status": 200,
            "message": "Success",
            "data": jobSectors
        }
    except Exception as error:
        print("Error fetching or scraping the web page:", error)
        return {"status": 500, "message": "Internal Server Error"}

# Function to fetch data with retry
def fetch_data_with_retry(url, retries=0):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        jobSectors = []
        for element in soup.select("section.box .card"):
            sector_name = element.select_one("h4 a").text.strip() if element.select_one("h4 a") else ""
            sectorUrl = element.select_one("h4 a").get("href") if element.select_one("h4 a") else ""
            subSectors = []
            for subElement in element.select("ul.list li"):
                subSectorName = subElement.select_one("a").text.strip() if subElement.select_one("a") else ""
                countText = subElement.text.strip().split('(')[-1].split(')')[0] if '(' in subElement.text.strip() else "0"
                count = int(countText)
                subSectorUrl = subElement.select_one("a").get("href") if subElement.select_one("a") else ""
                print("Sub Sector Url",subSectorUrl)
                subSectors.append(SubSector(subSectorName, count, subSectorUrl))

            jobSectors.append({
                "sector_name": sector_name,
                "sectorUrl": sectorUrl,
                "subSectors": subSectors
            })

            print("Job Sector", subSectors)
        for sector in jobSectors:
            for subSector in sector["subSectors"][:1]:
                subSector.jobList = scrape_sub_sector_detail(subSector.subSectorUrl, 0)

        return jobSectors

    except requests.RequestException as error:
        print("Error fetching or parsing job sectors:", error)
        return []

# Main function to run the scraping process
def main():
    try:
        scraped_data = scrape_web_page()

        if scraped_data["status"] == 200:
            print("Scraping completed successfully.")
            # Process or save scraped data as needed
            # Example: print out the job sectors and sub-sectors
            for sector in scraped_data["data"]:
                print(f"\nSector: {sector['sector_name']}")
                for subSector in sector["subSectors"]:
                    print(f"\tSub-Sector: {subSector.name}")
                    if subSector.jobList:
                        for job in subSector.jobList:
                            print(f"\t\tJob Title: {job.job_title}")
                            print(f"\t\tCompany: {job.company_name}")
                            print(f"\t\tLocation: {job.jobLocation}")
                            print(f"\t\tJob Type: {job.job_type}")
                            print(f"\t\tDate Posted: {job.posting_date}")
                            print(f"\t\tEasy Apply: {job.easyApply}")
                            print(f"\t\tDetail URL: {job.detailUrl}")
                            print("")
            save_to_excel(scraped_data["data"])

        else:
            print(f"Failed to scrape data. Status Code: {scraped_data['status']}, Message: {scraped_data['message']}")

    except Exception as ex:
        print(f"An error occurred: {ex}")

if __name__ == "__main__":
    main()
