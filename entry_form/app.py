"""

"""
from flask import Flask, render_template, request, redirect, url_for, flash
from config import CFG
from dynamodb_utilities import DynamoDBHandler
from validation import validate_email, validate_phone_number, validate_dob
import pandas as pd


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # todo: Needed for flashing messages

# Initialize DynamoDBHandler
handler = DynamoDBHandler('apl_meet_entry')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form.to_dict()  # convert ImmutableMultiDict to a regular dict

        if not validate_email(form_data['Email']):
            flash("Invalid email format.", "error")
        elif not validate_phone_number(form_data['phone_number']):
            flash("Invalid phone number format.", "error")
        elif not validate_dob(form_data['dob']):
            flash("Invalid date of birth.", "error")
        else:
            # Save data to DynamoDB
            handler.add_lifter(form_data)
            flash("Registration successful!", "success")

    return render_template('index.html')


if __name__ == '__main__':
    handler.create_table()  # Create DynamoDB table if it doesn't exist
    app.run(debug=True)
