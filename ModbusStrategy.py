from abc import ABC, abstractmethod

# Modbus 策略基類
class ModbusStrategy(ABC):
    @abstractmethod
    def apply(self, value1:int, value2:int):
        """計算處理邏輯，接受兩個參數"""
        pass
