"""
Main.py file for Microservice 2 - parsing data tables from ZTM server
@M-Malek
"""
from src.zip_gather import zip_downloading
from src.zip_reader import ZIPReader
from src.zip_parser import zip_parser
from src.zip_stops_parser import zip_parser_stops
from src.zip_shapes_reader import shape_parser
from boto3 import client
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from shared.tools.log_logging import main_logger
from pymongo.errors import ConnectionFailure
import os




def job_stops():
    """Load and save in MongoDB all stops data"""
    source = zip_downloading(os.getenv("DC_ZIP_URL"))
    data = ZIPReader(source)
    stops_data = zip_parser_stops(data)

    try:
        client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
        client.admin.command('ping')
        return client
    except ConnectionFailure as e:
        main_logger("error", f"Connection with MongoDB cannot be established: {e}")
    except Exception as e:
        main_logger("error", f"Error during connection with MongoDB: {e}")
        return None



def job_shapes():
    """Load and save to S3 all shapes data"""
    pass


def job_normal():
    """Load and save to S3 all stoptimes data"""
    pass


def main(action_type="normal"):
    s3 = client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    )

    bucket_name = os.getenv("S3_BUCKET")

    # utworzenie bucket (jeśli nie istnieje)
    try:
        s3.create_bucket(Bucket=bucket_name)
    except:
        pass

    # Dopisać funkcję od zapisywania każdej linii do osobnego pliku!
    source = zip_downloading(os.getenv("DC_ZIP_URL"))
    raw_data = ZIPReader(source)

    if action_type == "shapes":
        data = shape_parser(raw_data)
        # Save shapes to S3
    elif action_type == "stops":
        stops = zip_parser_stops(raw_data)
        # Save stops to S3
    elif action_type == "normal":
        data = zip_parser(os.getenv("DC_ZIP_URL"))


if __name__ == "__main__":
    main()
