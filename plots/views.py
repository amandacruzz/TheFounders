from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import HistoricalPrices
from trackapp.models import Acc_Positions, coinPrices
import plotly.express as px
from django.http import HttpResponse
from datetime import datetime
import pandas as pd
import time
import json

def getPrices() -> list[dict]:
    validSymbols = []
    for i in coinPrices.objects.all():
        validSymbols.append(dict(symbol=i.symbol, derivedUSD=i.derivedUSD, name=i.name))

    return validSymbols


def aggPos(user: str) -> list[dict]:
    user_positions = Acc_Positions.objects.filter(username_id__username=user)

    valids = {}
    with open("valids.json") as valid:
        valid = json.load(valid)

        for i in valid['valids']:
            valids[i['token']] = {'qty': 0, 'p': 0, 'c': 0}

    for i in user_positions:
        cur = valids[i.coin]
        cur['qty'] += i.quantity
        cur['p'] += i.price_per_coin * i.quantity
        cur['c'] += 1

    aggregate_pos = []
    for i in valids:
        if valids[i]['c'] > 0:
            aggregate_pos.append({'ticker': i,
                                  'cost': round(valids[i]['p'] / valids[i]['qty'], 8),
                                  'quantity': valids[i]['qty']})
    return aggregate_pos

def getHistoricalPrices() -> dict:
    prices = HistoricalPrices.objects.all()

    priceDict = {}
    for i in prices:
        if i.intTime in priceDict:
            priceDict[i.intTime][i.token] = i
        else:
            priceDict[i.intTime] = {i.token: i}

    return priceDict


def getUserPositions(user: str) -> dict:
    user = User.objects.get(username=user)
    positions = Acc_Positions.objects.filter(username_id=user)


    positionsDict = {}
    for i in positions:
        time = int(i.time_bought.timestamp())
        time = time - (time % 3600)

        if time in positionsDict:
            positionsDict[time].append(i)
        else:
            positionsDict[time] = [i]

    return positionsDict


def getValue(prices, position, time):
    values = {}
    for i in prices:
        if i >= time and position.coin in prices[i]:
            values[i] = position.quantity * prices[i][position.coin].price
    return values


def addDict(dict1: dict, dict2: dict) -> dict:
    for i in dict1:
        if i in dict2:
            dict2[i] += dict1[i]
        else:
            dict2[i] = dict1[i]

    return dict2


def dashplotval(agg: list[dict]):
    value = 0

    for position in agg:
        value += position['curValue']

    return round(value, 2)


def linechart(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('/account/login/')

    positions = getUserPositions(request.user)
    prices = getHistoricalPrices()

    values = []
    for i in positions:
        for j in positions[i]:
            values.append(getValue(prices, j, i))

    for i in values:
        maximum = None
        for j in i:
            if maximum is None:
                maximum = j
            elif j > maximum:
                maximum = j
        toAdd = {}
        for j in i:
            if j != maximum:
                if j + 3600 not in i:
                    l = j + 3600
                    while l not in i:
                        toAdd[l] = i[j]
                        l += 3600
                elif i[j + 3600] == 0:
                    i[j + 3600] = i[j]

        for j in toAdd:
            i[j] = toAdd[j]
    cumulativeVals = {}

    for i in values:
        cumulativeVals = addDict(cumulativeVals, i)

    xVals = []
    yVals = []

    for i in cumulativeVals:
        xVals.append(datetime.fromtimestamp(i))
        yVals.append(cumulativeVals[i])

    indexes = list(range(len(xVals)))
    indexes.sort(key=xVals.__getitem__)

    xVals = list(map(xVals.__getitem__, indexes))
    yVals = list(map(yVals.__getitem__, indexes))

    xVals = xVals[200: len(xVals) - 1]
    yVals = yVals[200: len(yVals) - 1]

    df = pd.DataFrame(dict(Time=xVals, Value=yVals))

    config = {'scrollZoom': True,
              'responsive': True,
              'displayModeBar': False
              }

    ch = px.line(df, x="Time", y="Value", template='plotly_white', color_discrete_sequence=['#8b2170'])

    ch.update_xaxes(
        title='',
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    ch.update_yaxes(
        title=''
    )

    ch.update_layout(margin={
        'l': 0,
        'r': 10
    },
        yaxis=dict(scaleanchor="x", scaleratio=1)
    )

    response = HttpResponse(request)
    response.write(ch.to_html(config=config, full_html=True, default_width='100%', include_plotlyjs='cdn'))
    return response



def linechartPlain(request):
    positions = getUserPositions(request.user)
    prices = getHistoricalPrices()

    values = []
    for i in positions:
        for j in positions[i]:
            values.append(getValue(prices, j, i))

    for i in values:
        maximum = None
        for j in i:
            if maximum is None:
                maximum = j
            elif j > maximum:
                maximum = j
        toAdd = {}
        for j in i:
            if j != maximum:
                if j + 3600 not in i:
                    l = j + 3600
                    while l not in i:
                        toAdd[l] = i[j]
                        l += 3600
                elif i[j + 3600] == 0:
                    i[j + 3600] = i[j]

        for j in toAdd:
            i[j] = toAdd[j]
    cumulativeVals = {}

    for i in values:
        cumulativeVals = addDict(cumulativeVals, i)

    xVals = []
    yVals = []

    for i in cumulativeVals:
        xVals.append(datetime.fromtimestamp(i))
        yVals.append(cumulativeVals[i])

    indexes = list(range(len(xVals)))
    indexes.sort(key=xVals.__getitem__)

    xVals = list(map(xVals.__getitem__, indexes))
    yVals = list(map(yVals.__getitem__, indexes))

    xVals = xVals[200: len(xVals) - 1]
    yVals = yVals[200: len(yVals) - 1]

    df = pd.DataFrame(dict(Time=xVals, Value=yVals))

    config = {'scrollZoom': True,
              'responsive': True,
              'displayModeBar': False
              }

    ch = px.line(df, x="Time", y="Value", template='plotly_white', color_discrete_sequence = ['#8b2170'])


    ch.update_xaxes(
        title='',
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    ch.update_yaxes(
        title=''
    )

    ch.update_layout(margin={
        'l': 0,
        'r': 10
    })

    return ch.to_html(config=config, full_html=False, default_width='100%', include_plotlyjs='cdn')


def pieChart(request): # total positions
    prices = getPrices()
    positions = aggPos(request.user)

    priceDict = {}
    for i in prices:
        priceDict[i['symbol']] = float(i['derivedUSD'])

    tokens = []
    tokenValue = []

    for i in positions:
        tokens.append(i['ticker'])
        tokenValue.append(i['quantity'] * priceDict[i['ticker']])

    df = pd.DataFrame(dict(values=tokenValue,names=tokens))

    ch = px.pie(df, values="values", names="names")

    config = {'responsive': True}

    return ch.to_html(config=config, full_html=False, default_width='100%', include_plotlyjs='cdn')



def portfolioValue(positions, prices):
    value = 0

    for i in positions:
        for j in prices:
            if i['ticker'] == j:
                value += i['quantity'] * prices[j].price
    return value



def historicPriceChange(request):
    oldPrices = getHistoricalPrices() # this is already a dict
    positions = aggPos(request.user)

    curTime = int(time.time())
    curTime = curTime - curTime % 3600

    oneDaysAgo = curTime - 3600 * 24 * 1
    sevenDaysAgo = curTime - 3600 * 24 * 7
    fifteenDaysAgo = curTime - 3600 * 24 * 15
    thirtyDaysAgo = curTime - 3600 * 24 * 30
    sixtyDaysAgo = curTime - 3600 * 24 * 60

    curPrice = getPrices()
    curValue = 0
    for i in positions:
        for j in curPrice:
            if i['ticker'] == j['symbol']:
                curValue += i['quantity'] * float(j['derivedUSD'])

    #TODO make sure this works correctly
    if oneDaysAgo not in oldPrices:
        while oneDaysAgo not in oldPrices:
            oneDaysAgo -= 3600


    if portfolioValue(positions, oldPrices[oneDaysAgo]) == 0:
        oneDaysAgo = 0
    else:
        oneDaysAgo = round((curValue / portfolioValue(positions, oldPrices[oneDaysAgo]) - 1) * 100, 2)

    if portfolioValue(positions, oldPrices[sevenDaysAgo]) == 0:
        sevenDaysAgo = 0
    else:
        sevenDaysAgo = round((curValue / portfolioValue(positions, oldPrices[sevenDaysAgo]) - 1) * 100, 2)

    if portfolioValue(positions, oldPrices[fifteenDaysAgo]) == 0:
        fifteenDaysAgo = 0
    else:
        fifteenDaysAgo = round((curValue / portfolioValue(positions, oldPrices[fifteenDaysAgo]) - 1) * 100, 2)

    if portfolioValue(positions, oldPrices[thirtyDaysAgo]) == 0:
        thirtyDaysAgo = 0
    else:
        thirtyDaysAgo = round((curValue / portfolioValue(positions, oldPrices[thirtyDaysAgo]) - 1) * 100, 2)

    if portfolioValue(positions, oldPrices[sixtyDaysAgo]) == 0:
        sixtyDaysAgo = 0
    else:
        sixtyDaysAgo = round((curValue / portfolioValue(positions, oldPrices[sixtyDaysAgo]) - 1) * 100, 2)
    
    stats = [oneDaysAgo, sevenDaysAgo, fifteenDaysAgo, thirtyDaysAgo, sixtyDaysAgo]
    return stats

