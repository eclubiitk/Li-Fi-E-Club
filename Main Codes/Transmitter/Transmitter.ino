int pulse = 500 ;
//pulse = pulse ;
int datax[]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int data[]={0,1,0,0,1,1,0,0,0,1,1,0,1,0,0,1,0,1,0,0,0,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,1,0};
void setup() {
  pinMode(6, OUTPUT) ;
  for(int i=0; i<30; i++){
      digitalWrite(6, LOW);
      delayMicroseconds(pulse);
      digitalWrite(6, HIGH);
      delayMicroseconds(pulse);
  }
//  int man = 0 ;
}

void loop() {
  for(int i=0; i<8*5; i++){
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
