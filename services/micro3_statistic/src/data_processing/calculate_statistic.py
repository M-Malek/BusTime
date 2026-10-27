from pandas import DataFrame as df
from datetime import datetime, timedelta

def calculate_statistic(current_trip, schedules_df):
    """
    Calculate statistic of given trip
    :param current_trip: TripProgress object with information about the current trip
    :return: current_calc: TripProgress object with statistic calculations added
    """
    # Take only detected stops
    detected_stops = current_trip.detected_stops[0]
    # Take current schedule of examined trip_id
    current_schedule = schedules_df.loc[current_trip.trip_id]["routes"]["trip_data"]
    current_trip.all_stops_count = len(current_schedule)
    # print(current_schedule)
    # print("Trip_id: " + current_trip.trip_id + " route_id: " + current_trip.route_id)
    # print(schedules_df)
    # print(detected_stops)
    # Find information about last examined stop:
    last_detected_stop = None
    last_detected_stop_time = None

    # If current_trip.last_processed_timestamp it's first run for given trip
    if current_trip.last_processed_timestamp is not None:
        last_detected_stop_time = current_trip.last_processed_timestamp

    # The same as above:
    if last_detected_stop_time is not None:
        last_detected_stop = current_trip.current_stop_seq

    # Iterate through detected stops in detected_stops
    for stop in detected_stops:
        # Take id of detected stop
        trip_stop_id = stop["referenced_stop_id"]
        # Take sequence number of detected stop:
        trip_sequence = stop["sequence"]
        # Find the scheduled stop matching both its sequence and stop id:
        schedule_for_trip_stop_id = next(
            (
                scheduled_stop
                for scheduled_stop in current_schedule
                if scheduled_stop["seq"] == trip_sequence
                and scheduled_stop["stop_id"] == trip_stop_id
            ),
            None,
        )
        stop_completed = False
        stop_delay = None
        if schedule_for_trip_stop_id is not None:
            observation_time = stop["observation_time"]
            observation_datetime = (
                observation_time.to_pydatetime()
                if hasattr(observation_time, "to_pydatetime")
                else observation_time
            )
            scheduled_date = observation_datetime.date()
            arv_time = datetime.strptime(
                schedule_for_trip_stop_id["arv_time"], "%H:%M:%S"
            ).time()
            dep_time = datetime.strptime(
                schedule_for_trip_stop_id["dep_time"], "%H:%M:%S"
            ).time()
            arv_datetime = datetime.combine(scheduled_date, arv_time)
            dep_datetime = datetime.combine(scheduled_date, dep_time)
            if dep_datetime < arv_datetime:
                dep_datetime += timedelta(days=1)

            window_start = arv_datetime + timedelta(minutes=3)
            window_end = dep_datetime - timedelta(minutes=2)
            if observation_datetime < window_start - timedelta(hours=12):
                observation_datetime += timedelta(days=1)
            elif observation_datetime > window_end + timedelta(hours=12):
                observation_datetime -= timedelta(days=1)

            stop_completed = window_start <= observation_datetime <= window_end
            if not stop_completed:
                stop_delay = max(timedelta(0), observation_datetime - window_end)

        print(schedule_for_trip_stop_id)
        print(f"Czy przystanek zaliczony w czasie?: {str(stop_completed)}. "
              f"Opóźnienie: {int(stop_delay.total_seconds()) if stop_delay is not None else 'b.d.'} min")
        print(stop_delay)
        print(stop)
    # print(current_trip.to_dict())

"""
[{'seq': 0, 'stop_id': 221, 'arv_time': '06:49:00', 'dep_time': '06:49:00', 'pickup': 0, 'dropoff': 1}, {'seq': 1, 'stop_id': 219, 'arv_time': '06:50:00', 'dep_time': '06:50:00', 'pickup': 0, 'dropoff': 0}, {'seq': 2, 'stop_id': 218, 'arv_time': '06:51:00', 'dep_time': '06:51:00', 'pickup': 0, 'dropoff': 0}, {'seq': 3, 'stop_id': 216, 'arv_time': '06:52:00', 'dep_time': '06:52:00', 'pickup': 0, 'dropoff': 0}, {'seq': 4, 'stop_id': 214, 'arv_time': '06:53:00', 'dep_time': '06:53:00', 'pickup': 0, 'dropoff': 0}, {'seq': 5, 'stop_id': 209, 'arv_time': '06:55:00', 'dep_time': '06:55:00', 'pickup': 0, 'dropoff': 0}, {'seq': 6, 'stop_id': 207, 'arv_time': '06:56:00', 'dep_time': '06:56:00', 'pickup': 0, 'dropoff': 0}, {'seq': 7, 'stop_id': 205, 'arv_time': '06:57:00', 'dep_time': '06:57:00', 'pickup': 0, 'dropoff': 0}, {'seq': 8, 'stop_id': 203, 'arv_time': '06:58:00', 'dep_time': '06:58:00', 'pickup': 0, 'dropoff': 0}, {'seq': 9, 'stop_id': 3804, 'arv_time': '06:59:00', 'dep_time': '06:59:00', 'pickup': 0, 'dropoff': 0}, {'seq': 10, 'stop_id': 202, 'arv_time': '07:00:00', 'dep_time': '07:00:00', 'pickup': 0, 'dropoff': 0}, {'seq': 11, 'stop_id': 238, 'arv_time': '07:02:00', 'dep_time': '07:02:00', 'pickup': 0, 'dropoff': 0}, {'seq': 12, 'stop_id': 236, 'arv_time': '07:03:00', 'dep_time': '07:03:00', 'pickup': 0, 'dropoff': 0}, {'seq': 13, 'stop_id': 184, 'arv_time': '07:04:00', 'dep_time': '07:04:00', 'pickup': 0, 'dropoff': 0}, {'seq': 14, 'stop_id': 188, 'arv_time': '07:06:00', 'dep_time': '07:06:00', 'pickup': 0, 'dropoff': 0}, {'seq': 15, 'stop_id': 106, 'arv_time': '07:07:00', 'dep_time': '07:07:00', 'pickup': 0, 'dropoff': 0}, {'seq': 16, 'stop_id': 104, 'arv_time': '07:09:00', 'dep_time': '07:09:00', 'pickup': 0, 'dropoff': 0}, {'seq': 17, 'stop_id': 95, 'arv_time': '07:11:00', 'dep_time': '07:11:00', 'pickup': 0, 'dropoff': 0}, {'seq': 18, 'stop_id': 100, 'arv_time': '07:13:00', 'dep_time': '07:13:00', 'pickup': 0, 'dropoff': 0}, {'seq': 19, 'stop_id': 101, 'arv_time': '07:15:00', 'dep_time': '07:15:00', 'pickup': 0, 'dropoff': 0}, {'seq': 20, 'stop_id': 70, 'arv_time': '07:17:00', 'dep_time': '07:17:00', 'pickup': 0, 'dropoff': 0}, {'seq': 21, 'stop_id': 74, 'arv_time': '07:18:00', 'dep_time': '07:18:00', 'pickup': 0, 'dropoff': 0}, {'seq': 22, 'stop_id': 75, 'arv_time': '07:19:00', 'dep_time': '07:19:00', 'pickup': 0, 'dropoff': 0}, {'seq': 23, 'stop_id': 78, 'arv_time': '07:20:00', 'dep_time': '07:20:00', 'pickup': 0, 'dropoff': 0}, {'seq': 24, 'stop_id': 80, 'arv_time': '07:21:00', 'dep_time': '07:21:00', 'pickup': 0, 'dropoff': 0}, {'seq': 25, 'stop_id': 82, 'arv_time': '07:22:00', 'dep_time': '07:22:00', 'pickup': 0, 'dropoff': 0}, {'seq': 26, 'stop_id': 1696, 'arv_time': '07:23:00', 'dep_time': '07:23:00', 'pickup': 0, 'dropoff': 0}, {'seq': 27, 'stop_id': 1693, 'arv_time': '07:24:00', 'dep_time': '07:24:00', 'pickup': 0, 'dropoff': 0}, {'seq': 28, 'stop_id': 1699, 'arv_time': '07:26:00', 'dep_time': '07:26:00', 'pickup': 0, 'dropoff': 0}, {'seq': 29, 'stop_id': 1697, 'arv_time': '07:27:00', 'dep_time': '07:27:00', 'pickup': 0, 'dropoff': 0}, {'seq': 30, 'stop_id': 1702, 'arv_time': '07:28:00', 'dep_time': '07:28:00', 'pickup': 0, 'dropoff': 0}, {'seq': 31, 'stop_id': 1703, 'arv_time': '07:28:00', 'dep_time': '07:28:00', 'pickup': 1, 'dropoff': 0}]
{'referenced_stop_id': 3804, 'lat': np.float64(52.376800537109375), 'lng': np.float64(16.95612907409668), 'observation_time': Timestamp('2026-10-13 04:59:54'), 'distance_to_point': 4.928142867701538}
"""
    
