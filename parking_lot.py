from constants import ParkingSpotType
from constants import VehicleType
from parking_spot import ParkingSpot
from vehicle import Vehicle
from parking_ticket import ParkingTicket
from parking_rate import ParkingRate
from payment import Payment
from utils import AutoIncrementID, curr_time, calculate_hrs, get_parking_rate, get_payment_mode

class _ParkingLot(type):
    __instance = None
    
    def __new__(cls,name, bases, dct):
        if cls.__instance is None:
            cls.__instance = super(_ParkingLot, cls).__new__(cls,name, bases, dct)
        return cls.__instance
    
class ParkingLot(metaclass=_ParkingLot):
    def __init__(self, id, name, address, capacity, display_board, parking_spots, entrances, exits) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.capicty = capacity
        self.display_board = display_board
        self.parking_spots = parking_spots # dict = {type:list[parking_spots]}
        self.entrances = entrances
        self.exits = exits
        self.tickets = {}
    
    def is_full(self):
        pass

    def book_ticket(self,vehicle): 
        parking_spot_type = self._get_parking_type(vehicle.type)
        parking_spot = self._get_parking_spot(parking_spot_type)
        if parking_spot is None:
            print("No free spot Available")
            return
        parking_spot.add_vehicle(vehicle)
        parking_ticket = ParkingTicket(AutoIncrementID.get_next_id(),vehicle,curr_time(),parking_spot)
        self.tickets[vehicle.license] = parking_ticket
        return parking_ticket

    def get_ticket(self,license):
        if license in self.tickets:
            return self.tickets[license]

    def _get_parking_type(self, type):
        if type == VehicleType.MOTORBIKE:
            return ParkingSpotType.MOTORCYCLE
        elif type == VehicleType.CAR:
            return ParkingSpotType.COMPACT
        return ParkingSpotType.LARGE
    
    def _get_parking_spot(self, type):
        parking_spots = self.parking_spots[type]
        for parking_spot in parking_spots:
            if parking_spot.is_empty :
                return parking_spot
        return None
    
    def make_payment(self,parking_ticket, mode):
        if parking_ticket is None or mode is None:
            return None
        
        vehicle = parking_ticket.vehicle
        parking_spot = parking_ticket.parking_spot

        hrs = calculate_hrs(parking_ticket.timestamp)
        rate = get_parking_rate(vehicle.type)
        mode = get_payment_mode(mode)
        
        parking_rate = ParkingRate(hrs,rate)
        amt = parking_rate.calculate_amt()
        print(f"processing payment of {amt:.2f} for {hrs:.2f} mins...")
        payment = Payment(AutoIncrementID.get_next_id(), mode, amt)
        payment.pay()
        
        parking_spot.remove_vehicle()
        del self.tickets[vehicle.license]
        return payment
    
    
