"""
simple web-based entry form to collect lifter's data for meet.

output is JSON to replicate expected output from EventBrite API

"""
import streamlit as st
import re
from datetime import date
import pandas as pd
import os


data_path = './../data'

# Define the DataFrame structure
columns = ["First Name", "Last Name", "Email", "Phone Number", "Gender", "Equipment", "Event", "Date of Birth", "Next of Kin Name", "Next of Kin Phone Number"]
data = pd.DataFrame(columns=columns)


def validate_email(email):
    """
    This function checks if the provided email string matches the pattern of a
    standard email address. It uses regex to ensure that the email address
    consists of characters allowed in the local part of the email, followed by
    an '@' symbol, and a domain part which includes domain labels separated by
    periods. The domain labels cannot start or end with hyphens.

    :param email: (str) The email address to be validated.
    :return: (bool) True if email address is in valid format, else False.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone_number(phone):
    """
    Validate a phone number to ensure it has 10 digits and starts with 0.
    This function uses regular expression to validate the phone number format.
    The phone number is expected to be a string or an integer. It first
    converts the phone number to a string (if it isn't already), then checks if
    it matches the pattern of starting with zero followed by exactly nine other
    digits.

    :param phone: (str or int): The phone number to be validated.
    :return bool: True if the phone number is valid, False otherwise.
    """
    pattern = r'^0\d{9}$'
    return re.match(pattern, str(phone)) is not None


def validate_dob(dob):
    """
    This function checks if the provided date of birth (dob) is a valid date
    not in the future. It compares the dob against the current date. The
    function assumes that the dob is provided as a date object. If the dob is
    today or in the past, the function returns True, indicating it's valid. If
    the dob is in the future, it returns False, indicating an invalid date of
    birth.

    :param dob: (Date) The date of birth to be validated. Expected to be a date
    object.
    :return: (Bool) True if the date of birth is today or in the past, False if
    it is in the future
    """
    today = date.today()
    return dob <= today


# title
st.title("Australian Powerlifting League Meet Registration")

# Creating form fields
with st.form(key='registration_form'):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email", help="Enter a valid email address")
    phone_number = st.text_input("Mobile Phone Number")
    gender = st.selectbox("Gender", options=["Male", "Female"])
    equipment = st.selectbox("Equipment", options=["Sleeves", "Wraps", "Single-ply"])
    event = st.selectbox("Event", options=["SBD", "Bench Only", "Deadlift Only"])
    dob = st.date_input("Date of Birth")
    nok_name = st.text_input("Next of Kin Name")
    nok_phone = st.text_input("Next of Kin Mobile Phone Number")

    # Submit button
    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if validate_email(email) and validate_phone_number(phone_number):
            # Create a new record as a DataFrame
            new_entry_df = pd.DataFrame([{
                "First Name": first_name,
                "Last Name": last_name,
                "Email": email,
                "Phone Number": phone_number,
                "Gender": gender,
                "Equipment": equipment,
                "Event": event,
                "Date of Birth": dob,
                "Next of Kin Name": nok_name,
                "Next of Kin Phone Number": nok_phone
            }])

            # Concatenate the new record with the existing DataFrame
            data = pd.concat([data, new_entry_df], ignore_index=True)

            # Save to JSON
            data.to_json(
                os.path.join(data_path, "registration_data.json"),
                index=False
            )
            st.success("Registration successful!")
