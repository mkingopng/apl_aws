# test launch the website
```bash
python app.py
```

# Testing
```bash
export PYTHONPATH=/home/noone/Documents/GitHub/apl_aws:$PYTHONPATH
pytest
```

### test the lambda functions
```bash
cd web_site
python test_lambda.py
```

### pytest
This works to test both while they are in the web_site_directory. This will 
need to change when they get moved to a tests directory

# todo: 
- bulk upload, 
- summary of lifters page
- weigh in page
- refactor test_dynamodb_utilities.py tests to eliminate repetition
- 
- how can we improve communication between meet organisers and the lifters and coaches

## todo: UI
- enhance visual appeal with a more modern or interactive design, improve form 
layout for better readability and user experience
  
- **Visual Feedback**: For interactive elements like the image upload you've 
just implemented, provide visual feedback (like the image preview) to 
reassure users that their actions are successful.

- mandatory vs non-mandatory fields

- **Error Handling and Validation**: Implement client-side validation for the 
form fields to ensure data quality before submission.Provide clear, immediate 
feedback when a user enters invalid information or skips a required field. 
Display user-friendly error messages in case of invalid inputs.

- **Messages**: let user know if they have successfully submitted the form or 
not. If successful, clear contents of cells.

- **Visual Hierarchy**: Use typography (size, weight) and color strategically 
to create a visual hierarchy. Important elements like section headings or key 
fields should stand out.
  
- **Responsive Design**: Ensure the form looks good and is easy to use on all 
devices. This may involve making input fields full-width on smaller screens 
and adjusting margins and padding.
  
- **Call-to-Action Buttons**: Make your submit button prominent and easy to 
find. Optionally, provide a clear button or a reset option.
  
- **Avoid Clutter**: Keep the design as simple as possible. Remove 
unnecessary elements or information that doesn't directly help in filling out 
the form.

- **Styling and Theme Consistency**: Ensure that the form's styling (colors, 
fonts, button styles) is consistent with the overall website theme to provide 
a seamless user experience.

## Accessibility:
- Make sure your website is accessible, including keyboard navigation and 
screen reader compatibility.
- Use ARIA (Accessible Rich Internet Applications) attributes where necessary.

## Responsive Design:
- Although there's a basic media query for responsiveness, further refine the 
design for different devices and screen sizes.

## Security:
- If not already implemented, ensure that data submitted through the form is 
properly sanitised and validated on the server-side to prevent injection 
attacks.

## Advanced Features:
- Consider adding a progress bar for the image upload. 
- Implement a date picker for the date of birth field for ease of use. 
- Include dynamic form fields (e.g., autofill city and state based on postal 
code).

## Performance Optimization:
- Optimize load times by compressing images and minifying CSS and JavaScript.

## SEO and Analytics:
- Add meta-tags for SEO optimisation.
- Integrate analytics to track user interactions with the form.

-------------------------------------

# apl_aws
The project idea is creating a platform for organising and running powerlifting 
events using AWS and Python. Leveraging the AWS Free Tier can be an 
efficient way to manage costs while building the application. Here's a 
high-level approach for your project:

## Step 1

### 1. Project Setup
- **AWS Account**: Ensure you have an AWS account and understand the limits of 
the AWS Free Tier.

- **Development Environment**: Set up your local environment with Python,  
AWS SDK (Boto3), and IAM authentication.

### 2. Registration Landing Page
- **Frontend**: Create a simple landing page using HTML/CSS/JavaScript.

  - AWS offers **AWS Amplify** which can be used for hosting static web pages. 
  Amplify falls under the Free Tier if the usage is within certain limits.
  
  - Alternatively, you could use **S3** to host a static website.

- **Backend**: For backend processing, you can use AWS Lambda (serverless 
compute) which integrates well with other AWS services and has a generous Free 
Tier offering.

- **API Gateway**: To connect your frontend with Lambda functions, use Amazon 
API Gateway.

### 3. Database
- **DynamoDB**: Store lifter registration details in Amazon DynamoDB, a NoSQL 
database service.
- **S3** Object storage: to store the lifter pics
- Ensure to design your database schema to optimise read/write operations 
within Free Tier limits.

### 4. Data Flow
- **Lifter Registration**: When a lifter submits their information on the 
landing page, the data is sent to a Lambda function via API Gateway. The 
Lambda function then processes and stores this data in DynamoDB.
- other steps:
  - weigh-in
  - run meet
  - calculate results
  - calculator
  - depth checker
  - improved analytics
  - lifter profile during meet

### 5. Development Steps
1. **Design Your Web Page**: Create the HTML form for lifter registration.

2. **Set Up API Gateway**: Create an API endpoint that your form can call upon 
submission.

3. **Lambda Function**: Write a Lambda function in Python to process the form 
data and write it to DynamoDB.

4. **DynamoDB Setup**: Create a table in DynamoDB to store the registration 
data.

5. **Test**: Ensure the entire flow works from form submission to data storage.

### 6. Considerations
- **Security**: Implement proper security measures, especially for data 
handling.

- **AWS Free Tier Limits**: Regularly monitor your usage to stay within the 
Free Tier limits.

- **Scalability**: Design your application to be scalable in case you need to 
move beyond the Free Tier in the future.

### 7. Next Steps
- After the registration module, you can expand to other features like weigh-in 
management, scheduling, and live updates during the event.

### Resources
- **AWS SDK for Python (Boto3)**: [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- **AWS Free Tier**: [AWS Free Tier Details](https://aws.amazon.com/free/)
- **Web Development**: [Flask](https://flask.palletsprojects.com/en/3.0.x/)

Start with the registration step, breaking down the project into manageable 
parts, which is an effective approach. Test each component thoroughly before 
moving on to the next phase.

## Estimated Time

1. **Frontend Development (Landing Page & Form)**:
   - Prototype using streamlit before moving on
   - figure out what data we get from eventbrite. most likely JSON. mimic this 
   in prototype
     - email validation, phone number validation, date validation functions;
     - display appropriate error messages using `st.error()` if any validation 
     fails
     - data handling, output to JSON to mimic API
     - process data and save to data-base
     - styling to look pretty
     - security
   - Basic HTML/CSS/JavaScript: 3-6 hours
   - More complex or polished design: additional 2-4 hours

2. **Setting Up AWS Services (API Gateway, Lambda, DynamoDB)**:
   - Learning and initial setup: 4-8 hours
   - Configuration and integration: 2-4 hours

3. **Backend Development (Lambda Function)**:
   - Writing and testing the Lambda function: 3-5 hours

4. **Integration and Testing**:
   - Integrating frontend with backend and testing the end-to-end process: 2-4 
   hours

5. **Additional Time for Learning/Debugging**:
   - If you are new to some technologies or AWS services: additional 
   5-10 hours

**Total Estimated Time**: 14-37 hours

### Considerations:

- **Experience Level**: If you are experienced with AWS, Python, and web 
development, you might be at the lower end of the estimate. For beginners, it 
might take longer.

- **Design and Feature Complexity**: A simple design with basic features will 
take less time compared to a more complex and feature-rich application.

- **Debugging and Troubleshooting**: This can often take more time than 
anticipated, especially with new technology stacks.

- **Learning Curve**: If you need to learn new technologies or AWS services, 
factor in additional time for tutorials and documentation.

-----------------------------------------

# Design Notes
Remember, these are rough estimates and actual development times can vary. It's 
always a good practice to start with a **minimal viable product (MVP)** and 
then iterate based on feedback and requirements.

A "Minimal Viable Product" (MVP) is a development strategy used to build a new 
product or service with sufficient features to attract early adopter customers 
and validate a product idea early in the product development cycle. The key 
aspects of an MVP are:

1. **Core Features**: It includes only the essential features that allow the 
product to be deployed, and no more. The goal is to provide immediate value, 
quickly, while minimizing development costs.

2. **Feedback Loop**: An MVP is designed to test a product hypothesis with 
minimal resources. It acts as a baseline for the product which can be used to 
gather user feedback that guides future development.

3. **Iteration and Improvement**: Based on feedback, the product is refined and 
improved. Additional features and enhancements are made over time, responding 
to user needs and demands.

In the context of your powerlifting event organisation platform, an MVP would 
include just enough features to allow for basic registration of participants, 
perhaps with a simple database backend and a basic user interface. This would 
be your starting point, from which you could add more features like weigh-in 
management, scheduling, real-time updates, and more, based on user feedback and 
demand.

1. **Agile Development**: A methodology emphasizing iterative development, 
where requirements and solutions evolve through collaborative effort. It allows 
for flexible response to change and encourages frequent reassessment of 
progress.

2. **Version Control**: Using tools like Git for source code management. It 
helps in tracking changes, collaborating with others, and managing different 
versions of your codebase.

3. **Test-Driven Development (TDD)**: A software development approach where you 
write tests for your functions before writing the function code itself. It 
ensures that your code does what it's supposed to do and leads to cleaner, more 
reliable code.

4. **Continuous Integration/Continuous Deployment (CI/CD)**: This practice 
involves automatically testing and deploying your code changes to a production 
environment. It helps in reducing manual errors and speeds up the release 
process.

5. **User Experience (UX) Design**: Focusing on the end-user's experience and 
ease of use. A good UX design can significantly increase user satisfaction and 
adoption rates.

6. **Responsive Design**: Ensuring that your web application looks good and 
functions well on a variety of devices and screen sizes.

7. **API Design and Development**: Designing efficient and scalable APIs if 
your application needs to communicate with other services or if you plan to 
expose parts of your service to third parties.

8. **Security Best Practices**: Understanding and implementing security 
measures to protect your application and user data. This includes secure coding 
practices, data encryption, and understanding AWS security features.

9. **Scalability and Performance Optimization**: Building your application in a 
way that it can handle growth in users or data without significant rework. This 
includes understanding AWS scalability options.

10. **Code Refactoring**: Regularly revising your code to improve its structure 
and readability without changing its functionality. This helps in maintaining 
and scaling your codebase over time.

11. **Documentation**: Keeping clear and comprehensive documentation for your 
code and architecture. This is crucial for collaboration, maintenance, and 
scaling your team.

12. **User Feedback and Analytics**: Implementing tools to collect user 
feedback and usage analytics. This data is invaluable for understanding how 
your product is used and what improvements are needed.

Each of these concepts plays a vital role in modern software development and 
can contribute significantly to the success of your project. As you progress, 
you'll likely find some more relevant to your needs than others, but having a 
foundational understanding of each will be highly beneficial.

------------------------------------------------------

# Blogging about the project
Blogging about my project on platforms like LinkedIn and Medium. My 
project has several compelling aspects that should make for engaging and 
informative blog content:

1. **Real-World Impact**: Sharing how your project addresses a genuine need, 
like modernizing the management of powerlifting events, makes your story 
relatable and impactful. Readers are often interested in real-world 
applications of technology.

2. **Learning Journey**: Documenting your process of learning new technologies 
is incredibly valuable to others who might be on a similar path. It shows your 
ability to tackle new challenges and adapt, which is highly regarded in the 
tech industry.

3. **Diversity in Skills**: Demonstrating a range of skills beyond your primary 
field can indeed make you appear more well-rounded. It highlights your 
versatility and willingness to step out of your comfort zone.

4. **Portfolio Enhancement**: Discussing a unique project enhances your 
portfolio, showcasing your abilities in areas like cloud development and 
full-stack project execution.

5. **Networking and Visibility**: Blogging on platforms like LinkedIn can 
increase your visibility in the professional community, opening doors for 
networking and job opportunities.

6. **Sharing Insights and Solutions**: Your experiences can offer valuable 
insights to others facing similar challenges or considering similar projects.

### Tips for Blogging About Your Project:

- **Start Early**: Begin writing about your project from the early stages. 
Share your motivations, initial challenges, and setup.

- **Regular Updates**: Provide regular updates on your progress, what you've 
learned, and any hurdles you've overcome.

- **Technical Deep-Dives**: Occasionally dive deep into a particular technology 
or problem you solved. This can attract readers interested in those specific 
areas.

- **Lessons Learned**: Reflect on what worked well and what didn’t, offering 
advice that others can learn from.

- **Engage with Readers**: Encourage feedback and questions. Engaging with your 
readers can provide additional insights and build a community around your 
interests.

- **Visuals and Demos**: Use visuals or demos to make your content more 
engaging and easier to understand.

- **Final Reflections**: Once the project is complete, share your overall 
experience, outcomes, and how it has impacted your friend's powerlifting 
federation.

Blogging your journey not only benefits your personal and professional growth 
but also contributes knowledge to the broader community. It's a win-win 
situation that can open up new opportunities and collaborations.

-----------------------------------------------------------------------
# Summary December 24th - January 2nd
Here's a summary so far:

1. **Project Overview**: I am developing a Flask-based web application for 
organizing and running powerlifting events. The application with the goal of 
improving the efficiency of meet administration, 

Right now, it includes a landing page and form for lifter registration, 
initially replacing handwritten entry forms.THis is somewhat redundant as APL 
uses Eventbrite for entries, so this will be replaced by an API call at some 
point. For now, storing entries in DynamoDB and returning a JSON replicates the 
expected behaviour of the API call.

the next step will be complete the summary page which allows the viewer to see
all the lifter entries and their profile pictures.

Next will be the weigh-in page, which will allow the weigh-in official to enter 
the actual body-weight of the lifter and the time of weigh-in. This will be 
stored in DynamoDB and displayed on the summary page.

Next step will be to add the calculations page, this calculates the various 
ratios used in powerlifting to adjust for gender, age and weight.

Next step will be to add the pre-meet functionality, especially splitting the 
lifters into flights and assigning the flight to a time. Any other 
functionality I've forgotten

Next will be the functionality to run the meet from the app rather than using 
Excel spreadsheets.
- judging
- loaders
- timers
- enter next attempt
- call next lifter

2. **AWS and Python SDK Usage**: The application utilizes AWS services, 
particularly DynamoDB for database storage and S3 for image uploads. I aim 
to use the free tier resources as much as possible. As the project grows it 
will need different resources. The most immediate is to add AWS API gateway 
to connect the frontend with the backend, and lambda functions for the S3 image 
uploads.

3. **Form Development**: I worked on creating a landing page and a web form 
using Flask, where users can submit their details. The form includes fields for 
name, email, phone number, gender, equipment type, event type, date of birth, 
and next of kin information.

4. **Data Validation and Processing**: I added Python functions for validating 
email, phone numbers, and dates. These functions ensure the integrity of the 
data entered into the form. These need to be expanded and improved

5. **DynamoDB Integration**: You've implemented functionality to interact with 
DynamoDB, including creating tables and saving entries from the form.

6. **Image Upload to S3**: I implemented a feature for users to a upload 
profile image related to their meet entry, which are stored in an S3 bucket, 
and related to the meet entry via a primary key

7. **Flask App Enhancements**: We improved the Flask app by handling AJAX form 
submissions, displaying flash messages for form submission feedback, and 
implementing logic for clearing the form upon successful submission.

8. **Lambda Functions**: We created AWS Lambda functions for CRUD 
(Create, Read, Update, Delete) operations related to the DynamoDB entries. 
Probably need to add AWS API Gateway to connect the frontend with the backend, 
and lambda functions for the S3 image uploads.

9. **Front-End Development**: We worked on the front-end aspect, including HTML 
and CSS modifications for styling and layout adjustments. We have limited js 
functionality for now, but will add more later as the project matures. I've 
chosen Flask as the framework for the front end for now, but may move to Django 
later if more functionality is required. THe website currently has a landing 
page, and the entry form page. There are place-holders for the other 4 pages

10. **Debugging and Troubleshooting**: Throughout the development, we addressed 
various issues such as 405 errors, form submission bugs, and problems with 
image uploads to S3.

11. **Security and Configuration**: Discussed using `.env` files for managing 
environment variables and configuring the Flask secret key for session 
security.

12. **testing** I implemented a few tests using pytest, including testing the 
lambda functions and the flask app. I am trying to keep tests concurrently up 
to date with the general development of the application.

This summary captures the key aspects of our discussion. You can use it to 
continue the thread or start a new one, focusing on further development, 
troubleshooting, or any specific aspect of the project you wish to concentrate 
on next.


"""
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

:Variable Usage: use the additional variables in webpage as required

:Flashing Messages: Ensure your HTML template is set up to display flash
messages. Typically, this is done by looping over get_flashed_messages() in
Jinja2 templating.

:Secret Key: The secret key is used for securely signing the session
cookie and should be a strong, random value in a production environment.

:DynamoDB Table Creation: The script includes a call to
handler.create_table() at startup, which is fine for development but
might not be ideal for production. Consider handling your table creation
separately from your application logic.

:Error Handling: Consider adding error handling around the DynamoDB
operations to gracefully handle any exceptions that might occur.

:Security Practices: Make sure to follow best practices for web application
security, such as validating and sanitizing all user inputs to prevent
injection attacks.

:HTML Template: Verify that your entry.html template is correctly set up to
handle the dynamic content (both the variable and the flashed messages).
By ensuring these points are addressed, your Flask app should function as
intended, handling form submissions, interacting with DynamoDB, and
displaying dynamic content based on Python variables.

# todo: update IAM creds
#  test locally
#  connect to dynamo db in IDE so i can see the data
#  add logging throughout

# todo: logging

# todo: update test to include S3 bucket

# todo:
"""




-----------------
# Notes on ideas for the project
1. meet entry
   - gather required data
   - process and enter into database
   - payment
2. weigh in
   - weigh lifter
   - record weight
3. Run meet
4. Calculate Results
5. Calculator
6. depth checker
7. improved analytics
8. lifter profile during meet


---------------------------------------------
# entry form info
- First Name
- Last Name
- Email
- Phone Number
- Gender: 
- Equipment: sleeves, wraps, single-ply
- Event: SBD, Bench Only, Deadlift Only
- DOB: 
- Age: (calculated from DOB)
- Age Group: (calculated from DOB)
  - {junior: [14-18]}
  - {open: [18-39]}
  - {master: [40-49, 50-59, 60-69, 70+]}
- Weight Class (in KG): 
  - {male: [56, 60, 67.5, 75, 82.5, 90, 100, 110, 125, 140, 140+]}
  - {female: [44, 48, 52, 56, 60, 67.5, 75, 82.5, 90, 100, 110, 110+]}
- Next of Kin Name
- Next of Kin Phone Number

----------------------------------------------------------------------
# Meet Results
we have competition records for the following meets

| Date       | Name                                | Location               | CSV |
|------------|-------------------------------------|------------------------|-----|
| 2023-09-07 | Strength Quest 3                    | Ground Zero            | ✓   |
| 2023-07-02 | Winter Cup                          | Strength HQ            | ✓   |
| 2023-07-01 | Deep North Powerlifting Challenge   | Iron Strength          |     |
| 2023-07-01 | Winter Warm Up                      | Ethos Strength         |     |
| 2023-06-24 | BNB Bash X                          | BNB                    |     |
| 2023-06-16 | APL Drug Tested Nationals           | QMC                    | ✓   |
| 2023-06-10 | Defiance                            | Ruthless Barbell       | ✓   |
| 2023-04-23 | Ben's Army Services Tribute         | Ben's Army             | ✓   |
| 2023-04-01 | NSW State Championships             | Strength Tribe         | ✓   |
| 2023-03-26 | VIC State Championships             | Strength HQ            | ✓   |
| 2023-03-26 | WA drug tested states               | Rucci's gym            | ✓   |
| 2023-03-26 | QLD State Championships             | Ground ZeroW           | ✓   |
| 2023-03-19 | ACT State Championships             | Burley Strength        | ✓   |
| 2023-03-18 | Lift3 tested qualifier              | Lift3                  | ✓   |
| 2023-03-12 | Cairns Cup                          | ZeroW Cairns           | ✓   |
| 2023-03-10 | Complete Strength Open              | Complete Strength      | ✓   |
| 2023-03-05 | Nationals Qualifier                 | ZeroW Mackay           | ✓   |
| 2023-02-25 | SA State Championships              | Ethos Strength         | ✓   |
| 2023-02-12 | BNB Brawl                           | Brisbane North Barbell | ✓   |
| 2023-02-12 | Strength HQ nationals qualifier     | Strength HQ            | ✓   |
| 2023-02-05 | Hobart Cup                          | Leviathan Strength     | ✓   |
| 2022-12-11 | Victoria Christmas Cup              | Strength HQ            | ✓   |
| 2022-12-03 | Queensland Christmas Cup            | Ground ZeroW           | ✓   |
| 2022-12-04 | NSW Christmas Cup                   | Lift3                  | ✓   |
| 2022-11-03 | IPL drug tested world championships | Gold Coast             | ✓   |
| 2022-10-02 | Strength Quest 2                    | Ground ZeroW           | ✓   |
| 2022-09-25 | Yeti Classic                        | Apex Strength          | ✓   |
| 2022-09-11 | Spring Classic                      | Burley Strength        | ✓   |
| 2022-08-27 | APL Open                            | Simm City              | ✓   |
| 2022-08-27 | Ethos Cup                           | Ethos Strength         | ✓   |
| 2022-08-14 | Lift3 Winter Cup                    | Lift3                  | ✓   |
| 2022-08-07 | Mackay National Qualifier           | ZeroW Mackay           | ✓   |
| 2022-06-17 | APL Open Nationals                  | Gold Coast             | ✓   |
| 2022-06-17 | APL Drug Tested Nationals           | Gold Coast             | ✓   |