int delmicro=150;
int pinNum=3;
void setup()
{
  Serial.begin(230400);
  pinMode(pinNum,INPUT);
}
void loop()
{
  Serial.println(digitalRead(pinNum));
  delayMicroseconds(delmicro);
}
