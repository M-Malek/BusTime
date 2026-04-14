"""
Read shapes.txt and creat set of shapes data
@M-Malek
"""


class ReadyShape:
    def __init__(self, shape_id, shapes):
        self.shape_id = shape_id
        self.shapes = shapes

    def to_dict(self) -> dict:
        return {
            "shape_id": self.shape_id,
            "shapes": self.shapes
        }


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


def shape_parser(zip_data):
    """
    Return all unique shapes based on Shapes class
    :param zip_data: downloaded .zip file as ZIPReader object
    :return: dict with all shapes
    """
    def build_shape(shape_ids):
        if shape_ids in shape_cache:
            return shape_cache[shape_ids]

        shape_rows = shapes_by_id.get_group(shape_ids)
        shape_list = []

        for s in shape_rows.itertuples(index=False):
            shape_list.append(
                Shape(
                    int(s.shape_pt_sequence),
                    float(s.shape_pt_lat),
                    float(s.shape_pt_lon)
                ).to_dict()
            )

        shape_cache[shape_ids] = shape_list
        return shape_list

    shape_cache = {}
    all_shapes = zip_data.shapes
    shapes_by_id = all_shapes.groupby("shape_id")
    trip_info_by_route = zip_data.trips[["route_id", "trip_id", "service_id", "shape_id"]].groupby("route_id")

    lines = zip_data.trips["route_id"].unique()
    shapes_by_shape_id = {}

    for line in lines:
        route_trip_info = trip_info_by_route.get_group(line)
        unique_shapes = route_trip_info["shape_id"].unique()

        # --- Building shapes  ---
        for shape_id in unique_shapes:
            shapes_by_shape_id[int(shape_id)] = build_shape(int(shape_id))

    return shapes_by_shape_id
