"""
This code helps one to track the current exchange rates, cryptocurrencies and the current value of NFTs by sending them as whatsapp messages.

The code retrieves cryptocurrency data from CoinGeckoAPI, NFT data from CoinGeckoAPI, and exchange rates from altin.in. 
It then sends a WhatsApp message containing today's exchange rates, cryptocurrency prices, and NFT information using the pywhatkit library.

In order to automate, Schedule a task from Task Scheduler in Windows.

Note:
- Ensure necessary libraries are installed by running 'pip install [package]' if required.
- Make sure to replace the phone number and name variables with the appropriate values before running the script.
- The script uses APIs to retrieve cryptocurrency and NFT data, and web scraping to get exchange rates. Ensure stable internet connectivity for successful execution.

@author: canbo
"""
#import necessary libraries, if it doesn't work, you may don't have the packages, pip install [package]
import pywhatkit as kit
import requests
from bs4 import BeautifulSoup
import sys

#Retrieving CryptoCurrency Data from CoinGeckoApi
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {
        'ids': 'bitcoin,ethereum,binancecoin',
        'vs_currencies': 'USD',
        'include_24hr_change': 'true'
}
response = requests.get(url, params = params)
if response.status_code == 200:
    watchlist = response.json()
    # print(watchlist)

else:
    print(f"Failed to retrieve data from the API, \nStatus: {response.status_code}")
    sys.exit()

#Retrieving CryptoCurrency Data from CoinGeckoApi
nfts = ['bored-ape-yacht-club','azuki','degods']
url = 'https://api.coingecko.com/api/v3/nfts/'
nftList = {}
for nft in nfts:
    
    response = requests.get(url+nft)
    if response.status_code == 200:
        
        nftData = response.json()
        info = {key: nftData[key] for key in nftData.keys()
                & {'name', 'floor_price','volume_24h'}}
        nftList[nft] = info
    else:
        print(f"Failed to retrieve data from the API, \nStatus: {response.status_code}")
        sys.exit()
# print(nftList)

#Scraping Exchange Rates from altin.in using BeautifulSoup
response = requests.get("https://altin.in/")

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    USDTRY = soup.find(id="dfiy").get_text()
    EURTRY = soup.find(id="efiy").get_text()
    AUUSD = soup.find(id="ofiy").get_text()
else:
    print(f"Failed to retrieve data from the API, \nStatus: {response.status_code}")
    sys.exit()


coinSummary =""
for coin,price in watchlist.items():
    coinSummary += f"\t{coin.upper()}: {price['usd']}$ {'{:.2f}'.format(price['usd_24h_change'])}%\n"

nftSummary = ""
for nft in nftList.values():
    nftSummary += f"\t{nft['name']} is trading at {nft['floor_price']['native_currency']}E today.\n"

#Send WhatsApp messages using pywhatkit
# Specify the phone number (with country code) and the message
phoneNumber = "+123456789"
yourName = "Canbo"
message = (f"Good Morning, {yourName}.\nHere are the today's exchange rates:\n\tUSD: {USDTRY}₺\n\tEUR: {EURTRY}₺\n\tGold per Ounce: {AUUSD}$ \n\nHere are the cryptocurrencies in your watchlist:\n"+coinSummary+"\nYour NFT watchlist:\n"+nftSummary)

# Send the message instantly
try:
    kit.sendwhatmsg_instantly(phoneNumber, message,30,tab_close=True)
except Exception as e:
    print(e)

