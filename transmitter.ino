char input[20]="abvfyvdbvczdfyDVHMH";
int pin;
int arr[7];
void setup() {
pinMode(pin,OUTPUT);  

}

void loop() {
  for(int i=0;i<20;i++){
    int ascai=input[i];
    for(int j=0;j<7;j++){
      int a=ascai%2;
      ascai=ascai/2;
      arr[6-j]=a;
    }
    for(int k=0;k<7;k++){
      if(arr[k]==1)
      {digitalWrite(pin,LOW);
      delay(200);
      digitalWrite(pin,HIGH);
      delay(200);
      }
      if(arr[k]==0){
        digitalWrite(pin,HIGH);
      delay(200);
      digitalWrite(pin,LOW);
      delay(200);
        
      }
    }
  }

}
