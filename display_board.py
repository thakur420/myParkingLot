# from parking_spot import ParkingSpot
class DisplayBoard:
    def __init__(self,id, parking_spots) -> None:
        self.id = id
        self.parking_spots = parking_spots

    def display(self):
        print("SpotType => VacantSpot")
        for type, parking_spot in self.parking_spots.items():
            count = 0
            for spot in parking_spot:
                if spot.is_empty:
                    count += 1
            print(f"{type} => {count}")


