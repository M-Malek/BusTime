# Tests for vehicles.py
# Test 1: test creation of object
# Test 2: test save_to_database method
# Test 3: test on living object: test preparing data from feeds.pb

# Tests for stop.py
# Test 4: test creation of object
# Test 5: test save_to_database method
# Test 6: test on living object: test preparing data from .zip file

# Tests for route.py
# Test 7: test creation of object
# Test 8: test long route decoding
# Test 9: test save_to_database method
# Test 10: test on living object: test preparing data from .zip file

# Tests for stop_times.py

# Common tests:
# Common test 1: test data download funtions

from data_collector_poznan.src.structures.vehicle import Vehicle as Vehicle


def vehicles_test_1():
    bus1 = Vehicle(101, "1Y23133", 51.3211, 52.25423, 3, -15)
    lat = bus1.lat
    number = bus1.vehicle_number
    print(bus1.identity_vehicle())
    assert lat == 51.3211, "Bad value!"
    assert number == 101, "Bad vehicle number"


def vehicles_test_2():
    bus2 = Vehicle(101, "1Y23133", 51.3211, 52.25423, 3, -15)
    to_db = bus2.save_to_database()
    assert to_db == [101, "1Y23133", 51.3211, 52.25423, 3, -15], "Wrong data sequence structure!"


def vehicles_test_3():
    pass


from data_collector_poznan.src.structures.stop import Stop as Stop


def stop_test_4():
    data = '1083,"GORC30","Górczyn PKM",52.3818397800,16.8814533600,A'
    stop1 = Stop(data)
    print(type(stop1.short_name))
    print(stop1.short_name)
    assert stop1.stop_id == 1083, "Wrong stop_id"
    assert stop1.lat == 52.3818397800, "Wrong latitude"
    assert stop1.lng == 16.8814533600, "Wrong longitude"
    assert stop1.short_name == "GORC30", "Wrong stop name!"


def stop_test_5():
    data = '1083,"GORC30","Górczyn PKM",52.3818397800,16.8814533600,A'
    stop2 = Stop(data)
    to_db = stop2.save_to_database()
    print(to_db)
    assert to_db == [1083, "Górczyn PKM", 52.3818397800, 16.8814533600, "A"], "Error with data to db!"


def common_test_1():
    from data_collector_poznan.src.data_preparing import ReadZipData as ReadZip
    import shared.tools.data_collector as test_dc
    from shared.tools import env_os_variables
    from shared.tools.filestoolbox import FilesToolBox as ToolBox
    zip_url = env_os_variables.dpt_zip_url
    test_file = test_dc.download_zip(zip_url)
    test_data = ReadZip(test_file)
    test_data.read_data_from_zip()
    print("Shapes:")
    print(len(test_data.shapes))
    # print(test_data.shapes)
    print("Trips:")
    print(len(test_data.trips))
    # print(test_data.trips)
    for i in range(0, 10):
        datum = test_data.trips[i]
        print(ToolBox.row_decoder(datum))


# Run tests:
# vehicles_test_1()
# vehicles_test_2()
# stop_test_4()
# stop_test_5()
common_test_1()
