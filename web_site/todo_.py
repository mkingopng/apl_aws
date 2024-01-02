
# todo: entry form page,
#  bulk upload
#  logo, name of meet, date of meet, location etc
#  upload lifter image to S3 for each lifter
#  suggested inputs for each cell,
#  error handling & "cleansing" inputs,
#  format names,
#  flash note about successful or unsuccessful registration

# todo: lifter summary page,
#  show list of all lifters entered, and photo if supplied,
#  spread over multiple pages once number of lifters reaches a point,
#  administrative updates from lifters summary page,
#  lifter summary page,
#  lifter edit page,
#  lifter delete page,
#  bulk upload, etc

# Todo: pre meet page
#  weigh in
#  flights
#  other pre-meet tasks

# todo: write up what I've done so far

# todo:
#  :Variable Usage: use the additional variables in webpage as required
#  :Flashing Messages: Ensure your HTML template is set up to display flash
#  messages. Typically, this is done by looping over get_flashed_messages() in
#  Jinja2 templating.
#  :Secret Key: The secret key is used for securely signing the session
#  cookie and should be a strong, random value in a production environment.
#  :DynamoDB Table Creation: The script includes a call to
#  handler.create_table() at startup, which is fine for development but
#  might not be ideal for production. Consider handling your table creation
#  separately from your application logic.
#  :Error Handling: Consider adding error handling around the DynamoDB
#  operations to gracefully handle any exceptions that might occur.
#  :Security Practices: Make sure to follow best practices for web application
#  security, such as validating and sanitizing all user inputs to prevent
#  injection attacks.
#  :HTML Template: Verify that your entry.html template is correctly set up to
#  handle the dynamic content (both the variable and the flashed messages).
#  By ensuring these points are addressed, your Flask app should function as
#  intended, handling form submissions, interacting with DynamoDB, and
#  displaying dynamic content based on Python variables.

# todo: update IAM creds
#  test locally
#  connect to dynamo db in IDE so i can see the data
#  add logging throughout
