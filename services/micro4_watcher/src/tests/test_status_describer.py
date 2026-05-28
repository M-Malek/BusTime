"""Test for logic describer"""
from src.logic.status_describer import status_describer
from unittest.mock import Mock, patch

@patch("src.logic.status_describer.checksum_bool")
@patch('src.logic.status_describer.s3_checker')
@patch('src.logic.status_describer.client')
def test_status_describer(mock_client, mock_checksum_bool, mock_s3_checker):

    # Case 1: simulate logic 1
    mock_checksum_bool.return_value = True
    mock_s3_checker.return_value = True

    assert status_describer() == 1, "Should be 1"

    # Case 2: simulate logic 2
    mock_checksum_bool.return_value = False

    assert status_describer() == 2, "Should be 2"

    # Case 3: simulate logic 3
    mock_s3_checker.return_value = False

    assert status_describer() == 3, "Should be 3"

    # Case 4: simulate logic 4
    mock_checksum_bool.return_value = False
    mock_s3_checker.return_value = False

    assert status_describer() == 4, "Should be 4"


test_status_describer()
