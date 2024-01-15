

import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

msg_api = "AC389a3929d93487c15bdcff78076147c4"
msg_api_auth = "367bb9b59da1469a119ee7b75bfed569"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
alpha_vintage_api = "OJT3HDCXPCX42EFV"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alpha_vintage_api
}

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api = "667382b07c064e59910fd565a97c5cca"
news_params = {
    "apikey": news_api,
    "qInTitle": COMPANY_NAME,
}

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
.00
stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)  # getting stock response
stock_response.raise_for_status()

data = stock_response.json()["Time Series (Daily)"]

stock_data_list = [value for (key, value) in data.items()]  # converted dictionary to list that only contains value not key
print(stock_data_list)

# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
yesterday_data = stock_data_list[0]  # got yesterdays data
yesterday_closing_prise = yesterday_data["4. close"]  # got yesterdays closing prise
print(yesterday_closing_prise)

day_before_yesterday = stock_data_list[1]  # got day before yesterday stock data
day_before_yesterday_closing_prise = day_before_yesterday["4. close"]  # got day before yesterday closing price
print(day_before_yesterday_closing_prise)

# difference = abs(float(yesterday_closing_prise) - float(day_before_yesterday_closing_prise))  # abs only returns actual value not sign
difference = float(yesterday_closing_prise) - float(day_before_yesterday_closing_prise)

#HINT 2: Work out the value of 5% of yerstday's closing stock price.
diff_percent = round((difference / float(yesterday_closing_prise)) * 100)  # got percentage
print(diff_percent)

if diff_percent >= 5:  # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    ## STEP 2: Use https://newsapi.org/docs/endpoints/everything
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_articles = news_response.json()["articles"]
    # Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
    # HINT 1: Think about using the Python Slice Operator
    articles = news_articles[:3]
    print("greater than 4")

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number.
    # HINT 1: Consider using a List Comprehension.
    up_down = ""
    if difference > 0:
        up_down = "🔺"
        msg = [f"{STOCK}{up_down}{diff_percent}%\nHeadline: {article['title']}\nBrief: {article['description']}" for
               article in articles]

        client = Client(msg_api, msg_api_auth)

        for m in msg:
            message = client.messages.create(
                body=f"{m}\n informed by: prathamesh",
                to="+917385348373",
                from_="+19362431129"
            )

            print(message.sid)
    else:
        up_down = "🔻"
        msg = [f"{STOCK}{up_down}{diff_percent}%\nHeadline: {article['title']}\nBrief: {article['description']}" for
               article in articles]

        client = Client(msg_api, msg_api_auth)

        for m in msg:
            message = client.messages \
                .create(
                from_="+19362431129",
                to="+917385348373",
                body=f"{m}\n informed by: prathamesh"

            )
            print(message.sid)



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

