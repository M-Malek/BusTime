from src.zip_parser import zip_parser
from src.zip_stops_parser import zip_parser_stops
from src.zip_shapes_reader import shape_parser
from src.zip_saver import s3_checker, save_data
from boto3 import client
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.log_logging import main_logger
from pymongo.errors import ConnectionFailure
import os
import json
from src.ztm_site_checker import checksum_checker
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
    # Check if its necessary to download new data:
    if checksum_checker():
        # print("Debug: new data needs to be downloaded!")
        stoptimes_data = zip_parser(os.getenv("DC_ZIP_URL"))
        # print("Debug: New data downloaded! Starting to saving data")
        # Set S3 config procedures: set maximum timeouts attempts
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

        bucket_name = os.getenv("S3_BUCKET")
        # bucket_prefix = "line-"
        bucket_prefix = os.getenv("S3-BUCKET_PREFIX")
        # print("Connected to s3!")
        if s3_checker(s3):
            # stoptimes_data = zip_parser(os.getenv("DC_ZIP_URL"))
            save_data(s3, stoptimes_data)
            main_logger("info", "Micro2 micro_jobs:job_normal - data saved!")
        else:
            main_logger("info", "Stop times data already stored in S3. New data hasn't been downloaded.")
    #
    # # Lines only for debug: test when S3 bucket hasn't been available:
    # import json
    # with open("json_stops.json", "w") as file:
    #     json.dump(stoptimes_data, file)
    #     file.close()
    #
    # for line, data in stoptimes_data.items():
    #     file_key = f"{bucket_prefix}{line}.json"
    #     try:
    #         s3.put_object(
    #             Bucket=os.getenv("S3_BUCKET"),
    #             Key=file_key,
    #             Body=json.dumps(data, ensure_ascii=False).encode("utf-8"),
    #             ContentType="application/json"
    #         )
    #     except Exception as e:
    #         main_logger("warning", f"Micro2 job_normal: failed to save line: {line}, error: {e}")
    #
    # main_logger("info", "Micro2 micro_jobs:job_normal - data saved!")
