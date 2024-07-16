from constants import PayementStatus
from utils import curr_time
class Payment:
    def __init__(self,id, mode, amt) -> None:
        self.id = id
        self.mode = mode
        self.status = PayementStatus.UNPAID
        self.amt = amt
        # self.timestamp = curr_time()

    def pay(self):
        self.timestamp = curr_time()
        print(f"making payment of {self.amt:.2f} via {self.mode}")
        self.status = PayementStatus.PAID

    def __repr__(self) -> str:
        return f"Made payment of {self.amt:.2f} via {self.mode} at {self.timestamp}"