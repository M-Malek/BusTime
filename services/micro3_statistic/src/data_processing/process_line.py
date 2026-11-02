"""Aggregate trip delay measurements into per-route statistics."""

from collections import defaultdict
from datetime import timedelta
from statistics import mean, median


def _delay_seconds(delay):
    """Normalize a stored delay to seconds; unknown delays are ignored."""
    if delay is None:
        return None
    if isinstance(delay, timedelta):
        return delay.total_seconds()
    if hasattr(delay, "total_seconds"):
        return delay.total_seconds()
    try:
        return float(delay)
    except (TypeError, ValueError):
        return None


def _flatten_detected_stops(trip):
    """TripProgress stores each processing batch as a list of observations."""
    for batch in trip.detected_stops or []:
        if isinstance(batch, dict):
            yield batch
        elif batch:
            yield from batch


def _stop_id_at(stops, index):
    stop = stops[index]
    return stop.get("stop_id") if isinstance(stop, dict) else stop


def _delay_location(trip, stop):
    stops = trip.stops or []
    stop_id = stop.get("referenced_stop_id", stop.get("stop_id"))
    sequence = stop.get("sequence", stop.get("seq"))

    index = None
    if sequence is not None:
        try:
            index = int(sequence)
        except (TypeError, ValueError):
            pass
    if index is None or index < 0 or index >= len(stops):
        try:
            index = next(i for i in range(len(stops)) if _stop_id_at(stops, i) == stop_id)
        except StopIteration:
            return {"sequence": sequence, "previous_stop_id": None,
                    "stop_id": stop_id, "next_stop_id": None}

    return {
        "sequence": sequence if sequence is not None else index,
        "previous_stop_id": _stop_id_at(stops, index - 1) if index > 0 else None,
        "stop_id": stop_id if stop_id is not None else _stop_id_at(stops, index),
        "next_stop_id": _stop_id_at(stops, index + 1) if index + 1 < len(stops) else None,
    }


def process_line(trips):
    """Return and print per-route delay summaries from TripProgress objects.

    Delays and summary values use seconds. The maximum delay includes the
    preceding and following stop IDs from that trip's ordered ``stops`` list.
    """
    grouped = defaultdict(list)
    for trip in trips or []:
        grouped[trip.route_id].append(trip)

    results = {}
    for route_id, route_trips in grouped.items():
        measurements = []
        for trip in route_trips:
            for stop in _flatten_detected_stops(trip):
                seconds = _delay_seconds(stop.get("delay"))
                if seconds is not None:
                    measurements.append((seconds, trip, stop))

        delays = [item[0] for item in measurements]
        max_location = None
        if measurements:
            max_delay, max_trip, max_stop = max(measurements, key=lambda item: item[0])
            max_location = {"delay_seconds": max_delay, **_delay_location(max_trip, max_stop)}

        results[route_id] = {
            "route_id": route_id,
            "trips_count": len(route_trips),
            "delays_seconds": delays,
            "mean_delay_seconds": mean(delays) if delays else None,
            "median_delay_seconds": median(delays) if delays else None,
            "maximum_delay_location": max_location,
        }
        print(results[route_id])

    return results
