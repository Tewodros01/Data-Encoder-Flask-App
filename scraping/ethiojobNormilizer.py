import xlsxwriter
from datetime import datetime

class NormalizedJob:
    def __init__(self, id=None, post_date=None, email='', password='', company_name=None, company_logo=None,
                 job_title=None, job_description=None, application_deadline=None, job_sector=None, job_type=None,
                 skills=None, job_apply_type=None, job_apply_url=None, salary_type=None, min_salary=None, max_salary=None,
                 salary_currency=None, salary_position=None, salary_separator=None, salary_decimals=None,
                 experience=None, gender=None, qualifications=None, career_level=None, country=None, state=None,
                 city=None, postal_code=None, full_address=None, latitude=None, longitude=None, zoom=None,
                 unique_job_id=None, detail_url=None):
        self.id = id
        self.post_date = post_date
        self.email = email
        self.password = password
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

def normalize_sector(job_sector):
    sector_mapping = {
        "Accounting and Finance": "Accounting, Finance, and Insurance",
        "Admin, Secretarial and Clerical": "Administrative and Secretarial Services",
        "Advertising and Media": "Advertising, Media Journalism and Public Relations",
        "Agriculture": "Agriculture, Forestry, and Environmental Science",
        "Architecture and Construction": "Architecture, Design, and Construction",
        "Automotive": "Engineering and Technology",
        "Banking and Insurance": "Banking, Investment and Insurance",
        "Business Development": "Business and Management",
        "Business and Administration": "Business and Management",
        "Civil Service and Government": "Law, Legal Services, and Public Administration",
        "Communications, PR and Journalism": "Communications, Marketing, and Sales",
        "Community Service": "Human Resources, Recruitment, and Organizational Development",
        "Consultancy and Training": "Consultancy, Training and Education",
        "Creative Arts": "Creative Arts, Event Management and Entertainment",
        "Customer Service": "Hospitality, Tourism, and Customer Service",
        "Development and Project Management": "Product, Program, and Project Management",
        "Economics": "Natural and Social Sciences",
        "Education": "Consultancy, Training and Education",
        "Energy": "Engineering and Technology",
        "Engineering": "Engineering and Technology",
        "Entertainment": "Creative Arts, Event Management and Entertainment",
        "Environment and Natural Resource": "Agriculture, Forestry, and Environmental Science",
        "Event Management": "Creative Arts, Event Management and Entertainment",
        "Health Care": "Health and Wellness",
        "Hotel and Hospitality": "Hospitality, Tourism, and Customer Service",
        "Human Resource and Recruitment": "Human Resources, Recruitment, and Organizational Development",
        "Information Technology": "Engineering and Technology",
        "Inventory and Stock": "Retail, Wholesale, and Inventory Management",
        "IT, Computer Science and Software Engineering": "Engineering and Technology",
        "Languages": "Communications, Marketing, and Sales",
        "Legal": "Law, Legal Services, and Public Administration",
        "Logistics, Transport and Supply Chain": "Logistics, Supply Chain, and Transportation",
        "Maintenance": "Engineering and Technology",
        "Management": "Business and Management",
        "Manufacturing": "Manufacturing and Production",
        "Media and Journalism": "Advertising, Media Journalism and Public Relations",
        "Natural Sciences": "Natural and Social Sciences",
        "Pharmaceutical": "Health and Wellness",
        "Purchasing and Procurement": "Logistics, Supply Chain, and Transportation",
        "Quality Assurance": "Quality Assurance, Safety, and Compliance",
        "Research and Development": "Product Development",
        "Retail, Wholesale and Distribution": "Retail, Wholesale, and Inventory Management",
        "Sales and Marketing": "Communications, Marketing, and Sales",
        "Science and Technology": "Engineering and Technology",
        "Security": "Quality Assurance, Safety, and Compliance",
        "Social Sciences and Community": "Natural and Social Sciences",
        "Strategic Planning": "Business and Management",
        "Telecommunications": "Communications, Marketing, and Sales",
        "Travel and Tourism": "Hospitality, Tourism, and Customer Service",
        "Veterinary Services": "Health and Wellness",
        "Warehouse, Supply Chain and Distribution": "Logistics, Supply Chain, and Transportation",
        "Water and Sanitation": "Engineering and Technology"
    }
    return sector_mapping.get(job_sector, "Unknown Sector")

def normalize_job_type(job_type):
    job_type_mapping = {
        "Part time": "Part time",
        "Full time": "Full time",
        "Contract": "Contract",
        "Commission": "Commission",
        "Consultancy": "Consultancy",
        "Freelance": "Freelance",
        "Hybrid": "Hybrid",
        "Internship": "Internship",
        "Project Based": "Project Based",
        "Remote": "Remote",
        "Temporary": "Temporary",
        "Volunteer": "Volunteer"
    }
    return job_type_mapping.get(job_type, "Unknown Job Type")

def normalize_experience(experience):
    experience_mapping = {
        "Mid Level(3-5 years)": "3+ Years",
        "Junior Level(1-3 years)": "1+ Years",
        "Senior(5-8 years)": "5+ Years",
        "Executive(VP, Director)": "8 Years +"
    }
    return experience_mapping.get(experience, "Unknown Experience Level")

def normalize_career_level(career_level):
    career_level_mapping = {
        "Mid Level(3-5 years)": "Mid-Level",
        "Junior Level(1-3 years)": "Junior Level",
        "Senior(5-8 years)": "Senior-Level",
        "Executive(VP, Director)": "Senior-Level"
    }
    return career_level_mapping.get(career_level, "Unknown Career Level")

def get_current_date_time_string():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

def save_to_excel(job_sectors):
    workbook = xlsxwriter.Workbook(f'EthioJobJobListings_{get_current_date_time_string()}.xlsx')
    worksheet = workbook.add_worksheet("All Job Listings")

    all_job_listings = []

    for sector in job_sectors:
        if sector['jobListings'] and len(sector['jobListings']) > 0:
            for job in sector['jobListings']:
                normalized_job = NormalizedJob(
                    id=job['id'],
                    post_date=job['posted_date'],
                    email="",
                    password="",
                    company_name=job['company_name'],
                    company_logo=job['company_logo'],
                    job_sector=normalize_sector(sector['sector_name']),
                    job_title=job['job_title'],
                    job_description=job['job_description'],
                    application_deadline=job['application_deadline'],
                    job_type=normalize_job_type(job['employment_type']),
                    skills=job['job_requirements'],
                    job_apply_type="external",
                    job_apply_url=job['detail_url'],
                    min_salary=job['salary'],
                    experience=normalize_experience(job['job_level']),
                    career_level=normalize_career_level(job['job_level']),
                    unique_job_id=job['unique_job_id'],
                    detail_url=job['detail_url']
                )

                if (normalized_job.company_name and
                    normalized_job.job_sector != "Unknown Sector" and
                    normalized_job.job_type != "Unknown Job Type"):
                    all_job_listings.append(normalized_job)

    headers = [attr for attr in dir(NormalizedJob) if not callable(getattr(NormalizedJob, attr)) and not attr.startswith("__")]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, job in enumerate(all_job_listings, 1):
        for col_num, header in enumerate(headers):
            worksheet.write(row_num, col_num, getattr(job, header))

    worksheet.set_column(0, len(headers) - 1, 20)
    workbook.close()
    print(f"Data saved to EthioJobJobListings_{get_current_date_time_string()}.xlsx")

