class StopTime:
    def __init__(self, stop_id, arv_time, dep_time, seq, pickup, dropoff):
        self.stop_id = stop_id
        self.arv_time = arv_time
        self.dep_time = dep_time
        self.seq = seq
        self.pickup = pickup
        self.dropoff = dropoff

    def to_dict(self) -> dict:
        return {
            "seq": self.seq,
            "stop_id": self.stop_id,
            "arv_time": self.arv_time,
            "dep_time": self.dep_time,
            "pickup": self.pickup,
            "dropoff": self.dropoff
        }

    @classmethod
    def from_dict(cls, stop_dict: dict):
        return cls(
            seq=stop_dict['seq'],
            stop_id=stop_dict['stop_id'],
            arv_time=stop_dict['arv_time'],
            dep_time=stop_dict['dep_time'],
            pickup=stop_dict['pickup'],
            dropoff=stop_dict['dropoff']
        )
