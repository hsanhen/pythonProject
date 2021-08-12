# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import *

df = pd.read_csv('C:\\Users\\snook\\OneDrive\\Desktop\\KWH\\Duisburg.csv', sep=";")

# Kopfzeilen in neue Tabelle "Zeit" kopieren
selected_columns = df[["From","To"]]
zeit = selected_columns.copy()
print(zeit)

#ersten beiden Spalten werden extra gespeichert
#Zeitspalten werden entfernt

df.drop("From", axis=1, inplace=True)
df.drop("To", axis=1, inplace=True)

#Doppelten header entfernen
df.drop(0,axis=0,inplace=True)

#NaN durch -1 ersetzt
df=df.fillna('-1')

#Kommata durch Punkte ersetzt
df = df.apply(lambda x: x.str.replace(',','.'))

#Datentyp wird in float geändert
for col in df.columns:
   df[col] = df[col].astype(float)
print (df.dtypes)

#Zählt Einträge, die -1 heißen, also vorher NaN waren pro Spalte
y=df.isin([-1]).sum(axis=0)
print(y)

#Zeilen aus Dataframe anzeigen
x=df.iloc[576:578]
print((type(x)))

#Doppelten Header aus Zeit Tabelle löschen
zeit.drop(0,axis=0,inplace=True)
print(zeit.head())

# Datum konvertieren und Wochentag angeben (Montag=0)
count: int = 0
ismonday = False
issunday = False
firstday = '01.01.2019 00:00'
lastday = '31.12.2020 00:00'
'''for date in zeit['From']:
    date = pd.Series(date)
    date = pd.to_datetime(date, format="%d.%m.%Y %H:%M")
    weekday = date.dt.dayofweek
    #print(weekday, date)
    if str(date) == firstday and weekday == 0:
        ismonday = True
    if str(date) == lastday and weekday == 6:
        issunday = True'''

# Anzahl der Wochen als ganze Zahl
wochen = int((len(zeit))/672)
print(wochen)

# Boolean zur Überprüfung, ob dieser Montag schon in der Liste ist
monday = False
#Liste von Indizes aller Montage
montage = []
for index, row in zeit.iterrows():
    date = pd.Series(row['From'])
    date = pd.to_datetime(date, format="%d.%m.%Y %H:%M")
    weekday = date.dt.dayofweek
    if int(weekday) == 0 and not monday:
        monday = True
        montage.append(index)
    if int(weekday) == 1 and monday:
        monday = False
print(montage)

#allData speichert die Daten jeder einzelnen Woche in Listen
allData = []
for m in montage:
    temp = df.iloc[(m-1):(m+671)]
    liste = []
    for col in df.columns:
        temp2 = temp[col]
        liste.append(temp2)
    allData.append(liste)
print(allData[1])
