import crcmod
import ModbusStrategy

class Modbus:
    def __init__(self, min_value, max_value, strategy: ModbusStrategy):
        self.min_value = min_value
        self.max_value = max_value
        self.strategy = strategy
        self.crc16 = crcmod.predefined.Crc('modbus')

    def apply(self, result):
        received_crc = int.from_bytes(result[-2:], 'little')
        calculated_crc = self.crc16.new(result[:-2])
        if received_crc == calculated_crc.crcValue:
            """應用策略處理信號"""
            return self.strategy.apply(result[self.min_value], result[self.max_value])
        else:
            return "CRC error"

