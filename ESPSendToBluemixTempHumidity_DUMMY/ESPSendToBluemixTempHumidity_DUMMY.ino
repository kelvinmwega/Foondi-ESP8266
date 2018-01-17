// Temp & Humidity Sender to IBM Bluemix
// HW: DHT11 , Data Connected to GPIO2
//     ESP8266-03
// Reha Yurdakul, rehay@ke.ibm.co 31.08.2017, Nairobi, Kenya



#include <ESP8266WiFi.h>
#include <PubSubClient.h> // https://github.com/knolleary/pubsubclient/releases/tag/v2.3

//-------- Customise these values -----------
//const char* ssid = "RehaMobileWiFi";
//const char* password = "afafafaf";

const char* ssid = "AVANI GUEST WIFI";
const char* password = "afafafaf";

#define ORG "y1pbdx"
#define DEVICE_TYPE "WiFiDummySensor"
#define DEVICE_ID "WiFiNode01"
#define TOKEN "12345678"


//-------- Customise the above values --------

char server[] = ORG ".messaging.internetofthings.ibmcloud.com";
char topic[] = "iot-2/evt/status/fmt/json";
char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "d:" ORG ":" DEVICE_TYPE ":" DEVICE_ID;

WiFiClient wifiClient;
PubSubClient client(server, 1883, NULL, wifiClient);

void setup() {
 Serial.begin(115200);
  delay(2000);
 Serial.println();
 Serial.print("WiFi Node, with dummy tem & humidity sensor");
 Serial.print("Connecting to "); Serial.print(ssid);
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
 delay(500);
 Serial.print(".");
 } 
 Serial.println("");

 Serial.print("WiFi connected, IP address: "); Serial.println(WiFi.localIP());
}

int counter = 0;

void loop() {

 if (!client.connected()) {
 Serial.print("Reconnecting client to ");
 Serial.println(server);
 while (!client.connect(clientId, authMethod, token)) {
 Serial.print(".");
 delay(60000);
 }
 Serial.println();
 }

  Serial.print("Dummy sensor: ");
  Serial.print("Humidity (%): ");
  Serial.println(50, DEC);

  Serial.print("Temperature (°C): ");
  Serial.println(25, DEC);

 String payload = "{\"d\":{\"Name\":\"18FE34D81E46\"";
 payload += ",\"counter\":";
 payload += counter++;
 payload += ",\"temperature\":";
 payload += 25;
 payload += ",\"humidity\":";
 payload += 50;
 payload += "}}";
 
 Serial.print("Sending payload: ");
 Serial.println(payload);
 
 if (client.publish(topic, (char*) payload.c_str())) {
 Serial.println("Publish ok");
 } else {
 Serial.println("Publish failed");
 }

 delay(5000);
}
