import botogram
from datetime import datetime
import requests

TOKEN = "REPLACE WITH YOUR TOKEN"
URL = "https://api.coinmarketcap.com/v2/ticker/"


bot = botogram.create( TOKEN )

def getCoinPriceDict():
    coindct = {}
    
    resp = requests.get(URL)
    data_dct = resp.json() # util to conver the resp object into pythondict
    
    for key in data_dct["data"]:
        name = data_dct["data"][key]["name"]
        price = data_dct["data"][key]["quotes"]["USD"]["price"]
        coindct [ name.lower() ] = price
    return coindct


@bot.command("hello")
def hello_command(chat, message, args):
    chat.send("Hello world" + str(datetime.now()))

global_coin_dct = getCoinPriceDict()

@bot.command("listcoins")
def hello_command(chat, message, args):
    """ To list all the available coins
    """
    resp = " , ".join( list(global_coin_dct.keys())[:10]  )
    chat.send ( resp  )


@bot.command("price")
def price(chat, message, args):
    
    if len(args) == 0:
        resp = """Usage /price <coinname>
        /price litecoin bitcoin
        /price litecoin
        """
        chat.send(resp)

    else:
        
        coindct = getCoinPriceDict()

        for coinname in args:
            price = coindct.get(coinname.lower())
            if price:
                resp = f"The price of {coinname} is {price}"
            else:
                resp = f"The coinname {coinname} is not found"
            chat.send(resp)
    

if __name__ == "__main__":
    bot.run()