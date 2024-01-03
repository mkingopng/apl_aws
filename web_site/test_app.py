import sys
sys.path.insert(0, '')
from app import app as flask_app
import pytest
from unittest.mock import patch


@pytest.fixture
def app():
	"""
	Create and configure a new app instance for each test.
	:return:
	"""
	# Setup code here, if any (e.g., configuring the app for testing)
	yield flask_app
	# Setup code here, if any (e.g., configuring the app for testing)


@pytest.fixture
def client(app):
	"""
	A test client for the app.
	:param app:
	:return:
	"""
	return app.test_client()


def test_entry_get(client):
	"""
	test for GET request
	:param client:
	:return:
	"""
	response = client.get('/entry')
	assert response.status_code == 200
	assert b'Australian Powerlifting League' in response.data  # replace with
	# actual content


#
def test_entry_post_success(client):
	"""
	test for POST request
	:param client:
	:return:
	"""
	with patch('boto3.client') as mock_s3_client:
		# mocking S3 client
		mock_s3_client.return_value.upload_fileobj.return_value = None
		with patch('app.handler.add_lifter') as mock_add_lifter:
			# mocking DynamoDB interaction
			mock_add_lifter.return_value = None

			response = client.post('/entry', data={
				'Email': 'test@gmail.com',
				'phone_number': '0412345678',
				'dob': '2000-01-01'
				# include other form fields as required
			})

			assert response.status_code == 302  # redirect status
			# assert b'success' in response.data  # check for success message


def test_landing_page(client):
	"""
	Test for Landing Page
	:param client:
	:return:
	"""
	response = client.get('/')
	assert response.status_code == 200
	assert b'Australian Powerlifting League' in response.data
	# replace with actual content check


def test_entry_page_get(client):
	response = client.get('/entry')
	assert response.status_code == 200
	assert b'Australian Powerlifting League' in response.data
	# replace with actual content check


def test_entry_page_post(client, monkeypatch):
	# mock the DynamoDBHandler and its methods
	monkeypatch.setattr('dynamodb_utilities.DynamoDBHandler.add_lifter', lambda *args, **kwargs: None)

	# example post data, adjust according to form
	data = {
		'Email': 'test@gmail.com',
		'phone_number': '0412345678',
		'dob': '2000-01-01'
	}
	response = client.post('/entry', data=data)
	assert response.status_code == 302
	# or 200, depending on your redirect
