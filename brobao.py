import time
import serial
from Modbus import Modbus
from Noise import Noise
from Temperature import Temperature
from Humidity import Humidity

tty = '/dev/tty.usbmodem14401'
# '/dev/ttyACM0'
ser = serial.Serial(tty, 115200, timeout=0.5) # or make sure that both are running at the same baudrate
ser.flushInput()

modbus_signals = {
    "noise": Modbus(17, 18, Noise()),
    "temperature": Modbus(3, 4, Temperature()),
    "humidity": Modbus(5, 6, Humidity()),
}

def handle_modbus_type(modbus_type, value):
    # 獲取對應的 Modbus 物件
    modbus = modbus_signals.get(modbus_type)
    if not modbus:
        return f"Unknown Modbus type: {modbus_type}"

    # 應用處理
    return modbus.apply(value)

def main():
    # 假設有三種客戶類型
    count = 0

    time.sleep(0.5) # include some sleep here also
    while True:
        line = ser.readline() # readline is not very nice, think about using read_all() or just read() instead.
        index = line.find(b">:")  # 找到 `>:` 的位置
        if index != -1:  # 確保 `>:` 存在
            result = line[index + 2:].strip()  # 擷取 `>:` 後面的字串
            print((line[index-7:index+2]).decode("iso8859"))
            print(handle_modbus_type("temperature", result)) # Temperature signal processing. Value1: 120.0, Value2: 144.0
        if(0 == count):
            ser.write(b"mesh test net-send 82030110\n")
            count = 1
            print("Led On")
        else:
            ser.write(b"mesh test net-send 82030000\n")
            count = 0
            print("Led Off")
        time.sleep(1.5)

if __name__ == "__main__":
    main()
