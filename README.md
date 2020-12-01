# rfid-card-reader-with-database-for-entrence-check

It keeps track of who has already entered the dinner room. This was achieved by using python to handle the database and all the logic and adruino to read the rfids and send the necessery data to the python script via the serial port.

## Requirements

__python__
pyserial:
```sh
pip3 install pyserial
```
playsound:
```sh
pip3 install playsound
```

__arduino__
Arduino RFID Library for MFRC522:
download link: https://www.arduino.cc/reference/en/libraries/mfrc522/
 
Alternatively you can you the requirements.txt to install all the necessary packeges.

## Running the application
First make sure that all the files are located in the same directory.
To run the application, run the main_iu.py.
