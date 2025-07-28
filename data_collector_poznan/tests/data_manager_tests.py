# Test 1:
# Check if data_manager.download_trips_data even work
from data_collector_poznan.src.gather.feeds_gater import download_trips_data

url = r""


def test_one(url):
    tested_data = download_trips_data(url)
    assert tested_data is None, "Test failed!"


# Help def for test 2 and 3:
def check_attributes(given_class):
    """
    Check if given object is a class
    :param given_class:
    :return:
    """
    class_attributes = [name for name in dir(given_class) if not name.startswith("__")]
    if len(class_attributes) != 0:
        return class_attributes
    else:
        raise NameError("Given object is not a class which you looking for")


# Test 2:
# Check if class ReadZip has been activated and work with data
def test_two(url):
    tested_data = download_trips_data(url)
    assert len(check_attributes(tested_data)) != 0, "Data managing failure!"

# Test 3:
# Check quality of data - find if element of ReadZip attributes are a not empty lists:

