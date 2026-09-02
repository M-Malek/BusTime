class DetectedStop:
    def __init__(self, stop_id, seq, scheduled_arrival, scheduled_departure, detected_time, delay, confidence,
        detection_method):
        self.stop_id = stop_id
        self.seq = seq

        self.scheduled_arrival = scheduled_arrival
        self.scheduled_departure = scheduled_departure

        self.detected_time = detected_time
        self.delay = delay

        self.confidence = confidence
        self.detection_method = detection_method

    def to_dict(self):
        return {
            "stop_id": self.stop_id,
            "seq": self.seq,

            "scheduled_arrival": self.scheduled_arrival,
            "scheduled_departure": self.scheduled_departure,

            "detected_time": self.detected_time,
            "delay": self.delay,

            "confidence": self.confidence,
            "detection_method": self.detection_method
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            stop_id=data["stop_id"],
            seq=data["seq"],
            scheduled_arrival=data["scheduled_arrival"],
            scheduled_departure=data["scheduled_departure"],
            detected_time=data["detected_time"],
            delay=data["delay"],
            confidence=data["confidence"],
            detection_method=data["detection_method"]
        )
