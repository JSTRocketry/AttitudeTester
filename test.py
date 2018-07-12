import serial

class ArduinoCommunicator():
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200)

    def readData(self):
        return self.ser.readline().decode('utf-8')

    def isAvailable(self):
        return self.ser.isOpen()

    def writeData(self, data):
        return self.ser.write(data.encode('utf-8'))

    def kill(self):
        self.ser.close()

def main():
    dataSent = False
    arduino = ArduinoCommunicator("/dev/ttyACM0")
    data = "X:50"
    while(arduino.isAvailable() and not dataSent):
        arduino.writeData(data)
        dataSent = True
    arduino.kill()

main()
