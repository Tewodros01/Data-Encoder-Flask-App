from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI(api_key="sk-proj-pSKOFeR5wt1K4twVwaVpT3BlbkFJse8vdvs8gaBkEbqg8nIG")

def organize_job_information(job_info):
    sectors = [
        "Accounting, Finance, and Insurance",
        "Administrative and Secretarial Services",
        "Advertising, Media Journalism, and Public Relations",
        "Architecture, Design, and Construction",
        "Banking, Investment, and Insurance",
        "Business and Management",
        "Communications, Marketing, and Sales",
        "Consultancy, Training, and Education",
        "Creative Arts, Event Management, and Entertainment",
        "Engineering and Technology",
        "Health and Wellness",
        "Hospitality, Tourism, and Customer Service",
        "Human Resources, Recruitment, and Organizational Development",
        "International Development and NGO",
        "Law, Legal Services, and Public Administration",
        "Logistics, Supply Chain, and Transportation",
        "Manufacturing and Production",
        "Natural and Social Sciences",
        "Product Development",
        "Product, Program, and Project Management",
        "Quality Assurance, Safety, and Compliance",
        "Relationship and Stakeholder Management",
        "Retail, Wholesale, and Inventory Management"
    ]

    job_types = [
        "Commission",
        "Consultancy",
        "Contract",
        "Freelance",
        "Full time",
        "Hybrid",
        "Internship",
        "Part time",
        "Project Based",
        "Remote",
        "Temporary",
        "Volunteer"
    ]

    apply_types = [
        "Internal",
        "External URL",
        "By Email"
    ]

    experience_levels = [
        "Fresh",
        "0-1 Years",
        "1+ Years",
        "2+ Years",
        "3+ Years",
        "4+ Years",
        "5+ Years",
        "6+ Years",
        "7+ Years",
        "8 Years +"
    ]

    gender_options = [
        "Male",
        "Female",
        "Prefer not to say"
    ]

    qualifications = [
        "Diploma",
        "Associate Degree",
        "MA Degree",
        "MSc Degree",
        "BSc Degree",
        "BA Degree",
        "PHD",
        "Doctorate",
        "Grade 10",
        "Grade 8",
        "TVET"
    ]

    fields_of_study = [
        "Institute of Technology",
        "Business and Economics",
        "Education and Behavioral Studies",
        "Social Sciences",
        "Biotechnology",
        "Peace and Security Study",
        "Health Sciences",
        "Humanities, Language Studies, Journalism and Communication",
        "Law and Governance Studies",
        "Natural and Computational Sciences",
        "Performing and Visual Arts",
        "Veterinary Medicine and Agriculture",
        "Architecture, Building Construction and City Development"
    ]

    career_levels = [
        "Student",
        "Entry",
        "Junior Level",
        "Mid-Level",
        "Senior-Level",
        "Executive"
    ]

    columns_to_include = {
        "job_title": "",
        "job_description": "",
        "application_deadline": "",
        "job_sector": [""],
        "job_type": [""],
        "skills": [],
        "job_apply_type": "",
        "job_apply_url": "",
        "salary_type": "",
        "min_salary": "",
        "max_salary": "",
        "salary_currency": "",
        "salary_position": "",
        "salary_separator": "",
        "salary_decimals": "",
        "experience": "",
        "gender": "",
        "qualifications": [""],
        "career_level": "",
        "country": "",
        "state": "",
        "city": "",
        "postal_code": "",
        "full_address": "",
        "latitude": "",
        "longitude": "",
        "zoom": ""
    }

    example_job = {
        "job_title": "Site Engineer",
        "job_description": "As a Site Engineer, you will be responsible for coordinating and overseeing all aspects of finishing works on our construction sites. You will work closely with the project team to ensure timely completion, quality control, and adherence to project specifications. The ideal candidate will have a Bachelor's Degree in Civil Engineering, a minimum of 3 years of relevant experience with at least 2 years specifically focused on finishing works.\n\nKey Responsibilities:\n- Supervise and manage finishing works on construction sites\n- Ensure compliance with project specifications and quality standards\n- Provide technical expertise and guidance to project team members\n- Collaborate with subcontractors and vendors to ensure smooth project execution\n- Create and maintain project documentation and reports\n- Coordinate with clients, architects, and other stakeholders as required\n- Identify and resolve any technical issues or challenges that may arise during construction\n\nRequirements:\n- Bachelor's Degree in Civil Engineering\n- Minimum of 3 years of relevant experience, with at least 2 years in finishing works\n- Capacity and experience to supervise finishing works\n- Excellent technical skills and knowledge of construction practices\n- Exceptional written and spoken communication skills\n- Ability to work well under pressure and meet deadlines\n- Proficiency in AUTOCAD and Excel\n- Professionalism, punctuality, and strong problem-solving skills",
        "application_deadline": "June 26th, 2024",
        "job_sector": [
            "Architecture, Design, and Construction"
        ],
        "job_type": [
            "Full time"
        ],
        "skills": [
            "Supervision",
            "Quality Control",
            "Project Management",
            "Communication",
            "Technical Skills",
            "Construction Practices",
            "Problem-solving"
        ],
        "job_apply_type": "External URL",
        "job_apply_url": "https://forms.gle/vM4ysAzZaDm9tCjC6",
        "salary_type": "",
        "min_salary": "",
        "max_salary": "",
        "salary_currency": "",
        "salary_position": "",
        "salary_separator": "",
        "salary_decimals": "",
        "experience": "3+ Years",
        "gender": "",
        "qualifications": [
            "BA Degree"
        ],
        "career_level": "Mid-Level",
        "country": "Ethiopia",
        "state": "",
        "city": "Addis Ababa",
        "postal_code": "",
        "full_address": "",
        "latitude": "",
        "longitude": "",
        "zoom": ""
    }
    context = """
    You are an AI assistant who helps with organizing job information into specified JSON format. The user prefers responses in JSON format only and needs the following fields normalized:
    - Sectors
    - Job types
    - Job apply types
    - Experience
    - Gender
    - Qualifications
    - Fields of study
    - Career levels

    Additionally, extract skills, experience, and qualifications from the job description.
    """

    prompt = f"""
    {context}
    Please organize the following job information into JSON format with the specified columns: {columns_to_include}.
    Here is an example job: {example_job}.
    Job Information: {job_info}.

    Ensure to normalize the following fields from the job information:
    - Sectors into: {sectors}
    - Job types into: {job_types}
    - Job apply types into: {apply_types}
    - Experience into: {experience_levels}
    - Gender into: {gender_options}
    - Qualifications into: {qualifications}
    - Fields of study into: {fields_of_study}
    - Career levels into: {career_levels}

    Additionally, extract skills, experience, and qualifications from the job description.
    Please provide your response in JSON format only.
    """

    messages = [
        {"role": "user", "content": prompt},
    ]

    try:
        # Send request to OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        # Get chatbot response
        response = completion.choices[0].message.content

        # Load the JSON response
        job_info_dict = json.loads(response)
    except json.JSONDecodeError:
        print("Failed to decode JSON response")
        job_info_dict = {column: None for column in columns_to_include}
    except Exception as e:
        print(f"An error occurred: {e}")
        job_info_dict = {column: None for column in columns_to_include}

    return job_info_dict

