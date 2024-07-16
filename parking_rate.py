class ParkingRate:
    def __init__(self, hrs, rate) -> None:
        self.hrs = hrs
        self.rate = rate

    def calculate_amt(self):
        return self.hrs * self.rate