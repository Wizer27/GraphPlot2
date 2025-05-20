import streamlit as st
import stripe
from urllib.parse import parse_qs, urlparse



#st.title("Buy a preimium subcription and user some more functions")
#Public_key = 'public_key'
stripe.api_key = 'i hate sasha mishin'
def create_session(amount,currency='usd'):
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=stripe.api_key,  # Тестовый токен (можно заменить на реальный)
            description="Платеж через Python"
        )
        return charge
    except stripe.error.StripeError as e:
        st.error(f"Error {e}")


st.title('Buy premium subcription')
def test():
    s = {}
    return hash(s)
st.button('Confirm',on_click=test)

### Make a pay page 