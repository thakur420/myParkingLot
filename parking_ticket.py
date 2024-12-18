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