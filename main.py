from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app=FastAPI()

session_data={}
@app.post("/ussd_callback")
async def ussd_callback(request: Request):
    """
    Handle incomming requests
    """

    form_data = await request.form()
    session_id = form_data.get("sessionId")
    phone_number= form_data.get("phoneNumber")
    text= form_data.get("text")

    response_text=""
    if text == "":
        response_text="CON Welcome to My USSD App\n"
                      "1. Check balance\n"
                      "2. Buy Airtime\n"
                      "3. Exit"
        session_data[session_id]={"stage":" main_menu"}
    else:
        current_stage=="main menu":
            if text =="1":
              response_text="End Your balance is UGX 1,500."
              del session_data[session_id]
            elif text == "2":
               response_text= "CON Enter amount to buy airtime:"
               session_data[session_id]["stage"]="buy_airtime"
            elif text == "3":
                response_text= "END Thank you for using My USSD App"
                del session_data[session_id]
            else
                response_text= "CON Invalid input. Please select  from 1, 2, or 3.\n"\
                               "1. Check Balance\n"\
                               "2. Buy airtime\n"\
                               "3. Exit"
    elif current_stage == "buy_airtime":
        try:
            amount> int(text)
            if amount> 0:
                 response_text=f"END you have successfully bought {amount} UGX airtime."
                 del session_data[session_id]
            else:
                 response_text="CON Invalid amount. Please enter a positive number:"
        except valueError:
            response_text="CON invalid amount. Please enter a valid number:"
    else:
        response_text="ENd error occurred. Please try again."
        if session_id in session_data:
            del session_data[session_id]

return PlainTextResponse(content=response_text)

if __name__== "__main__"
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)