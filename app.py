import os
import requests
from dotenv import load_dotenv

# 1. Load your AI21 key
load_dotenv()
API_KEY = os.getenv("AI21_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing AI21_API_KEY in your environment")

# 2. Define the system prompt with menu + behavior
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """
You are PizzaBot, an automated service to collect orders for a pizza restaurant. 
You first greet the customer, then collect the order, 
and then ask if it's a pickup or delivery. 
You wait to collect the entire order, then summarize it and check one final 
time if the customer wants to add anything else. 
If it's a delivery, you ask for an address. 
Finally you collect the payment.
Make sure to clarify all options, extras and sizes to uniquely 
identify the item from the menu.
You respond in a short, very conversational friendly style.
The menu includes:
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
"""
}
def pizza_chatbot_ai21(user_message, history=None):
    history = history or []
    # 3. Build the full messages array
    messages = [SYSTEM_MESSAGE]
    for role, msg in history:
        messages.append({"role": role.lower(), "content": msg})
    messages.append({"role": "user", "content": user_message})

    # 4. Call the Chat API
    url = "https://api.ai21.com/studio/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jamba-large",       # or "jamba-mini" for a smaller model
        "messages": messages,
        "maxTokens": 60,
        "temperature": 0.7
    }
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    data = r.json()

    # 5. Extract the assistant’s reply
    reply = data["choices"][0]["message"]["content"].strip()

    # 6. Update history and return
    history.append(("User", user_message))
    history.append(("Assistant", reply))
    return reply, history

if __name__ == "__main__":
    conversation = []
    print("🍕 Pizzabot (AI21 Chat API) — type 'exit' or 'quit' to stop")
    while True:
        user = input("You: ")
        if user.lower() in ("exit", "quit"):
            break
        bot_reply, conversation = pizza_chatbot_ai21(user, conversation)
        print("Bot:", bot_reply)
