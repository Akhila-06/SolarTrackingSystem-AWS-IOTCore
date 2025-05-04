Smart Solar Monitoring System with ML and AWS IOT Core

1. Hardware Setup & Data Collection

Sensors Used: Two LDRs (LDR1 and LDR2), a DHT11 temperature and humidity sensor, and a solar panel for voltage measurement.

Arduino Uno R4 WiFi collects analog readings:

LDR1 and LDR2 measure light intensity.

The solar panel provides voltage levels.

The DHT11 sensor provides temperature and humidity.

Data Transmission: Sensor data is printed as a structured string via the Arduino's Serial interface.

2. Python Integration

A Python script reads real-time serial data from the Arduino using pyserial.

Data is parsed into JSON format containing: LDR1, LDR2, Voltage, Temp, Humid, and a timestamp.

The JSON payload is published to AWS IoT Core using MQTT (AWSIoTPythonSDK).

3. Cloud Integration with AWS IoT Core

A thing is registered in AWS IoT with attached certificates and policies.

The device publishes data to an MQTT topic like arduino/ldr-servo.

Rules in AWS IoT forward the incoming MQTT messages to a Timestream database table for storage.

4. AWS Timestream Storage

A Timestream database and table (SolarTrackingDB.SensorDataTable) is created.

Each incoming MQTT message is logged as a time-series record with:

device_id, sensor, measure_name, time, measure_value.

5. Grafana Visualization

A Grafana dashboard is connected to the AWS Timestream data source.

Multiple panels are created for each sensor showing average, latest value, and trend graphs over time.

Time filters allow visualization over minutes, hours, or days.

6. Machine Learning Prediction

Historical sensor data from AWS or local logs is saved into a CSV file.

A Python ML script reads the CSV and trains linear regression models to predict each sensor metric:

Inputs: LDR1, LDR2, Temp, Humid.

Outputs: Predicted LDR1, LDR2, Temp, Humid, Voltage.

The model results are saved in a new CSV file with actual vs predicted values.

7. Visualization of Predictions

Using Matplotlib, actual vs predicted plots are generated for all five metrics.

These graphs show how well the ML models track sensor behavior over time.

8. Dashboard-Based Summary

The final dashboard in Grafana uses the uploaded CSV data.

Stat panels show the mean value for each sensor along with a small trend line.