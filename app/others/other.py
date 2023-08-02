from ..dependencies import *
import httpx
# import these 3 for email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# for SMS
# from twilio.rest import Client

# for otp
# import pyotp

import json

router = APIRouter(
    tags=['Other']
)

# for sms & otp
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

# for push notification
FCM_SERVER_KEY = "your_server_key"


@router.get("/geolocation/{address}")
async def geolocation(address: str):
    # Make a GET request to the Nominatim API
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://nominatim.openstreetmap.org/search?format=json&q={address}")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract latitude and longitude from the API response
        if len(data) > 0:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])

            return {"latitude": latitude, "longitude": longitude}
        else:
            return {"error": "No results found for the given address."}
    else:
        return {"error": "Failed to retrieve geolocation data."}
    
@router.post("/send-email")
async def send_email(payload: schemas.Email):

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = payload.sender_email
    message["To"] = payload.recipient_email
    message["Subject"] = payload.subject

    # Attach the email body as plain text
    message.attach(MIMEText(payload.body, "plain"))

    try:
        # Connect to the SMTP server (for Gmail, use port 587)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Enable TLS encryption
            server.login(payload.sender_email, payload.sender_password)
            server.send_message(message)

        return {"message": "Email sent successfully."}
    except Exception as e:
        return {"error": f"Failed to send email. Error: {str(e)}"}
    
@router.post("/send-otp")
async def send_sms(phone_number: str, message: str):
    client = ""
    otp = ""

    # Generate OTP
    # otp = pyotp.TOTP(pyotp.random_base32()).now()  # need to install pyotp, tht's why commented it

    # Send OTP via SMS
    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = f"Your OTP is: {otp}"
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return {"message": "SMS sent successfully."}
    except Exception as e:
        return {"error": f"Failed to send SMS. Error: {str(e)}"}
    

@router.post("/push-notification")
async def send_push_notification(device_token: str, message: str):
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={FCM_SERVER_KEY}"
    }
    payload = {
        "to": device_token,
        "notification": {
            "title": "New Notification",
            "body": message
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return {"message": "Push notification sent successfully."}
        else:
            return {"error": "Failed to send push notification."}
    except Exception as e:
        return {"error": f"Failed to send push notification. Error: {str(e)}"}
    
