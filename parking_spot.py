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
            