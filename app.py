"""
This is the main file for the website. It contains the routes for the website.
"""
import logging
import boto3
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from CFG import table_name, meet_name
from dynamodb_utilities import DynamoDBHandler
from validation import validate_email, validate_phone_number, validate_dob
import sys
import os
import calculators

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    c_handler = logging.StreamHandler()  # console handler
    c_handler.setLevel(logging.INFO)

    f_handler = logging.FileHandler(f'logs/app_log_{current_time}.log')
    f_handler.setLevel(logging.INFO)  # file handler

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(formatter)  # Create formatters & add to handlers
    f_handler.setFormatter(formatter)

    logger.addHandler(c_handler)  # add handlers to the logger
    logger.addHandler(f_handler)

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# initialize DynamoDBHandler
handler = DynamoDBHandler(table_name)


@app.route('/')
def landing():
    """
    Route to handle the landing page.
    :return:
    """
    my_variable = meet_name
    return render_template('landing.html', my_variable=my_variable)


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    """
    enter meet by filling in lifter details and the submitting
    :return:
    """
    app.logger.info("Processing the entry route")
    my_variable = meet_name

    if request.method == 'POST':
        form_data = request.form.to_dict()
        app.logger.info(f"Form data: {form_data}")

        # Ensure new fields are included
        if 'tested_or_open' not in form_data or 'weight_class' not in form_data:
            flash("Missing information in the form.", "error")
            return render_template('entry.html', my_variable=my_variable)

        if 'lifterImage' in request.files:
            file = request.files['lifterImage']
            if file.filename != '':
                filename = secure_filename(file.filename)
                s3 = boto3.client('s3')
                bucket_name = 'apl-lifter-images'
                try:
                    s3.upload_fileobj(file, bucket_name, filename)
                    s3_file_url = (f'https://{bucket_name}.s3.amazonaws.com/{filename}')
                    form_data['image_url'] = s3_file_url
                except Exception as e:
                    flash(f"Error uploading image: {str(e)}", "error")
                    return render_template('entry.html', my_variable=my_variable)

        # validation checks
        if not validate_email(form_data['Email']):
            flash("Invalid email format.", "error")
        elif not validate_phone_number(form_data['phone_number']):
            flash("Invalid phone number format.", "error")
        elif not validate_dob(form_data['dob']):
            flash("Invalid date of birth.", "error")
        else:
            handler.add_lifter(form_data)
            flash("Registration successful!", "success")
            # fix_me: redirect to clear the form - redirects back to entry page
            return redirect(url_for('entry'))

    return render_template('entry.html', my_variable=my_variable)


@app.route('/summary_of_lifters')
def summary_table():
    """
    Route to handle the summary of lifters page.
    :return:
    """
    my_variable = meet_name
    lifters = handler.get_all_lifters()
    return render_template('summary_table.html', my_variable=my_variable, lifters=lifters)


# fix_me: need to see the image for each lifter, if supplied
# todo: build this out


@app.route('/weigh_in')
def weight_in():
    """
    Route to handle the weigh in page.
    :return:
    """
    return render_template('weigh_in.html')

    # todo: build this out


@app.route('/calculator')
def calculator_page():
    return render_template('calculate_scores.html')


@app.route('/calculate_scores', methods=['POST'])
def calculate_scores():
    """

    :return:
    """
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")
        results = calculators.get_scores(
            float(data['bodyWeight']),
            float(data['totalLift']),
            data['unit'] == 'kg',
            data['gender'] == 'female',
            data['competition']
        )
        app.logger.info(f"Results: {results}")
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Error in calculate_scores: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/estimate_deadlift', methods=['POST'])
def planned_deadlift():
    """
    Estimate the deadlift attempt required to achieve a target score.
    """
    try:
        data = request.get_json()
        # extract necessary data from request and convert to appropriate types
        body_weight = float(data['bodyWeight'])
        best_squat = float(data['bestSquat'])
        best_bench = float(data['bestBench'])
        target_score = float(
            data['targetScore'])  # Convert targetScore to float
        is_female = data['gender'] == 'female'
        is_kg = data['unit'] == 'kg'

        # calculate the required dead lift attempt
        required_deadlift = calculators.calculate_required_deadlift(
            body_weight, best_squat, best_bench, target_score, is_female, is_kg
        )

        # return the result
        return jsonify(required_deadlift)
    except Exception as e:
        app.logger.error(f"Error in estimate_deadlift: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/run_meet')
def run_meet():
    """
    Route to handle the run meet page.
    :return:
    """
    return render_template('run_meet.html')
    # todo: build this out


@app.route('/results')
def results():
    """
    Route to handle the results page.
    :return:
    """
    return render_template('results.html')
    # todo: build this out


if __name__ == '__main__':
    # Set the logging level. You can change it to DEBUG or ERROR as needed.
    app.logger.setLevel(logging.INFO)

    # Optional: Add a file handler to also log to a file.
    log_handler = logging.FileHandler(f'logs/flask_app.log')
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    # create DynamoDB table if not exists
    handler.create_table()

    app.run(debug=True)
