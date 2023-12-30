

## launch the website
```bash
cd web_site
python app.py
```

## test the lambda functions
```bash
cd web_site
python test_lambda.py
```

## tests
```bash
pytest
```

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

- Ensure to design your database schema to optimize read/write operations 
within Free Tier limits.

### 4. Data Flow
- **Lifter Registration**: When a lifter submits their information on the 
landing page, the data is sent to a Lambda function via API Gateway. The 
Lambda function then processes and stores this data in DynamoDB.

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
- **AWS SDK for Python (Boto3)**: 
[AWS SDK for Python (Boto3) Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

- **AWS Free Tier**: [AWS Free Tier Details](https://aws.amazon.com/free/)

- **Web Development**: Consider online tutorials for basic web development if 
needed.

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

## Design Notes
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

## Blogging about the project
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

## Entry

1. web app to enter

### entry form info
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

## Meet Results

| Date       | Name                                | Location               | CSV |
|------------|-------------------------------------|------------------------|-----|
| 09-07-2023 | Strength Quest 3                    | Ground Zero            | ✓   |
| 02-07-2023 | Winter Cup                          | Strength HQ            | ✓   |
| 2023-07-01 | Deep North Powerlifting Challenge   | Iron Strength          |     |
| 2023-07-01 | Winter Warm Up                      | Ethos Strength         |     |
| 2023-06-24 | BNB Bash X                          | BNB                    |     |
| 2023-06-16 | APL Drug Tested Nationals           | QMC                    | ✓   |
| 2023-06-10 | Defiance                            | Ruthless Barbell       | ✓   |
| 2023-04-23 | Bens Army Services Tribute          | Bens Army              | ✓   |
| 2023-04-01 | NSW State Championships             | Strength Tribe         | ✓   |
| 2023-03-26 | VIC State Championships             | Strength HQ            | ✓   |
| 2023-03-26 | WA drug tested states               | Ruccis gym             | ✓   |
| 2023-03-26 | QLD State Championships             | Ground ZeroW           | ✓   |
| 2023--3-19 | ACT State Championships             | Burley Strength        | ✓   |
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