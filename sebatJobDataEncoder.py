from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains

from jobDetailValidation import validate_job_details

class JobDataEncoder:
    def __init__(self, login_url, username, password):
        try:
            self.login_url = login_url
            self.username = username
            self.password = password
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            self.one_hot_encoder = OneHotEncoder(sparse_output=False)
            self.label_encoders = {}
            self.one_hot_encoded_columns = []
        except WebDriverException as e:
            print(f"Error initializing WebDriver: {e}")

    def capture_screenshot(self, filename):
        try:
            self.driver.save_screenshot(filename)
        except WebDriverException as e:
            print(f"Error capturing screenshot: {e}")

    def login(self):
            try:
                self.driver.get(self.login_url)
                time.sleep(2)  # Wait for the page to load

                sign_in_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.jobsearch-open-signin-tab'))
                )
                sign_in_link.click()
                time.sleep(2)  # Wait for the modal to appear

                # Ensure the modal is fully loaded and visible
                modal = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'JobSearchModalLogin'))
                )

                username_field = WebDriverWait(modal, 10).until(
                    EC.visibility_of_element_located((By.NAME, 'pt_user_login'))
                )
                username_field.send_keys(self.username)

                password_field = modal.find_element(By.NAME, 'pt_user_pass')
                password_field.send_keys(self.password)

                submit_button = modal.find_element(By.CSS_SELECTOR, 'input.jobsearch-login-submit-btn')
                submit_button.click()

                # Wait for the login process to complete
                time.sleep(5)

                # Check if login was successful by looking for a specific element that appears only when logged in
                try:
                    dashboard_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.jobsearch-column-3'))  # Adjust the selector to match your dashboard element
                    )
                    if dashboard_element:
                        print("Login successful!")
                        return True
                    else:
                        print("Login failed!")
                        return False
                except TimeoutException:
                    print("Login failed!")
                    return False
            except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                print(f"Login failed due to exception: {e}")
                return False
            except WebDriverException as e:
                print(f"WebDriver exception during login: {e}")
                return False

    def register_employer_account(self, registration_data):
        try:
            self.driver.get(self.login_url)
            time.sleep(2)  # Wait for the page to load

            # Click on the Register link
            register_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.jobsearch-open-register-tab'))
            )
            register_link.click()
            time.sleep(2)  # Wait for the modal to appear

            # Ensure the modal is fully loaded and visible
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'JobSearchModalLogin'))
            )

            # Choose Employer account type
            employer_account_type = WebDriverWait(modal, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.user-type-chose-btn[data-type="jobsearch_employer"]'))
            )
            employer_account_type.click()
            time.sleep(1)  # Wait for the form to adjust

            # Locate the registration form
            registration_form = WebDriverWait(modal, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'form[id^="registration-form-"]'))
            )

            # Ensure all fields are in view before interacting
            def scroll_to_element(element):
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)  # Wait for scrolling to complete

            # Fill out the registration form within the form element
            first_name_field = WebDriverWait(registration_form, 10).until(
                EC.element_to_be_clickable((By.NAME, 'pt_user_fname'))
            )
            scroll_to_element(first_name_field)
            first_name_field.send_keys(registration_data['first_name'])

            last_name_field = registration_form.find_element(By.NAME, 'pt_user_lname')
            scroll_to_element(last_name_field)
            last_name_field.send_keys(registration_data['last_name'])

            username_field = registration_form.find_element(By.NAME, 'pt_user_login')
            scroll_to_element(username_field)
            username_field.send_keys(registration_data['username'])

            email_field = registration_form.find_element(By.NAME, 'pt_user_email')
            scroll_to_element(email_field)
            email_field.send_keys(registration_data['email'])

            password_field = registration_form.find_element(By.NAME, 'pt_user_pass')
            scroll_to_element(password_field)
            password_field.send_keys(registration_data['password'])

            confirm_password_field = registration_form.find_element(By.NAME, 'pt_user_cpass')
            scroll_to_element(confirm_password_field)
            confirm_password_field.send_keys(registration_data['confirm_password'])

            phone_field = WebDriverWait(registration_form, 10).until(
                EC.element_to_be_clickable((By.NAME, 'pt_user_phone'))
            )
            scroll_to_element(phone_field)
            self.driver.execute_script("arguments[0].click();", phone_field)  # Trigger click to initialize validation
            time.sleep(1)  # Wait for the phone input to be fully initialized
            phone_field.send_keys(registration_data['phone'])

            organization_name_field = registration_form.find_element(By.NAME, 'pt_user_organization')
            scroll_to_element(organization_name_field)
            organization_name_field.send_keys(registration_data['organization_name'])

            # Handling job sectors input
            sectors_field = registration_form.find_element(By.CSS_SELECTOR, 'div.selectize-control')
            scroll_to_element(sectors_field)
            input_element = sectors_field.find_element(By.CSS_SELECTOR, 'input[type="text"]')

            for sector in registration_data['sectors']:
                input_element.send_keys(sector)
                input_element.send_keys(Keys.ENTER)
                time.sleep(0.5)  # Add a small delay to ensure each sector is added

            # Submit the registration form within the form element
            submit_button = WebDriverWait(registration_form, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.jobsearch-register-submit-btn'))
            )
            scroll_to_element(submit_button)
            submit_button.click()
            time.sleep(5)  # Wait for the registration to complete

            print("Employer account registration successful!")
            return True
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            print(f"Employer account registration failed due to exception: {e}")
            return False
        except NoSuchWindowException as e:
            print(f"No such window exception during employer registration: {e}")
            return False
        except WebDriverException as e:
            print(f"WebDriver exception during employer registration: {e}")
            return False

    def navigate_to_post_job(self):
        try:
            sidebar = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'aside.jobsearch-column-3'))
            )
            self.capture_screenshot('sidebar_visible.png')

            post_job_link = sidebar.find_element(By.CSS_SELECTOR, 'a[href*="tab=user-job"]')
            self.capture_screenshot('post_job_link_found.png')

            self.driver.execute_script("arguments[0].scrollIntoView(true);", post_job_link)
            time.sleep(1)  # Wait for the element to scroll into view

            self.capture_screenshot('post_job_link_scrolled_into_view.png')

            self.driver.execute_script("arguments[0].click();", post_job_link)
            time.sleep(3)  # Wait for the navigation to complete

            self.capture_screenshot('after_click.png')
            if "tab=user-job" in self.driver.current_url:
                print("Navigation to 'Post a New Job' form successful!")
                return True
            else:
                print("Navigation to 'Post a New Job' form failed!")
                return False
        except WebDriverException as e:
            self.capture_screenshot('navigation_exception.png')
            print(f"An error occurred during navigation: {e}")
            return False

    def fill_post_job_form(self, job_details):
        """
        Fill in the "Post a New Job" form with the provided job details.

        Parameters:
        job_details (dict): A dictionary containing job details.
        """
        job_details = {
            "job_title": "Host for TikTok",
            "job_description": "We at Afriwork (Freelance Ethiopia) are looking for a TikTok Host who is energetic and charismatic individual to join our team. The ideal candidate will be the face of our YouTube and TikTok channels, responsible for engaging with our audience, presenting content in an entertaining and informative manner, and contributing to the overall growth of our channels.\n\nResponsibilities:\n\n- Host and present various types of content including tutorials, reviews, interviews, vlogs, and live streams\n- Interact with viewers through comments, live chats, and social media\n- Collaborate with the content team to create, refine, and deliver scripts\n- Deliver engaging contents\n\nPlease send your CV and portfolio. And please submit a professional headshot with a clean background.",
            "application_deadline": "June 27th, 2024",
            "job_sector": ["Communications, Marketing, and Sales"],
            "job_type": ["Contract"],
            "skills": [],
            "job_apply_type": "external",
            "job_apply_url": "https://t.me/afriworkapplicantbot?start=7803d51d-52d4-4ec9-b109-16ab72dff0c4",
            "job_apply_email": "",
            "salary_type": "",
            "min_salary": "",
            "max_salary": "",
            "salary_currency": "",
            "salary_position": "",
            "salary_separator": "",
            "salary_decimals": "",
            "experience": "Fresh",
            "gender": "Female",
            "qualifications": [],
            "career_level": "Entry",
            "country": "Ethiopia",
            "state": "Addis Ababa",
            "city": "Addis Ababa",
            "postal_code": "",
            "full_address": "",
            "latitude": "",
            "longitude": "",
            "zoom": ""
        }

        # Wait for the form to be present
        validation_errors = validate_job_details(job_details)
        if validation_errors:
            print(f"Job details validation failed: {', '.join(validation_errors)}")
            return

        try:
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'form'))
            )

            # Helper function to find element within the form
            def find_element_in_form(by, value):
                return WebDriverWait(form, 10).until(
                    EC.presence_of_element_located((by, value))
                )

            all_fields_filled_successfully = True

            # Fill in the job title
            try:
                title_field = find_element_in_form(By.ID, 'ad-posting-title')
                self.driver.execute_script("arguments[0].value = arguments[1];", title_field, job_details['job_title'])
            except Exception as e:
                print(f"Error filling job title: {e}")
                all_fields_filled_successfully = False

            # Switch to the iframe for the job description
            try:
                self.driver.switch_to.frame(find_element_in_form(By.ID, 'job_detail_ifr'))
                description_field = self.driver.find_element(By.ID, 'tinymce')
                self.driver.execute_script("arguments[0].innerHTML = arguments[1];", description_field, job_details['job_description'])
                self.driver.switch_to.default_content()
            except Exception as e:
                print(f"Error filling job description: {e}")
                all_fields_filled_successfully = False

            # Fill in the application deadline
            try:
                deadline_field = find_element_in_form(By.ID, 'jobsearch_job_application_deadline')
                self.driver.execute_script("arguments[0].value = arguments[1];", deadline_field, job_details['application_deadline'])
            except Exception as e:
                print(f"Error filling application deadline: {e}")
                all_fields_filled_successfully = False

            # Select job sector
            try:
                for sector in job_details['job_sector']:
                    sector_field = find_element_in_form(By.CSS_SELECTOR, '#job-sector-multi + .selectize-control input')
                    sector_field.send_keys(sector)
                    sector_field.send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error selecting job sector: {e}")
                all_fields_filled_successfully = False

            # Select job type
            try:
                for job_type in job_details['job_type']:
                    job_type_field = find_element_in_form(By.CSS_SELECTOR, '#job-type-multi + .selectize-control input')
                    job_type_field.send_keys(job_type)
                    job_type_field.send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error selecting job type: {e}")
                all_fields_filled_successfully = False

            # Fill in skills
            try:
                for skill in job_details['skills']:
                    skill_field = find_element_in_form(By.CSS_SELECTOR, '#job-skills .tagit-new input')
                    skill_field.send_keys(skill)
                    skill_field.send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error filling skills: {e}")
                all_fields_filled_successfully = False

            # Select job apply type and fill application URL or email
            try:
                # Open the dropdown menu
                apply_type_field = find_element_in_form(By.CSS_SELECTOR, '#jobsearch_job_apply_type + .selectize-control .selectize-input')
                apply_type_field.click()

                # Select the appropriate option
                action_chain = ActionChains(self.driver)
                option = find_element_in_form(By.CSS_SELECTOR, f'#jobsearch_job_apply_type + .selectize-control .selectize-dropdown-content .option[data-value="{job_details["job_apply_type"].lower()}"]')
                action_chain.move_to_element(option).click().perform()

                if job_details['job_apply_type'].lower() == 'external':
                    apply_url_field = find_element_in_form(By.NAME, 'job_apply_url')
                    self.driver.execute_script("arguments[0].value = arguments[1];", apply_url_field, job_details['job_apply_url'])
                elif job_details['job_apply_type'].lower() == 'with_email':
                    apply_email_field = find_element_in_form(By.NAME, 'job_apply_email')
                    self.driver.execute_script("arguments[0].value = arguments[1];", apply_email_field, job_details['job_apply_email'])
            except Exception as e:
                print(f"Error selecting job apply type: {e}")
                all_fields_filled_successfully = False
            # Fill in the salary details
            try:
                salary_min_field = find_element_in_form(By.NAME, 'job_salary')
                self.driver.execute_script("arguments[0].value = arguments[1];", salary_min_field, job_details['min_salary'])

                salary_max_field = find_element_in_form(By.NAME, 'job_max_salary')
                self.driver.execute_script("arguments[0].value = arguments[1];", salary_max_field, job_details['max_salary'])

                salary_currency_field = find_element_in_form(By.CSS_SELECTOR, 'select[name="job_salary_currency"] + .selectize-control input')
                salary_currency_field.send_keys(job_details['salary_currency'])
                salary_currency_field.send_keys(Keys.ENTER)

                salary_position_field = find_element_in_form(By.CSS_SELECTOR, 'select[name="job_salary_pos"] + .selectize-control input')
                salary_position_field.send_keys(job_details['salary_position'])
                salary_position_field.send_keys(Keys.ENTER)

                salary_separator_field = find_element_in_form(By.NAME, 'job_salary_sep')
                self.driver.execute_script("arguments[0].value = arguments[1];", salary_separator_field, job_details['salary_separator'])

                salary_decimals_field = find_element_in_form(By.NAME, 'job_salary_deci')
                self.driver.execute_script("arguments[0].value = arguments[1];", salary_decimals_field, job_details['salary_decimals'])
            except Exception as e:
                print(f"Error filling salary details: {e}")
                all_fields_filled_successfully = False

            # Fill in experience
            try:
                experience_field = find_element_in_form(By.CSS_SELECTOR, 'select[name="experience"] + .selectize-control input')
                experience_field.send_keys(job_details['experience'])
                experience_field.send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error filling experience: {e}")
                all_fields_filled_successfully = False

            # Select gender
            try:
                gender_field = find_element_in_form(By.CSS_SELECTOR, 'select[name="gender"] + .selectize-control input')
                gender_field.send_keys(job_details['gender'])
                gender_field.send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error selecting gender: {e}")
                all_fields_filled_successfully = False

            # Fill in qualifications
            try:
                for qualification in job_details['qualifications']:
                    qualification_field = find_element_in_form(By.CSS_SELECTOR, 'select[name="qualifications[]"] + .selectize-control input')
                    qualification_field.send_keys(qualification)
                    qualification_field.send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error filling qualifications: {e}")
                all_fields_filled_successfully = False

            # Click submit button only if all fields were filled successfully
            if all_fields_filled_successfully:
                try:
                    submit_button = find_element_in_form(By.CSS_SELECTOR, 'input.jobsearch-employer-profile-submit.jobsearch-postjob-btn')
                    # submit_button.click()
                    print("Job form submitted successfully.")
                except Exception as e:
                    print(f"Error clicking submit button: {e}")
            else:
                print("Form was not submitted due to errors in filling fields.")

        except Exception as e:
            self.capture_screenshot('fill_form_exception.png')
            print(f"An error occurred while filling the form: {e}")

    def one_hot_encode(self, df, columns):
        try:
            self.one_hot_encoded_columns = columns

            one_hot_encoded = self.one_hot_encoder.fit_transform(df[columns])
            one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=self.one_hot_encoder.get_feature_names_out(columns))

            df = df.drop(columns, axis=1)
            df = pd.concat([df, one_hot_encoded_df], axis=1)

            return df
        except Exception as e:
            print(f"Error during one-hot encoding: {e}")

    def label_encode(self, df, columns):
        try:
            for column in columns:
                le = LabelEncoder()
                df[column] = le.fit_transform(df[column])
                self.label_encoders[column] = le
            return df
        except Exception as e:
            print(f"Error during label encoding: {e}")

    def inverse_transform_one_hot(self, encoded_df):
        try:
            if not self.one_hot_encoded_columns:
                raise ValueError("No columns have been one-hot encoded.")

            decoded_columns = self.one_hot_encoder.inverse_transform(
                encoded_df[self.one_hot_encoder.get_feature_names_out(self.one_hot_encoded_columns)]
            )

            decoded_df = pd.DataFrame(decoded_columns, columns=self.one_hot_encoded_columns)

            encoded_df = encoded_df.drop(self.one_hot_encoder.get_feature_names_out(self.one_hot_encoded_columns), axis=1)
            encoded_df = pd.concat([encoded_df, decoded_df], axis=1)

            return encoded_df
        except Exception as e:
            print(f"Error during inverse one-hot transformation: {e}")

    def inverse_transform_label(self, df, columns):
        try:
            for column in columns:
                if column in self.label_encoders:
                    le = self.label_encoders[column]
                    df[column] = le.inverse_transform(df[column])
                else:
                    raise ValueError(f"No label encoder found for column: {column}")
            return df
        except Exception as e:
            print(f"Error during inverse label transformation: {e}")

    def close(self):
        try:
            self.driver.quit()
        except WebDriverException as e:
            print(f"Error closing WebDriver: {e}")

    def logout(self):
        try:
            my_account_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "My Account"))
            )
            my_account_element.click()
            time.sleep(2)  # Wait for the dropdown to appear

            logout_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
            )
            logout_element.click()
            time.sleep(2)  # Wait for the logout to complete

            print("Logout successful!")
            return True
        except WebDriverException as e:
            print(f"An error occurred while logging out: {e}")
            return False