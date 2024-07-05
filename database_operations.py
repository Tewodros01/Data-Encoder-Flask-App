from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=True)
    job_description = db.Column(db.Text, nullable=True)
    application_deadline = db.Column(db.String(100), nullable=True)
    job_sector = db.Column(db.String(200), nullable=True)
    job_type = db.Column(db.String(200), nullable=True)
    skills = db.Column(db.String(200), nullable=True)
    job_apply_type = db.Column(db.String(50), nullable=True)
    job_apply_url = db.Column(db.String(200), nullable=True)
    job_apply_email = db.Column(db.String(200), nullable=True)
    min_salary = db.Column(db.String(50), nullable=True)
    max_salary = db.Column(db.String(50), nullable=True)
    salary_currency = db.Column(db.String(50), nullable=True)
    salary_position = db.Column(db.String(50), nullable=True)
    salary_separator = db.Column(db.String(50), nullable=True)
    salary_decimals = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    qualifications = db.Column(db.String(200), nullable=True)
    field_of_study = db.Column(db.String(200), nullable=True)
    career_level = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(50), nullable=True)
    full_address = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(50), nullable=True)
    zoom = db.Column(db.String(50), nullable=True)
    posting_date = db.Column(db.String(100), nullable=True)
    company_name = db.Column(db.String(200), nullable=True)

def save_job_to_db(job_info):
    def get_value(key, default=''):
        return ', '.join(job_info.get(key, [])) if isinstance(job_info.get(key, []), list) else job_info.get(key, default)

    job = Job(
        job_title=get_value('job_title'),
        job_description=get_value('job_description'),
        application_deadline=get_value('application_deadline'),
        job_sector=get_value('job_sector', ''),
        job_type=get_value('job_type', ''),
        skills=get_value('skills', ''),
        job_apply_type=get_value('job_apply_type', ''),
        job_apply_url=get_value('job_apply_url', ''),
        job_apply_email=get_value('job_apply_email', ''),
        min_salary=get_value('min_salary', ''),
        max_salary=get_value('max_salary', ''),
        salary_currency=get_value('salary_currency', ''),
        salary_position=get_value('salary_position', ''),
        salary_separator=get_value('salary_separator', ''),
        salary_decimals=get_value('salary_decimals', ''),
        experience=get_value('experience', ''),
        gender=get_value('gender', ''),
        qualifications=get_value('qualifications', ''),
        field_of_study=get_value('field_of_study', ''),
        career_level=get_value('career_level', ''),
        country=get_value('country', ''),
        state=get_value('state', ''),
        city=get_value('city', ''),
        postal_code=get_value('postal_code', ''),
        full_address=get_value('full_address', ''),
        latitude=get_value('latitude', ''),
        longitude=get_value('longitude', ''),
        zoom=get_value('zoom', ''),
        posting_date=get_value('posting_date', ''),
        company_name=get_value('company_name', '')
    )
    db.session.add(job)
    db.session.commit()
    print(f"Job {job.job_title} at {job.company_name} saved to database")

def job_exists(job_info, threshold=90):
    def normalize_value(value):
        return value.strip().lower() if value else ''

    normalized_title = normalize_value(job_info.get('job_title'))
    normalized_description = normalize_value(job_info.get('job_description'))
    normalized_company = normalize_value(job_info.get('company_name'))
    posting_date = job_info.get('posting_date')
    application_deadline = job_info.get('application_deadline')

    existing_jobs = db.session.query(Job).all()

    for job in existing_jobs:
        title_match = fuzz.ratio(normalized_title, normalize_value(job.job_title))
        description_match = fuzz.ratio(normalized_description, normalize_value(job.job_description))
        company_match = fuzz.ratio(normalized_company, normalize_value(job.company_name))
        posting_date_match = fuzz.ratio(normalize_value(posting_date), normalize_value(job.posting_date))
        deadline_match = fuzz.ratio(normalize_value(application_deadline), normalize_value(job.application_deadline))

        if title_match >= threshold and description_match >= threshold and company_match >= threshold and posting_date_match >= threshold and deadline_match >= threshold:
            return True

    return False

