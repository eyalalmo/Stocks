import yfinance as yf
import urllib3


def nosigns(s):
    return "." not in s and "$" not in s


http = urllib3.PoolManager()
lines = str(http.request('GET', "http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt").data).split("\"")[1].split("\\n")

stocks = [line.split("|")[1] for line in lines if len(line) > 1][1:-1]
stocks = [stock for stock in stocks if nosigns(stock)]

stocks = [[stock, yf.Ticker(stock).history(period="6mo")] for stock in stocks[1:20]]

res = [[stock[0], max(stock[1].Close.array), min(stock[1].Close.array)] for stock in stocks if (max(stock[1].Close.array) > 2*min(stock[1].Close.array))]
f = open("result.txt", "w+")
for stock in res:
    f.write(str(stock) + '\n')
f.close()
