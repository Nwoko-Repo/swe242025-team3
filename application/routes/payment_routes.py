from flask import Blueprint, request
from application.models import Customer, Payment, db
from application.utils import ResponseHelper  # Import the helper class
import uuid
import os
import stripe

# Load Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/checkout', methods=['POST'])
def create_checkout_session():
    """
    Create a Stripe Checkout session for one-time payments.
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["customer_id", "email", "name", "order_id", "amount", "success_url", "cancel_url"]
        if not all(field in data for field in required_fields):
            return ResponseHelper.default_response("Missing required fields", 400)

        # Check if the customer already exists in the database
        customer = Customer.query.filter_by(customer_id=data["customer_id"]).first()
        if not customer:
            # Create a new Stripe customer
            stripe_customer = stripe.Customer.create(
                email=data["email"],
                name=data["name"]
            )

            # Save the customer in the database
            customer = Customer(
                customer_id=data["customer_id"],
                stripe_customer_id=stripe_customer.id,
                email=data["email"],
                name=data["name"]
            )
            db.session.add(customer)
            db.session.commit()

        # Generate a unique payment ID
        payment_id = str(uuid.uuid4())

        # Create Stripe Checkout session with expanded payment intent
        session = stripe.checkout.Session.create(
            customer=customer.stripe_customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": f"Order {data['order_id']}"},
                    "unit_amount": int(data["amount"] * 100)  # Convert to cents
                },
                "quantity": 1
            }],
            mode="payment",
            success_url=data["success_url"],
            cancel_url=data["cancel_url"],
            # expand=["payment_intent"]  # Expand the payment intent
        )

        # Debugging: Print the session object
        print("Stripe Checkout Session:", session)

          # Use `session.id` as the stripe_payment_id since payment_intent is not present
        stripe_payment_id = session.id  # Use session.id as the unique identifier

        # Fallback: If payment_intent is None, explicitly retrieve it
        if not stripe_payment_id:
            # Attempt to retrieve the Payment Intent directly
            if session.id:
                session_details = stripe.checkout.Session.retrieve(session.id)
                stripe_payment_id = session_details.payment_intent
            else:
                raise Exception("Stripe session does not contain payment_intent.")

        # Save payment details in the database
        payment = Payment(
            id=payment_id,
            customer_id=customer.customer_id,
            stripe_payment_id=stripe_payment_id,
            stripe_session_id=session.id,
            order_id=data["order_id"],
            amount=data["amount"],
            status="pending"
        )
        db.session.add(payment)
        db.session.commit()

        return ResponseHelper.default_response(
            "Checkout session created successfully",
            200,
            {"checkout_url": session.url}
        )

    except Exception as e:
        return ResponseHelper.default_response(f"Error: {str(e)}", 500)
