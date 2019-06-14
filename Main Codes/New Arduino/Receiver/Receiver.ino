long t ;
int out = 0 ;
int flag = 1 ;
void setup() {
  pinMode(3, INPUT) ;
  attachInterrupt(digitalPinToInterrupt(3), function, FALLING) ;
  Serial.begin(230400) ;
  t = micros() ;
}

void loop() {
  if(out != 0) {
    
    if(100 <= out && out <= 124  ) {
      if(flag) {
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
    
    // Serial.println(out) ;
    out = 0  ;
  }
}

void function() {
  long num = micros() ;
  out = num - t ;
  t = num ;
}
