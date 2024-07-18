import pandas as pd
from datetime import datetime

# Normalization functions
def normalize_sector(job_sector):
    sector_mapping = {
        "Natural Science": "Natural and Social Sciences",
        "Business": "Business and Management",
        "Creative Arts": "Creative Arts, Event Management and Entertainment",
        "Education": "Consultancy, Training and Education",
        "Hospitality": "Hospitality, Tourism, and Customer Service",
        "Low and Medium Skilled Worker": "Administrative and Secretarial Services",
        "Transportation & Logistics": "Logistics, Supply Chain, and Transportation",
        "Engineering": "Engineering and Technology",
        "Finance": "Accounting, Finance, and Insurance",
        "Legal Services": "Law, Legal Services, and Public Administration",
        "ICT": "Engineering and Technology",
        "Health Care": "Health and Wellness",
        "Manufacturing": "Manufacturing and Production",
        "Non Profit / Volunteer": "International Development and NGO",
        "Social Science": "Natural and Social Sciences",
    }
    return sector_mapping.get(job_sector, "Unknown Sector")

def normalize_job_type(job_type):
    job_type_mapping = {
        "Bid": "Project Based",
        "Part Time": "Part time",
        "Full Time": "Full time",
        "Contract": "Contract",
        "Internship": "Internship",
    }
    return job_type_mapping.get(job_type, "Unknown Job Type")

def normalize_experience(experience):
    if "0-1" in experience:
        return "0-1 Years"
    elif "1-3" in experience or "1+" in experience:
        return "1+ Years"
    elif "3-5" in experience or "3+" in experience:
        return "3+ Years"
    elif "5-10" in experience or "5+" in experience:
        return "5+ Years"
    elif "10" in experience or "8" in experience:
        return "8 Years +"
    else:
        return "Unknown Experience Level"

def get_current_date_time_string():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")


def save_to_excel(job_sectors):
    all_job_listings = []

    for sector in job_sectors:
        if sector.get("job_list"):
            for job in sector["job_list"]:
                normalized_job = {
                    "email": "",
                    "password": "",
                    "posted_date":job.get("posted_date"),
                    "company_name": job.get("company_name"),
                    "job_sector": normalize_sector(sector.get("sector_name")),
                    "job_title": job.get("job_title"),
                    "job_description": job.get("job_description"),
                    "application_deadline": job.get("application_deadline", ""),
                    "job_type": normalize_job_type(job.get("job_type", "")),
                    "skills": job.get("skills"),
                    "job_apply_type": "external",
                    "job_apply_url": job.get("job_apply_url"),
                    "experience": normalize_experience(job.get("experience", "")),
                    "detail_url": job.get("job_apply_url"),
                }

                if normalized_job["company_name"] and normalized_job["job_sector"] != "Unknown Sector" and normalized_job["job_type"] != "Unknown Job Type":
                    all_job_listings.append(normalized_job)

    df = pd.DataFrame(all_job_listings)

    with pd.ExcelWriter(f"HahuJobJobListings_{get_current_date_time_string()}.xlsx", engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='All Job Listings')

        # Set column widths based on the maximum length of the content
        worksheet = writer.sheets['All Job Listings']
        for column in df:
            max_len = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx, col_idx, max_len)

    print(f"Data saved to HahuJobJobListings_{get_current_date_time_string()}.xlsx")
