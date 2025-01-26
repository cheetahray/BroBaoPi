import Temperature, Humidity, Noise

class ModbusFactory:
    _strategies = {
        "Temperature": Temperature,
        "Humidity": Humidity,
        "Noise": Noise
    }

    @staticmethod
    def get_strategy(customer_type):
        strategy_class = ModbusFactory._strategies.get(customer_type)
        if not strategy_class:
            raise ValueError(f"Unknown customer type: {customer_type}")
        return strategy_class()
