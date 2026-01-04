Microservice no. 1 

Vehicles data collector:\
Service responsible for downloading, parsing and saving vehicle data in MongoDB database.

Description: \
From ZTM server (link: https://www.ztm.poznan.pl/otwarte-dane/dla-deweloperow/) service downloads data:
- feeds.pb - contains trips information and delay,
- vehicle_positions.pb - contains vehicles positions and trip status,

And save downloaded and prepared data in MongoDB Database. Downloaded data from 1-day period will be used to calculate
lines statistics. \

Current status:
Production ready

Pre-requirements: \
Set given environmental variables:
- log file name,
- URL to feeds.pb file from ZTM Poznań page,
- URL to vehicles.pb file from ZTM Poznań page,
- MONGODB URI,
- MONGODB Password,

Environmental variables will be automatically imported by env_os_variables.py file.
