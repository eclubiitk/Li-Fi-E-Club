#taking input
string=input()
#get length of string
j=len(string)
#to divide it into into segments of length 7
k=j//7
#str3 string in char final result
str3=""
#sstr binay string of each character
sstr=""

for i in range(k):
    sstr=string[7*i:7*(i+1)]
    #getting ascii value
    h=int(sstr,2)
    #adding it to str3
    str3+=chr(h)

print(str3)