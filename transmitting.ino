int pulse = 500 ;
//pulse = pulse ;
int data[]={0,1,0,0,0,0,1,1};
void setup() {
  pinMode(6, OUTPUT) ;
  
//  int man = 0 ;
}

void loop() {
  for(int i=0; i<=7; i++){
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
}
