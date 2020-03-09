#include <ESP8266WiFi.h>
/*
{
  int ledPin;
  long OnTime;
  long OffTime;
  int ledState;                
  unsigned long previousMillis;
  public:
  Flasher(int pin, long ont, long off)
  {
  ledPin = pin;
  pinMode(ledPin, OUTPUT);     
    
  OnTime = ont;
  OffTime = off;
  
  ledState = LOW; 
  previousMillis = 0;
  }
 
  void Update()
  {
    unsigned long currentMillis = millis();
     
    if((ledState == HIGH) && (currentMillis - previousMillis >= OnTime))
    {
      ledState = LOW;
      previousMillis = currentMillis;
      digitalWrite(ledPin, ledState);
    }
    else if ((ledState == LOW) && (currentMillis - previousMillis >= OffTime))
    {
      ledState = HIGH;
      previousMillis = currentMillis;
      digitalWrite(ledPin, ledState);
    }
  }
};*/
char ssid[] = "Avinash";        
char pass[] = "password";         
uint8_t buf2[30];
uint8_t i2=0;
IPAddress server(192,168,43,95);
WiFiClient client;
long int i = 0;
/*  Flasher led(4, 300, 600);
  Flasher blue(12, 200, 600);
  Flasher red(13, 100, 600);
  Flasher green(16, 800, 600); 
*/
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);      
  while (WiFi.status() != WL_CONNECTED) {
     Serial.print(".");
     delay(500);
    //  led.Update();
  }
 
     while(!client.connect(server, 8080)) {
     delay(200);
  }
}

void loop () {
   while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

  if(Serial.available()>0){
    while(Serial.available()){
      buf2[i2] = (char)Serial.read();
      if(i2<30) i2++;
    }
    client.write((char*)buf2,30);
    i2 = 0;
  }
}
