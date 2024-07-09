import requests
from bs4 import BeautifulSoup

# URL of the FlexJobs search page
url = "https://www.flexjobs.com/search?&remoteoptions=100%25%20Remote%20Work&careerlevel=Entry-Level&anywhereinworld=0&anywhereinus=1"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the job listings in the HTML structure
job_listings = soup.find_all('div', class_='sc-14nyru2-2 fmkHkh')

# Extract the relevant information from each job listing
jobs = []
for listing in job_listings:
    job_id = listing.find('div', class_='sc-jv5lm6-0')['id']
    job_title = listing.find('a', class_='sc-jv5lm6-13').text.strip()
    job_age = listing.find('div', id=f'job-age-{job_id}').text.strip()
    job_description = listing.find('p', id=f'description-{job_id}').text.strip()
    job_salary = listing.find('li', id=f'salartRange-0-{job_id}').text.strip()
    job_remote = listing.find('li', id=f'remoteoption-0-{job_id}').text.strip()
    job_schedule = listing.find('li', id=f'jobschedule-0-{job_id}').text.strip()
    job_location = listing.find('span', class_='allowed-location').text.strip()

    jobs.append({
        'id': job_id,
        'title': job_title,
        'age': job_age,
        'description': job_description,
        'salary': job_salary,
        'remote': job_remote,
        'schedule': job_schedule,
        'location': job_location
    })

# Print the extracted job listings
for job in jobs:
    print(f"Job ID: {job['id']}")
    print(f"Title: {job['title']}")
    print(f"Posted: {job['age']}")
    print(f"Description: {job['description']}")
    print(f"Salary: {job['salary']}")
    print(f"Remote: {job['remote']}")
    print(f"Schedule: {job['schedule']}")
    print(f"Location: {job['location']}")
    print("-" * 40)
