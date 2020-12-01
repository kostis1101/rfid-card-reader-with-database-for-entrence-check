import serial
import serial.tools.list_ports
import pickle
import os
import os.path

os.chdir('C:\\Users\\ΙΤ\\Desktop\\Kostis-Computer\\pythonProjects\\munDataBase')

file_name = 'other_db.pickle'

port = 'COM3'

if not os.path.isfile(file_name) or os.path.getsize(file_name) > 0:
    with open(file_name, 'wb') as f:
        pickle.dump({'port': port}, f)

if os.path.getsize(file_name) > 0:
    with open(file_name, 'rb') as f:
        other = pickle.load(f)
        port = other['port']

try:
    ser = serial.Serial(port, 9600)
except serial.serialutil.SerialException as e:
    ser = -1
    print(e)


def read():
    if ser != -1:
        cc = str(ser.readline())[2:-5]
        number = (cc)
        return number
    else:
        return -1


def list_ports():
    return list(serial.tools.list_ports.comports())
