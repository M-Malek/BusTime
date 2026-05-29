"""Test for logic describer"""
from logic.status_describer import status_describer


def test_status_describer():


    # Case 1: simulate logic 1
    #  s3_bool and checksum_bool are True
    assert status_describer(True, True) == 1, "Should be 1"

    # Case 2: simulate logic 2
    # s3 bool is True, checksum_bool is False

    assert status_describer(False, True) == 2, "Should be 2"

    # Case 3: simulate logic 3
    # s3_bool is False, checksum_bool is True
    assert status_describer(True, False) == 3, "Should be 3"

    # Case 4: simulate logic 4
    # s3_bool and checksum_bool are False
    assert status_describer(False, False) == 4, "Should be 4"


test_status_describer()
