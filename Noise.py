from ModbusStrategy import ModbusStrategy

class Noise(ModbusStrategy):
    def apply(self, value1:int , value2:int):
        return f"Noise Value: {((float(value1 << 8) + float(value2)) / 10.0)}"


