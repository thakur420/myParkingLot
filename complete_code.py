'''Requirement
---------------------
1. The parking lot should have multiple levels, each level with a certain number of parking spots.
2. The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
3. The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
4. The system should track the availability of parking spots and provide real-time information to customers.
5. The system should handle multiple entry and exit points and support concurrent access. 
6. The system should generate ticket at the entry and bill based upon vehicle and duration at the exit.
7. The system should accept multiple payment option for paying the bill amount, such as cash, upi, card.
'''
    
# gate.py
class Gate:
    def __init__(self, id, type):
        self.id = id
        self.type = type

# parking_enum.py
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


# parking_level.py
import logging
logging.basicConfig(level=logging.INFO)
import utility as util

class ParkingLevel:
    def __init__(self, id, spots, gates):
        self.id = id
        self.parking_spots = spots
        self.gates = gates

class SpotManager:
    def __init__(self, parking_levels):
        self.parking_levels = parking_levels

    def __str__(self):
        for level in self.parking_levels:
            details = f"  Level {level.id}: {len(level.parking_spots)} spots, {len(level.gates)} gates\n"
        return details

    def get_free_slot(self, vehicle_type):
        '''Strategy design pattern can be used for 
            differnt strategy of assigning parking spot.
            Current Implementation of simple linear search.
        '''
        for parking_level in self.parking_levels:
            for parking_spot in parking_level.parking_spots:
                if parking_spot.vacant and vehicle_type.value == parking_spot.type.value:
                    try:
                        parking_spot.book_spot()
                        return parking_spot
                    except ValueError as e:
                        logging.warning(f"[{util.get_curr_time()}]: slot already booked exception {e}")
        return None
    
# parking_spot.py
from threading import RLock
class ParkingSpot:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.vacant = True
        self._lock = RLock()
    
    def __str__(self):
        return f"Parking Spot Id={self.id}, type={self.type}, is vacant ={self.vacant}"
    
    def book_spot(self):
        with self._lock:
            if self.vacant:
                self.vacant = False
            else:
                # custom exception can be used for better readability
                raise ValueError("Slot Already booked") 
    def release_spot(self):
        with self._lock:
            if not self.vacant:
                self.vacant = True
            else:
                raise ValueError("Slot booked for multiple vehicle")
            

# parking_ticket.py
import time
import utility as util
from threading import RLock
class ParkingTicket:
    def __init__(self, ticket_id, vehicle, parking_spot):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.entry_time = time.time()

class TicketManager:
    def __init__(self):
        self.active_tickets = {}
        self._lock = RLock()
    
    def create_ticket(self, vehicle, parking_spot):
        ticket_id=f"T{util.get_curr_time()}_{vehicle.license}"
        ticket = ParkingTicket(ticket_id, vehicle, parking_spot)
        self.active_tickets[ticket.ticket_id] = ticket
        return ticket

    def get_ticket(self, ticket_id):
        with self._lock:
            return self.active_tickets.get(ticket_id)

    def remove_ticket(self, ticket_id):
        with self._lock:
            return self.active_tickets.pop(ticket_id, None)

# payment.py
from abc import ABC, abstractmethod
from parking_enum import PaymentStatus

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class CreditCardPayment(Payment):
    def __init__(self, card_number ):
        self.card_number = card_number
        self.status = PaymentStatus.UNPAID
    
    def __str__(self):
        return f"Card No = {self.card_number}"
        
    def pay(self, amount):
        print(f"Paid ${amount} using Credit Card (Card Number: {self.card_number}).")
        self.status = PaymentStatus.PAID

class UPIPayment(Payment):
    def __init__(self, upi_id):
        self.upi_id = upi_id
        self.status = PaymentStatus.UNPAID
    
    def __str__(self):
        return f"UPI No = {self.upi_id}"
    
    def pay(self, amount):
        print(f"Paid ${amount} using UPI (ID: {self.upi_id}).")
        self.status = PaymentStatus.PAID

class CASHPayment(Payment):
    def __init__(self, cash_count):
        self.cash_count = cash_count
        self.status = PaymentStatus.UNPAID
    
    def __str__(self):
        return f"Cash Count = {self.cash_count}"

    def pay(self, amount: float):
        print(f"Paid ${amount} using Cash (Count: {self.cash_count}).")
        self.status = PaymentStatus.PAID

#payment_factory_manager.py
from payment import CASHPayment, CreditCardPayment, UPIPayment
from parking_enum import PaymentMode, PricingPolicy
from threading import RLock
import random
import string
import time

class PaymentFactory:
    @staticmethod
    def get_payment_obj(type):
        if type == PaymentMode.CASH:
            cash_count = random.randint(1, 10)
            return CASHPayment(cash_count)
        if type == PaymentMode.CARD:
            card_number = random.randint(10**15, 10**16 - 1)
            return CreditCardPayment(card_number)
        if type == PaymentMode.UPI:
            length = random.randint(3, 5)
            random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
            upi_id = f"{random.randint(10**9, 10**10 - 1)}@{random_string}" 
            return UPIPayment(upi_id)
        else:
            raise ValueError(f"No payment option available for: {type}")
        
class PaymentManager:
    def __init__(self):
        self.payments = {}
        self._lock = RLock()
     
    def calculate_charge(self, vehicle_type, entry_time):
        cost = PricingPolicy.get_price(vehicle_type)
        duration = time.time() - entry_time
        return cost * duration

    def process_payment(self, ticket_id, payment_type, amount):
        payment = PaymentFactory.get_payment_obj(payment_type)
        payment.pay(amount)
        with self._lock:
            self.payments[ticket_id] = payment
        return payment
    
# utility.py
from datetime import datetime

def get_curr_time():
    current_time = datetime.now()
    return current_time.strftime("%H:%M:%S")

# vehicle.py
class Vehicle:
    def __init__(self, vehicle_no, type):
        self.license = vehicle_no
        self.type = type

# parking_lot.py
from vehicle import Vehicle
from parking_enum import PaymentStatus
from collections import Counter
import utility as util
import logging
logging.basicConfig(level=logging.INFO)

class ParkingLot:
    def __init__(self, id, spot_manager, ticket_manager, payment_manager):
        self.id = id
        self.spot_manager = spot_manager
        self.ticket_manager = ticket_manager
        self.payment_manager = payment_manager

    def __str__(self):
        details = f"ParkingLot(ID: {self.id}, Levels: {len(self.parking_levels)})\n"
        details += str(self.spot_manager)
        return details
    
    def book_parking(self, vehicle: Vehicle):
        parking_spot = self.spot_manager.get_free_slot(vehicle.type)
        if not parking_spot:
            logging.info(f"[{util.get_curr_time()}]: No available parking spots for this vehicle type.")
            return None
        ticket = self.ticket_manager.create_ticket(vehicle,parking_spot)
        logging.info(f"[{util.get_curr_time()}]:Parking booked. Ticket ID: {ticket.ticket_id}")
        return ticket.ticket_id

    def make_payment(self, ticket_id: int , payment_type):
        ticket = self.ticket_manager.get_ticket(ticket_id)
        if not ticket:
            logging.error(f"[{util.get_curr_time()}]: Invalid ticket ID.")
            return 
        
        amount = self.payment_manager.calculate_charge(ticket.vehicle.type, ticket.entry_time)
        payment = self.payment_manager.process_payment(ticket_id, payment_type, amount)
        if payment and payment.status == PaymentStatus.PAID:
            logging.info(f"[{util.get_curr_time()}]: Paid Sucessfully. Generating Bill ...")
            ticket.parking_spot.release_spot()
            self.ticket_manager.remove_ticket(ticket_id)
        else:
            logging.info(f"[{util.get_curr_time()}]: Payment failed. Try again ...")

    
    def display(self):
        counter = Counter()
        for parking_level in self.spot_manager.parking_levels:
            for parking_spot in parking_level.parking_spots:
                if parking_spot.vacant:
                    counter[parking_spot.type] += 1

        print(f"{'vehicleType':<15}{'freeSpot':<10}")
        for vehicle_type, free_spot in counter.items():
            print(f"{vehicle_type.name:<15}{free_spot:<10}")

# client.py
from vehicle import Vehicle
from gate import Gate
from parking_lot import ParkingLot
from parking_spot import ParkingSpot
from parking_ticket import TicketManager
from parking_level import ParkingLevel, SpotManager
from parking_enum import VehicleType, PaymentMode, ParkingSpotType, GateType
from payment_factory_manager import PaymentManager
import time
import random

def create_parking_lot(
    max_levels=10, 
    min_spots=50, max_spots=100, 
    min_gates=2, max_gates=6
):
    """Initializes a parking lot with random levels, spots, and gates."""
    parking_level_count = random.randint(1, max_levels)
    parking_levels = []

    for level in range(parking_level_count):
        parking_spots = _create_parking_spots(level, random.randint(min_spots, max_spots))
        gates = _create_gates(level, random.randint(min_gates, max_gates))
        parking_level = ParkingLevel(level, parking_spots, gates)
        parking_levels.append(parking_level)
    
    return parking_levels

def _create_parking_spots(level_id, spot_count):
    """Creates a list of parking spots for a specific level."""
    parking_spots = []
    for spot_id in range(1, spot_count+1):
        spot_type = random.choices(
            list(ParkingSpotType), 
            weights=[0.3, 0.6, 0.1],  # Example: More car spots than truck spots
            k=1
        )[0]
        parking_spot = ParkingSpot(f"L{level_id}_S{spot_id}", spot_type)
        parking_spots.append(parking_spot)
    return parking_spots

def _create_gates(level_id, gate_count):
    """Creates a list of gates for a specific level."""
    gates = []
    for gate_id in range(1, gate_count + 1):
        gate_type = random.choice(list(GateType))
        gate = Gate(f"{level_id}_G{gate_id}", gate_type)
        gates.append(gate)
    return gates
    
def client():
    parking_levels = create_parking_lot()
    spot_manager = SpotManager(parking_levels)
    ticket_manager = TicketManager()
    payment_manager = PaymentManager()
    parking_lot = ParkingLot("P1", spot_manager, ticket_manager, payment_manager)
    
    parking_lot.display()

    bike = Vehicle("BR12AZ2345", VehicleType.BIKE)
    car = Vehicle("KA21AZ4598", VehicleType.CAR)
    
    ticket_id1 = parking_lot.book_parking(bike)
    ticket_id2 = parking_lot.book_parking(car)
    
    parking_lot.display()
    time.sleep(10)
    
    parking_lot.make_payment(ticket_id1, PaymentMode.CASH)
    parking_lot.display()
    parking_lot.make_payment(ticket_id2, PaymentMode.UPI)
    parking_lot.display()

if __name__ == "__main__":
    client()
