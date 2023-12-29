import re
from datetime import date


# validation functions
def validate_email(email):
	"""
	This function checks if the provided email string matches the pattern of a
	standard email address. It uses regex to ensure that the email address
	consists of characters allowed in the local part of the email, followed by
	an '@' symbol, and a domain part which includes domain labels separated by
	periods. The domain labels cannot start or end with hyphens.
	:param email: (Str) The email address to be validated.
	:return: (Bool) True if email address is in valid format, else False.
	"""
	pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	return re.match(pattern, email) is not None


def validate_phone_number(phone):
	"""
	Validate a phone number to ensure it has 10 digits and starts with 0.
	This function uses regular expression to validate the phone number format.
	The phone number is expected to be a string or an integer. It first
	converts the phone number to a string (if it isn't already),
	then checks if it matches the pattern of starting with zero followed by
	exactly nine other digits.
	:param phone: (Str or Int): The phone number to be validated.
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
	:param dob: (Date) The date of birth to be validated. Expected to be a
	date object.
	:return bool: True if the date of birth is today or in the past, False if
	it is in the future.
	"""
	today = date.today()
	return dob <= today
