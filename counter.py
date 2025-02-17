import time
import serial
from Modbus import Modbus
from Noise import Noise
from Temperature import Temperature
from Humidity import Humidity

tty = ('/dev/tty.usbmodem14301')
#tty = '/dev/ttyACM0'
ser = serial.Serial(tty, 115200, timeout=0.2) # or make sure that both are running at the same baudrate
ser.flushInput()

def swap_pairs(hex_str: str) -> str:
    hex_list = list(hex_str)  # 轉成可變 list
    length = len(hex_list)

    # 交換對應位置的字元
    for i in range(0, length, 2):
        j = length - 2 - i  # 找到對應的交換位置
        if j > i:  # 確保只交換前半部
            hex_list[i], hex_list[i+1], hex_list[j], hex_list[j+1] = hex_list[j], hex_list[j+1], hex_list[i], hex_list[i+1]

    swapped_hex = ''.join(hex_list)  # 轉回字串

    # 轉換成 UUID 格式（8-4-4-4-12）
    uuid_formatted = f"{swapped_hex[:8]}-{swapped_hex[8:12]}-{swapped_hex[12:16]}-{swapped_hex[16:20]}-{swapped_hex[20:]}"

    return uuid_formatted

def main():
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
                result = line[index + 3:-4].strip()  # 擷取 `>:` 後面的字串
                bytestr = result.decode("iso8859-1")
                output_str = swap_pairs(bytestr[:-2])
                print(f"{output_str}, {line[index0+3:index].decode()}, {bytestr[-2:]}")  # 00001523-1212-efde-1523-785feabcd123
        
if __name__ == "__main__":
    main()
