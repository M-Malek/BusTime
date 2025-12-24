"""
Microservice no. 1 - Vehicle time and position collector
Respond for collecting and saving in DB current vehicle position in given time period (now 30 sec.)
@M-Malek
"""
# Libs:
import time
from micro1.src.collector_runner import vehicles


# Main loop:
def main():
    while True:
        vehicles()
        time.sleep(30)


if __name__ == "__main__":
    main()
