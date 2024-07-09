import pandas as pd
from fuzzywuzzy import process, fuzz
from datetime import datetime

# Load the Excel files
job_listings_path = 'file/EthioJobJobListings_2024-07-08_16-30-31.xlsx'
employer_list_path = 'file/Employer_List_For_Job_Posting_V0.0_05-22-2024.xlsx'

job_listings_df = pd.read_excel(job_listings_path, sheet_name='All Job Listings')
employer_list_df = pd.read_excel(employer_list_path, sheet_name='jordi&yordi')

# Ensure email and password columns are present in job listings dataframe with object type
if 'email' not in job_listings_df.columns:
    job_listings_df['email'] = None
if 'password' not in job_listings_df.columns:
    job_listings_df['password'] = None

job_listings_df['email'] = job_listings_df['email'].astype('object')
job_listings_df['password'] = job_listings_df['password'].astype('object')

# Extract relevant columns
job_listings_companies = job_listings_df[['company_name']]
employer_list = employer_list_df[['Organization Name', 'Email', 'Password']]

# Define a threshold for fuzzy matching
threshold = 90

# Function to find best match using fuzzy matching
def find_best_match(company, choices, threshold):
    match, score, _ = process.extractOne(company, choices, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else None

# Iterate through job listings and find best matches
valid_job_listings_df = pd.DataFrame()
invalid_job_listings_df = pd.DataFrame()

for idx, company in job_listings_companies.iterrows():
    company_name = company['company_name']
    match = find_best_match(company_name, employer_list['Organization Name'], threshold)

    if match:
        # Get the corresponding email and password from the employer list
        match_row = employer_list[employer_list['Organization Name'] == match].iloc[0]
        email = match_row['Email']
        password = match_row['Password']

        if pd.notnull(email) and pd.notnull(password):
            # Add the email and password to the job listings dataframe
            job_listings_df.at[idx, 'email'] = email
            job_listings_df.at[idx, 'password'] = password
            # Append the valid row to the new dataframe
            valid_job_listings_df = pd.concat([valid_job_listings_df, job_listings_df.iloc[[idx]]])
        else:
            # Append the invalid row to the new dataframe
            invalid_job_listings_df = pd.concat([invalid_job_listings_df, job_listings_df.iloc[[idx]]])
    else:
        # Append the invalid row to the new dataframe
        invalid_job_listings_df = pd.concat([invalid_job_listings_df, job_listings_df.iloc[[idx]]])

# Process and save the valid job listings dataframe if not empty
if not valid_job_listings_df.empty:
    today = datetime.today()
    valid_job_listings_df['date'] = today.day
    valid_job_listings_df['month'] = today.month
    valid_job_listings_df['year'] = today.year

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    valid_output_path = f'validate_job/Job_Listings_With_CompaniesEmailAndPassword_{current_date_time}.xlsx'
    valid_job_listings_df.to_excel(valid_output_path, index=False)
else:
    valid_output_path = "No valid job listings found."

# Save the invalid job listings dataframe if not empty
if not invalid_job_listings_df.empty:
    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    invalid_output_path = f'validate_job/CompaniesWithoutEmailAndPassword_{current_date_time}.xlsx'
    invalid_job_listings_df.to_excel(invalid_output_path, index=False)
else:
    invalid_output_path = "No companies without email and password found."

print(f"Valid job listings saved to: {valid_output_path}")
print(f"Companies without email and password saved to: {invalid_output_path}")
