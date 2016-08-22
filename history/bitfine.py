from sqlalchemy import *
import time
import numpy as np
from decimal import Decimal
# using bitfinex APIs to get today's_ticker
from bitfinex.client import Client, TradeClient
client = Client()
trade = TradeClient('K4HJultQmdvroWCnNy5OMcXx7QfGoQgZw0vrkWmuV1Y','dFt4tsMFszh2vTGGvHqFEP3fkaaSniJ4zDA4pSWyJOM')
# we are inporting the Databse that is being created by bitfinex-boat

engine = create_engine('sqlite:////home/metal-machine/Desktop/all_ticker.db')
metadata = MetaData(engine)
tickers = Table('ticker', metadata, autoload=True)



def find_nearest(array,value):
	""" gets the numpy array and timestamp as input and retunrs the nearest value"""
	
	idx = np.abs(array-value).argmin()
	return  array[idx]

def ohlc_past(hours):
	"""This function returns the seconds as input and retrun the required ohlc_4"""
	
	seconds = 3600*hours # converting hours into seconds
	time_delta = float('{:7f}'.format(time.time()-seconds))
	time_stamp = tickers.select(tickers.c.timestamp)
	timestamp_array = np.array([i[1] for i in time_stamp.execute()])
	time_stamp_value = find_nearest(timestamp_array,time_delta)	
	sql_statement = tickers.select(tickers.c.timestamp==time_stamp_value)
	match_list = [i for i in sql_statement.execute()]
	ohlc_delta = match_list[0]
	
     #1469192333.2017772, 660.03, 668.0, 660.0	
	# presently ohlc_delta is returning timedelta[1],lastprice[2],high[3],low[4] ::: now How to get close as well
	#return type(ohlc_delta[2])
	return (ohlc_delta[2]+ohlc_delta[3]+ohlc_delta[4]+ohlc_delta[2])/4.0


def ohlc4_today(symbol_used):

	'''returns open,high,low and close(yet not completed) this function will save in database'''
	
	ticker_data = client.ticker(symbol_used)
	today_data = client.today(symbol_used)
	return (ticker_data['last_price']+ticker_data['high']+ticker_data['low']+ticker_data['last_price'])/4.0


def ticker_last(symbol_used):

	'''returns open,high,low and close(yet not completed) this function will save in database'''
	
	ticker_data = client.ticker(symbol_used)
	today_data = client.today(symbol_used)
	return ticker_data['last_price']


'''
getDiff() =>
yesterday=security(tickerid, timeframe, ohlc4[1])
today=ohlc4
delta=today-yesterday
percentage=delta/yesterday
'''

def auto_order_buy(amount, price):

	order_made = trade.place_order(amount, price, side='buy', ord_type='market', symbol='btcusd', exchange='bitfinex')
	return order_made



def auto_order_sell(amount, price):

	order_made = trade.place_order(amount, price, side='sell', ord_type='market', symbol='btcusd', exchange='bitfinex')
	return order_made

def getDiff(symbol,hours):
	
	delta = ohlc4_today(symbol)-ohlc_past(hours)
	return delta/ohlc_past(hours)


'''
PineActivationFunctionLinear(v) => v
PineActivationFunctionTanh(v) => (exp(v) - exp(-v))/(exp(v) + exp(-v))
l0_0 = PineActivationFunctionLinear(getDiff())
l1_0 = PineActivationFunctionTanh(l0_0*0.8446488687)
'''

def strategy(l0_0):
    l1_0 = np.tanh(l0_0*0.8446488687)

    l1_1 = np.tanh(l0_0*-0.5674069006)
    l1_2 = np.tanh(l0_0*0.8676766445)
    l1_3 = np.tanh(l0_0*0.5200611473)
    l1_4 = np.tanh(l0_0*-0.2215499554)

    l2_0 = np.tanh(l1_0*0.3341657935 + l1_1*-2.0060003664 + l1_2*0.8606354375 +l1_3*0.9184846912 + l1_4*-0.8531172267)
    l2_1 = np.tanh(l1_0*-0.0394076437 + l1_1*-0.4720374911 + l1_2*0.2900968524 +l1_3*1.0653326022 + l1_4*0.3000188806)
    l2_2 = np.tanh(l1_0*-0.559307785 + l1_1*-0.9353655177 + l1_2*1.2133832962 + l1_3*0.1952686024+ l1_4*0.8552068166)
    l2_3 = np.tanh(l1_0*-0.4293220754 + l1_1*0.8484259409 + l1_2*-0.7154087313 +l1_3*0.1102971055 + l1_4*0.2279392724)
    l2_4 = np.tanh(l1_0*0.9111779155 + l1_1*0.2801691115 + l1_2*0.0039982713 + l1_3*-0.5648257117 + l1_4*0.3281705155)


    l2_5 = np.tanh(l1_0*-0.2963954503 + l1_1*0.4046532178 + l1_2*0.2460580977 +l1_3*0.6608675819 + l1_4*-0.8732022547)
    l2_6 = np.tanh(l1_0*0.8810811932 + l1_1*0.6903706878 + l1_2*-0.5953059103 + l1_3*-0.3084040686 + l1_4*-0.4038498853)
    l2_7 = np.tanh(l1_0*-0.5687101164 + l1_1*0.2736758588 + l1_2*-0.2217360382 +l1_3*0.8742950972 + l1_4*0.2997583987)
    l2_8 = np.tanh(l1_0*0.0708459913 + l1_1*0.8221730616 + l1_2*-0.7213265567 + l1_3*-0.3810462836 + l1_4*0.0503867753)
    l2_9 = np.tanh(l1_0*0.4880140595 + l1_1*0.9466627196 + l1_2*1.0163097961 + l1_3*-0.9500386514 + l1_4*-0.6341709382)
    l2_10 = np.tanh(l1_0*1.3402207103 + l1_1*0.0013395288 + l1_2*3.4813009133 + l1_3*-0.8636814677 + l1_4*41.3171047132)
    l2_11 = np.tanh(l1_0*1.2388217292 + l1_1*-0.6520886912 + l1_2*0.3508321737 +l1_3*0.6640560714 + l1_4*1.5936220597)

    l2_12 = np.tanh(l1_0*-0.1800525171 + l1_1*-0.2620989752 + l1_2*0.056675277 + l1_3*-0.5045395315 + l1_4*0.2732553554)
    l2_13 = np.tanh(l1_0*-0.7776331454 + l1_1*0.1895231137 + l1_2*0.5384918862 +l1_3*0.093711904 + l1_4*-0.3725627758)
    l2_14 = np.tanh(l1_0*-0.3181583022 + l1_1*0.2467979854 + l1_2*0.4341718676 + l1_3*-0.7277619935 + l1_4*0.1799381758)
    l2_15 = np.tanh(l1_0*-0.5558227731 + l1_1*0.3666152536 + l1_2*0.1538243225 + l1_3*-0.8915928174 + l1_4*-0.7659355684)
    l2_16 = np.tanh(l1_0*0.6111516061 + l1_1*-0.5459495224 + l1_2*-0.5724238425 + l1_3*-0.8553500765 + l1_4*-0.8696190472)
    l2_17 = np.tanh(l1_0*0.6843667454 + l1_1*0.408652181 + l1_2*-0.8830470112 + l1_3*-0.8602324935 + l1_4*0.1135462621)
    l2_18 = np.tanh(l1_0*-0.1569048216 + l1_1*-1.4643247888 + l1_2*0.5557152813 +l1_3*1.0482791924 + l1_4*1.4523116833)
    l2_19 = np.tanh(l1_0*0.5207514017 + l1_1*-0.2734444192 + l1_2*-0.3328660936 + l1_3*-0.7941515963 + l1_4*-0.3536051491)
    l2_20 = np.tanh(l1_0*-0.4097807954 + l1_1*0.3198619826 + l1_2*0.461681627 + l1_3*-0.1135575498 + l1_4*0.7103339851)
    l2_21 = np.tanh(l1_0*-0.8725014237 + l1_1*-1.0312091401 + l1_2*0.2267643037 + l1_3*-0.6814258121 + l1_4*0.7524828703)
    l2_22 = np.tanh(l1_0*-0.3986855003 + l1_1*0.4962556631 + l1_2*-0.7330224516 +l1_3*0.7355772164 + l1_4*0.3180141739)
    l2_23 = np.tanh(l1_0*-1.083080442 + l1_1*1.8752543187 + l1_2*0.3623326265 + l1_3*-0.348145191+ l1_4*0.1977935038)
    l2_24 = np.tanh(l1_0*-0.0291290625 + l1_1*0.0612906199 + l1_2*0.1219696687 + l1_3*-1.0273685429 + l1_4*0.0872219768)
    l2_25 = np.tanh(l1_0*0.931791094 + l1_1*-0.313753684 + l1_2*-0.3028724837 + l1_3*0.7387076712+ l1_4*0.3806140391)
    l2_26 = np.tanh(l1_0*0.2630619402 + l1_1*-1.9827996702 + l1_2*-0.7741413496 +l1_3*0.1262957444 + l1_4*0.2248777886)


    l2_27 = np.tanh(l1_0*-0.2666322362 + l1_1*-1.124654664 + l1_2*0.7288282621 + l1_3*-0.1384289204 + l1_4*0.2395966188)
    l2_28 = np.tanh(l1_0*0.6611845175 + l1_1*0.0466048937 + l1_2*-0.1980999993 +l1_3*0.8152350927 + l1_4*0.0032723211)
    l2_29 = np.tanh(l1_0*-0.3150344751 + l1_1*0.1391754608 + l1_2*0.5462816249 + l1_3*-0.7952302364 + l1_4*-0.7520712378)
    l2_30 = np.tanh(l1_0*-0.0576916066 + l1_1*0.3678415302 + l1_2*0.6802537378 +l1_3*1.1437036331 + l1_4*-0.8637405666)
    l2_31 = np.tanh(l1_0*0.7016273068 + l1_1*0.3978601709 + l1_2*0.3157049654 + l1_3*-0.2528455662 + l1_4*-0.8614146703)
    l2_32 = np.tanh(l1_0*1.1741126834 + l1_1*-1.4046408959 + l1_2*1.2914477803 +l1_3*0.9904052964 + l1_4*-0.6980155826)

    l3_0 = np.tanh(l2_0*-0.1366382003 + l2_1*0.8161960822 + l2_2*-0.9458773183 + \
    l2_3*0.4692969576 + l2_4*0.0126710629 + l2_5*-0.0403001012 + l2_6*-0.0116244898 + l2_7*-0.4874816289 + l2_8*\
      -0.6392241448 + l2_9*-0.410338398 + l2_10*-0.1181027081 + l2_11*0.1075562037 + l2_12*-0.5948728252 \
      +l2_13*0.5593677345 + l2_14*-0.3642935247 + l2_15*-0.2867603217 + l2_16*0.142250271 + l2_17*-0.0535698019 \
      +l2_18*-0.034007685 + l2_19*-0.3594532426 + l2_20*0.2551095195 + l2_21*0.4214344983 + l2_22*0.8941621336 \
      +l2_23*0.6283377368 + l2_24*-0.7138020667 + l2_25*-0.1426738249 + l2_26*0.172671223 + l2_27*0.0714824385 \
      +l2_28*-0.3268182144 + l2_29*-0.0078989755 + l2_30*-0.2032828145 + l2_31*-0.0260631534 + l2_32*0.4918037012)
    return l3_0              
      

'''   
   # print(value)  # for testing
    if state(value):
        print("changing state")
        state = TABLE[state] 

  ''' 
# if I make function execution set false after one execution 
   
'''                    
    if(l3_0>0):
		#do whatever you did a candlestick ago? how to sort out this one?
                print l3_0
            elif(l3_0<0):
                print l3_0
            else:
                pass
                
        except KeyboardInterrupt:
            raise
            exit()
   '''
#while True:
 #   print main_call().next()
'''        
if(l3_0>0):
		#do whatever you did a candlestick ago? how to sort out this one?
   print l3_0
   print auto_order_buy('0.01',str(ticker_last('btcusd')))
elif(l3_0<0):
    print l3_0
    print auto_order_sell('0.01',str(ticker_last('btcusd')))
else:
    pass
    
main_call()
   '''
    
'''
l3_0

def auto_order(amount, price):
    
If l3_0 is more than 0, try to buy
If l3_0 is less than 0, try to sell
if l3_0 is neither (in other words, it is 0), 

'''
