from threading import RLock
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
        # self._lock = RLock()

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
    
