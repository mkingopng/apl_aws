"""
asdf
"""
from ..app import app as flask_app
import logging
from datetime import datetime
import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

# configure logging at the beginning of the script
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_formatter)

# file handler
f_handler = logging.FileHandler(f'logs/test_app_{current_time}.log')
f_handler.setLevel(logging.DEBUG)
f_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_formatter)

# add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


@pytest.fixture
def app():
	"""
	Create and configure a new app instance for each test.
	:return:
	"""
	# setup code here, if any (e.g., configuring the app for testing)
	yield flask_app
	# teardown code here, if any


@pytest.fixture
def client(app, caplog):
	"""
	A test client for the app.
	:param app:
	:return:
	"""
	return app.test_client()


# test class
class TestAppRoutes:
	@pytest.fixture(autouse=True)
	def setup_method(self, client, monkeypatch):
		"""
		Setup for each test method; runs before each test method.
		:param client:
		:param monkeypatch:
		:return:
		"""
		self.client = client
		self.monkeypatch = monkeypatch

	def test_entry_get(self, caplog):
		"""
		test for GET request
		:return:
		"""
		response = self.client.get('/entry')
		assert response.status_code == 200
		assert b'Australian Powerlifting League' in response.data
		# todo: other assertions

	def test_entry_post_success(self):
		"""
		test for POST request
		:return:
		"""
		with patch('boto3.client') as mock_s3_client:
			mock_s3_client.return_value.upload_fileobj.return_value = None
			with patch('app.handler.add_lifter') as mock_add_lifter:  # watch this line as you refactor the project
				mock_add_lifter.return_value = None

				response = self.client.post('/entry', data={
					'Email': 'test@gmail.com',
					'phone_number': '0412345678',
					'dob': '2000-01-01'
					# include other form fields as required
				})

		assert response.status_code == 200  # success
		# todo: other assertions

	def test_landing_page(self):
		"""
		Test for Landing Page
		:return:
		"""
		response = self.client.get('/')
		assert response.status_code == 200
		assert b'Australian Powerlifting League' in response.data
		# todo: other assertions

	def test_entry_page_get(self):
		"""

		:return:
		"""
		response = self.client.get('/entry')
		assert response.status_code == 200
		assert b'Australian Powerlifting League' in response.data
		# todo: other assertions

	def test_entry_page_post(self):  # fix_me
		"""

		:return:
		"""
		# mock the DynamoDBHandler and its methods
		self.monkeypatch.setattr(
			'dynamodb_utilities.DynamoDBHandler.add_lifter',  # watch this line as you refactor the project
			lambda *args, **kwargs: None)

		# example post data, adjust according to form
		data = {
			'Email': 'test@gmail.com',
			'phone_number': '0412345678',
			'dob': '2000-01-01'
		}
		response = self.client.post('/entry', data=data)
		assert response.status_code == 200
		# todo: other assertions
		#  or 200, depending on your redirect
