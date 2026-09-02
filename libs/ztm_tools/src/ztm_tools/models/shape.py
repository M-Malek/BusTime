class ReadyShape:
    def __init__(self, shape_id, shapes):
        self.shape_id = shape_id
        self.shapes = shapes

    def to_dict(self) -> dict:
        return {
            "shape_id": self.shape_id,
            "shapes": self.shapes
        }

    @classmethod
    def from_dict(cls, shape_data):
        ready_shapes = []

        for shape_data in shape_data["shapes"]:
            shape = Shape.from_dict(shape_data)
            ready_shapes.append(shape)

        return cls(
            shape_id=shape_data["shape_id"],
            shapes=ready_shapes
        )

class Shape:
    def __init__(self, seq, lat, lon):
        self.sequence = seq
        self.latitude = lat
        self.longitude = lon

    def to_dict(self) -> dict:
        return {
            "sequence": self.sequence,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @classmethod
    def from_dict(cls, shape_data):
        return cls(
            seq=shape_data["seq"],
            lat=shape_data["lat"],
            lon=shape_data["lon"]
        )
