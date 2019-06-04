int pulse_time = 150 ;
int start = 785 ;
char data = 'S' ;
int output_pin = 6 ;
int temp = 8 ;
void setup() {
  pinMode(output_pin, OUTPUT) ;
}


void sendbit(int bit) {
  if(bit == 1) {
    digitalWrite(output_pin, LOW) ;
    delayMicroseconds(pulse_time) ;
    digitalWrite(output_pin, HIGH);
    delayMicroseconds(pulse_time) ;
    digitalWrite(output_pin, LOW) ;
    delayMicroseconds(pulse_time) ;
    digitalWrite(output_pin, HIGH);
    delayMicroseconds(pulse_time) ;
  }
  else {
    digitalWrite(output_pin, LOW) ;
    delayMicroseconds(pulse_time * 2) ;
    digitalWrite(output_pin, HIGH);
    delayMicroseconds(pulse_time * 2) ;
  }
}
void sendnum(int num) {
  int array[temp] ;
  for(int i = temp ; i >= 0 ; i--) {
    array[i] = num % 2 ;
    num /= 2 ;
  }
  for(int i = 0 ; i < temp ; i++) {
    sendbit(array[i]) ;
  }
}

void loop() {
    // sendnum(start) ;
    sendnum((int)data)  ;
    // sendbit(1) ;
    // sendbit(0) ;
    // sendbit(1) ;
    // sendbit(0) ;
    // sendbit(0) ;
    // sendbit(0) ;
    // sendbit(1) ;
    // sendbit(0) ;
}
