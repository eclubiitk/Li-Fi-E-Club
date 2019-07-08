int pin = 3;
unsigned volatile int tnot = 0 ;
unsigned volatile int tnew = 0 ;
volatile int delta = 0 ;
byte one_flag = 1 ;
byte inter_flag = 1 ;

void func() {
  tnew = micros() ;
  delta = (tnew - tnot) ;
  tnot = tnew ;
}
void setup() {
  pinMode(pin, INPUT) ;
  attachInterrupt(digitalPinToInterrupt(3), func, FALLING) ;
  Serial.begin(230400);
}

void loop() {
  if(delta) {
    // LOWER threshold is compulsory.
    // LOWER = PULSE_TIME*2 - 20 
    // UPPER = PULSE_TIME*2 + 20 
    if(100 < delta && delta < 140) {
      if(one_flag) {
        one_flag = 0 ;
      }
      else{
        one_flag = 1 ;
        Serial.write(1) ;  
      }
      
    } else {
      Serial.write(0) ;
    }
    
    // Serial.println(delta) ;
    delta = 0 ;
  }

}
