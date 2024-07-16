from datetime import datetime
from constants import VehicleType, PaymentMode

class AutoIncrementID:
    _id_counter = 0  # Class variable to keep track of the current ID

    @classmethod
    def get_next_id(cls):
        cls._id_counter += 1
        return cls._id_counter
    

def curr_time():
    current_timestamp = datetime.now()
    formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_timestamp

def get_vehicle_type(type):
    if type.lower() == "car":
        return VehicleType.CAR
    if "motor" in type.lower():
        return VehicleType.MOTORBIKE
    if "van" in type.lower():
        return VehicleType.VAN
    if "truck" in type.lower():
        return VehicleType.TRUCK
    
def calculate_hrs(old_timestamp):
    old_timestamp = datetime.strptime(old_timestamp, "%Y-%m-%d %H:%M:%S")
    curr_timestamp = datetime.strptime(curr_time(), "%Y-%m-%d %H:%M:%S")

    total_time_secs = (curr_timestamp - old_timestamp).total_seconds()
    return total_time_secs / 60

def get_parking_rate(vehicle_type):
    if vehicle_type == VehicleType.MOTORBIKE:
        return 10
    if vehicle_type == VehicleType.CAR:
        return 15
    return 20

def get_payment_mode(mode):
    if "card" in mode.lower():
        return PaymentMode.CARD
    if "upi" in mode.lower():
        return PaymentMode.UPI
    return PaymentMode.CASH