import subprocess as sp
import re
import time
import paho.mqtt.client as mqtt
import json

def on_publish(client, userdata, mid, reason_code, properties):
    try:
        userdata.remove(mid)
    except KeyError:
        print("Warning: MID not found in unacked_publish. Possible race condition.")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish
mqttc.user_data_set(unacked_publish)

mqttc.connect("mqtt.eclipseprojects.io")
mqttc.loop_start()

wt = 5 # Wait time -- I purposefully make it wait before the shell command
accuracy = 3 #Starting desired accuracy is fine and builds at x1.5 per loop
# -6.317808, 106.687100
while True:
    time.sleep(wt)
    pshellcomm = ['powershell']
    pshellcomm.append('add-type -assemblyname system.device; '\
                      '$loc = new-object system.device.location.geocoordinatewatcher;'\
                      '$loc.start(); '\
                      'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
                      '{start-sleep -milliseconds 100}; '\
                      '$acc = %d; '\
                      'while($loc.position.location.horizontalaccuracy -gt $acc) '\
                      '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
                      '$loc.position.location.latitude; '\
                      '$loc.position.location.longitude; '\
                      '$loc.position.location.horizontalaccuracy; '\
                      '$loc.stop()' %(accuracy))

    #Remove >>> $acc = [math]::Round($acc*1.5) <<< to remove accuracy builder
    #Once removed, try setting accuracy = 10, 20, 50, 100, 1000 to see if that affects the results
    #Note: This code will hang if your desired accuracy is too fine for your device
    #Note: This code will hang if you interact with the Command Prompt AT ALL 
    #Try pressing ESC or CTRL-C once if you interacted with the CMD,
    #this might allow the process to continue

    p = sp.Popen(pshellcomm, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
    (out, err) = p.communicate()
    out = re.split('\n', out)
    # lat = float(out[0])
    # long = float(out[1])
    # -6.317827, 106.687069
    # lat = float(out[0]) - 0.00009
    # long = float(out[1]) - 0.000194
    # lat = float(out[0]) + (-0.00006754631523)
    # long = float(out[1]) - 0.00015520628
    # -6.317827, 106.687055
    lat = float(out[0]) + (-0.00007575)
    long = float(out[1]) - 0.0002075
    # -6.317726, 106.687183
    radius = int(out[2])

    device = "device1"

    print(lat, long, radius)
    topic = "MIT/GPS/1"
    message = json.dumps({"latitude": lat, "longitude": long, "device": device})
    qos = 1
    msg_info = mqttc.publish(topic, message, qos=qos)
    unacked_publish.add(msg_info.mid)
    msg_info.wait_for_publish()
    print(f"Message '{message}' published to {topic} with QoS {qos}")