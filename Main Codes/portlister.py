import json
from serial.tools import list_ports
y = list(list_ports.comports())
x = {'data':y}
po = open('portlist.json','w')
po.write(json.dumps(x))
po.close()