int pulse_time = 150 ;
int start = 785 ;
int ends  = 423 ;
int half1 ;
int half2 ;
int bytecount=0;
byte f;
byte data[]=new byte[8];
int output_pin = 6 ;
int temp = 10 ;

void setup() {
  pinMode(output_pin, OUTPUT) ;
  Serial.begin(9600) ;
}

int enc_backend(int in) {
  switch(in) {
    case  0 : return 30 ; break ;
    case  1 : return  9 ; break ;
    case  2 : return 20 ; break ;
    case  3 : return 21 ; break ;
    case  4 : return 10 ; break ;
    case  5 : return 11 ; break ;
    case  6 : return 14 ; break ;
    case  7 : return 15 ; break ;
    case  8 : return 18 ; break ;
    case  9 : return 19 ; break ;
    case 10 : return 22 ; break ;
    case 11 : return 23 ; break ;
    case 12 : return 26 ; break ;
    case 13 : return 27 ; break ;
    case 14 : return 28 ; break ;
    case 15 : return 29 ; break ;
    default : return 00 ;
  }
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
  for(int i = temp-1 ; i >= 0 ; i--) {
    array[i] = num % 2 ;
    num /= 2 ;
  }
  for(int i = 0 ; i < temp ; i++) {
    sendbit(array[i]) ;
  }
}

int enc(int num) {
  half1 = num >> 4 ;
  half2 = num % 16 ;
  half1 = enc_backend(half1) ;
  half2 = enc_backend(half2) ;
  return (half1 * 32) + (half2) ;
}

void loop() {
  while(1){
    if(Serial.available()>0){
      f=Serial.read();
      data[bytecounter++]=f;
      if(bytecounter==8){
        bytecounter=0;
        sendnum(start) ;
        for (int i=0; i<8; i++)
        {
          f=data[i];
          sendnum(enc((int)f));
        }
        sendnum(ends) ;
        data="";}
    }
    else{
      digitalWrite(output_pin,HIGH);
      break;
    }
  }
}
