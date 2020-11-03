import pymongo
from pymongo import MongoClient

Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]
Col = DbM["Ser"]
TraEco = DbM["Ind"]

def CleanDb(Stf):
    DbB = TraEco.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    for Wp in KMeys:
        if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup" or Wp == "ReqXp" or Wp == "Gold" or Wp == "Bank" or Wp == "XP" or Wp == "Level":
            pass
        else:
            if i[Wp] == 0:
                TraEco.update_one(Stf,{"$unset":{Wp: ""}})   

def DbAdd(Stf, ItV):
    DbB = TraEco.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    if ItV not in KMeys:
        TraEco.update_one(i,{"$set":{ItV:0}})

def AddTo(Stf, ItV, Num):
    DbB = TraEco.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    if ItV in KMeys:
        TraEco.update_one(i,{"$set":{ItV:i[ItV] +Num}})