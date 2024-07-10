import pandas as pd
from datetime import datetime
from datetime import datetime

class NormalizedJob:
    def __init__(self, id=None, company_name=None, company_logo=None, job_title=None, job_description=None,
                 application_deadline=None, job_sector=None, job_type=None, skills=None, job_apply_type=None,
                 job_apply_url=None, salary_type=None, min_salary=None, max_salary=None, salary_currency=None,
                 salary_position=None, salary_separator=None, salary_decimals=None, experience=None, gender=None,
                 qualifications=None, career_level=None, country=None, state=None, city=None, postal_code=None,
                 full_address=None, latitude=None, longitude=None, zoom=None, unique_job_id=None, detail_url=None):
        self.id = id
        self.company_name = company_name
        self.company_logo = company_logo
        self.job_title = job_title
        self.job_description = job_description
        self.application_deadline = application_deadline
        self.job_sector = job_sector
        self.job_type = job_type
        self.skills = skills
        self.job_apply_type = job_apply_type
        self.job_apply_url = job_apply_url
        self.salary_type = salary_type
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.salary_currency = salary_currency
        self.salary_position = salary_position
        self.salary_separator = salary_separator
        self.salary_decimals = salary_decimals
        self.experience = experience
        self.gender = gender
        self.qualifications = qualifications
        self.career_level = career_level
        self.country = country
        self.state = state
        self.city = city
        self.postal_code = postal_code
        self.full_address = full_address
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.unique_job_id = unique_job_id
        self.detail_url = detail_url

def sanitize_sector_name(sector_name):
    return sector_name.split('(')[0].strip()

def normalize_job_type(job_type):
    job_type_mapping = {
        "Part Time Employee": "Part time",
        "Full Time Employee": "Full time",
        "Contractor": "Contract",
        "Internship": "Internship",
        "Temporary": "Temporary"
    }
    return job_type_mapping.get(job_type, "Unknown Job Type")

def normalize_job_sector(subsector):
    if subsector in [
        "Accounting", "Banking", "Financial Auditing", "Financial Services", "Investment, Securities & Funds",
        "Islamic Banking", "Venture Capital & Private Equity", "Insurance & TPA"
    ]:
        return 'Accounting, Finance, and Insurance'
    elif subsector in ["Administration Support Services", "Administrative Support Services"]:
        return 'Administrative and Secretarial Services'
    elif subsector in [
        "Advertising", "Media Production", "Broadcast Media Production", "Graphic Design", "Journalism",
        "Publishing", "Public Relations (PR)"
    ]:
        return 'Advertising, Media Journalism and Public Relations'
    elif subsector in [
        "Agriculture & Crop Production", "Animal Production", "Dairy Production", "Forestry & Logging",
        "Scientific Research & Development", "Natural Gas Distribution", "Mining & Quarrying", "Environmental Science"
    ]:
        return 'Agriculture, Forestry, and Environmental Science'
    elif subsector in ["Architecture", "Interior Design", "Construction & Building", "Facilities & Property Management", "Fit-Out & Joinery"]:
        return 'Architecture, Design, and Construction'
    elif subsector in ["Banking", "Investment, Securities & Funds", "Islamic Banking", "Venture Capital & Private Equity"]:
        return 'Banking, Investment and Insurance'
    elif subsector in [
        "Management Consulting", "Business Consultancy Services", "Business Support Services",
        "Business Process Outsourcing (BPO)", "Consulting"
    ]:
        return 'Business and Management'
    elif subsector in ["Marketing", "Market Research", "Sales Outsourcing", "Telemarketing", "Communications"]:
        return 'Communications, Marketing, and Sales'
    elif subsector in [
        "Consultancy", "Training & Education Center", "Higher Education", "Vocational Education", "Events Management"
    ]:
        return 'Consultancy, Training and Education'
    elif subsector in [
        "Creative Arts", "Event Management", "Entertainment", "Fashion Design", "Performing Arts",
        "Video & Film Production", "Music Production", "Amusement & Recreation Facility"
    ]:
        return 'Creative Arts, Event Management and Entertainment'
    elif subsector in [
        "Engineering Consultancy", "Industrial Engineering & Automation", "Mechanical Engineering",
        "Electrical Engineering", "General Engineering Consultancy", "Technical Maintenance & Repair"
    ]:
        return 'Engineering and Technology'
    elif subsector in [
        "Health", "Wellness", "Medical Clinic", "Medical Hospital", "Other Healthcare Services", "Pharmaceutical Manufacturing"
    ]:
        return 'Health and Wellness'
    elif subsector in [
        "Hospitality", "Tourism", "Customer Service", "Hospitality & Accommodation",
        "Catering, Food Service, & Restaurant", "Travel Agency"
    ]:
        return 'Hospitality, Tourism, and Customer Service'
    elif subsector in [
        "Human Resources Outsourcing", "Recruitment & Employee Placement Agency", "Organizational Development"
    ]:
        return 'Human Resources, Recruitment, and Organizational Development'
    elif subsector in ["International Humanitarian Organization", "Non-profit Organization", "NGO"]:
        return 'International Development and NGO'
    elif subsector in [
        "Law Firm", "Legal Process Outsourcing (LPO)", "Legal Services", "Public Administration", "Government Services"
    ]:
        return 'Law, Legal Services, and Public Administration'
    elif subsector in [
        "Logistics", "Supply Chain", "Transportation", "Distribution, Supply Chain & Logistics",
        "Marine Transport Services", "Aviation Support Services"
    ]:
        return 'Logistics, Supply Chain, and Transportation'
    elif subsector in [
        "Manufacturing", "Production", "Industrial Production", "Automotive Manufacture",
        "Consumer Packaged Goods Manufacture", "Food & Beverage Production"
    ]:
        return 'Manufacturing and Production'
    elif subsector in [
        "Natural Sciences", "Social Sciences", "Scientific Research & Development"
    ]:
        return 'Natural and Social Sciences'
    elif subsector in ["Product Development", "Software Development", "Cyber & Network Security"]:
        return 'Product Development'
    elif subsector in ["Program Management", "Project Management"]:
        return 'Product, Program, and Project Management'
    elif subsector in [
        "Quality Assurance", "Safety", "Compliance", "Laboratory & Quality Control"
    ]:
        return 'Quality Assurance, Safety, and Compliance'
    elif subsector in ["Relationship Management", "Stakeholder Management"]:
        return 'Relationship and Stakeholder Management'
    elif subsector in [
        "Retail", "Wholesale", "Inventory Management", "Consumer Electronics",
        "Fashion & Apparel", "Household Appliances", "Jewelry & Gold"
    ]:
        return 'Retail, Wholesale, and Inventory Management'
    else:
        return 'Other'

def normalize_career_level(career_level):
    career_level_mapping = {
        "Mid Career": "Mid-Level",
        "Management": "Executive",
        "Director/Head": "Executive",
        "Entry Level": "Entry",
        "Fresh Graduate": "Entry",
        "Student/Internship": "Student",
        "Senior Executive": "Senior-level"
    }
    return career_level_mapping.get(career_level, "Unknown Career Level")

def get_current_date_time_string():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

def save_to_excel(job_sectors):
    all_job_listings = []

    for sector in job_sectors:
        for sub_sector in sector["subSectors"]:
            for job in sub_sector.jobList:
                normalized_job = {
                    'company_name': job.company_name,
                    'job_sector': normalize_job_sector(sanitize_sector_name(sub_sector.name)),
                    'job_title': job.job_title,
                    'job_description': job.job_description,
                    'job_type':normalize_job_type(job.employmentType),
                    'skills': job.skillsRequired,
                    'job_apply_type': "external",
                    'job_apply_url': job.detailUrl,
                    'career_level': job.experience,
                    'experience':job.experience,
                    'unique_job_id': job.detailUrl,  # Assuming detail URL can be used as a unique ID
                    'detail_url': job.detailUrl
                }

                # Debugging output
                print(f"Job Title: {job.job_title}")
                print(f"Company Name: {job.company_name}")
                print(f"Job Sector: {normalized_job['job_sector']}")
                print(f"Job Type: {normalized_job['job_type']}")
                print(f"Job Skills: {job.skillsRequired}")

                all_job_listings.append(normalized_job)

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(all_job_listings)

    # Save the DataFrame to an Excel file
    file_name = f'BaytJobJobListings_{get_current_date_time_string()}.xlsx'
    df.to_excel(file_name, index=False)
    print(f'Data saved to {file_name}')

