from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException

class EthioJobScraper:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://ethiojobs.net/jobs"  # Replace with the actual URL

    def get_page_content(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobcardcontainer"))
        )
        return self.driver.page_source

    def scrape_job_categories(self):
        try:
            self.driver.get(self.base_url)
            categories_elements = self.driver.find_elements(By.CSS_SELECTOR, '.MuiAccordionSummary-content p[style*="font-size: 15px;"]')
            categories = [element.text.strip() for element in categories_elements]
            return categories
        except Exception as e:
            print(f"Error scraping job categories: {e}")
            return []

    def scrape_jobs_by_category(self, category_url):
        try:
            self.driver.get(category_url)
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, '.MuiGrid-root .MuiPaper-root .MuiGrid-container .MuiGrid-item')
            jobs = []
            for job in job_cards:
                try:
                    job_title_element = job.find_element(By.CSS_SELECTOR, 'a p[style*="font-size: 20px;"]')
                    job_title = job_title_element.text.strip() if job_title_element else 'N/A'
                    company_name_element = job.find_element(By.CSS_SELECTOR, 'p a[style*="padding: 0px 15px;"]')
                    company_name = company_name_element.text.strip() if company_name_element else 'N/A'
                    location_element = job.find_element(By.CSS_SELECTOR, 'a img[alt="location"] + p')
                    location = location_element.text.strip() if location_element else 'N/A'
                    deadline_element = job.find_element(By.CSS_SELECTOR, 'a img[alt="location"] + p + p')
                    deadline = deadline_element.text.strip() if deadline_element else 'N/A'
                    job_link_element = job.find_element(By.CSS_SELECTOR, 'a')
                    job_link = job_link_element.get_attribute('href') if job_link_element else 'N/A'
                    job_details = {
                        'title': job_title,
                        'company': company_name,
                        'location': location,
                        'deadline': deadline,
                        'link': job_link
                    }
                    jobs.append(job_details)
                except NoSuchElementException:
                    continue
            return jobs
        except Exception as e:
            print(f"Error scraping jobs by category: {e}")
            return []

    def close(self):
        try:
            self.driver.quit()
        except WebDriverException as e:
            print(f"Error closing WebDriver: {e}")

def main():
    scraper = EthioJobScraper()

    # Scrape job categories
    job_categories = scraper.scrape_job_categories()
    print("Job Categories:")
    for category in job_categories:
        print(category)

    # Scrape jobs for each category
    all_jobs = {}
    for category in job_categories:
        print(f"\nScraping jobs in category: {category}")
        # Assuming there's a way to filter by category via URL params or other means
        # Here you might need to modify the URL or use some interaction to filter by category
        # For now, let's just use the base URL and assume it loads relevant jobs
        category_url = f"{scraper.base_url}?category={category.replace(' ', '%20')}"
        jobs = scraper.scrape_jobs_by_category(category_url)
        all_jobs[category] = jobs

        # Print jobs in the current category
        for job in jobs:
            print(f"Title: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Deadline: {job['deadline']}")
            print(f"Link: {job['link']}")
            print("\n")

    scraper.close()

if __name__ == "__main__":
    main()
