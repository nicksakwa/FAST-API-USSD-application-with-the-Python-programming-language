from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

# A simple dictionary to simulate session state (for demonstration purposes only).
# In a real app, you'd use a database (Redis, PostgreSQL, etc.) to store session data.
session_data = {}

@app.post("/ussd_callback")
async def ussd_callback(request: Request):
    """
    Handles incoming USSD requests from the USSD gateway.
    """
    # Parse the incoming form data (USSD gateways often send data as x-www-form-urlencoded)
    form_data = await request.form()
    
    session_id = form_data.get("sessionId")
    phone_number = form_data.get("phoneNumber")
    text = form_data.get("text") # This contains the user's input or is empty/default for initial request

    response_text = ""

    # USSD logic
    if text == "":
        # Initial request: Display main menu
        response_text = "CON Welcome to My USSD App\n" \
                        "1. Check Balance\n" \
                        "2. Buy Airtime\n" \
                        "3. Exit"
        session_data[session_id] = {"stage": "main_menu"}
    else:
        # Subsequent requests based on user input
        current_stage = session_data.get(session_id, {}).get("stage")

        if current_stage == "main_menu":
            if text == "1":
                response_text = "END Your balance is KES 1,500."
                del session_data[session_id] # End session, clear data
            elif text == "2":
                response_text = "CON Enter amount to buy airtime:"
                session_data[session_id]["stage"] = "buy_airtime"
            elif text == "3":
                response_text = "END Thank you for using My USSD App."
                del session_data[session_id]
            else:
                response_text = "CON Invalid input. Please select from 1, 2, or 3.\n" \
                                "1. Check Balance\n" \
                                "2. Buy Airtime\n" \
                                "3. Exit"
        elif current_stage == "buy_airtime":
            try:
                amount = int(text)
                if amount > 0:
                    response_text = f"END You have successfully bought {amount} KES airtime."
                    del session_data[session_id]
                else:
                    response_text = "CON Invalid amount. Please enter a positive number:"
            except ValueError:
                response_text = "CON Invalid amount. Please enter a valid number:"
        else:
            # Fallback for unexpected session state
            response_text = "END An error occurred. Please try again."
            if session_id in session_data:
                del session_data[session_id]

    # USSD responses must be plain text
    return PlainTextResponse(content=response_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)