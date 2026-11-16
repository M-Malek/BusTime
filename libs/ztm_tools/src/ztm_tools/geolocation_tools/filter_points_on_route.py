from ztm_tools.geolocation_tools.lat_lng_to_meters import lat_lng_to_meters
import numpy as np
import pandas as pd
from numpy import column_stack
from scipy.spatial import cKDTree

def filter_points_on_route(gather_data, reference_data, max_distance=20):
    """
    Filter points which belongs to Vehicle route
    :param gather_data: data gathered from moving Vehicle - data from MongoDB collection Vehicles
    :param reference_data: referenced data - data from S3 bucket shapes from ZTM .zip file: shapes.txt
    :param max_distance: maximum acceptable distance between points in meters, default value: 20 meters
    :return: DataFrame with filtered data
    """
    if gather_data.empty or reference_data.empty:
        return gather_data.iloc[0:0].copy()

    # Coerce Mongo values to numeric and exclude invalid coordinates before
    # building/querying cKDTree (which cannot accept NaN or infinity).
    gather_data = gather_data.copy()
    gather_data["lat"] = pd.to_numeric(gather_data["lat"], errors="coerce")
    gather_data["lng"] = pd.to_numeric(gather_data["lng"], errors="coerce")
    gather_valid = (
        np.isfinite(gather_data["lat"].to_numpy(dtype=np.float64))
        & np.isfinite(gather_data["lng"].to_numpy(dtype=np.float64))
        & gather_data["lat"].between(-90, 90).to_numpy()
        & gather_data["lng"].between(-180, 180).to_numpy()
    )
    gather_data = gather_data.loc[gather_valid].copy()
    if gather_data.empty:
        return gather_data

    reference_data = reference_data.copy()
    reference_data["latitude"] = pd.to_numeric(reference_data["latitude"], errors="coerce")
    reference_data["longitude"] = pd.to_numeric(reference_data["longitude"], errors="coerce")
    reference_valid = (
        np.isfinite(reference_data["latitude"].to_numpy(dtype=np.float64))
        & np.isfinite(reference_data["longitude"].to_numpy(dtype=np.float64))
        & reference_data["latitude"].between(-90, 90).to_numpy()
        & reference_data["longitude"].between(-180, 180).to_numpy()
    )
    reference_data = reference_data.loc[reference_valid]
    if reference_data.empty:
        return gather_data.iloc[0:0].copy()

    # print("Gather data:")
    # print(gather_data)
    # print("Reference data:")
    # print(reference_data)
    # b = input()
    # Recalculate reference data to x, y cords
    reference_x, reference_y = lat_lng_to_meters(reference_data["latitude"].to_numpy(), reference_data["longitude"].to_numpy())
    # Stack reference data 2-dimensional matrix
    reference_coordinates = column_stack((reference_x, reference_y))
    # Create KD Tree from reference data
    reference_tree = cKDTree(reference_coordinates)

    # Recalculate gathered data to x,y cords
    gather_x, gather_y = lat_lng_to_meters(gather_data["lat"].to_numpy(), gather_data["lng"].to_numpy())
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

