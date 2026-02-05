"""
Opis logiki odczytu danych z pliku zip
Dla każdej linii trzeba rozpisać dokładnie dane które potrzeba zapisać:
numer linii:
    id_przewoźnika: <value>,
    id_trasy:
        przebieg trasy:
            numer w sekwencji: nazwa_przystanku (id przystanku?), czas_przyjazdu, czas_odjazdu
Każda linia jako osobny .json?
Linia:
    numer,
    color,
    przewoźnik,
    trasy (trip_id): -> każda trasa ma swoje id, dzień kiedy kursuje, przebieg trasy po przystankach i shape id
    czyli przebieg trasy po mapie (do każdego z przystanków można dojechać na różne sposoby, stąd to shape!)
        id danej trasy (trip_id)
        service_id (dzień kursowania)
        shape_id
        kształt (szukany dla danego shape_id): -> potrzebny do wyświetlenia trasy pojazdu na mapie
            numer w kolejności,
            lat,
            lng,
        przebieg trasy (szukany dla danego trip_id): -> potrzebny do statystyk
            numer w kolejności (sequence),
            arrival_time,
            departure_time,
            stop_id,

Skąd jakie dane:
numer - routes.txt
color - routes.txt
przewoźnik - routes.txt
---numer, color i przewoźnik mam w basic_line_info---
trasy:
    trip_id - trips.txt
    service_id - trip.txt
    shape_id - trip.txt
    kształt trasy - shapes.txt szukamy po shape_id:
            sekwencja - shape.txt
            lat - shape.txt
            lng - shape.txt
    przebieg trasy - stop_time.txt szukamy po trip_id:
        sekwencja - stop_time.txt
        przystanek - stop_time.txt
        godzina przyjazdu (arrival time) - stop_time.txt
        godzina odjazdu (departure time) - stop_time.txt

Osobno do wczytania pozycje przystanków (do wyświetlenia na mapie, jeden wspólny plik):
stop_id
nazwa - stops.txt
lat - stops.txt
lng - stops.txt
strefa - stops.txt
"""
import datetime

from services.micro2_timetables.src.zip_reader import ZIPReader
from services.micro2_timetables.src.zip_gather import zip_downloading


from services.micro2_timetables.src.zip_parser import StopTime, Shape

# Pierwsza wersja kodu parsera .zip - bardzo powolne działanie! - ok. 30 minut na jedną operację pełnego odczytu!
def zip_parser2(url_raw_data_set):
    raw_zip = zip_downloading(url_raw_data_set)
    raw_data_set = ZIPReader(raw_zip)

    # Basic vehicle information: line number, agency, color
    # Step 1: reading all lines:
    # basic_line_info - describes basic information about the line
    basic_line_info = raw_data_set.routes[["route_id", "agency_id", 'route_color', "route_type"]]

    # basic_trip_info - basic information's about trips
    basic_trip_info = raw_data_set.trips[["route_id", "trip_id", "service_id", "shape_id"]]

    # Loop to finding shape set and route set
    # Find all unique sets: route_id, trip_id, shape_id
    searching_set = basic_trip_info[["route_id", "trip_id", "shape_id"]]

    # Find all unique line numbers
    lines = basic_trip_info["route_id"].unique()

    # Find all shapes and all times data
    all_shapes = raw_data_set.shapes
    all_times = raw_data_set.stop_times

    # Dictionary with all necessary data
    ready_lines = {}
    # Debug:
    # print(basic_line_info[basic_line_info["route_id"] == "405"]["agency_id"].unique()[0])
    # print(searching_set.head(10))
    # stop = input("Press Enter to continue")
    time1 = datetime.datetime.now()
    for line in lines:  # Lines - set of vehicle lines numbers: PKS, T7, 1, 2, 3...
        print(f"Opracowuje linię: {line}")
        # Find all unique shapes for given route
        all_unique_shapes = basic_trip_info[basic_trip_info["route_id"] == line]["shape_id"].unique()

        # Find all unique trips for given route:
        all_unique_trips = basic_trip_info[basic_trip_info["route_id"] == line]["trip_id"].unique()

        # For all shapes create set of Shape objects describing route shape
        # Debug:
        # time1 = datetime.datetime.now()
        ready_shapes = {}
        for shape in all_unique_shapes:  # all_unique_shapes - all shape numbers
            shape_list = []
            for s_entry in all_shapes[all_shapes["shape_id"] == shape].iterrows():
                # print(s_entry)
                shape_seq = int(s_entry[1].iloc[3])  # int(s_entry[1][3])
                shape_lat = float(s_entry[1].iloc[1])  # float(s_entry[1][1])
                shape_lng = float(s_entry[1].iloc[2])  # float(s_entry[1][2])
                # Create Shape object from founded data
                ready_shape = Shape(shape_seq, shape_lat, shape_lng).to_dict()
                shape_list.append(ready_shape)
            ready_shapes[int(shape)] = shape_list

        # FInd all stops of vehicle - stop_id, times and sequence position
        ready_times = {}
        for trip in all_unique_trips:  # all_unique_trips - all trip_id numbers
            # print(trip)
            stop_time_list = []
            for t_entry in all_times[all_times["trip_id"] == trip].iterrows():
                time_seq = int(t_entry[1].iloc[4])  # int(t_entry[1][4])
                time_stop = int(t_entry[1].iloc[3])  # int(t_entry[1][3])
                time_arr_time = str(t_entry[1].iloc[1])  # str(t_entry[1][1])
                time_dep_time = str(t_entry[1].iloc[2])  # str(t_entry[1][2])
                time_pickup = int(t_entry[1].iloc[5])  # int(t_entry[1][5])
                time_dropoff = int(t_entry[1].iloc[6])  # int(t_entry[1][6])
                ready_time = StopTime(time_stop, time_arr_time, time_dep_time, time_seq, time_pickup, time_dropoff). \
                    to_dict()
                stop_time_list.append(ready_time)
            ready_times[str(trip)] = stop_time_list

        # Each vehicle has his own set of pairs trip - shape: shape describe how physically vehicle drive between
        # stops, trip describes which stops vehicle has and times of reaching and leaving this points.
        # Putting together shape and time data for vehicle:
        """
        {
            numer, - numer linii
            color, - color linii
            przewoźnik, - co to za przewoźnik
            trasy: 
            {
                trip_id, - numer tripa
                service_day, - w jakie dni jeździ
                shape, - kształt tego tripa
                stop_times, - przystanki w tym tripie
            }

        }

        """
        # Preparing pairs: route - shape:
        filtered_searching_set = searching_set[
            searching_set["route_id"] == line
            ]

        ready_data_set = {}
        for _, row in filtered_searching_set.iterrows():
            trip_id = row["trip_id"]
            shape_id = row["shape_id"]

            ready_data_set[trip_id] = {
                "trip_id": trip_id,
                "shape_id": shape_id,
                "trip_data": ready_times[trip_id],
                "shape_data": ready_shapes[int(shape_id)]
            }

        # ready_data_set = {}
        # for data_set in searching_set.iterrows():
        #     ready_data_set[data_set[1].iloc[1]] = {
        #         "trip_id": data_set[1].iloc[1],
        #         "shape_id": data_set[1].iloc[2],
        #         "trip_data": ready_times[data_set[1].iloc[1]],  # to ma być z ready_times
        #         "shape_data": ready_shapes[data_set[1].iloc[2]]  # to ma być z ready_shapes
        #     }
        # print(ready_data_set)
        # stop = input("Press enter")

        # Preparing information about vehicle type: bus or tram:
        if int(basic_line_info[basic_line_info["route_id"] == line]["route_type"].unique()[0]) == 0:
            vehicle_type = "tram"
        else:
            vehicle_type = "bus"

        # Main comparison for examined line
        ready_lines[line] = {
            "line_number": str(line),
            "type": str(vehicle_type),
            "agency": int(basic_line_info[basic_line_info["route_id"] == line]["agency_id"].unique()[0]),
            "line_color": str(basic_line_info[basic_line_info["route_id"] == line]["route_color"].unique()[0]),
            "routes": ready_data_set,
        }
    time2 = datetime.datetime.now()
    print(f"Czas dla opracowania danych pojazdów: {time2 - time1} ")
    return ready_lines
