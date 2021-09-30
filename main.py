# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

from datetime import *
path = 'C:\\Users\\snook\\OneDrive\\Desktop\\KWH\\20210902\\Zwickau.csv'
df = pd.read_csv(path, sep=";")

import hashlib
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

print(md5(path))

# Variable, um Stadt zu wechseln
stadt = path.split("\\")[-1].split(".")[0]

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
#df=df.fillna('-1')

#Kommata durch Punkte ersetzt
df = df.apply(lambda x: x.str.replace(',','.'))

#Datentyp wird in float geändert
for col in df.columns:
   df[col] = df[col].astype(float)
print (df.dtypes)
#Zählt Einträge, die -1 heißen, also vorher NaN waren pro Spalte
#y=df.isin(["NaN"]).sum(axis=0)
y = df.isna().sum(axis=0)
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

#leere Listen zur Erstellung der Wochentags- und Jahreszeiten-Variablen
wochentag = []
montage = []
jahreszeit = []
werktage = []
#########
tagArt = []# kriegt 0 für normalen wochentag, 1 für samstage und 2 für sonntage und feiertage

stadt = path.split("/")[-1].split(".")[0]
feiertage = ["01.01.2019","19.04.2019","21.04.2019","22.04.2019", "01.05.2019","30.05.2019", "09.06.2019", "10.06.2019","03.10.2019", "25.12.2019", "26.12.2019", "01.01.2020","10.04.2020","12.04.2020","13.04.2020", "01.05.2020","21.05.2020", "31.05.2020", "01.06.2020", "03.10.2020", "25.12.2020", "26.12.2020","01.01.2021","02.04.2021", "04.04.2021", "05.04.2021", "01.05.2021","13.05.2021","23.05.2021", "24.05.2021", "03.10.2021", "25.12.2021", "26.12.2021"] #himmelfahrt mit jahr, pfingstmontag mit jahr, karfreitag mit jahr (oder?) ostermontag mit jahr# alle tage mit jahr angeben!
if stadt == "Duisburg":
    feiertage += ["20.06.2019", "01.11.2019", "01.11.2020", "01.11.2021", "11.06.2020", "03.06.2021"] #in dieser liste stehen die feiertage die es nur in NRW gibt

elif stadt == "Karlsruhe":
    feiertage += ["06.01.2019", "06.01.2020", "06.01.2021", "20.06.2019", "01.11.2019","11.06.2020", "01.11.2020","03.06.2021", "01.11.2021"] #feiertage, die es nur in BW gibt

elif stadt == "Zwickau":
    feiertage += ["31.10.2019", "31.10.2020", "31.10.2021", "20.11.2019","18.11.2020"] #feiertage, die es nur in sachsen gibt
#########
#Dictionary für Jahreszeiten
seasonDict = {"01":"Winter", "02": "Winter", "03":"Frühling", "04":"Frühling", "05":"Frühling", "06":"Sommer", "07":"Sommer", "08":"Sommer", "09":"Herbst", "10":"Herbst", "11":"Herbst", "12":"Winter"}

for index, row in zeit.iterrows():
    date = pd.Series(row['From'])
    monat = str(row["From"]).split(" ")[0].split(".")[1]
    tag = str(row["From"]).split(" ")[0].split(".")[0]
    datumString = str(row["From"].split(" ")[0])  # im format tt.mm.jjjj

# Liste von Indizes aller Montage

    date = pd.to_datetime(date, format="%d.%m.%Y %H:%M")

    weekday = int(date.dt.dayofweek)
    wochentag.append(weekday)
    #jahreszeit.append(seasonDict.get(monat))
    if monat in ["11", "12", "01", "02"] or (monat =="03" and int(tag) < 21):
        jahreszeit.append("Winter")
    elif monat in ["06", "07", "08"] or (monat == "05" and int(tag) > 14) or (monat == "09" and int(tag) < 15):
        jahreszeit.append("Sommer")
    else:
        jahreszeit.append("Übergang")
    if weekday == 0 and not monday:
        monday = True
        montage.append(index)
    if weekday == 1 and monday:
        monday = False
#########
#jetzt die tagArt liste füllen, welche art tag haben wir?
    if datumString in feiertage or weekday == 6:
        tagArt.append(2)
    elif "24.12." in datumString or "31.12." in datumString or weekday == 5:
        tagArt.append(1)
    else:
        tagArt.append(0)
#########
print(montage)
#Neue Spalten für Jahreszeit und Wochentag hinzugefügt

df["wochentag"] = wochentag
df["jahreszeit"] = jahreszeit
df["SummmeHauptzähler"] = df[df.columns[0]]+df[df.columns[1]]
df["tagArt"] = tagArt

#allData speichert die Daten jeder einzelnen Woche und jeder einzelnen Zähler in Listen
allData = []
for m in montage:
    woche = df.iloc[(m-1):(m+671)]
    liste = []
    for col in df.columns:
        temp2 = woche[col]
        liste.append(temp2)
    allData.append(liste)
print(allData[1])

'''
#Abspeichern der Datei 
filename = "C:\\Users\\snook\\OneDrive\\Desktop\\KWH\\DB_Saison.csv"
with open(filename, "w") as file:
    file.write(df.to_csv(header=True, index=True, sep=";"))
print(df.head(200))
'''
# Variable, die angibt, welche Spalte geplottet werden soll

verb=0

#Plotte i Wochen für einen Zähler

#leere Listen für die Erstellung der Wochen-Plots
v = allData[1]
x = list(range(672))
v1wochei = np.array(v[verb])
listmini = v1wochei
listmaxi = v1wochei
listmedian = []
listupquantil = []
listdownquantil = []

#Liste von Listen für alle Uhrzeiten aller Zähler

viertelstunden = []
for k in range(672):
    viertelstunden.append([])
for i in range(wochen-1):
    v = allData[i]
    # Jahreszeiten in Arbeit, weil nur die Jahreszeit des Montags ausschlaggebend
    #if v[7].to_list()[1] != "Sommer":
     #   continue
   #if v[-1].to_list()[1] == "Winter" or v[-1].to_list()[1] == "Sommer" - Übergangszeit
    # if v[-1].to_list()[1] != "Winter" - Wintertage
    v1wochei = np.array(v[verb])
    listmaxi = np.maximum(v1wochei, listmaxi)
    temp = v1wochei
    for j in range(len(temp)):
        viertelstunden[j].append(temp[j])
    listmini = np.minimum(temp, listmini)
for z in viertelstunden:
    z=[b for b in z if np.isnan(b)==False]
    median = stat.median(z)
    listmedian.append(median)
    upquantil = np.quantile(z, .95)
    listupquantil.append(upquantil)
    downquantil = np.quantile(z, .05)
    listdownquantil.append(downquantil)
#plt.plot(x, listmaxi, listmini)
#Plots aller Wochen mit Quantilen
plt.fill_between(x, listmedian, listupquantil, alpha=.5, color="blue")
plt.fill_between(x, listmedian, listdownquantil, alpha=.5, color="blue")
plt.fill_between(x, listmaxi, listupquantil, alpha=.5, color="grey")
plt.fill_between(x, listmini, listdownquantil, alpha=.5, color="grey")
plt.plot(x, listmedian, color="black")
plt.plot(x, listupquantil, color="black")
plt.plot(x, listdownquantil, color="black")
plt.show()
#fill-between min-max, median




#------------------------------------------------------------------
'''firstMondayIndex = montage[0]
lastSundayIndex = montage[-1]-1



spalte = df.columns[verb]
alleTage = df[spalte] #hier dann vielleicht die ersten tage des jahres rauslöschen, falls sie kein montag sind? wir haben ja die liste der montage mit index
alleTage = alleTage[firstMondayIndex:lastSundayIndex+1]
med = []
q5 = []
q95 = []
minim = []
maxim = []
for a in list(range(672)):
    temp = list(alleTage[a::672])
    temp = [b for b in temp if np.isnan(b) == False]
    med.append(stat.median(temp))
    q5.append(np.quantile(temp, 0.05))
    q95.append(np.quantile(temp, 0.95))
    minim.append(min(temp))
    maxim.append(max(temp))
    
x = list(range(672))
plt.plot(x, q95, color="black")
plt.plot(x, q5, color="black")
#plt.plot(x, minim, color="black")
#plt.plot(x, maxim, color="black")
plt.plot(x, med, color="black")
plt.fill_between(x, med, q95, alpha=0.5, color="blue")
plt.fill_between(x, med, q5, alpha=0.5, color="blue")
plt.fill_between(x, maxim, q95, alpha=0.5, color="grey")
plt.fill_between(x, minim, q5, alpha=0.5, color="grey")
plt.show()'''
#-----------------------------------------------------

#Variable gibt Spaltennamen aus
spalte = df.columns[verb]
#Feiertage
weihnachten = []
df["datum"] = str(zeit["From"])
#format="%d.%m.%Y %H:%M"

#Angabe des Wochentags
df2 = df[df["tagArt"]==0]
#Trennung nach Jahreszeit
df2 = df2[df2["jahreszeit"] == "Übergang"]
#Anzahl der beobachteten Daten
werktage = df2[spalte]
print(len(werktage))

werktagemedian = []
werktageupquantil = []
werktagedownquantil = []
werktagemaximum = []
werktageminimum = []
for a in list(range(96)):
    temp = list(werktage[a::96])
    #while -1 in temp:
        #temp.remove(-1)
# Kommende Zeile löscht NaN
    temp = [b for b in temp if np.isnan(b)==False]
    median = stat.median(temp)
    werktagemedian.append(median)
    werktageupquantil.append(np.quantile(temp, .95))
    werktagedownquantil.append(np.quantile(temp, .05))
    werktagemaximum.append(max(temp))
   # temp = [1000 if b == -1 else b for b in temp]
    werktageminimum.append(min(temp))
plt.plot(list(range(96)), werktageupquantil, color="black")
plt.plot(list(range(96)), werktagedownquantil, color="black")
#plt.plot(list(range(96)), werktagemaximum, color="black")
#plt.plot(list(range(96)), werktageminimum, color="black")
plt.plot(list(range(96)), werktagemedian, color="black")
x = list(range(96))
plt.fill_between(x, werktagemedian, werktageupquantil, alpha=.5, color="blue")
plt.fill_between(x, werktagemedian, werktagedownquantil, alpha=.5, color="blue")
plt.fill_between(x, werktagemaximum, werktageupquantil, alpha=.5, color="grey")
plt.fill_between(x, werktageminimum, werktagedownquantil, alpha=.5, color="grey")
plt.ylim([0,150])
plt.show()