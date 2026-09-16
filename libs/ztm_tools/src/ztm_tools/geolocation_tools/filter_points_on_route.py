from ztm_tools.geolocation_tools.lat_lng_to_meters import lat_lng_to_meters
from numpy import column_stack
from scipy.spatial import cKDTree

def filter_points_on_route(gather_data, reference_data, max_distance=5):
    """
    Filter points which belongs to Vehicle route
    :param gather_data: data gathered from moving Vehicle - data from MongoDB collection Vehicles
    :param reference_data: referenced data - data from S3 bucket shapes from ZTM .zip file: shapes.txt
    :param max_distance: maximum acceptable distance between points in meters, default value: 5
    :return: DataFrame with filtered data
    """
    # Recalculate reference data to x, y cords
    reference_x, reference_y = lat_lng_to_meters(reference_data["lat"].to_numpy(), reference_data["lng"].to_numpy())
    # Stack reference data 2-dimensional matrix
    reference_coordinates = column_stack((reference_x, reference_y))
    # Create KD Tree from reference data
    reference_tree = cKDTree(reference_coordinates)

    # Recalculate gathered data to x,y cords
    gather_x, gather_y = lat_lng_to_meters(gather_data["lat"].to_numpy(), reference_data["lng"].to_numpy())
    # Stack gather data to 2-dimensional matrix
    gather_coordinates = column_stack((gather_x, gather_y))

    # Query data
    distances, shape_indices = reference_tree.query(gather_coordinates, k=1)

    # Create accepted_mask - information about measurement acceptation condition
    accepted_mask = distances <= max_distance

    # Copy coordinates with mask
    accepted_coordinates_df = gather_data.loc[
        accepted_mask
    ].copy()

    # Add distance and shape index data and return
    accepted_coordinates_df["distance_to_shape_m"] = distances[accepted_mask]
    accepted_coordinates_df["shape_index"] = shape_indices[accepted_mask]

    return accepted_coordinates_df


