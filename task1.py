import os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from datetime import datetime

# Base folder for output
base_folder = "./task1"


os.makedirs(base_folder, exist_ok=True)


# Helper to read Excel into list of dicts
def excel_to_dict_list(file_path, sheet_name="Sheet1"):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []


# Compute best_spearman values for a map file
def compute_best_list(file_path, ref1, ref2, map_number):
    data = excel_to_dict_list(file_path)
    best_list = []
    # Filter for rows with a valid ordering string
    ordering_rows = [
        item
        for item in data
        if isinstance(item.get("Ordering the Landmarks"), str)
        and ";" in item.get("Ordering the Landmarks")
    ]

    for item in ordering_rows:
        ordering = item["Ordering the Landmarks"].rstrip(";").split(";")
        ref1_rank = {v: idx + 1 for idx, v in enumerate(ref1)}
        ref2_rank = {v: idx + 1 for idx, v in enumerate(ref2)}
        resp_rank = {v: idx + 1 for idx, v in enumerate(ordering)}

        common1 = [v for v in ref1 if v in resp_rank]
        common2 = [v for v in ref2 if v in resp_rank]

        r1, _ = spearmanr(
            [ref1_rank[v] for v in common1], [resp_rank[v] for v in common1]
        )
        r2, _ = spearmanr(
            [ref2_rank[v] for v in common2], [resp_rank[v] for v in common2]
        )

        if map_number == 2:
            best_val = r2 if ordering[:3] == ref2[:3] else r1
        else:
            best_val = max(r1, r2)

        best_list.append(best_val)
    return best_list


# Reference orders for each map
ref1_map1 = [
    "Park",
    "Outdoor fan-like decoration",
    "Graveyard Entrance",
    "Cross Statue",
    "Graffiti Wall",
    "Bus Stop",
    "Contruction Site",
]
ref2_map1 = [
    "Outdoor fan-like decoration",
    "Park",
    "Graveyard Entrance",
    "Cross Statue",
    "Graffiti Wall",
    "Bus Stop",
    "Contruction Site",
]
ref1_map2 = [
    "Statue",
    "Play ground",
    "Apollo",
    "Car Roundabout",
    "Small Roundabout with Fountain",
    "Kodi Store",
    "Defense Tower",
]
ref2_map2 = [
    "Statue",
    "Play ground",
    "Defense Tower",
    "Apollo",
    "Car Roundabout",
    "Small Roundabout with Fountain",
    "Kodi Store",
]


combined = []
for map_number, ref1, ref2 in [
    (1, ref1_map1, ref2_map1),
    (2, ref1_map2, ref2_map2),
]:
    file_name = f"Hossein - Map {map_number}.xlsx"
    df = pd.read_excel(file_name)
    # Keep only rows with an ID
    df = df[df["ID"].notna()].reset_index(drop=True)

    # Compute best_spearman for each valid row
    best_list = compute_best_list(file_name, ref1, ref2, map_number)
    df["best_spearman"] = best_list

    # Insert Map column at the front
    df.insert(0, "Map", f"Map {map_number}")
    combined.append(df)

# Concatenate both maps
df_combined = pd.concat(combined, ignore_index=True)

xlsx = "combined_maps_with_best.xlsx"
csv = "combined_maps_with_best.csv"

df_combined.to_excel(os.path.join(base_folder, xlsx), index=False)

df_combined.to_csv(os.path.join(base_folder, csv), index=False)

print(f"Combined file saved:\n ")
