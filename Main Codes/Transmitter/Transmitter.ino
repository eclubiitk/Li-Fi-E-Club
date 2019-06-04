int pulse = 500 ;
String x="";
byte datax[]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
byte len;
byte data[1000];
//int data[]={0,1,0,0,1,1,0,0,0,1,1,0,1,0,0,1,0,1,0,0,0,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,1,0}; //Lifi'\n'

void input()
{
  char f;
  while(1)
  {if(Serial.available()>0){
    f=Serial.read();
    if(f=='\n')
    return;
    else
    x+=f;}
  }
}

void reset() {
  for(byte i=0;i<1000;i++)
    data[i]=0;
}

void conv() {
  byte t=x.length();
  len=8*t+8;
  char c;
  byte b=0,r=0;
  for(byte i=0; i<t; i++) {
    c=x.charAt(i);
    b=(byte)c;
    r=0;
    while(b!=0){
      data[7-r+8*i]=b%2;
      b/=2;
      r++;
    }
  }
  b=10;
  r=0;
  while(b!=0){
      data[7-r+len-8]=b%2;
      b/=2;
      r++;
  }
}

void setup() {
  pinMode(6, OUTPUT);
  input();
  reset();
  conv();
  for(byte i=0; i<30; i++){
      digitalWrite(6, LOW);
      delayMicroseconds(pulse);
      digitalWrite(6, HIGH);
      delayMicroseconds(pulse);
  }
//  int man = 0 ;
}

void loop() {
  for(int i=0; i<len; i++){
    if(data[i]==1){
      digitalWrite(6, HIGH);
      delayMicroseconds(pulse);
      digitalWrite(6, LOW);
      delayMicroseconds(pulse);
      }
    else{
      digitalWrite(6, LOW);
      delayMicroseconds(pulse);
      digitalWrite(6, HIGH);
      delayMicroseconds(pulse);
      }  
  }
//  digitalWrite(6,HIGH);
//  delay(10);
}
