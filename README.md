# Li-Fi-E-Club

#### To Run on device(s):

###### Windows : System Type : nt

* Install node and npm
* Navigate to Main Codes folder and execute:
```
npm i express formidable cors
python3 -m pip install pyserial
```
* Then RUN:
```
python3 pyLiFi.py
```

##### Ubuntu : System Type : posix

* Install node and npm

* Navigate to Main Codes folder and execute:
```
sudo npm i express formidable cors
sudo python3 -m pip install pyserial
```
* Then RUN:
```
sudo python3 pyLiFi.py
```

##### OR

* Navigate to Main Codes folder and RUN install.sh as root user, i.e., execute the following command(s) :
```
sudo chmod 777 install.sh
sudo ./install.sh
```
* Execute:
```
sudo npm i express formidable cors
sudo python3 -m pip install pyserial
```
* Then RUN:
```
sudo python3 pyLiFi.py
```

#### To check if node/npm is installed on your system, run the following:
```
node --version
npm --version
```

### PS: I assume, like any sane man you have Python installed on your system (executed as : python3)

#### Alternative Approach:

* Installation part remains the same
* Instead of runnning pyLiFi.py you can run:

nt:
```
node mainserver.js
```

posix:
```
sudo node mainserver.js
```
and the run index.html
