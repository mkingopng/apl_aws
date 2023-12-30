"""
asdf
"""
from flask import Flask, render_template, request, flash
from config import CFG
from dynamodb_utilities import DynamoDBHandler
from validation import validate_email, validate_phone_number, validate_dob

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # todo: Needed for flashing messages

# Initialize DynamoDBHandler
handler = DynamoDBHandler(CFG.table_name)


@app.route('/', methods=['GET', 'POST'])
def index():
    """

    :return:
    """
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


# todo: app
#  needs multiple pages,
#  landing page,
#  summary of lifters entered page, weigh in,
#  administrative updates
#  bulk upload

# todo: entry form page,
#  logo, name of meet, date of meet, location etc
#  upload lifter image to S3
#  suggested inputs for each cell,
#  error handling,
#  format names,
#  note about successful registration

# todo:
#  lifter profile page,
#  lifter edit page,
#  lifter delete page,
