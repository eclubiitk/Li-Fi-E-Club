int c;
void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  c=0;
}

void loop() {
  if(c==0)
    {
      digitalWrite(13, c);
      c=1;
    }
    /*else
    {
      digitalWrite(13, c);
      c=0;
    }*/
    Serial.println(c);
    delay(20);
}
