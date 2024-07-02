import math

from numpy import average

from bot import klinesCoin

# from mainBot import *

# 09.04.2022
# print(math.isclose(13.6, 15.9, abs_tol = 2))
# print(math.ceil(44545.1))
# print((40570.74 * 0.5)/100)

def destek_direnc():
    coin = klinesCoin("BTCUSDT","4h",200)
    close = coin["close"] 
    time = coin["close_time"]
    direncList = []
    destekList= []
    direnc = 0
    destek = 0
    count = 0
    for x in close:
        aroundPrice = math.isclose(x, close[len(close)-1], abs_tol= (close[len(close)-1] * 10)/100)
        if aroundPrice:
            if x > close[len(close)-1]:
                direncList.append(x)
            else:
                destekList.append(x)
            # calcTime = mn.calculate_time(time[count])   
            # print(calcTime, x) 
        count+=1


    for i in direncList:
        direnc += i 
    print("DIRENC: ", direnc/len(direncList))
    for i in destekList:
        destek +=i
    print("DESTEK: ", destek / len(destekList))

destek_direnc()