import pymongo
from pymongo import MongoClient

Mdb = "mongodb+srv://Kappa:85699658@cbotdb.exsit.mongodb.net/CBot?retryWrites=true&w=majority"
Cls = MongoClient(Mdb)
DbM = Cls["CBot"]
Col = DbM["Ser"]
TraEco = DbM["Ind"]


def DbAdd(Datab, Stf, ItV, Num):
    DbB = Datab.find(Stf)
    try:
        for i in DbB:
            KMeys = i.keys()
        if (
            (ItV not in KMeys)
            and (ItV != "IDd")
            and (ItV != "IDg")
            and (ItV != "Setup")
            and (ItV != "_id")
        ):
            Datab.update_one(i, {"$set": {ItV: Num}})
            return True
        return False
    except UnboundLocalError:
        return False


def DbRem(Datab, Stf, ItV):
    DbB = Datab.find(Stf)
    try:
        for i in DbB:
            KMeys = i.keys()
        if (
            (ItV in KMeys)
            and (ItV != "IDd")
            and (ItV != "IDg")
            and (ItV != "Setup")
            and (ItV != "_id")
        ):
            Datab.update_one(i, {"$unset": {ItV: ""}})
            return True
        return False
    except UnboundLocalError:
        return False


def DbAppendRest(Datab, Stf, Exc, ItV, Num, Act):
    DbA = Datab.find(Stf)
    try:
        for j in DbA:
            if j == Exc:
                pass
            else:
                if Act == "a":
                    Datab.update_one(j, {"$set": {ItV: Num}})
                elif Act == "r":
                    Datab.update_one(j, {"$unset": {ItV: ""}})
    except UnboundLocalError:
        return False


def AddTo(Datab, Stf, ItV, Num):
    DbB = Datab.find(Stf)
    try:
        for i in DbB:
            KMeys = i.keys()
        if (
            (ItV in KMeys)
            and (ItV != "IDd")
            and (ItV != "IDg")
            and (ItV != "Setup")
            and (ItV != "_id")
        ):
            Datab.update_one(i, {"$set": {ItV: i[ItV] + Num}})
            return True
        return False
    except UnboundLocalError:
        return False


def ChangeTo(Datab, Stf, ItV, Num):
    DbB = Datab.find(Stf)
    try:
        for i in DbB:
            KMeys = i.keys()
        if (
            (ItV in KMeys)
            and (ItV != "IDd")
            and (ItV != "IDg")
            and (ItV != "Setup")
            and (ItV != "_id")
        ):
            Datab.update_one(i, {"$set": {ItV: Num}})
            return True
        return False
    except UnboundLocalError:
        return False


def CheckIf(Datab, Stf, ItV, Sub, IFEq, Case):
    DbB = Datab.find(Stf)
    try:
        for i in DbB:
            KMeys = i.keys()
        if (
            (ItV in KMeys)
            and (ItV != "IDd")
            and (ItV != "IDg")
            and (ItV != "Setup")
            and (ItV != "_id")
        ):
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
    except UnboundLocalError:
        return False