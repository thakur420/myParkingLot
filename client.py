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
