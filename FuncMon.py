import pymongo
from pymongo import MongoClient

Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]
Col = DbM["Ser"]
TraEco = DbM["Ind"]

def CleanDb(Datab, Stf):
    DbB = Datab.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    for Wp in KMeys:
        if Wp == "_id" or Wp == "IDd" or Wp == "IDg" or Wp == "Setup" or Wp == "ReqXp" or Wp == "Gold" or Wp == "Bank" or Wp == "XP" or Wp == "Level":
            pass
        else:
            if i[Wp] == 0:
                Datab.update_one(Stf,{"$unset":{Wp: ""}})   

def DbAdd(Datab, Stf, ItV, Num):
    DbB = Datab.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    if (ItV not in KMeys) and (ItV != "IDd") and (ItV != "IDg") and (ItV != "Setup") and (ItV != "_id"):
        Datab.update_one(i,{"$set":{ItV:Num}})
        return True
    return False

def DbRem(Datab, Stf, ItV):
    DbB = Datab.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    if (ItV in KMeys) and (ItV != "IDd") and (ItV != "IDg") and (ItV != "Setup") and (ItV != "_id"):
        Datab.update_one(i,{"$unset":{ItV: ""}})
        return True
    return False

def DbAppendRest(Datab, Stf, Exc, ItV, Num, Act):
    DbA = Datab.find(Stf)
    for j in DbA:
        if j == Exc:
            pass
        else:
            if Act == "a":
                Datab.update_one(j,{"$set":{ItV:Num}})
            elif Act == "r":
                Datab.update_one(j,{"$unset":{ItV:""}})

def AddTo(Datab, Stf, ItV, Num):
    DbB = Datab.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    if (ItV in KMeys) and (ItV != "IDd") and (ItV != "IDg") and (ItV != "Setup") and (ItV != "_id"):
        Datab.update_one(i,{"$set":{ItV:i[ItV]+Num}})
        return True
    return False

def ChangeTo(Datab, Stf, ItV, Num):
    DbB = Datab.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    if (ItV in KMeys) and (ItV != "IDd") and (ItV != "IDg") and (ItV != "Setup") and (ItV != "_id"):
        Datab.update_one(i,{"$set":{ItV:Num}})
        return True
    return False

def CheckIf(Datab, Stf, ItV, Sub, IFEq, Case):
    DbB = Datab.find(Stf)
    for i in DbB:
        KMeys = i.keys()
    if (ItV in KMeys) and (ItV != "IDd") and (ItV != "IDg") and (ItV != "Setup") and (ItV != "_id"):
        if Case == "G":
            if (i[ItV] - Sub) > IFEq:
                return True 
        elif Case == "L":
            if (i[ItV] - Sub) < IFEq:
                return True
        elif Case == "E":
            if (i[ItV] - Sub) == IFEq:
                return True
        elif Case == "GE":
            if (i[ItV] - Sub) >= IFEq:
                return True
        elif Case == "LE":
            if (i[ItV] - Sub) <= IFEq:
                return True
        return False