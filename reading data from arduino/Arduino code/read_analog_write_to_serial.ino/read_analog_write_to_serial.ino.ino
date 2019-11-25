void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  //Serial.begin(4800);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  // read the input on analog pin 1:
  //int sum = 0;
  //int group = 5;
  //for(int i = 0; i < group; i++) sum += analogRead(A0);
  //int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
//  float voltage = sensorValue * (5.0 / 1023.0);
  Serial.println(analogRead(A0));
  
}
