# Live MQTT Subscriber & Laptop Device Tracker

## 📌 Overview
This project is a real-time MQTT subscriber system with GPS tracking, visualized using Streamlit and Leafmap. It consists of three key components:
1. **mqtt-subs.py** - Listens to MQTT topics and displays subscriber count and GPS data on an interactive map.
2. **iam.py** - Retrieves the device's geolocation coordinates.
3. **device1.py** - Publishes GPS data to an MQTT broker.

## 🚀 Features
✅ **Live Subscriber Count** - Updates in real-time via MQTT.
✅ **GPS Tracking** - Displays device locations on an interactive map.
✅ **Customizable Map Styles** - Choose between OpenStreetMap, Satellite, Terrain, and Hybrid views.
✅ **Efficient Asynchronous Processing** - Utilizes multithreading for smooth UI and data updates.

---

## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/mqtt-gps-tracker.git
cd mqtt-gps-tracker
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the MQTT Subscriber
```bash
streamlit run mqtt-subs.py
```

### 4️⃣ Run the Device GPS Publisher
```bash
python device1.py
```

### 5️⃣ Run the Location Retriever (Optional)
```bash
python iam.py
```

---

## ⚙️ How It Works
- `device1.py` retrieves GPS coordinates and publishes them to the MQTT broker.
- `mqtt-subs.py` listens to the MQTT topic and updates the UI in real time.
- `iam.py` (optional) fetches location coordinates on Windows devices.
- Streamlit displays subscriber count and live GPS tracking on an interactive map.

---

## 📌 Example Output
| Device  | Latitude   | Longitude  |
|---------|-----------|------------|
| device1 | -6.317726 | 106.687183 |

Map visualization will update dynamically as data arrives.

---

## 🌎 UI Preview
![UI Preview](https://github.com/omenxuinsgd/M-TAG_GEOLOCATION-LAPTOP/blob/main/demo.mp4)

---

## 🚀 Future Improvements
- [ ] Improve UI with better color coding and labels.
- [ ] Add support for multiple MQTT topics.
- [ ] Implement historical data visualization.
- [ ] Add authentication for MQTT broker.

📩 **Contributions are welcome! Feel free to fork and enhance the project.**

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

Happy coding! 🚀

