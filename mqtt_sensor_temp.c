#include <ESP8266WiFi.h>
#include <PubSubClient.h>

//Libraries
#include <DHT.h>;

//Constants
#define DHTPIN D2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

//Variables
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value

// WiFi
const char *ssid = "sensornet"; // Enter your WiFi name
const char *password = "sensor123";  // Enter WiFi password
// MQTT Broker
const char *mqtt_broker = "10.37.132.5"; // Enter your WiFi or Ethernet IP
const char *topic = "temperatura/sensor1";
const int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient client(espClient);


void setup() {
 // Set software serial baud to 115200;
 Serial.begin(115200);
 dht.begin();
 
 // connecting to a WiFi network
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
  delay(500);
  Serial.println("Connecting to WiFi..");
 }
 
 Serial.println("Connected to the WiFi network");
 
 //connecting to a mqtt broker
 client.setServer(mqtt_broker, mqtt_port);
 client.setCallback(callback);
 
 while (!client.connected()) {
 String client_id = "esp8266-client-";
 client_id += String(WiFi.macAddress());
 
 Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
 if (client.connect(client_id.c_str())) {
  Serial.println("Public emqx mqtt broker connected");
 } else {
  Serial.print("failed with state ");
  Serial.print(client.state());
  delay(2000);
 }
}
 
 
}
void callback(char *topic, byte *payload, unsigned int length) {
 Serial.print("Message arrived in topic: ");
 Serial.println(topic);
 Serial.print("Message:");
 
 for (int i = 0; i < length; i++) {
  Serial.print((char) payload[i]);
 }
 
 Serial.println();
 Serial.println(" - - - - - - - - - - - -");
}
void loop() {
  
  //Read data and store it to variables hum and temp
  hum = dht.readHumidity();
  temp= dht.readTemperature();
  //Print temp and humidity values to serial monitor
  Serial.print("Humidity: ");
  Serial.print(hum);
  Serial.print(" %, Temp: ");
  Serial.print(temp);
  Serial.println(" Celsius");
  String message = ("temp: " + String(temp) + " hum: " + String(hum));
  Serial.print(message);
  char charArray[message.length()];
  message.toCharArray(charArray, message.length()+1);
  // publish and subscribe
  client.publish(topic, charArray);
  client.subscribe(topic);
  delay(10000);
  client.loop();
}
