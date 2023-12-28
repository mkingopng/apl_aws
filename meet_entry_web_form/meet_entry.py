"""
simple web-based entry form to collect lifter's data for meet.

output is JSON to replicate expected output from EventBrite API

"""
import os
import streamlit as st
from functions import *
from variables import *


if __name__ == '__main__':
    # title
    st.title("Australian Powerlifting League \nMeet Registration")

    # creating form fields
    with st.form(key='registration_form'):
        first_name = st.text_input("First Name")

        last_name = st.text_input("Last Name")

        email = st.text_input(
            "Email",
            help="Enter a valid email address"
        )

        phone_number = st.text_input("Mobile Phone Number")

        gender = st.selectbox(
            "Gender",
            options=["Male", "Female"]
        )

        equipment = st.selectbox(
            "Equipment",
            options=[
                "Sleeves",
                "Wraps",
                "Single-ply"
            ]
        )

        event = st.selectbox(
            "Event",
            options=[
                "SBD",
                "Bench Only",
                "Deadlift Only"
            ]
        )

        dob = st.date_input("Date of Birth")

        nok_name = st.text_input("Next of Kin Name")

        nok_phone = st.text_input("Next of Kin Mobile Phone Number")

        # submit button
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if validate_email(email) and validate_phone_number(phone_number):
                # create a new record as a df
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

                # concatenate the new record with the existing df
                data = pd.concat([data, new_entry_df], ignore_index=True)

                # save to JSON
                data.to_json(
                    os.path.join(DATA_PATH, "registration_data.json"),
                    index=False
                )

                # save_to_dynamodb('YourTableName', data)

                st.success("Registration successful!")
            else:
                st.error("Please enter a valid email address and phone number")
