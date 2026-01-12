"""
Microservice no. 1 - Vehicle time and position collector
Respond for collecting and saving in DB current vehicle position in given time period (now 30 sec.)
@M-Malek
"""
# Libs:
from time import sleep
from services.micro1_vehicles.src.collector_runner import vehicles
from services.micro1_vehicles.src.data_sender import connection_establisher
from shared.tools.env_os_variables import db_uri


# This code has to bee adopted for AWS service. While True loop has to be replaced.

# Main loop:
def main():
    """while True:
        client = connection_establisher(db_uri)
        vehicles()
        client.close()
        sleep(30)"""
    client = connection_establisher(db_uri)
    vehicles(client)
    client.close()
    sleep(30)


if __name__ == "__main__":
    main()
