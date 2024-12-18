from abc import ABC, abstractmethod
from parking_enum import PaymentStatus

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class CreditCardPayment(Payment):
    def __init__(self, card_number ):
        self.card_number = card_number
        self.status = PaymentStatus.UNPAID
    
    def __str__(self):
        return f"Card No = {self.card_number}"
        
    def pay(self, amount):
        print(f"Paid ${amount:.2f} using Credit Card (Card Number: {self.card_number}).")
        self.status = PaymentStatus.PAID

class UPIPayment(Payment):
    def __init__(self, upi_id):
        self.upi_id = upi_id
        self.status = PaymentStatus.UNPAID
    
    def __str__(self):
        return f"UPI No = {self.upi_id}"
    
    def pay(self, amount):
        print(f"Paid ${amount:.2f} using UPI (ID: {self.upi_id}).")
        self.status = PaymentStatus.PAID

class CASHPayment(Payment):
    def __init__(self, cash_count):
        self.cash_count = cash_count
        self.status = PaymentStatus.UNPAID
    
    def __str__(self):
        return f"Cash Count = {self.cash_count}"

    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} using Cash (Count: {self.cash_count}).")
        self.status = PaymentStatus.PAID

