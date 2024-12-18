from enum import Enum

class PaymentStatus(Enum):
    UNPAID = 1
    FAILED = 2
    PAID = 3

class ParkingSpotType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

class PaymentMode(Enum):
    CASH = 1
    CARD = 2
    UPI = 3

class GateType(Enum):
    ENTRY = 1
    EXIT = 2

class PricingPolicy:
    PRICES = {
        VehicleType.BIKE: 10,
        VehicleType.CAR: 20,
        VehicleType.TRUCK: 30,
    }

    @staticmethod
    def get_price(vehicle_type):
        return PricingPolicy.PRICES.get(vehicle_type, 0)