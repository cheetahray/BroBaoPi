import time
import serial
from Modbus import Modbus
from Noise import Noise
from Temperature import Temperature
from Humidity import Humidity

#tty = '/dev/tty.usbmodem14401'
tty = '/dev/ttyACM0'
ser = serial.Serial(tty, 115200, timeout=0.2) # or make sure that both are running at the same baudrate
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
    onoff = 0
    time.sleep(0.5) # include some sleep here also
    init = "mesh init\n"
    print(init)
    ser.write(init.encode("iso8859-1"))
    time.sleep(0.1)
    init = "mesh target dst 0xc000\n"
    print(init)
    ser.write(init.encode("iso8859-1")) # group 位址
    time.sleep(0.1)
    line = ser.readline() # readline is not very nice, think about using read_all() or just read() instead.
    print(line)
    while True:
        line = ser.readline() # readline is not very nice, think about using read_all() or just read() instead.
        if(line):
            index = line.find(b">: ")  # 找到 `>:` 的位置
            if index != -1:  # 確保 `>:` 存在
                index0 = line.find(b"<0x")
                print(line[index0:index+1])
                result = line[index + 3:-4].strip()  # 擷取 `>:` 後面的字串
                bytestr = result.decode("iso8859-1")
                print(handle_modbus_type("temperature", bytes.fromhex(bytestr))) # Temperature signal processing. Value1: 120.0, Value2: 144.0
                print(handle_modbus_type("humidity", bytes.fromhex(bytestr))) # Temperature signal processing. Value1: 120.0, Value2: 144.0
                print(handle_modbus_type("noise", bytes.fromhex(bytestr))) # Temperature signal processing. Value1: 120.0, Value2: 144.0
                cmd = f"mesh test net-send 82030{onoff:d}{count:02d}\n"
                print(cmd)
                ser.write(cmd.encode('iso8859-1'))
                onoff = (onoff + 1) % 2
                count = (count + 1) % 100
            
if __name__ == "__main__":
    main()
