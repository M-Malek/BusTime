import pandas as pd

def organize_vehicles_data(data):
    vehicles_df = pd.DataFrame(data)
    # print("Type vehicles_df: ", type(vehicles_df))
    # print(f"Debug: vehicles_df: {vehicles_df}")
    return vehicles_df.groupby(["route_id"])
