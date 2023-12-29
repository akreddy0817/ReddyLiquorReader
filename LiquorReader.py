# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 20:00:19 2022

@author: akhil
"""

import pandas as pd 
from tkinter import *
from datetime import date
from datetime import datetime
import csv 
import pymongo
from pymongo import MongoClient
import dns 

itemList = pd.read_csv('ItemList.csv')
itemList=itemList.rename(columns={"MAINUPC": "UPC","SizeName":"Size"})
itemList=itemList.drop(["PackName","ItemTypeDesc","TOTALQTY_MULTI"],axis=1)


liq = Tk()
liq.title("Reddy's Liquor Reader Updated")
liq.geometry('900x600')


liq_after_ten = pd.DataFrame(columns=['DATE','TIME','UPC','PRODUCTNAME','SIZE','QUANTITY','PRICE'])



def add():
    global liq_after_ten
    today = date.today()
    now = datetime.now()
    item_upc = item.get().strip()
    if item_upc in itemList['UPC'].values: 
        liq_result = itemList[itemList['UPC'] == item_upc].reset_index()
        liq_str = liq_result["ITEMNAME"][0] + " " + liq_result["Size"][0] + " $" + str(liq_result["ItemPrice"][0])
        
        temp = {"DATE":today.strftime("%m/%d/%y"),
                "TIME":now.strftime("%H:%M:%S"),
                "UPC":liq_result["UPC"][0],
                "PRODUCTNAME":liq_result["ITEMNAME"][0],
                "SIZE":liq_result["Size"][0],
                "QUANTITY":1,
                "PRICE": liq_result["ItemPrice"][0]}
        
        for i in range(quantity.get()):
            #print("ADD:  "+ liq_str)
            cartList.insert(END,liq_str)
            liq_after_ten = liq_after_ten.append(temp,ignore_index=True)
            liq_after_ten=liq_after_ten.reset_index(drop=True)
            
        #print(liq_after_ten)
    
        
        item.set("")
        quantity.set(1)
        
       
        #totalcart.set(totalcart.get()+(liq_result["ItemPrice"][0] * quantity.get()))
       
        
def remove():
    global liq_after_ten
    liq_after_ten=liq_after_ten.reset_index(drop=True)
    index = cartList.index(ACTIVE)
    
    cartList.delete(index)
    liq_after_ten=liq_after_ten.drop(index)
    liq_after_ten=liq_after_ten.reset_index(drop=True)
    
    #print("Remove index: " + str(index))
    #print(liq_after_ten)
    
   
def update():
   global liq_after_ten
   
   #conn_str = "mongodb+srv://@reddyliquor.a77bf.mongodb.net/LiquorTransactions?retryWrites=true&w=majority"
 
   #client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
   try:
       
       #client = pymongo.MongoClient("mongodb+srv://srreddy:<reddy123>@reddyliquor.a77bf.mongodb.net/LiquorTransactions?retryWrites=true&w=majority")
       
       client = pymongo.MongoClient("mongodb+srv://srreddy:reddy123@reddyliquor.a77bf.mongodb.net/test?retryWrites=true&w=majority")
       db = client.get_database('student_db')
       records = db.student_records
       print(records.count_documents({}))
       
   except Exception:
       print("Unable to connect to the server.")
    
   
   item.set("")
   quantity.set(1)
   cartList.delete(0,END)
   liq_after_ten=liq_after_ten.reset_index(drop=True)
    #print("UPDATE ")
    #print(liq_after_ten)        
    
   with open('liquor_trans.csv', 'a', newline="") as csvfile:
        for j in range(len(liq_after_ten)):
            writer = csv.writer(csvfile)
            writer.writerow([liq_after_ten.loc[j]['DATE'],
                              liq_after_ten.loc[j]['TIME'],
                              liq_after_ten.loc[j]['UPC'],
                              liq_after_ten.loc[j]['PRODUCTNAME'],
                              liq_after_ten.loc[j]['SIZE'],
                              liq_after_ten.loc[j]['QUANTITY'],
                              liq_after_ten.loc[j]['PRICE']])

   liq_after_ten =  pd.DataFrame(columns=liq_after_ten.columns)    
    #print(liq_after_ten)
    
    
    
    
    
    
    
    

item=StringVar()
quantity=IntVar()
totalcart=IntVar()

quantity.set(1)
totalcart.set(0)


Label(liq, text="UPC:",font=("Times", 18)).grid(row=1, column=0, sticky=E)
Entry(liq, textvariable=item,font=("Times", 18)).grid(row=1, column=1, sticky=W)

Label(liq, text="Quantity:",font=("Times", 18)).grid(row=1, column=2, sticky=E)
Entry(liq, textvariable=quantity,font=("Times", 18)).grid(row=1, column=3, sticky=W)

Button(liq, text="Add", command=add,font=("Times", 18)).grid(row=1, column=4, columnspan=3)
Button(liq, text="Remove", command=remove,font=("Times", 18)).grid(row=3, column=6)
Button(liq, text="Update", command=update,font=("Times", 18)).grid(row=3, column=7)


cartList = Listbox(liq, selectmode=SINGLE,font=("Times", 18),width=50)
cartList.grid(row=3,column=1,columnspan=4,sticky=E)



Label(liq, text="TOTAL COST:",font=("Times", 18)).grid(row=7, column=3, sticky=E)
Label(liq, text=totalcart.get(),font=("Times", 18)).grid(row=7, column=4, sticky=W)

liq.mainloop()

