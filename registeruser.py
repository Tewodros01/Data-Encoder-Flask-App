from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import os
from excell_operation import save_unsuccessful_job_to_excel
from sebatJobDataEncoder import JobDataEncoder
import json
from database_operations import db, save_job_to_db, Job

app = Flask(__name__)

# Configuration for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sebatsab_dataencoder:dataencoder@sebatsolutions.com:3306/sebatsab_job_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

def organize_employer_data(employer_data):
    # Create a DataFrame from the job_data dictionary
    df = pd.DataFrame([employer_data])

    # Replace NaN values with empty strings
    df = df.fillna('')

    # Extract the first (and only) row as a dictionary
    employer_data_cleaned = df.iloc[0].to_dict()

    employer_data = {
        'first_name': employer_data_cleaned.get('first_name', ''),
        'last_name': employer_data_cleaned.get('email', ''),
        'username': employer_data_cleaned.get('email', ''),
        'email': employer_data_cleaned.get('email', ''),
        'password': 'company@7jobs12',
        'confirm_password': 'company@7jobs12',
        'phone': '900000000',
        'organization_name': employer_data_cleaned.get('first_name', ''),
        'sectors': 'Accounting, Finance, and Insurance',

    }

    return employer_data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
        # Ensure the uploads directory exists
        uploads_dir = os.path.abspath('uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        file_path = os.path.join(uploads_dir, file.filename)
        file.save(file_path)

        if file.filename.endswith('.xlsx'):
            employer_data = pd.read_excel(file_path)
        elif file.filename.endswith('.csv'):
            employer_data = pd.read_csv(file_path)

        results = []
        error_logs = []

        for index, row in employer_data.iterrows():
            data = row.to_dict()
            employer_data = organize_employer_data(data)
            try:
                print("Employer Data", data)

                encoder = JobDataEncoder(login_url='https://gamezone.7jobs.co', username='email', password='password')


                if encoder.register_employer_account(employer_data):
                     print("Registration done")
                     encoder.close()
                else:
                    save_unsuccessful_job_to_excel(employer_data)
                    error_message = "Failed to log in."
                    results.append({
                        "first_name": employer_data[""],
                        "status": "error",
                        "message": error_message
                    })
                    error_logs.append({"first_name": employer_data['first_name'], "error": error_message})
                    encoder.close()
            except Exception as e:
                print(f"Error posting job : {e}")
        if error_logs:
            error_df = pd.DataFrame(error_logs)
            error_df.to_excel(os.path.join(uploads_dir, 'error_log.xlsx'), index=False)

        return jsonify(results)
    else:
        return jsonify({'error': 'File type not allowed. Please upload an Excel file.'}), 400

if __name__ == "__main__":
    # Create the database tables if they do not exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
