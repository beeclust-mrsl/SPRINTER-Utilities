#include <ESP8266WiFi.h>

char ssid[] = "pranav";        
char pass[] = "pranav123";

byte ack[20];

IPAddress server(192,168,43,113);
WiFiClient client;

long int i = 0;

void setup(){

	pinMode(4, OUTPUT);
	digitalWrite(4, LOW);

	Serial.begin(115200);   
         
	WiFi.begin(ssid, pass);      
	while (WiFi.status() != WL_CONNECTED) {
		digitalWrite(4, HIGH);
		delay(1000);
		digitalWrite(4, LOW);
		delay(1000);
	}
        
}

void loop(){
if (client.connect(server, 8080))
  {
    while (client.connected() || client.available())
    {
      if (client.available())
      {
        String line = client.readStringUntil('\n');
        digitalWrite(4, HIGH);
        Serial.println(line);

        while(!Serial.available())
          delay(5);

        String resp = Serial.readString();

        resp.getBytes(ack, 20);
        client.write(ack, 20);
        i++;
      }
    }

    Serial.print(i);
    Serial.println("lines received");
    client.stop();
    
//    while(true){
//      delay(2000);
//    };
  }
}
