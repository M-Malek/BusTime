from src.mongo_micro_tools.get_active_url import get_active_url
from unittest.mock import patch, MagicMock
from datetime import datetime

@patch("src.mongo_micro_tools.get_active_url.create_mongo_connection")
def test_get_active_url(mock_create_connection):
    mock_collection = MagicMock()

    mock_collection.find.return_value = [
        {"state": "active", "url": "test1", "began_at": "20240101"},
        {"state": "pending", "url": "test2_winner", "began_at": "20230101"},
        {"state": "archive", "url": "test3", "began_at": "20250101"},
    ]
    # with patch("src.mongo_micro_tools.get_active_url.create_mongo_connection") as mock_con:
    #     mock_con.return_value = {
    #         "Poznan":
    #             {
    #                 "Stop_times_arch": mock_collection,
    #             }
    #     }
    mock_db = {"Stop_times_arch": mock_collection}
    mock_create_connection.return_value = {"Poznan": mock_db}

    result = get_active_url()
    assert result == "test2_winner", "Error in case 1!"

@patch("src.mongo_micro_tools.get_active_url.create_mongo_connection")
def test_get_active_url_fail(mock_create_connection):
    mock_collection = MagicMock()

    mock_collection.find.return_value = [
        {"state": "pending", "url": "test1_winner", "began_at": "20230101"},
        {"state": "archive", "url": "test2", "began_at": "20240101"},
    ]
    # with patch("src.mongo_micro_tools.get_active_url.create_mongo_connection") as mock_con:
    #     mock_con.return_value = {
    #         "Poznan":
    #             {
    #                 "Stop_times_arch": mock_collection,
    #             }
    #     }
    mock_db = {"Stop_times_arch": mock_collection}
    mock_create_connection.return_value = {"Poznan": mock_db}

    result = get_active_url()
    print(result)
    assert result == "test1_winner", "Error in case 2!"


@patch("src.mongo_micro_tools.get_active_url.create_mongo_connection")
def test_get_active_url_many_active(mock_create_connection):
    mock_collection = MagicMock()

    mock_collection.find.return_value = [
        {"state": "active", "url": "test1_winner", "began_at": "20230101"},
        {"state": "active", "url": "test2", "began_at": "20240101"},
    ]
    # with patch("src.mongo_micro_tools.get_active_url.create_mongo_connection") as mock_con:
    #     mock_con.return_value = {
    #         "Poznan":
    #             {
    #                 "Stop_times_arch": mock_collection,
    #             }
    #     }
    mock_db = {"Stop_times_arch": mock_collection}
    mock_create_connection.return_value = {"Poznan": mock_db}

    result = get_active_url()
    assert result == "test1_winner", "Error in case 3!"

def test_get_active_url_live_object():
    """
    In this case testing normal connection. In database in [Poznan][Stop_times_arch] there is no entry with state equals
    to "active"
    :return:
    """
    assert get_active_url() is None, "Error in case 4!"