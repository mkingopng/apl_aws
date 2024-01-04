"""
This is the main file for the website. It contains the routes for the website.
"""
from flask import Flask, render_template, request, flash, redirect, url_for
import boto3
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
from web_site.config import table_name, meet_name
from web_site.dynamodb_utilities import DynamoDBHandler
from web_site.validation import validate_email, validate_phone_number, validate_dob


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
    return render_template('landing.html')


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    """

    :return:
    """
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

        # Validation checks
        if not validate_email(form_data['Email']):
            flash("Invalid email format.", "error")
        elif not validate_phone_number(form_data['phone_number']):
            flash("Invalid phone number format.", "error")
        elif not validate_dob(form_data['dob']):
            flash("Invalid date of birth.", "error")
        else:
            handler.add_lifter(form_data)
            flash("Registration successful!", "success")
            # Redirect to clear the form - redirects back to the entry page
            return redirect(url_for('entry'))

    return render_template('entry.html', my_variable=my_variable)


@app.route('/summary_of_lifters')
def summary_of_lifters():
    """
    Route to handle the summary of lifters page.
    :return:
    """
    return render_template('summary_of_lifters.html')


@app.route('/weigh_in')
def weight_in():
    """
    Route to handle the weigh in page.
    :return:
    """
    return render_template('weigh_in.html')


@app.route('/run_meet')
def run_meet():
    """
    Route to handle the run meet page.
    :return:
    """
    return render_template('run_meet.html')


@app.route('/results')
def results():
    """
    Route to handle the results page.
    :return:
    """
    return render_template('results.html')


if __name__ == '__main__':
    handler.create_table()  # create DynamoDB table if it doesn't exist
    app.run(debug=True)


