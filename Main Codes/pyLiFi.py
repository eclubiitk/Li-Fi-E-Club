import os
if(os.name=='nt'):
    os.system('start "Backend : Server" node mainserver.js')
    os.system('start "Frontend : User Interface" index.html')
if(os.name=='posix'):
    os.system('node mainserver.js &')
    os.system('index.html &')