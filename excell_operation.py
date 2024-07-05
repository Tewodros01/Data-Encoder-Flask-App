import os
import pandas as pd
from datetime import datetime

def save_unsuccessful_job_to_excel(job_details):
    """
    Save unsuccessful job details to an Excel file.

    Parameters:
    job_details (dict): A dictionary containing job details.
    """
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Define the filename
    filename = f"unsuccessful_jobs_{current_date}.xlsx"

    # Create a DataFrame from the job details
    df = pd.DataFrame([job_details])

    # Check if the file already exists
    if os.path.exists(filename):
        # Append to the existing file
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)

    # Write to the Excel file
    df.to_excel(filename, index=False)