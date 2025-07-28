# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class DataParserZipTester:
    import shared.tools.data_collector as test_dc
    from shared.tools import env_os_variables
    zip_url = env_os_variables.dpt_zip_url
    test_file = test_dc.download_zip(zip_url)

    def test_one(self):
        from data_collector_poznan.src.parser import data_parser as test_dp

        test_dp.PrepareZip(self.test_file).read_all_zip()
        # test_dp.read_zip(self.test_file)

    def test_two(self):
        """
        Check if collected data have right shape
        :return: Assertion error when fails
        """
        import data_collector_poznan.src.parser.data_parser as test_dp

        test_two = test_dp.PrepareZip(self.test_file)
        test_two.read_all_zip()
        shape_agency = 6
        shape_calendar = 10
        shape_calendar_dates = 3
        shape_feed_info = 5
        shape_routes = 8
        shape_shapes = 4
        shape_stops = 6
        shape_stop_times = 8
        shape_trips = 8

        # print(test_two.agency)
        assert len(test_two.agency.columns) == shape_agency, "Invalid column amount: agency!"
        assert len(test_two.calendar.columns) == shape_calendar, "Invalid column amount: calendar!"
        assert len(test_two.calendar_dates.columns) == shape_calendar_dates, "Invalid column amount: calendar_dates!"
        assert len(test_two.feed_info.columns) == shape_feed_info, "Invalid column amount: calendar!"
        assert len(test_two.routes.columns) == shape_routes, "Invalid column amount: calendar!"
        assert len(test_two.shapes.columns) == shape_shapes, "Invalid column amount: calendar!"
        assert len(test_two.stops.columns) == shape_stops, "Invalid column amount: calendar!"
        assert len(test_two.stop_times.columns) == shape_stop_times, "Invalid column amount: calendar!"
        assert len(test_two.trips.columns) == shape_trips, "Invalid column amount: calendar!"

        print("All data correct, test passed!")

    def test_three(self):
        """
        Test only routes download
        :return: AssertionError if we cannot prepare data
        """
        import data_collector_poznan.src.parser.data_parser as dp
        tested_data = dp.PrepareZip(self.test_file)
        prepare_routes = tested_data.routes
        print(type(prepare_routes))
        print(prepare_routes)
        # print(dp.PrepareZip(self.test_file).read_routes().head())

    def test_four(self):
        import data_collector_poznan.src.parser.data_parser as dp
        routes = dp.BasicZipData(self.test_file, "routes.txt").routes
        # print(routes.head())
        # assert type(routes) == pandas.DataFrame, "Error: no DataFrame"


# DataParserZipTester().test_four()
"""
    Catched errors:
    1. Error with handling response
    Reason: I tried to unpack with zipfile a file which was represented as byres
    Solution: I used io library and io.BytesIO function to load .zip as zip file

    2. Error with .txt file open
    Reason: pandas -> OSError [Errno 22]
    Solution: I give to pandas.read_csv file content, not simple file
"""

