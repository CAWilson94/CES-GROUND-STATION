#include <Servo.h>

Servo AzServo;
Servo ElServo;

int degrees[1];

void setup(){
  Serial.begin(9600);
  AzServo.attach(2);
  ElServo.attach(4);
}

void loop(){
  while(Serial.available() >= 2){
    for (int i = 0; i < 2; i++){
      degrees[i] = Serial.read();
    }
    AzServo.write(degrees[0]);
    //Serial.print("Az-");
    //Serial.println(degrees[0]);
    //Serial.print("El-");
    ElServo.write(degrees[1]);
    //Serial.println(degrees[1]);
    Serial.print("end");
  }
}
