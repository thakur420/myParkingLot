from enum import Enum

class ParkingSpotType(Enum):
    HANDICAPPED = 1
    COMPACT = 2
    LARGE = 3
    MOTORCYCLE = 4

class VehicleType(Enum):
    CAR = 1
    TRUCK = 2
    ELECTRIC = 3
    VAN = 4
    MOTORBIKE = 5

class PayementStatus(Enum):
    UNPAID = 1
    PENDING = 2
    PAID = 3
    FAILED = 4

class PaymentMode(Enum):
    CASH = 1
    CARD = 2
    UPI = 3

