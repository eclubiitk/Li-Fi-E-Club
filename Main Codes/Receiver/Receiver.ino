int pin = 3;
unsigned long duration;

void setup() {
  Serial.begin(230400);
  pinMode(pin, INPUT);
}

int flag = 1 ;
void loop() {
  duration = pulseIn(pin, HIGH);
  if(duration < 75) {
    if(flag == 1) {
      Serial.println(1) ;
      flag = 0 ;
    }
    else {
      flag = 1 ;
    }
  }
  else {
    Serial.println(0) ;
  }
  // Serial.println(duration);
}
