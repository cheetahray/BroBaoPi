from ModbusStrategy import ModbusStrategy

class Temperature(ModbusStrategy):
    def apply(self, value1: int, value2: int):
        return f"Temperature Value: {((float(value1 << 8) + float(value2)) / 10.0)}"
