import requests
import smtplib
import os
from email.mime.text import MIMEText
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
USEREMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD") 
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_KEY = "L5TSOTC6XQ7IOE9V"
NEWS_KEY = "aa46588b39764a19bb447404f3f148bc"
stock_properties = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY,
}

stack_api_response = requests.get(STOCK_ENDPOINT, params=stock_properties)
stack_api_response.raise_for_status()
stack_daily_data = stack_api_response.json()["Time Series (Daily)"]
daily_closing = [value["4. close"] for key, value in stack_daily_data.items()]

difference = float(daily_closing[0])-float(daily_closing[1])
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

difference_percentage = round((difference/float(daily_closing[0]))*100)

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_KEY
}
news_api_response = requests.get(NEWS_ENDPOINT, params=news_params)
news_api_response.raise_for_status()
latest_news = news_api_response.json()["articles"]

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint:
#  https://stackoverflow.com/questions/509211/understanding-slice-notation
if abs(difference_percentage) > 5:
    important_news = latest_news[:3]
    print("Before the email")
    with smtplib.SMTP('smtp.gmail.com', 587) as message:
        print("Before the start")
        message.starttls()
        print("login part")
        message.login(user=USEREMAIL, password=PASSWORD)
        print("In prose of sending")
        for mail in important_news:
            body = f"Brief: {mail['description']}"
            msg = MIMEText(body, 'plain')
            msg["Subject"] = f"{up_down}{difference_percentage}% Headline: {mail['title']}"
            message.sendmail(USEREMAIL, USEREMAIL, msg.as_string())


