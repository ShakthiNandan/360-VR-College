import sqlite3 as sq
a=sq.connect("visitors.db")
b=a.cursor()
b.execute("select * from visits")
c=b.fetchall()
ips=[]
for i in c: ips.append(i[1])
print(len(ips))
print(ips)
with open("f.txt","w") as wf:
    st=""
    for i in ips:
        st+=i
        st+="\n"
    wf.write(st)
    wf.close()
import requests
import folium

def get_ip_location(ip):
    """Fetch IP location using ipinfo.io (PythonAnywhere Whitelisted)"""
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        data = response.json()
        if 'loc' in data:
            lat, lon = map(float, data['loc'].split(','))
            return {
                'ip': ip,
                'lat': lat,
                'lon': lon,
                'city': data.get('city', 'Unknown'),
                'region': data.get('region', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'isp': data.get('org', 'Unknown')
            }
        else:
            print(f"❌ No location found for {ip}")
    except Exception as e:
        print(f"❌ Error fetching IP {ip}: {e}")
    return None

def plot_ip_locations(ip_list):
    """Plot all IPs on a single interactive map"""
    all_locations = []

    for ip in ip_list:
        location = get_ip_location(ip)
        if location:
            all_locations.append(location)

    if not all_locations:
        print("No valid locations to plot.")
        return

    # Center the map on the first IP
    center = [all_locations[0]['lat'], all_locations[0]['lon']]
    map_ = folium.Map(location=center, zoom_start=2)

    for loc in all_locations:
        popup_info = f"IP: {loc['ip']}<br>{loc['city']}, {loc['region']}, {loc['country']}<br>ISP: {loc['isp']}"
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=popup_info,
            icon=folium.Icon(color='green')
        ).add_to(map_)

    map_.save("templates/ip_locations_map.html")
    print("✅ Map saved as 'ip_locations_map.html'")

# Example usage
if __name__ == "__main__":
    ip_list = []
    with open("f.txt", "r") as rf:
        ip_list.extend([x.strip() for x in rf.readlines()])
    plot_ip_locations(ip_list)
