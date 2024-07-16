class ParkingSpot:
    def __init__(self, id , type, is_empty = True) -> None:
        self.id = id
        self.type  = type
        self.is_empty = is_empty
        # self.vehicle = None

    def add_vehicle(self,vehicle):
        self.vehicle = vehicle
        self.is_empty = False

    def remove_vehicle(self):
        self.vehicle = None
        self.is_empty = True