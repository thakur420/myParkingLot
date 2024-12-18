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

    
    