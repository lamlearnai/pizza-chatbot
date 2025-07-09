import os
import requests
import streamlit as st
from dotenv import load_dotenv

# —————————————————————————————————————————————————————
# 1. Load AI21 key and define the system prompt
# —————————————————————————————————————————————————————
load_dotenv()
API_KEY = os.getenv("AI21_API_KEY")
if not API_KEY:
    st.error("Missing AI21_API_KEY in .env")
    st.stop()

SYSTEM_MESSAGE = {
    "role": "system",
    "content": """
You are PizzaBot, a friendly pizza-ordering assistant who can speak Malay, English, or any mix of both (Manglish!). 
When the user types in Malay, reply in Malay; when they type in English, reply in English; when they mix, match their style.

Menu:
 • pepperoni pizza — Large $12.95 / Medium $10.00 / Small $7.00
 • cheese pizza   — Large $10.95 / Medium $9.25 / Small $6.50
 • eggplant pizza — Large $11.95 / Medium $9.75 / Small $6.75
 • fries — Large $4.50 / Small $3.50
 • greek salad — $7.25

Toppings:
 • extra cheese — $2.00
 • mushrooms    — $1.50
 • sausage      — $3.00
 • canadian bacon — $3.50
 • AI sauce     — $1.50
 • peppers      — $1.00

Drinks:
 • coke — Large $3.00 / Medium $2.00 / Small $1.00
 • sprite — Large $3.00 / Medium $2.00 / Small $1.00
 • bottled water — $5.00

Flow:
1) Greet the customer.
2) Collect the entire order (items, sizes, toppings, extras).
3) Ask pickup vs delivery; if delivery, ask for address.
4) Summarize the order and ask if anything else.
5) Collect payment.

Always clarify all options, extras, and sizes so the menu items are uniquely identified. Keep your style short, conversational, and friendly.
"""
}

# —————————————————————————————————————————————————————
# 2. AI21 chat-call helper
# —————————————————————————————————————————————————————
def query_ai21(messages):
    url = "https://api.ai21.com/studio/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jamba-large",
        "messages": messages,
        "maxTokens": 80,
        "temperature": 0.7
    }
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

# —————————————————————————————————————————————————————
# 3. Streamlit page config
# —————————————————————————————————————————————————————
st.set_page_config(page_title="🍕 PizzaBot made by Lam", layout="wide")
st.title("🍕 PizzaBot made by Lam")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = [SYSTEM_MESSAGE]

# —————————————————————————————————————————————————————
# 4. Render chat messages
# —————————————————————————————————————————————————————
for msg in st.session_state.history[1:]:  # skip system
    st.chat_message(msg["role"]).write(msg["content"])

# —————————————————————————————————————————————————————
# 5. Capture user input
# —————————————————————————————————————————————————————
if user_input := st.chat_input("Type your message…"):
    st.session_state.history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # get bot reply
    bot_reply = query_ai21(st.session_state.history)
    st.session_state.history.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
