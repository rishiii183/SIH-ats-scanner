import sys
import os
import hmac
import hashlib
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.routers.payments import (
    verify_razorpay_signature, 
    verify_webhook_signature,
    RAZORPAY_KEY_SECRET,
    RAZORPAY_WEBHOOK_SECRET
)

def test_payments_pipeline():
    client = TestClient(app)
    test_email = "sih_test_user_payments@example.com"

    print("==================================================")
    print("      RAZORPAY PAYMENTS END-TO-END AUDIT          ")
    print("==================================================")

    # 1. Test POST /api/v1/payments/create-order
    create_res = client.post(
        "/api/v1/payments/create-order",
        json={"amount_in_rupees": 99.0, "user_email": test_email, "currency": "INR"}
    )
    print("1. Create Order Response Code:", create_res.status_code)
    order_data = create_res.json()
    print("   Order Data:", order_data)

    assert create_res.status_code == 200
    assert order_data["amount"] == 9900
    order_id = order_data["order_id"]

    # 2. Test HMAC Signature Verification Logic
    payment_id = "pay_test_sih2026_999"
    msg = f"{order_id}|{payment_id}".encode("utf-8")
    valid_sig = hmac.new(RAZORPAY_KEY_SECRET.encode("utf-8"), msg, hashlib.sha256).hexdigest()

    is_sig_valid = verify_razorpay_signature(order_id, payment_id, valid_sig, RAZORPAY_KEY_SECRET)
    print(f"\n2. HMAC Signature Verification: {is_sig_valid}")
    assert is_sig_valid is True

    # 3. Test POST /api/v1/payments/verify-payment
    verify_res = client.post(
        "/api/v1/payments/verify-payment",
        json={
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": valid_sig,
            "user_email": test_email
        }
    )
    print("\n3. Verify Payment API Response Code:", verify_res.status_code)
    print("   Verify Payload:", verify_res.json())
    assert verify_res.status_code == 200

    # 4. Test POST /api/v1/payments/webhook
    webhook_payload = {
        "event": "payment.captured",
        "payload": {
            "payment": {
                "entity": {
                    "id": payment_id,
                    "order_id": order_id,
                    "amount": 9900,
                    "status": "captured",
                    "email": test_email,
                    "notes": {"user_email": test_email}
                }
            }
        }
    }

    body_bytes = json.dumps(webhook_payload).encode("utf-8")
    webhook_sig = hmac.new(RAZORPAY_WEBHOOK_SECRET.encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()

    webhook_res = client.post(
        "/api/v1/payments/webhook",
        content=body_bytes,
        headers={"Content-Type": "application/json", "X-Razorpay-Signature": webhook_sig}
    )
    print("\n4. Webhook API Response Code:", webhook_res.status_code)
    print("   Webhook Payload:", webhook_res.json())
    assert webhook_res.status_code == 200

if __name__ == "__main__":
    test_payments_pipeline()
