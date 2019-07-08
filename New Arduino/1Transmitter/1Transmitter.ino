#define PULSE_TIME 60

#include <FastGPIO.h>
int start = 785 ;
int ends  = 423 ;
// String data = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG \v kyu nahi chal raha hai.\n" ;
// String data="*\v*\v*\n*\v*\v*\n*\v*\v*\n";
String data  = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum." ;

void setup() {
//  pinMode(output_pin, OUTPUT) ;/
  FastGPIO::Pin<6>::setOutput(LOW) ;
  //Serial.begin(230400) ;
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
//    FastGPIO::Pin<6>::setOutput(LOW) ;/
  }
  else {    
    FastGPIO::Pin<6>::setOutput(LOW) ;
    delayMicroseconds(PULSE_TIME*2) ;
    FastGPIO::Pin<6>::setOutput(HIGH) ;
    delayMicroseconds(PULSE_TIME*2) ;
//    FastGPIO::Pin<6>::setOutput(LOW) ;/
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

    /*
    sendbit(1) ;
    sendbit(0) ;
    sendbit(0) ;
    */
    
    sendnum(start) ;

    
    for (int i=0; i<data.length(); i++)
    {
      char f=data.charAt(i);
      sendnum(enc((int)f));
    }
    //sendnum(enc(10))  ;
    
    sendnum(ends) ;
    
    
    
    /*
    digitalWrite(6, HIGH) ;
    delayMicroseconds(10) ;
    digitalWrite(6, LOW) ;
    delayMicroseconds(10) ;
    */
    
 }
