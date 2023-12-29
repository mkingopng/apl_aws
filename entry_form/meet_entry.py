"""
simple web-based entry form to collect lifter's data for meet.

output is JSON to replicate expected output from Eventbrite API or saved to
dynamodb table.
"""
import os
import streamlit as st
import pandas as pd
from entry_form.config import CFG
from entry_form.dynamodb_utilities import *
from entry_form.validation import *


# variables
# define the DataFrame structure


data = pd.DataFrame(columns=CFG.columns)

# Initialize DynamoDBHandler
handler = DynamoDBHandler('apl_meet_entry')


class StreamlitApp:
	"""
	asdf
	"""
	def __init__(self):
		self.handler = DynamoDBHandler(CFG.table_name)

	def create_form(self):
		"""

		:return:
		"""
		with st.form(key='registration_form'):
			first_name = st.text_input("First Name")
			last_name = st.text_input("Last Name")
			# lifter_state
			# lifter_country
			email = st.text_input("Email", help="Enter a valid email address")
			phone_number = st.text_input("Mobile Phone Number")
			gender = st.selectbox("Gender", options=["Male", "Female"])
			equipment = st.selectbox(
				"Equipment",
				options=["Sleeves", "Wraps", "Single-ply"]
			)
			event = st.selectbox(
				"Event",
				options=["SBD", "Bench Only", "Deadlift Only"]
			)
			dob = st.date_input("Date of Birth")
			nok_name = st.text_input("Next of Kin Name")
			nok_phone = st.text_input("Next of Kin Mobile Phone Number")

			submit_button = st.form_submit_button(label="Submit")
			return submit_button, {
				"First Name": first_name, "Last Name": last_name,
				"Email": email,
				"Phone Number": phone_number, "Gender": gender,
				"Equipment": equipment,
				"Event": event, "Date of Birth": dob,
				"Next of Kin Name": nok_name,
				"Next of Kin Phone Number": nok_phone
			}

	def handle_form_submission(self, submit_button, form_data):
		"""

		:param submit_button:
		:param form_data:
		:return:
		"""
		if submit_button:
			# perform validation checks
			if not validate_email(form_data['Email']):
				st.error("Invalid email format.")
				return
			if not validate_phone_number(form_data['Phone Number']):
				st.error("Invalid phone number format.")
				return
			if not validate_dob(form_data['Date of Birth']):
				st.error("Invalid date of birth.")
				return

			# save data if all validations pass
			self.handler.add_lifter(form_data)
			st.success("Registration successful!")

	def run(self):
		"""

		:return:
		"""
		st.title("Australian Powerlifting League \nMeet Registration")
		submit_button, form_data = self.create_form()
		self.handle_form_submission(submit_button, form_data)


if __name__ == '__main__':
	DynamoDBHandler.create_table(self=handler)
	app = StreamlitApp()
	app.run()
