def calculate_statistic(current_trip, schedules_df):
    """
    Calculate statistic of given trip
    :param current_trip: TripProgress object with information about the current trip
    :return: current_calc: TripProgress object with statistic calculations added
    """
    detected_stops = current_trip.detected_stops
    for stop in detected_stops:
        print(stop.to_dict())
    # print(current_trip.to_dict())
    