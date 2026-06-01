"""Test for mongo_connect.py"""
from unittest.mock import patch, MagicMock
import pytest
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection

# Błędne nazwy odwołań do biblioteki!
@patch("ztm_tools.mongo_tools.mongo_connect.db.MongoClient")
def test_success_first_try(mock_mongo):
    mock_client = MagicMock()
    mock_mongo.return_value = mock_client

    result = create_mongo_connection("mongodb://test")

    assert result == mock_client
    mock_mongo.assert_called_once()

@patch("ztm_tools.mongo_tools.mongo_connect.sleep", return_value=None)
@patch("ztm_tools.mongo_tools.mongo_connect.main_logger")
@patch("ztm_tools.mongo_tools.mongo_connect.MongoClient")
def test_retry_then_success(mock_mongo, mock_logger, mock_sleep):
    mock_mongo.side_effect = [Exception("fail1"), Exception("fail2"), MagicMock()]

    result = create_mongo_connection("mongodb://test")

    assert result is not None
    assert mock_mongo.call_count == 3
    assert mock_sleep.call_count == 2

@patch("ztm_tools.mongo_tools.mongo_connect.sleep", return_value=None)
@patch("ztm_tools.mongo_tools.mongo_connect.main_logger")
@patch("ztm_tools.mongo_tools.mongo_connect.MongoClient", side_effect=Exception("fail"))
def test_all_fail_returns_none(mock_mongo, mock_logger, mock_sleep):
    result = create_mongo_connection("mongodb://test")

    assert result is None
    assert mock_mongo.call_count == 3
    mock_logger.assert_called()
