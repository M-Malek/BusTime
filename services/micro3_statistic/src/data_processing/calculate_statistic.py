from pandas import DataFrame as df

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
    # print(current_schedule)
    # print("Trip_id: " + current_trip.trip_id + " route_id: " + current_trip.route_id)
    # print(schedules_df)
    # print(detected_stops)

    # Iterate through detected stops in detected_stops
    for stop in detected_stops:
        # Take id of detected stop
        trip_stop_id = stop["referenced_stop_id"]
        # Find trip_stop_id in current_schedule:
        schedule_for_trip_stop_id = current_schedule
        print(schedule_for_trip_stop_id)
        print(stop)
    # print(current_trip.to_dict())
    