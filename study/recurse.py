# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 10:29:52 2014

@author: Pyltsin
"""

def toStr(n,base):
   convertString = "0123456789ABCDEF"
   if n < base:
      return convertString[n]
   else:
      return toStr(n//base,base) + convertString[n%base]


def reverse(s):
    if len(s)==1:
        s=s
    else:
        s=reverse(s[1:])+s[0]
    return s


def drawSpiral(myTurtle, lineLen):
    if lineLen > 0:
        myTurtle.forward(lineLen)
        myTurtle.right(90)
        drawSpiral(myTurtle,lineLen-5)


def tree(branchLen,t):
    if branchLen > 5:
        t.forward(branchLen)
        t.right(20)
        tree(branchLen-15,t)
        t.left(40)
        tree(branchLen-15,t)
        t.right(20)
        t.backward(branchLen)

def main():
    t = turtle.Turtle()
    myWin = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(100)
    t.down()
    tree(150,t)
    myWin.exitonclick()

def moveTower(height,fromPole, toPole, withPole):
    if height >= 1:
        moveTower(height-1,fromPole,withPole,toPole)
        moveDisk(fromPole,toPole)
        moveTower(height-1,withPole,toPole,fromPole)

def moveDisk(fp,tp):
    print("moving disk from",fp,"to",tp)

def recMC(coinValueList,change):
   minCoins = change
   if change in coinValueList:
     return 1
   else:
      for i in [c for c in coinValueList if c <= change]:
         numCoins = 1 + recMC(coinValueList,change-i)
         if numCoins < minCoins:
            minCoins = numCoins
   return minCoins

def dpMakeChange(coinValueList,change,minCoins,coinsUsed):
   for cents in range(change+1):
      coinCount = cents
      newCoin = 1
      print 'gen', 'coinCount', coinCount, 'newCoin', newCoin
      for j in [c for c in coinValueList if c <= cents]:
            print 'j',j
            print minCoins[cents-j] + 1 , coinCount
            if minCoins[cents-j] + 1 < coinCount:
               coinCount = minCoins[cents-j]+1
               newCoin = j
               print 'coinCount', coinCount, 'newCoin', newCoin
      minCoins[cents] = coinCount
      coinsUsed[cents] = newCoin
      print 'minCoins', minCoins, 'coinUsed', coinsUsed
   return minCoins[change]

def printCoins(coinsUsed,change):
   coin = change
   while coin > 0:
      thisCoin = coinsUsed[coin]
      print(thisCoin)
      coin = coin - thisCoin

def main():
    amnt = 12
    clist = [2,5,10,21,25]
    coinsUsed = [0]*(amnt+1)
    coinCount = [0]*(amnt+1)

    print("Making change for",amnt,"requires")
    print(dpMakeChange(clist,amnt,coinCount,coinsUsed),"coins")
    print("They are:")
    printCoins(coinsUsed,amnt)
    print("The used list is as follows:")
    print(coinsUsed)


def myMakeChange(coinValueList,change):
    minCoin=[0]*(change+1)
    coinUsed=[0]*(change+1)
    minCoin[0]='-'
    coinUsed[0]='-'
    for i in range(change):
        k=i+1
        '''считаем на к'''
        minCoin[k]='-'
        coinUsed[k]='-'

        for j in coinValueList:
            '''случай для малых значений, которых нельхя сделать'''
            if j<=k:
#                print j, k , minCoin, coinUsed
                if j==k and minCoin[k-j]=='-':
                    minCoin[k]=1
                    coinUsed[k]=j
                elif j<k and minCoin[k-j]!='-' and minCoin[k]!='-' and minCoin[k-j]+1<minCoin[k]:
                    minCoin[k]=minCoin[k-j]+1
                    coinUsed[k]=j
                elif j<k and minCoin[k-j]!='-' and minCoin[k]=='-':
                    minCoin[k]=minCoin[k-j]+1
                    coinUsed[k]=j
    return minCoin, coinUsed
def myCoin(temp, coin):
    lst=[]
    tempCoin=coin
    if temp[0][coin]!='-':
        while tempCoin!=0:
            lst.append(temp[1][tempCoin])
            tempCoin=tempCoin-temp[1][tempCoin]
    return lst
    
valueList=[2,4,10,23,25]
coin=163
temp=myMakeChange(valueList, coin)
print 'temp', myMakeChange(valueList, coin)
print u' количество монет', temp[0][-1]
print u'монеты', myCoin(temp, coin)                        
