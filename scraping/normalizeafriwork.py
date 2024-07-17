import pandas as pd
from datetime import datetime
import re

# from database_operations import job_exists

def get_current_date_time_string():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

def normalize_sector(sector):
    sector_mapping = {
        "Software design and Development": "Engineering and Technology",
        "Information technology": "Engineering and Technology",
        "Media and communication": "Communications, Marketing, and Sales",
        "Food and Drink preparation or service": "Hospitality, Tourism, and Customer Service",
        "Accounting and finance": "Accounting, Finance, and Insurance",
        "Creative art and design": "Creative Arts, Event Management and Entertainment",
        "Multimedia content production": "Creative Arts, Event Management and Entertainment",
        "Architecture and urban planning": "Architecture, Design, and Construction",
        "Construction and Civil engineering": "Architecture, Design, and Construction",
        "Health care": "Health and Wellness",
        "Pharmaceutical": "Health and Wellness",
        "Hospitality and Tourism": "Hospitality, Tourism, and Customer Service",
        "Translation and Transcription": "Communications, Marketing, and Sales",
        "Documentation and Writing services": "Communications, Marketing, and Sales",
        "Manufacturing and production": "Manufacturing and Production",
        "Logistic and Supply chain": "Logistics, Supply Chain, and Transportation",
        "Transportation and Delivery": "Logistics, Supply Chain, and Transportation",
        "Installation and Maintenance technician": "Engineering and Technology",
        "Mechanical and Electrical engineering": "Engineering and Technology",
        "Chemical and Biomedical engineering": "Engineering and Technology",
        "Environmental and Energy engineering": "Engineering and Technology",
        "Sales and Promotion": "Communications, Marketing, and Sales",
        "Marketing and Advertisement": "Communications, Marketing, and Sales",
        "Purchasing and procurement": "Retail, Wholesale, and Inventory Management",
        "Retail, Wholesale, and Inventory Management": "Retail, Wholesale, and Inventory Management",
        "Secretarial and office management": "Administrative and Secretarial Services",
        "Administrative and Secretarial Services": "Administrative and Secretarial Services",
        "Janitorial and other Office services": "Administrative and Secretarial Services",
        "Security and Safety": "Quality Assurance, Safety, and Compliance",
        "Quality Assurance, Safety, and Compliance": "Quality Assurance, Safety, and Compliance",
        "Horticulture": "Agriculture, Forestry, and Environmental Science",
        "Agriculture": "Agriculture, Forestry, and Environmental Science",
        "Livestock and animal husbandry": "Agriculture, Forestry, and Environmental Science",
        "Gardening and landscaping": "Agriculture, Forestry, and Environmental Science",
        "Aeronautics and Aerospace": "Engineering and Technology",
        "Entertainment": "Creative Arts, Event Management and Entertainment",
        "Event management and Organization": "Creative Arts, Event Management and Entertainment",
        "Fashion design": "Creative Arts, Event Management and Entertainment",
        "Clothing and Textile": "Manufacturing and Production",
        "Project management and administration": "Product, Program, and Project Management",
        "Business and Commerce": "Product, Program, and Project Management",
        "Product, Program, and Project Management": "Product, Program, and Project Management",
        "Human resource and talent management": "Consultancy, Training and Education",
        "Consultancy, Training and Education": "Consultancy, Training and Education",
        "Research and data Analytics": "Natural and Social Sciences",
        "Data mining and analytics": "Natural and Social Sciences",
        "Psychiatry, Psychology and Social work": "Health and Wellness",
        "Law": "Law, Legal Services, and Public Administration",
        "Beauty and Grooming": "Health and Wellness",
        "Labor work and Masonry": "Construction and Civil engineering",
        "Teaching and Tutor": "Consultancy, Training and Education",
        "Training and Mentorship": "Consultancy, Training and Education",
        "Customer service and care": "Hospitality, Tourism, and Customer Service",
        "Woodwork and Carpentry": "Architecture, Design, and Construction",
        "Broker and Case closer": "Relationship and Stakeholder Management",
        "Advisory and Consultancy": "Consultancy, Training and Education",
        "Veterinary": "Health and Wellness",
    }
    return sector_mapping.get(sector, "Unknown Sector")

def normalize_job_type(job_type):
    job_type_mapping = {
        "PART_TIME": "Part time",
        "FULL_TIME": "Full time",
        "CONTRACTUAL": "Contract",
        "FREELANCE": "Freelance",
        "VOLUNTEER": "Volunteer",
        "PAID_INTERN": "Internship",
        "UNPAID_INTERN": "Internship"
    }
    return job_type_mapping.get(job_type, "Unknown Job Type")


def normalize_and_save_jobs(job_sectors):
    all_job_listings = []

    for sector in job_sectors:
        if 'joblist' in sector and sector['joblist']:
            for job in sector['joblist']:
                # Skip jobs with company name "Private Client"
                if job['company_name'] == "Private Client":
                    print("Skipping Private Client job", job)
                    continue

                normalized_job = {
                    'id': job.get('id'),
                    'post_date': job.get('post_date'),
                    'email': "",  # Add your email here if necessary
                    'password': "",  # Add your password here if necessary
                    'company_name': job.get('company_name'),
                    'job_sector': normalize_sector(sector['sector']),
                    'job_title': job.get('job_title'),
                    'job_description': job.get('job_description', ""),
                    'application_deadline': job.get('application_deadline'),
                    'job_type': normalize_job_type(sector['jobtype']),
                    'skills': ', '.join(job.get('skills', [])),
                    'job_apply_type': "external",
                    'job_apply_url': job.get('job_apply_url'),
                    'min_salary': job.get('salary'),
                    'experience': job.get('experience_level', ""),
                    'unique_job_id': job.get('job_apply_url'),
                    'detail_url': job.get('job_apply_url'),
                }

                print("Normalized Job", normalized_job)

                # Check for null values and exclude the job if company_name, job_sector, or job_type is null
                if (
                    normalized_job['company_name'] and
                    normalized_job['job_sector'] != "Unknown Sector" and
                    normalized_job['job_type'] != "Unknown Job Type"
                ):
                    # if job_exists(normalized_job):
                    #     print("Job Alredy Exit")
                    # else:
                    all_job_listings.append(normalized_job)

    print("All Job Listings", all_job_listings)

    # Create DataFrame and set column widths based on the maximum length of the content
    df = pd.DataFrame(all_job_listings)
    file_path = f'AfriworketJobListings_{get_current_date_time_string()}.xlsx'
    df.to_excel(file_path, index=False)

    print(f"Data saved to {file_path}")

