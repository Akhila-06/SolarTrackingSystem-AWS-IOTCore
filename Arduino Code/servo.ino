#include <Servo.h>
#include <DHT.h>

// === Pin Definitions ===
const int light1Pin = A0;
const int light2Pin = A1;
const int solarPin  = A2;
const int servoPin  = 9;
#define DHTPIN 7
#define DHTTYPE DHT11


int angle = 90;
int light1Reading, light2Reading, difference;
int margin = 20;
int solarReading;
float solarVoltage;
float temperature, humidity;

Servo servo1;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  servo1.attach(servoPin);
  servo1.write(angle);
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  light1Reading = analogRead(light1Pin);
  light2Reading = analogRead(light2Pin);
  difference = light2Reading - light1Reading;

  if (difference > margin && angle < 180) {
    angle += 1;
  } else if (difference < -margin && angle > 0) {
    angle -= 1;
  }

 
  if (angle > 180) angle = 180;
  if (angle < 0) angle = 0;

  int currentAngle = servo1.read();
  if (currentAngle < angle) {
    servo1.write(currentAngle + 1);
  } else if (currentAngle > angle) {
    servo1.write(currentAngle - 1);
  }
  delay(20);  

  solarReading = analogRead(solarPin);
  solarVoltage = solarReading * 5.0 / 1023.0;

  temperature = dht.readTemperature();
  humidity = dht.readHumidity();

  Serial.print("LDR1:");
  Serial.print(light1Reading);
  Serial.print(",LDR2:");
  Serial.print(light2Reading);
  Serial.print(",Voltage:");
  Serial.print(solarVoltage, 2);
  Serial.print(",Temp:");
  Serial.print(temperature, 1);
  Serial.print(",Humid:");
  Serial.println(humidity, 1);

  delay(1000);
}