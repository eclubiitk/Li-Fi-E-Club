#include <String.h>
String userinput="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
int i=0;
int len;
byte arr[9];
int laserPin=13;
int j,count;
//int k=0;


void setup() 
{
  pinMode(laserPin,OUTPUT);
  Serial.begin(9600);
  //input();
  //Serial.print(userinput);
  set();
  len=userinput.length();
  digitalWrite(laserPin,HIGH);
  digitalWrite(laserPin,HIGH);
}
void loop()
{
 count=charconv();
 //Serial.println(count);
 if (count != 0){
  for (j=0;j<9;j++){
    digitalWrite(laserPin,arr[j]);
    delay(20);
    Serial.println(arr[j]);
    //if(arr[j]==0){digitalWrite(laserPin,1);Serial.println(1);}
    //else{digitalWrite(laserPin,0);Serial.println(0);}    
    //delay(10);
    Serial.flush();
    //delay(7);
    //k+=2;
    
    } 
 }
 else{
  //Serial.println(k);
  digitalWrite(laserPin,0);
  digitalWrite(laserPin,0);
  exit(0);
 }   
}


void input()
{
  char f;
  while(1)
  {if(Serial.available()>0){
    f=Serial.read();
    //Serial.println(f);
    if(f=='\n')
    return;
    else
    userinput+=f;}
    //Serial.print(userinput);
  }
}
void set()
{
  for(byte i2=0;i2<9;i2++)
  arr[i]=0;
}
byte charconv()
{
  if(i<len)
{
  char c=userinput.charAt(i); 
  //Serial.println(c);
  byte f=(byte)c;
  //Serial.print(f);
  i++;
  byte x=1;
  while(f!=0)
  {
    arr[7-x]=f%2;
    f/=2;
    x++;
    
  }
  return 1;
}
else 
return 0;
}
