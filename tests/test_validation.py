"""

"""
import pytest
from web_site.validation import validate_email, validate_phone_number, validate_dob
from datetime import date


def test_validate_email():
    """

    :return:
    """
    assert validate_email("test@example.com")
    assert not validate_email("testexample.com")
    # todo: add more tests


def test_validate_phone_number():
    """

    :return:
    """
    assert validate_phone_number("0123456789")
    assert not validate_phone_number("12345")
    # todo: add more tests


def test_validate_dob():
    """

    :return:
    """
    assert validate_dob(date(2000, 1, 1))
    assert not validate_dob(date(2100, 1, 1))
    # todo: add more tests
