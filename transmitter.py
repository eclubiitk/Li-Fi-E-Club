string =input("")#justchange input
string2=""
for x in string:
    i=ord(x)
    print(i)
    string2+=bin(i)


string3=""
for x in string2:
    if x=="b":
        continue
    else:
        string3+=x

string2=""
#manchester incoding starts
for x in string3:
    if x=="0":
        string2+="10"
    else:
        string2+="01"

print(string2)#comment this its for checking only
print(string3)
