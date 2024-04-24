from typing import List

class BJAchievements:
    def __init__(self, acq:List[int]) -> None:
        self.achieved = acq
        self.streak = 0
        self.emptyBets = 0

    def updateStreak(self, res:int) -> None:
        if res > 0 and self.streak > 0:
            self.streak += res
        elif res < 0 and self.streak < 0:
            self.streak += res
        else:
            self.streak = res
        if self.streak >= 5:
            if 1 not in self.achieved:
                self.achieved.append(1)
        if self.streak <= -5:
            if 10 not in self.achieved:
                self.achieved.append(10)
    
    def onBJ(self, bet:int) -> None:
        if bet >= 2000:
            if 2 not in self.achieved:
                self.achieved.append(2)

    def allTimeProfits(self, profit:int) -> None:
        if profit >= 5000:
            if 3 not in self.achieved:
                self.achieved.append(3)
        if profit >= 10000:
            if 4 not in self.achieved:
                self.achieved.append(4)
        if profit >= 50000:
            if 5 not in self.achieved:
                self.achieved.append(5)

    def dealsPlayed(self, nDeals:int) -> None:
        if nDeals >= 100:
            if 9 not in self.achieved:
                self.achieved.append(9)
    
    def allInProfit(self, profit:int) -> None:
        if profit <= -10000:
            if 13 not in self.achieved:
                self.achieved.append(13)
        if profit >= 10000:
            if 14 not in self.achieved:
                self.achieved.append(14)

    def tableProfit(self, profit:int) -> None:
        if profit <= -10000:
            if 11 not in self.achieved:
                self.achieved.append(11)
        if profit >= 5000:
            if 17 not in self.achieved:
                self.achieved.append(17)
        if profit <= -50000:
            if 24 not in self.achieved:
                self.achieved.append(24)

    def allTimeBalance(self, bet:int) -> None:
        if bet >= 1000000:
            if 19 not in self.achieved:
                self.achieved.append(19)
        if bet >= 1000000000:
            if 20 not in self.achieved:
                self.achieved.append(20)

    def updateEmptyBet(self) -> None:
        self.emptyBets += 1
        if self.emptyBets >= 10:
            if 23 not in self.achieved:
                self.achieved.append(23)

    def addAchieved(self, id:int) -> None:
        if id not in self.achieved:
            self.achieved.append(id)
    
    def getAchieved(self) -> List[int]:
        return self.achieved
    
class GeneralAchievements:
     def __init__(self, acq:List[int]) -> None:
        self.achieved = acq

class RRAchievements:
     def __init__(self, acq:List[int]) -> None:
        self.achieved = acq