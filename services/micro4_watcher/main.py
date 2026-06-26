import time
import os
import asyncio
from dotenv import load_dotenv
from src.site_checking.ztm_site_checker import ztm_site_checker

load_dotenv("config.env")


def main():
    while True:
        # 1. Check microservices status from status SQS
        # 2. Handle catch errors
        # 3. Check ZTM site
        # 4. If new .zip file detected:
        # 4.1 Send
        pass

if __name__ == "__main__":
    main()

