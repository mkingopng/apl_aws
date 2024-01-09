"""
This is the main file for the website. It contains the routes for the website.
"""
import logging
import os
import boto3
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from _config import table_name, meet_name
from dynamodb_utilities import DynamoDBHandler
from validation import validate_email, validate_phone_number, validate_dob


load_dotenv()

current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

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
    return render_template('landing.html')


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

        if 'lifterImage' in request.files:  # handle file upload
            file = request.files['lifterImage']
            if file.filename != '':
                filename = secure_filename(file.filename)
                s3 = boto3.client('s3')
                bucket_name = 'apl-lifter-images'
                try:
                    s3.upload_fileobj(file, bucket_name, filename)
                    s3_file_url = f'https://{bucket_name}.s3.amazonaws.com/{filename}'
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
    # fix_me: flash messages are not showing


@app.route('/summary_of_lifters')
def summary_table():
    """
    Route to handle the summary of lifters page.
    :return:
    """
    lifters = handler.get_all_lifters()
    return render_template('summary_table.html', lifters=lifters)
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
    log_handler = logging.FileHandler(f'./../logs/flask_app.log')
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    # create DynamoDB table if it doesn't exist
    handler.create_table()

    app.run(debug=True)
