import re
from datetime import date, datetime


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
	Validate the date of birth.

	This function checks if the provided date of birth string is a valid date
	and not in the future compared to the current date.

	:param dob_str: str
		The date of birth as a string in 'YYYY-MM-DD' format.
	:return: bool
		True if the date of birth is valid and not in the future, False otherwise.
	"""
	try:
		dob = datetime.strptime(dob, '%Y-%m-%d').date()
	except ValueError:
		# The string is not a valid date
		return False
	today = datetime.now().date()
	return dob <= today
