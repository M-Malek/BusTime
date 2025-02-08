class DataCollectorTests:
    from shared.tools import env_os_variables as var_storage
    zip_url = var_storage.dct_zip_url
    feed_url = var_storage.dct_feed_url
    feeds_urls = []
    zip_location = var_storage.dct_zip_url

    def test_file_collector(self):
        import shared.tools.data_collector as test_dc
        for i in range(0, 5):
            assert test_dc.file_collector(self.feed_url), "Test zakończony niepowodzeniem"

    def test_zip_download(self):
        import shared.tools.data_collector as test_dc
        import os

        for j in range(0, 5):
            # For step 2:
            print(f"Attempt: {j}")
            zip_control_number = len([f for f in os.listdir(self.zip_location) if os.path.isfile
            (os.path.join(self.zip_location, f))])
            print(f"Zip control number: {zip_control_number}")
            # Step #1: try download file:
            print("Test: pobieranie zip:")
            assert test_dc.file_collector(self.zip_url), "Test failed, .zip file not downloaded"

            # Step #2: check if .zip can be saved:
            zip_file = test_dc.file_collector(self.zip_url)
            test_dc.save_zip(zip_file)
            download_zip_number = len([f for f in os.listdir(self.zip_location) if os.path.isfile
            (os.path.join(self.zip_location, f))])
            # print(f"Zip control number: {zip_control_number}")
            print(f"Download control number: {download_zip_number}")

            assert download_zip_number == zip_control_number + 1, "Test failed, .zip file not saved"
        print("Zakończono testy")

        """
                    Catched errors:
                    1. [Errno 13] Permission denied: 
                    'C:\\Users\\malek\\Desktop\\Dokumenty\\Projekty\\PythonPrograms\\MPK\\archive\\zip_archive'
                    Reason: trying to save file with the name of directory where I want to save all files
                    Solution: add a line for .zip file name change
                    Added save_path variable: 
                    save_path = PATH + r"" + "--" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".zip"

                    2. AssertionError: Test failed, .zip file not saved
                    Reason: bad test script: I ordered to test if .zip file can be downloaded, then I want to check
                    number of saved .zip's - I forgot to run sav_zip() function.

                    3. Test error: assert passed but incorrect files number


        """


DataCollectorTests().test_zip_download()
