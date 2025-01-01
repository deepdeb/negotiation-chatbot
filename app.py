from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Predefined starting price for the product
starting_price = 100
current_price = starting_price

# List of responses that the bot can use during the negotiation
responses = {
    "greeting": ["Hi! I'm your price negotiator bot.", "Hello! Let's negotiate a price!", "Hi there! Ready to haggle?"],
    "price_offer": ["That sounds good, but how about a price of ${}?".format(current_price)],
    "counter_offer": ["Hmm, I can go down to ${}, but that’s my final offer.".format(current_price - random.randint(5, 10))],
    "final_offer": ["Great! You've got the deal at ${}. Have a good day!".format(current_price)],
    "rejected_offer": ["I'm afraid I can't go that low. How about a new price of ${}?".format(current_price - random.randint(10, 20))],
    "negotiation_end": ["It seems like we’ve reached a deal. Would you like to continue?", "The negotiation is over. Thank you for your time!"],
    "price_too_low": ["Sorry, but I can't go that low. How about we consider a price of ${}?".format(current_price)],
    "price_middle_ground": ["How about a price of ${}?".format(random.randint(70, 80))],
    "ask_for_offer": ["Please provide your offer, and let's see if we can make a deal."]
}

# Global conversation history (user and bot messages)
conversation_history = []

def process_user_input(user_input):
    global current_price

    # Normalize the input to lowercase to make it case-insensitive
    user_input = user_input.lower().strip()  # Remove any extra spaces
    
    # Check if the input contains a price (number)
    if any(char.isdigit() for char in user_input):
        # Extract the first number from the input
        numbers = [int(word) for word in user_input.split() if word.isdigit()]
        offer = numbers[0]
        
        if offer < 60:
            bot_response = random.choice(responses["price_too_low"])
        elif 60 <= offer < 80:
            bot_response = random.choice(responses["price_middle_ground"])
        elif offer >= 80:
            current_price = offer  # Update the current price if the user offers higher than or equal to 80
            bot_response = random.choice(responses["final_offer"])
    elif "accept" in user_input.lower() or "deal" in user_input.lower() or "great" in user_input.lower() or "agree" in user_input.lower():
        bot_response = "Great! We have a deal."
    elif "no" in user_input.lower() or "reject" in user_input.lower():
        # Reject the offer and try a lower price
        current_price -= random.randint(10, 20)
        bot_response = random.choice(responses["rejected_offer"])
    elif "end" in user_input.lower() or "quit" in user_input.lower():
        bot_response = random.choice(responses["negotiation_end"])
    else:
        bot_response = random.choice(responses["ask_for_offer"])

    # Append the user input and bot response to the conversation history
    conversation_history.append({"user": user_input, "bot": bot_response})

    return bot_response

@app.route("/", methods=["GET", "POST"])
def home():
    global conversation_history

    if request.method == "GET":
        conversation_history = []

    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = process_user_input(user_input)
        return render_template("index.html", conversation_history=conversation_history)

    if not conversation_history:
        greeting_message = random.choice(responses["greeting"])
        conversation_history.append({"bot": greeting_message})

    return render_template("index.html", conversation_history=conversation_history)

if __name__ == "__main__":
    app.run(debug=True)
