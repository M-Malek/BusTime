from src.zip_managing.zip_parser import zip_parser
from src.zip_managing.zip_stops_parser import zip_parser_stops
from src.zip_managing.zip_shapes_reader import shape_parser
from src.zip_managing.zip_saver import s3_checker, save_data, empty_s3
from src.zip_managing.zip_gather import zip_downloading
from src.zip_managing.zip_reader import ZIPReader
from boto3 import client
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.log_logging import main_logger
from pymongo.errors import ConnectionFailure
import os
import json
from src.site_checking.checksum_checker import checksum_checker
from botocore.config import Config


def db_connector():
    # Function multiplied - to be moved to own lib
    counter = 0
    while counter <= 3:
        try:
            client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
            client.admin.command('ping')
            return client
        except ConnectionFailure as e:
            main_logger("error", f"Connection with MongoDB cannot be established: {e}. "
                                 f"\n Reconnecting: attempt {counter}")
        except Exception as e:
            main_logger("error", f"Error during connection with MongoDB: {e}. \n Reconnecting: attempt {counter}")
        counter -= 1


def job_stops():
    """Load and save in MongoDB all stops data"""
    source = zip_downloading(os.getenv("DC_ZIP_URL"))
    data = ZIPReader(source)
    stops_data = zip_parser_stops(data)

    client = db_connector()
    db_set = client["Poznan"]
    collection = db_set["Stops"]
    collection.drop()
    collection.insert_many(stops_data.to_dict("records"))
    main_logger("info", "Downloaded stops saved in MongoDB")


def job_shapes():
    """Load and save to S3 all shapes data"""
    s3 = client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    )

    bucket_name = os.getenv("S3_BUCKET")
    bucket_prefix = "shapes"

    # utworzenie bucket (jeśli nie istnieje)
    try:
        s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        main_logger("error", "micro_jobs.py: S3 bucket has been created earlier")

    shapes_data = shape_parser()  # stoped here!
    file_key = f"{bucket_prefix}-shapes.json"
    try:
        s3.put_object(
            Bucket=os.getenv("S3_BUCKET"),
            Key=file_key,
            Body=json.dumps(shapes_data, ensure_ascii=False).encode("utf-8"),
            ContentType="application/json"
        )
    except Exception as e:
        main_logger("warning", f"Micro2 job_shapes: falied to save shapes, error: {e}")


def job_normal():
    """Load and save to S3 all stoptimes data"""

    # Check if it's necessary to download new data:
    def status_describer(s3_object):
        """
        Describe logic for job_normal:
        - if there is new file on ZTM server and S3 is empty - download new data - return logic 1
        - if there is empty S3 - download new data - return logic 2
        - if there is new file on ZTM server and S3 isn't empty - empty S3 and download new data - return logic 3
        - if there isn't new file on ZTM server - skip - return logic 4
        """
        if checksum_checker() and s3_checker(s3_object):
            return 1
        elif s3_checker(s3_object):
            return 2
        elif checksum_checker() and not s3_checker(s3_object):
            return 3
        elif checksum_checker():
            return 4

    config = Config(
        connect_timeout=3,
        read_timeout=5,
        retries={'max_attempts': 3}
    )
    s3 = client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
        config=config
    )
    status = status_describer(s3)
    match status:
        case 1:
            stoptimes_data = zip_parser(os.getenv("DC_ZIP_URL"))
            save_data(s3, stoptimes_data)
            main_logger("info", "Micro2 micro_jobs:job_normal - new.zip file and empty S3: new data saved!")
        case 2:
            stoptimes_data = zip_parser(os.getenv("DC_ZIP_URL"))
            save_data(s3, stoptimes_data)
            main_logger("info", "Micro2 micro_jobs:job_normal - empty S3: new data saved!")
        case 3:
            empty_s3(s3)
            stoptimes_data = zip_parser(os.getenv("DC_ZIP_URL"))
            save_data(s3, stoptimes_data)
            main_logger("info", "Micro2 micro_jobs:job_normal - new .zip file: new data saved!")
        case 4:
            main_logger("info", "S3 has data and new .zip file hasn't been detected. New data hasn't been downloaded.")
        case _:
            main_logger("info", "Microservice 2 cannot identify, which action done.")

    # if checksum_checker():
    #     # print("Debug: new data needs to be downloaded!")
    #     stoptimes_data = zip_parser(os.getenv("DC_ZIP_URL"))
    #     # print("Debug: New data downloaded! Starting to saving data")
    #     # Set S3 config procedures: set maximum timeouts attempts
    #     config = Config(
    #         connect_timeout=3,
    #         read_timeout=5,
    #         retries={'max_attempts': 3}
    #     )
    #     s3 = client(
    #         "s3",
    #         endpoint_url=os.getenv("S3_ENDPOINT"),
    #         aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    #         aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    #         config=config
    #     )
    #
    #     bucket_name = os.getenv("S3_BUCKET")
    #     # bucket_prefix = "line-"
    #     bucket_prefix = os.getenv("S3-BUCKET_PREFIX")
    #     # print("Connected to s3!")
    #     if s3_checker(s3):
    #         # stoptimes_data = zip_parser(os.getenv("DC_ZIP_URL"))
    #         save_data(s3, stoptimes_data)
    #         main_logger("info", "Micro2 micro_jobs:job_normal - data saved!")
    #     else:
    #         main_logger("info", "Stop times data already stored in S3. New data hasn't been downloaded.")
