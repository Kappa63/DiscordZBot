from typing import List
    
class GeneralAchievements:
    def __init__(self, acq:List[int]) -> None:
        self.achieved = acq

    def allTimeBalance(self, bal:float) -> None:
        if bal >= 1000000:
            self.addAchieved(19)
        if bal >= 1000000000:
            self.addAchieved(20)

    def inOutProfit(self, prft:float, rnds:int):
        if rnds == 1 and prft >= 10000:
            self.addAchieved(29)
    
    def addAchieved(self, id:int) -> None:
        if id not in self.achieved:
            self.achieved.append(id)
    
    def getAchieved(self) -> List[int]:
        return self.achieved
    
class BJAchievements(GeneralAchievements):
    def __init__(self, acq:List[int]) -> None:
        super().__init__(acq)
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
            self.addAchieved(10)
        if self.streak <= -5:
            self.addAchieved(1)
    
    def onBJ(self, bet:int) -> None:
        if bet >= 2000:
            self.addAchieved(2)

    def allTimeProfits(self, profit:int) -> None:
        if profit >= 5000:
            self.addAchieved(3)
        if profit >= 10000:
            self.addAchieved(4)
        if profit >= 50000:
            self.addAchieved(5)

    def dealsPlayed(self, nDeals:int) -> None:
        if nDeals >= 100:
            self.addAchieved(9)
    
    def allInProfit(self, profit:float) -> None:
        if profit <= -10000:
            self.addAchieved(13)
        if profit >= 10000:
            self.addAchieved(14)

    def tableProfit(self, profit:float) -> None:
        if profit <= -10000:
            self.addAchieved(11)
        if profit >= 5000:
            self.addAchieved(17)
        if profit <= -50000:
            self.addAchieved(24)

    def updateEmptyBet(self) -> None:
        self.emptyBets += 1
        if self.emptyBets >= 10:
            self.addAchieved(23)
    
    def onCards21(self, nCards:int) -> None:
        if nCards >= 6:
            self.addAchieved(15)

class RRAchievements(GeneralAchievements):
    def roundDeath(self, pPos:int, rnd:int):
        if pPos == 0 and rnd == 1:
            self.addAchieved(6)

    def usrJoin(self, id:int):
        if id == 443986051371892746:
            self.addAchieved(18)

    def headPrice(self, bet:float):
        if bet == 0:
            self.addAchieved(8)

class SAchievements(GeneralAchievements):
    def __init__(self, acq:List[int]) -> None:
        super().__init__(acq)
        self.foodWins = []

    def onWin(self, type):
        if type in ["🍒", "🍉", "🍋", "🍫"] and type not in self.foodWins:
            self.foodWins.append(type)
        if len(self.foodWins) == 4:
            self.addAchieved(28)

    def allTimeJackPots(self, jp:int) -> None:
        if jp >= 5:
            self.addAchieved(27)
        
class MAchievements(GeneralAchievements):
    def boardFinished(self):
        self.addAchieved(26)