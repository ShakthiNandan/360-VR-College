import os
import json

# Directory containing panorama images
image_dir = "static/images/panoramas"

# Extract filenames and coordinates
scenes = {}
files = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]

# Parse coordinates from filenames like "(x,y).jpg"
coords = {}
for file in files:
    try:
        name, _ = os.path.splitext(file)
        x, y = map(int, name.strip("()").split(","))
        coords[(x, y)] = file
    except ValueError:
        continue  # Ignore files that don't match pattern

# Build scene connections
for (x, y), filename in coords.items():
    scene_id = f"{x}_{y}"
    scenes[scene_id] = {
        "title": f"Scene ({x}, {y})",
        "image": f"static/images/panoramas/{filename}",
        "hotspots": []
    }

    # Check neighboring coordinates
    neighbors = {
        "left": (x - 1, y),
        "right": (x + 1, y),
        "up": (x, y + 1),
        "down": (x, y - 1)
    }

    for direction, (nx, ny) in neighbors.items():
        if (nx, ny) in coords:
            scenes[scene_id]["hotspots"].append({
                "target": f"{nx}_{ny}",
                "direction": direction
            })

# Save JSON config
with open("scenes.json", "w") as f:
    json.dump(scenes, f, indent=4)

print("Scene configuration saved to scenes.json")
