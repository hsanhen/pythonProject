# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd

df = pd.read_csv('C:\\Users\\snook\\OneDrive\\Desktop\\KWH\\Test.csv', sep=";")

df.drop(0,axis=0,inplace=True)
df = df.apply(lambda x: x.str.replace(',','.'))
#count = 0
#for col in df.columns:
    #if count < 2:
     #   count +=1
      #  continue
    #df[col] = df[col].astype(float)
    #print(type(col))
#print(df)
selected_columns = df[["From","To"]]
zeit = selected_columns.copy()
print(zeit)
#ersten beiden Spalten werden extra gespeichert
df.drop("From", axis=1, inplace=True)
df.drop("To", axis=1, inplace=True)
#Zeitspalten werden entfernt
for col in df.columns:
    df[col] = df[col].astype(float)
print(df)
print (df.dtypes)
#Datentyp wird in float geändert
for col in df.columns:
    df[col].sum()
    summe=df[col].sum()
    print(summe)
#Werte werden aufsummiert
