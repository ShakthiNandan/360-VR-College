import json

# Load existing scenes.json
with open('scenes.json', 'r') as file:
    original_data = json.load(file)

# New coordinates to add under "coor" for each key
new_coors = {
    "10_1": "11.026866229052022, 77.0268303696604",
    "11_1": "11.025848546712945, 77.02701558144032",
    "12_1": "11.024886651651352, 77.02727605575842",
    "12_2": "11.02496957670958, 77.02770185662008",
    "12_3": "11.025163621254462, 77.02789110144747",
    "12_4": "11.025082067126059, 77.028156642079",
    "12_5": "11.025259450737734, 77.02867417474292",
    "12_6": "11.025670552863472, 77.02928345861542"
}

# Update the original_data: add "coor" field if key exists in new_coors.
for key, coor in new_coors.items():
    if key in original_data:
        # If the current value is a dictionary, add or update the "coor" field.
        if isinstance(original_data[key], dict):
            original_data[key]["coor"] = coor
        else:
            # If it's not a dictionary, replace it with a dictionary containing "coor".
            original_data[key] = {"coor": coor}
    else:
        print(f"Key {key} not found in the original data. Skipping.")

# Save the updated JSON back to scenes.json
with open('scenes.json', 'w') as file:
    json.dump(original_data, file, indent=4)

print("Updated 'scenes.json' with new coordinates under 'coor' for each key.")
