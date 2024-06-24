from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from sebatJobDataEncoder import JobDataEncoder
from sebatJobAnalysis import organize_job_information

app = Flask(__name__)

def organize_job_information_from_dict(job_data):
    organized_job = {
        'email': job_data.get('email'),
        'password': job_data.get('password'),
        'job_title': job_data.get('job_title', '').strip(),
        'job_description': job_data.get('job_description', '').strip(),
        'application_deadline': job_data.get('application_deadline', '').strip(),
        'job_sector': job_data.get('job_sector'),
        'job_type': job_data.get('job_type'),
        'skills': job_data.get('skills'),
        'job_apply_type': job_data.get('job_apply_type'),
        'job_apply_url': job_data.get('job_apply_url'),
        'job_apply_email': job_data.get('job_apply_email'),
        'salary_type': job_data.get('salary_type'),
        'min_salary': job_data.get('min_salary'),
        'max_salary': job_data.get('max_salary'),
        'salary_currency': job_data.get('salary_currency'),
        'salary_position': job_data.get('salary_position'),
        'salary_separator': job_data.get('salary_separator'),
        'salary_decimals': job_data.get('salary_decimals'),
        'experience': job_data.get('experience'),
        'gender': job_data.get('gender'),
        'qualifications': job_data.get('qualifications'),
        'field_of_study': job_data.get('field_of_study'),
        'career_level': job_data.get('career_level'),
        'country': job_data.get('country'),
        'state': job_data.get('state'),
        'city': job_data.get('city'),
        'postal_code': job_data.get('postal_code'),
        'full_address': job_data.get('full_address'),
        'latitude': job_data.get('latitude'),
        'longitude': job_data.get('longitude'),
        'zoom': job_data.get('zoom')
    }

    return organized_job

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

    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        job_df = pd.read_excel(file_path)
        results = []

        for index, row in job_df.iterrows():
            job_data = row.to_dict()
            jobInfo = organize_job_information_from_dict(job_data)
            print(jobInfo)
            results.append(jobInfo)

            encoder = JobDataEncoder(login_url='https://gamezone.7jobs.co', username=jobInfo['email'], password=jobInfo['password'])

            if encoder.login():
                if encoder.navigate_to_post_job():
                    encoder.fill_post_job_form(jobInfo)
                    if encoder.logout():
                        results.append({"status": "Logged out successfully after posting job."})
                    else:
                        results.append({"status": "Failed to log out."})
                encoder.close()
            else:
                results.append({"status": "Failed to log in."})
                encoder.close()

        return jsonify(results)
    else:
        return jsonify({'error': 'File type not allowed. Please upload an Excel file.'}), 400

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
