"""
Microservice no. 1 - Vehicle time and position collector
Respond for collecting and saving in DB current vehicle position in given time period (now 30 sec.)
@M-Malek
"""
# Libs:
from time import sleep
from services.micro1_vehicles.src.collector_runner import vehicles


# This code has to bee adopted for AWS service. While True loop has to be replaced.

# Main loop:
def main():
    while True:
        vehicles()
        sleep(30)


if __name__ == "__main__":
    main()
