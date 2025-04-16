import json
import folium

# Load the scenes.json file
with open('scenes.json', 'r') as file:
    data = json.load(file)

# Choose a center for the map; here we use the first valid coordinate we find.
def get_first_coordinate(data):
    for key, value in data.items():
        if isinstance(value, dict):
            coord = value.get("coor")
        else:
            coord = value
        if coord:
            try:
                lat_str, lng_str = coord.split(',')
                return float(lat_str.strip()), float(lng_str.strip())
            except Exception:
                continue
    return 0, 0  # fallback center

center_lat, center_lng = get_first_coordinate(data)

# Create a folium map with no default tiles.
m = folium.Map(location=[center_lat, center_lng], zoom_start=15, tiles=None)

# Add a custom tile layer for Google Maps.
# Note: Using Google Maps tiles in this way might be subject to licensing or TOS restrictions.
folium.TileLayer(
    tiles='http://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Maps',
    overlay=False,
    control=True
).add_to(m)

# Add markers for each coordinate from the JSON file.
for key, value in data.items():
    if isinstance(value, dict):
        coord = value.get("coor")
    else:
        coord = value
    if coord:
        try:
            lat_str, lng_str = coord.split(',')
            lat = float(lat_str.strip())
            lng = float(lng_str.strip())
            popup_text = f"{key}<br>{coord}"
            folium.Marker(location=[lat, lng], popup=popup_text).add_to(m)
        except Exception as e:
            print(f"Error parsing coordinate for key '{key}': {coord}")
            print("Error:", e)

# Optionally, add a layer control to toggle tile layers.
folium.LayerControl().add_to(m)

# Save the map to an HTML file.
m.save("map.html")
print("Map has been generated and saved to 'map.html'.")
