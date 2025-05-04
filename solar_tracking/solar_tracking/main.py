from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import serial
import json
import time
import os
import pandas as pd

basedir = os.path.dirname(__file__)

try:
    ser = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    print("Connected to Arduino.")
except Exception as e:
    print("Failed to open serial port:", e)
    exit(1)

client = AWSIoTMQTTClient("unoR4Client")
client.configureEndpoint("abwhs8d732x6a-ats.iot.us-east-1.amazonaws.com", 8883)
client.configureCredentials(
    os.path.join(basedir, "AmazonRootCA1.pem"),
    os.path.join(basedir, "private.pem.key"),
    os.path.join(basedir, "device-certificate.pem.crt")
)

client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

try:
    client.connect()
    print("Connected to AWS IoT Core.")
except Exception as e:
    print("MQTT connection failed:", e)
    exit(1)

columns = ["LDR1", "LDR2", "Voltage", "Temp", "Humid", "timestamp"]
df = pd.DataFrame(columns=columns)
csv_file = os.path.join(basedir, "arduino_data.csv")

while True:
    try:
        line = ser.readline().decode().strip()
        if line:
            print("Raw Serial:", line)

            parts = line.split(',')
            data = {}
            for part in parts:
                if ':' in part:
                    k, v = part.split(':')
                    data[k.strip()] = float(v.strip())

            data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

            payload = json.dumps(data)
            print("Publishing payload:", payload)
            client.publish("arduino/ldr-servo", payload, 1)

            new_row = pd.DataFrame([data])
            df = pd.concat([df, new_row], ignore_index=True)

            if len(df) % 10 == 0:
                try:
                    if not os.path.exists(csv_file):
                        df.to_csv(csv_file, index=False)
                    else:
                        df.to_csv(csv_file, mode='a', index=False, header=False)
                    print("Saved to CSV:", csv_file)
                    df = pd.DataFrame(columns=columns)
                except Exception as e:
                    print("Error saving to CSV:", e)

    except Exception as e:
        print("Error during loop:", e)

    time.sleep(1)


