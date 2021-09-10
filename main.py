import requests
from datetime import *
import os
import math

TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)
DAY_BEFORE_YESTERDAY = YESTERDAY - timedelta(days=1)
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAV_API_KEY = os.environ["ALPHAV_API_KEY"]
NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]
NEWSAPI_URL = "https://newsapi.org/v2/everything"
ALPHAV_URL = "https://www.alphavantage.co/query"
ALPHAV_PRAM = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAV_API_KEY
}
NEWSAPI_PRAM = {
    "q": "Tesla",
    "from": YESTERDAY,
    "sortBy": "popularity",
    "apiKey": NEWSAPI_KEY
}
percentage = 0
top_five = []
def get_price_percentage():
    global percentage
    r = requests.get(ALPHAV_URL, params=ALPHAV_PRAM)
    data = r.json()
    yesterday_price = data["Time Series (Daily)"][str(YESTERDAY)]["4. close"]
    day_before_yesterday_price = data["Time Series (Daily)"][str(DAY_BEFORE_YESTERDAY)]["4. close"]
    percentage = ((float(yesterday_price) - float(day_before_yesterday_price)) / float(day_before_yesterday_price)) * 100
    if abs(percentage) > 5:
        get_news()

def get_news():
    global top_five
    r = requests.get(NEWSAPI_URL, params=NEWSAPI_PRAM)
    data = r.json()
    top_five = [data["articles"][i]["title"] for i in range(0,5)]
    if percentage > 0:
        print(f"{STOCK} : 🔺{math.floor(percentage)}%")
    else:
        print(f"{STOCK} : 🔻{math.floor(percentage)}%")
    for _ in range(0,5):
        print(top_five[_])

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 






## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
get_price_percentage()

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

