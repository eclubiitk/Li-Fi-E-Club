int pulse_time = 150 ;
int start = 785 ;
char data = A ;
int output_pin = 6 ;

void setup() {
  pinMode(output_pin, OUTPUT) ;
}


void sendbit(int bit) {
  if(bit) {
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
  int array[10] ;
  for(int i = 9 ; i >= 0 ; i++) {
    array[i] = num % 2 ;
    num /= 2 ;
  }
  for(int i = 0 ; i < 9 ; i++) {
    sendbit(array[i]) ;
  }
}
void loop() {
    // sendnum(start) ;
    sendnum(data)  ;
}
