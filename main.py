import requests
from datetime import *
import os
import math

TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)
DAY_BEFORE_YESTERDAY = YESTERDAY - timedelta(days=1)
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
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
    "qInTitle": COMPANY_NAME,
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

get_price_percentage()