from ModbusStrategy import ModbusStrategy

class Humidity(ModbusStrategy):
    def apply(self, value1: int, value2:int ):
        return f"Humidity Value: {((float(value1 << 8) + float(value2)) / 10.0)}"


