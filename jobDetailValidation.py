def validate_job_details(job_details):
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
        "internal",
        "external",
        "with_email"
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

    def is_valid_value(value, valid_values):
        return value in valid_values

    def are_valid_values(values, valid_values):
        return all(value in valid_values for value in values)

    errors = []

    if not are_valid_values(job_details['job_sector'], sectors):
        errors.append("Invalid job sector(s)")

    if not are_valid_values(job_details['job_type'], job_types):
        errors.append("Invalid job type(s)")

    return errors