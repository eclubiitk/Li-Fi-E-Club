
int pin=2;
String strin;

String outstr;

int j=0;
int k=0;
int o=0;
void setup() {
  Serial.begin(9600);
  
  pinMode(pin,INPUT);
}

void loop() {
  while (Serial.available()==0) {
  
  }
  strin=Serial.readString();
  
  int i;
  
  while(strin[i]!="\0")
  
  {
    for(int p=0;p<7;p++)
    {
      k=int(strin[i+p]);
      
      j+=(k*pow(2,p));    
      
    }
    char c=char(j);
    
    outstr[o]=c;
    o++;
    i+=7;
    
  }
}
