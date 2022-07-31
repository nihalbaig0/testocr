String cmd;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

while(!Serial){

}
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){

 //receives signal from pi and stores in cmd variable
 cmd = Serial.readStringUntil('\n');
 Serial.println(cmd);
 }
}