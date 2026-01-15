"""
Testing micro2 in given parameters: check how .zip file ise read
@M-Malek
"""
import pandas

from services.micro2_timetables.src.zip_gather import zip_downloading
from services.micro2_timetables.src.zip_reader import ZIPReader
from shared.tools.env_os_variables import dc_zip_url


def test1():
    """First global test of zip downloading object"""
    # Download and test if zip file has been downloaded ok.
    test_zip = zip_downloading(dc_zip_url)
    # print(test_zip)
    assert test_zip is not None, "Test zip is none! Data not downloaded?"

    test_read_zip = ZIPReader(test_zip)

    # Test types of data:
    assert type(test_read_zip.stops) != pandas.DataFrame, "Stops read improperly"
    print(test_read_zip.stops.head(10))
    assert type(test_read_zip.trips) != pandas.DataFrame, "Trips read improperly"
    print(test_read_zip.trips.head(10))
    assert type(test_read_zip.stop_times) != pandas.DataFrame, "Stop times read improperly"
    print(test_read_zip.stop_times.head(10))
    assert type(test_read_zip.shapes) != pandas.DataFrame, "Shapes read improperly"
    print(test_read_zip.shapes.head(10))
    assert type(test_read_zip.agency) != pandas.DataFrame, "Agency read improperly"
    print(test_read_zip.agency.head(10))
    assert type(test_read_zip.routes) != pandas.DataFrame, "Routes read improperly"
    print(test_read_zip.routes.head(10))


test1()

