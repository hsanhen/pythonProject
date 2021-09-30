import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

path = 'C:\\Users\\snook\\OneDrive\\Desktop\\KWH\\Ausfahrten2.csv'
df = pd.read_csv(path, sep=";")
df.drop("Ausfahrt Dauerparker", axis=1, inplace=True)
df.drop("EinfahrtKZP", axis=1, inplace=True)
df.drop("Ausfahrt KZP", axis=1, inplace=True)
df.drop("Einfahrt Dauerparker", axis=1, inplace=True)
df.drop(range(6), axis=0, inplace=True)
print(df.head)

monday = False
montage = []
wochentag = []
for index, row in df.iterrows():
    date = pd.Series(row['Datum'])
    date = pd.to_datetime(date, format="%d.%m.%Y")
    weekday = int(date.dt.dayofweek)
    wochentag.append(weekday)
    if weekday == 0 and not monday:
        monday = True
        montage.append(index)
    if weekday == 1 and monday:
        monday = False
print(montage)
wochen = []
for m in montage:
    woche = df.iloc[(m):(m+7)]
    wochen.append(woche)
print(wochen[50])
print(len(wochen))
einfahrten = []
ausfahrten = []
einmedian = []
einq5 = []
einq95 = []
einmin = []
einmax = []
for i in [0,1,2,3,4,5,6]:
    temp = list(df["Summe Einfahrten"][i::7])
    einmedian.append(stat.median(temp))
    einq5.append(np.quantile(temp, .05))
    einq95.append(np.quantile(temp, .95))
    einmin.append(min(temp))
    einmax.append(max(temp))
print(einmedian)
x = list(range(7))
plt.plot(x, einmedian, color="black")
plt.plot(x, einq5, color="black")
plt.plot(x, einq95, color="black")
plt.fill_between(x, einmedian, einq95, alpha=.5, color="blue")
plt.fill_between(x, einmedian, einq5, alpha=.5, color="blue")
plt.fill_between(x, einmax, einq95, alpha=.5, color="grey")
plt.fill_between(x, einmin, einq5, alpha=.5, color="grey")
plt.show()
ausmedian = []
ausq5 = []
ausq95 = []
ausmin = []
ausmax = []
for i in range(7):
    temp = list(df["Summe Ausfahrten"][i::7])
    ausmedian.append(stat.median(temp))
    ausq5.append(np.quantile(temp, .05))
    ausq95.append(np.quantile(temp, .95))
    ausmin.append(min(temp))
    ausmax.append(max(temp))
x = list(range(7))
plt.plot(x, ausmedian, color="black")
plt.plot(x, ausq5, color="black")
plt.plot(x, ausq95, color="black")
plt.fill_between(x, ausmedian, ausq95, alpha=.5, color="blue")
plt.fill_between(x, ausmedian, ausq5, alpha=.5, color="blue")
plt.fill_between(x, ausmax, ausq95, alpha=.5, color="grey")
plt.fill_between(x, ausmin, ausq5, alpha=.5, color="grey")
plt.show()
print(len(ausmedian))
'''for i in range(len(wochen)-1):
    ein = np.array(wochen[i])
    aus = np.array(wochen[i])
    einfahrten.append(ein[])
    ausfahrten.append(aus[])
print(einfahrten)'''