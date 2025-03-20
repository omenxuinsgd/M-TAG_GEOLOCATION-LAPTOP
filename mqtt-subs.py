import streamlit as st
import paho.mqtt.client as mqtt
import json
import queue
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
import time
import threading

# Callback function for MQTT connection
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        print("Connected successfully")
        client.subscribe("subscriber/count")
        client.subscribe("MIT/GPS/1")

# Callback function for receiving messages
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")
    if message.topic == "subscriber/count":
        subscriber_count = int(message.payload.decode())
        print(f"Subscriber Count Updated: {subscriber_count}")
        userdata.put(("subscriber_count", subscriber_count))
    elif message.topic == "MIT/GPS/1":
        try:
            gps_data = json.loads(message.payload.decode())
            lat, lon, dev = gps_data.get("latitude"), gps_data.get("longitude"), gps_data.get("device")
            if lat is not None and lon is not None:
                print(f"Updated GPS Data: Lat {lat}, Lon {lon}, Device {dev}")
                userdata.put(("gps_data", (lat, lon, dev)))
        except json.JSONDecodeError:
            print("Invalid JSON format received")

# Streamlit app title
st.title("Live Subscriber Count via MQTT with Leafmap")

# MQTT setup
broker = "mqtt.eclipseprojects.io"
msg_queue = queue.Queue()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=msg_queue)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker)

# Start MQTT thread
mqtt_thread = threading.Thread(target=client.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

# Initialize session state
if "subscriber_count" not in st.session_state:
    st.session_state.subscriber_count = 0
if "gps_data" not in st.session_state:
    st.session_state.gps_data = {}
if "basemap" not in st.session_state:
    st.session_state.basemap = "OpenStreetMap"
if "map_key" not in st.session_state:
    st.session_state.map_key = "map_1"

# Dropdown for selecting basemap
type_map = {
    "OpenStreetMap": "OpenStreetMap",
    "Satellite": "SATELLITE",
    "Terrain": "TERRAIN",
    "Hybrid": "HYBRID"
}

map_type = st.selectbox("Pilih Mode Peta", list(type_map.keys()), index=0)
st.session_state.basemap = type_map[map_type]

# Placeholders for subscriber count and map
subscriber_placeholder = st.empty()
map_placeholder = st.empty()

# Define colors for devices
COLORS = ["red", "blue", "green", "orange", "purple", "black", "pink", "gray", "brown"]

# Function to render map with multiple markers
def render_map(device_data):
    print("Rendering map with multiple markers")
    if not device_data:
        return st_folium(leafmap.Map(center=[-6.2, 106.8], zoom=12), width=700, height=500, key=st.session_state.map_key)
    
    # Calculate center of the map
    latitudes = [lat for lat, lon in device_data.values()]
    longitudes = [lon for lat, lon in device_data.values()]
    center_lat = sum(latitudes) / len(latitudes)
    center_lon = sum(longitudes) / len(longitudes)
    
    m = leafmap.Map(center=[center_lat, center_lon], zoom=19)
    m.add_basemap(st.session_state.basemap)
    
    # Assign a unique color to each device
    device_colors = {device: COLORS[i % len(COLORS)] for i, device in enumerate(device_data.keys())}
    
    for dev, (lat, lon) in device_data.items():
        color = device_colors[dev]
        popup_text = f"Device: {dev}"
        m.add_marker(location=[lat, lon], popup=popup_text, icon_color=color)
    
    return st_folium(m, width=700, height=500, key=st.session_state.map_key)

# Initial map rendering
print("Initializing map...")
map_display = render_map(st.session_state.gps_data)

# Main loop to process incoming messages
while True:
    try:
        key, value = msg_queue.get(timeout=1)
        print(f"Processing queue item: {key} -> {value}")
        if key == "subscriber_count":
            st.session_state.subscriber_count = value
            subscriber_placeholder.metric(label="Subscribers", value=value)
        elif key == "gps_data":
            lat, lon, dev = value
            st.session_state.gps_data[dev] = (lat, lon)
            print(f"Updating map with new GPS Data: Device {dev}, Lat {lat}, Lon {lon}")
            
            # Update map key to force re-rendering
            st.session_state.map_key = f"map_{time.time()}"
            map_placeholder.empty()
            map_display = map_placeholder.write(render_map(st.session_state.gps_data))
    except queue.Empty:
        pass