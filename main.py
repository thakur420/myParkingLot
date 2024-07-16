from constants import ParkingSpotType
from parking_spot import ParkingSpot
from utils import AutoIncrementID, get_vehicle_type
from display_board import DisplayBoard
from parking_lot import ParkingLot
from vehicle import Vehicle

def initialize_parking_lot():
    parking_spots = {}
    for type in ParkingSpotType:
        parking_spot = []
        for _ in range(10):
            parking_spot.append(ParkingSpot(AutoIncrementID.get_next_id(),type))
        parking_spots[type] = parking_spot
    entrances = []
    exits = []
    display_board = DisplayBoard(AutoIncrementID.get_next_id(),parking_spots)
    id = AutoIncrementID.get_next_id()
    parking_lot = ParkingLot(id, "p1", "add1", 40, display_board, parking_spots, entrances, exits)
    return parking_lot


def main():
    parking_lot = initialize_parking_lot()
    while True:
        parking_lot.display_board.display()
        print("Choose Option")
        print("1. Book a Parking Slot")
        print("2. Pay and Exit")
        op = input("Enter 1 or 2\n")
        if op == str(1):
            license, type = input("Enter Vehicle license and its type\n").split()
            ticket = parking_lot.book_ticket(Vehicle(license,get_vehicle_type(type)))
            print(ticket)
        elif op == str(2):
            license, mode = input("Enter Vehicle license and payment mode\n").split()
            ticket = parking_lot.get_ticket(license)
            payment = parking_lot.make_payment(ticket, mode)
            print(payment)
        else:
            print("Invalid Input") 

if __name__ == "__main__":
    main()