from payment import CASHPayment, CreditCardPayment, UPIPayment
from parking_enum import PaymentMode, PricingPolicy
from threading import RLock
import random
import string
import time

class PaymentFactory:
    @staticmethod
    def get_payment_obj(type):
        if type == PaymentMode.CASH:
            cash_count = random.randint(1, 10)
            return CASHPayment(cash_count)
        if type == PaymentMode.CARD:
            card_number = random.randint(10**15, 10**16 - 1)
            # print(f"Card number => {card_number}")
            return CreditCardPayment(card_number)
        if type == PaymentMode.UPI:
            length = random.randint(3, 5)
            random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
            upi_id = f"{random.randint(10**9, 10**10 - 1)}@{random_string}" 
            return UPIPayment(upi_id)
        else:
            raise ValueError(f"No payment option available for: {type}")
        
class PaymentManager:
    def __init__(self):
        self.payments = {}
        self._lock = RLock()
     
    def calculate_charge(self, vehicle_type, entry_time):
        cost = PricingPolicy.get_price(vehicle_type)
        duration = time.time() - entry_time
        return cost * duration

    def process_payment(self, ticket_id, payment_type, amount):
        payment = PaymentFactory.get_payment_obj(payment_type)
        payment.pay(amount)
        with self._lock:
            self.payments[ticket_id] = payment
        return payment