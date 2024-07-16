class ParkingTicket:
    def __init__(self,id, vehicle, timestamp, parking_spot) -> None:
        self.id = id
        self.vehicle = vehicle
        self.timestamp = timestamp
        self.parking_spot = parking_spot

    def __repr__(self) -> str:
        return f"{self.id}, {self.vehicle.license}, {self.timestamp}"