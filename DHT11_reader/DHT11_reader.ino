#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  bool error = isnan(temperature) || isnan(humidity);

  if (!error) {
    Serial.print("T:");
    Serial.print(temperature);
    Serial.print(";H:");
    Serial.print(humidity);
    Serial.println(";OK");
  } else {
    Serial.println("ERR;DHT_FAIL");
  }

  delay(2000); 
}
