"""
asdf
"""
from flask import Flask, render_template, request, flash
from config import CFG
from dynamodb_utilities import DynamoDBHandler
from validation import validate_email, validate_phone_number, validate_dob

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # fix_me: Needed for flashing messages

# initialize DynamoDBHandler
handler = DynamoDBHandler(CFG.table_name)


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    """
    Route to handle the home page and form submission.
    """
    my_variable = CFG.meet_name

    if request.method == 'POST':
        form_data = request.form.to_dict()

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

    return render_template('entry.html', my_variable=my_variable)


@app.route('/summary_of_lifters')
def summary_of_lifters():
    return render_template('summary_of_lifters.html')


@app.route('/weigh_in')
def weight_in():
    return render_template('weigh_in.html')


@app.route('/run_meet')
def run_meet():
    return render_template('run_meet.html')


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    handler.create_table()  # Create DynamoDB table if it doesn't exist
    app.run(debug=True)


