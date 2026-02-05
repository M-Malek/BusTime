"""
Testing micro2 in given parameters: check how .zip file ise read
@M-Malek
"""
import pandas

from services.micro2_timetables.src.zip_gather import zip_downloading
from services.micro2_timetables.src.zip_reader import ZIPReader
from shared.tools.env_os_variables import dc_zip_url

from sys import getsizeof


def test1():
    """First global test of zip downloading object"""
    # Download and test if zip file has been downloaded ok.
    test_zip = zip_downloading(dc_zip_url)
    # print(test_zip)
    assert test_zip is not None, "Test zip is none! Data not downloaded?"

    test_read_zip = ZIPReader(test_zip)
    test_read_zip.data_reader()

    # Test types of data:
    print("Stops: ")
    assert type(test_read_zip.stops) == pandas.DataFrame, "Stops read improperly"
    print(test_read_zip.stops.head(10))
    print("Trips")
    assert type(test_read_zip.trips) == pandas.DataFrame, "Trips read improperly"
    print(test_read_zip.trips.head(10))
    print("Stop times")
    assert type(test_read_zip.stop_times) == pandas.DataFrame, "Stop times read improperly"
    print(test_read_zip.stop_times.head(10))
    print("Shapes")
    assert type(test_read_zip.shapes) == pandas.DataFrame, "Shapes read improperly"
    print(test_read_zip.shapes.head(10))
    print("Agency")
    assert type(test_read_zip.agency) == pandas.DataFrame, "Agency read improperly"
    print(test_read_zip.agency.head(10))
    print("Routes")
    assert type(test_read_zip.routes) == pandas.DataFrame, "Routes read improperly"
    print(test_read_zip.routes.head(10))

    # Check size of files:
    print("Routes: " + str(getsizeof(test_read_zip.routes)/1000000))
    print("Shapes: " + str(getsizeof(test_read_zip.shapes)/1000000))
    print("Stop times: " + str(getsizeof(test_read_zip.stop_times)/1000000))


def test2():
    """Only idea testing purposes"""
    from services.micro2_timetables.src.zip_parser import Line, Routes, Stop
    import json

    stop1 = Stop("221_2", "14:52", "14:53", 1)
    stop2 = Stop("221_2", "14:55", "14:56", 2)
    routes = Routes("221_2")
    veh = Line(2, "Pan Samochodzik")

    print(stop1.to_dict())
    print(stop2.to_dict())
    print(routes.to_dict())


def test3():
    from services.micro2_timetables.src.zip_parser import zip_parser
    from shared.tools.env_os_variables import dc_zip_url
    import json

    data = zip_parser(dc_zip_url)
    with open("data_test.json", "w") as file:
        json.dump(data, file)
        file.close()


#test1()
#test2()
test3()
