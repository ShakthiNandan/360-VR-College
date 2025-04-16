import json

# Load existing scenes.json
with open('scenes.json', 'r') as file:
    original_data = json.load(file)

# New coordinates to add under "coor" for each key
new_coors = {
    "0_1": "11.02910942261983, 77.02636489604187",
    "1_1": "11.028779681473415, 77.02645912475805",
    "2_0": "11.028474067397733, 77.02621740761636",
    "2_1": "11.028562534662846, 77.02650009376487",
    "2_2": "11.028618831999513, 77.0267090357007",
    "2_3": "11.028687193036692, 77.02718837308296",
    "2_4": "11.02873544787688, 77.02746696233075",
    "2_5": "11.02877968147344, 77.02776193918137",
    "2_6": "11.028823915064871, 77.02795449350302",
    "3_1": "11.028337345209902, 77.0265533534626",
    "3_6": "11.028626874476844, 77.02797497800653",
    "4_1": "11.028071943131401, 77.02662300077455",
    "4_6": "11.028353430176663, 77.02802414081496",
    "5_-1": "11.027781109744357, 77.02611682230578",
    "5_0": "11.027854795798053, 77.02645093094503",
    "5_1": "11.027903050774876, 77.02666806668228",
    "5_2": "11.02796336948477, 77.02698352803641",
    "5_3": "11.02804781565784, 77.02738092740461",
    "5_4": "11.028096070602986, 77.02763493524819",
    "5_5": "11.028120198072589, 77.02779471437562",
    "5_6": "11.028180516737931, 77.02804052841778",
    "6_1": "11.027750781790605, 77.0266841657989",
    "7_-1": "11.027369118969544, 77.02615332154187",
    "7_1": "11.02755217891118, 77.02671175749204",
    "8_1": "11.027362603310221, 77.02675774364727",
    "9_-1": "11.027033102570064, 77.02622890286212",
    "9_0": "11.027100808231753, 77.02667496856785",  # Only the last "9_0" value is effective.
    "9_1": "11.027132404201868, 77.0267853353404",
    "9_2": "11.02716400016859, 77.02701526611656"
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
