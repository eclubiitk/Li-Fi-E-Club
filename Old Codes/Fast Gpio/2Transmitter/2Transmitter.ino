#include <FastGPIO.h>

int PULSE_TIME = 150 ;
int start = 785 ;
int ends  = 423 ;
int half1 ;
int half2 ;
int bytecounter=0;
byte f;
byte data[8];


void setup() {
  FastGPIO::Pin<6>::setOutput(LOW) ;
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
    FastGPIO::Pin<6>::setOutput(LOW) ;
    delayMicroseconds(PULSE_TIME) ;
    FastGPIO::Pin<6>::setOutput(HIGH) ;
    delayMicroseconds(PULSE_TIME) ;
    FastGPIO::Pin<6>::setOutput(LOW) ;
    delayMicroseconds(PULSE_TIME) ;
    FastGPIO::Pin<6>::setOutput(HIGH) ;
    delayMicroseconds(PULSE_TIME) ;
  }
  else {    
    FastGPIO::Pin<6>::setOutput(LOW) ;
    delayMicroseconds(PULSE_TIME*2) ;
    FastGPIO::Pin<6>::setOutput(HIGH) ;
    delayMicroseconds(PULSE_TIME*2) ;
  }
}
void sendnum(int num) {
  for(int div = 512 ; div >= 1 ; div = div >> 1) {
    if(num >= div) {
      sendbit(1) ;
      num -= div ;
    }
    else {
      sendbit(0) ;
    }
  }
}

int enc(int num) {
  int half1 ;
  int half2 ;
  half1 = num >> 4 ;
  half2 = num & 15 ;
  half1 = enc_backend(half1) ;
  half2 = enc_backend(half2) ;
  return (half1 << 5) + (half2) ;
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
        sendnum(ends) ;}
    }
    else{
      FastGPIO::Pin<6>::setOutput(HIGH) ;
      // FastGPIO::Pin<6>::setOutput(LOW) ;
      // Comment out the above for blinking. Uncommenting this line should solve blinking issue.
      break;
    }
  }
}
