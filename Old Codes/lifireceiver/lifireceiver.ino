byte n=0;
byte u=0;
byte arr[10000];
void refine()
{
  int h,k;
  for(u=0;u<10000;u++)
  {if(arr[u]==1 && arr[u+1]==1){h=u+2;break;}}
  for(u=0;u<10000-h;u++)
  {arr[u]=arr[u+h];}
  for(u=0;u<10000-h;u++)
  {if(arr[u]==0 && arr[u+1]==0 && arr[u+2]==0){k=u;break;}}
  for(u=0;u<k;u++)
  {
    Serial.println(arr[u]);
  }
  n=k;
  //k is the limit of indexes, all loop will work till k-1
}

void setup()
{
  Serial.begin(9600);
  pinMode(4,INPUT);
}

void loop()
{
  if(n<10000)
  arr[n]=digitalRead(A4);
  else
  {refine();exit(0);}
}
