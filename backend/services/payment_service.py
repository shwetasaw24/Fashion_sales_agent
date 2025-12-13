import razorpay
import os

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = razorpay.Client(auth=(key_id, key_secret))

def create_order(amount_in_rupees: float):
    amount_paise = int(amount_in_rupees * 100)

    order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    return order  # contains id, amount, currency, status
