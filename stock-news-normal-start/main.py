import requests
import smtplib
from email.mime.text import MIMEText
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
USEREMAIL = "torayevaziz1@gmail.com"
PASSWORD = "home.2020"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_KEY = "L5TSOTC6XQ7IOE9V"
NEWS_KEY = "aa46588b39764a19bb447404f3f148bc"
stock_properties = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY,
}
# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
#  e.g. [new_value for (key, value) in dictionary.items()]
stack_api_response = requests.get(STOCK_ENDPOINT, params=stock_properties)
stack_api_response.raise_for_status()
stack_daily_data = stack_api_response.json()["Time Series (Daily)"]
daily_closing = [value["4. close"] for key, value in stack_daily_data.items()]
# TODO 2. - Get the day before yesterday's closing stock price
# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#  Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(daily_closing[0])-float(daily_closing[1])
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day
#  before yesterday.
# last_day_percent = float(daily_closing[0]) / float(daily_closing[0]) + float(daily_closing[1]) * 100
# day_before_percent = float(daily_closing[1]) / float(daily_closing[0]) + float(daily_closing[1]) * 100

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
difference_percentage = round((difference/float(daily_closing[0]))*100)

# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
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

# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""TSLA: 🔺2% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey have 
gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 
or 
"TSLA: 🔻5% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey have 
gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 
"""
