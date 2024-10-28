import math
import time
import random
import json

counter = 2
nations = []

with open("ww1game\map_data.json", "r") as f:
    map_data = json.load(f)


class military:
    def __init__(
        self,
        soldiers,
        morale=1,
        salary=10,  # balance salary and all these default values at some point
    ):
        self.soldiers = soldiers
        self.morale = morale
        self.salary = salary

    def __str__(self):
        return f"""
        Soldiers: {self.soldiers}
        Morale: {self.morale}%
        Salary: {self.salary}$ Per month
"""


class government:
    def __init__(
        self,
        population,
        alliance,
        taxerate=15,
        stability=100,
    ):
        self.population = population
        self.alliance = alliance
        self.taxrate = taxerate
        self.stability = stability

    def update(
        self,
    ):
        self.stability += (
            15 - self.taxrate
        )  # put more in depth stability (how many recruits, economic performance, losing war, etc.)

        def __str__(self):
            report = f"""
Government Report:
Population: {self.population}
Tax: {self.taxrate}%
Political Unrest: {100 - self.stability}
"""
            return report


class economy:
    def __init__(
        self,
        money,
        income=None,
        costs=None,
        netProfit=None,
    ):
        self.money = money
        self.income = income
        self.costs = costs
        self.netProfit = netProfit

    def update(self, parent):
        self.income = parent.govt.population * parent.govt.taxrate
        self.costs = parent.army.soldiers * parent.army.salary + parent.tech.budget
        self.netProfit = self.income - self.costs
        self.money += self.netProfit
        print("__str__() has been defined")

    def __str__(self):
        return f"""
Economic report:
Profit: {self.netProfit}
        
Administration:
Tax Revenue: {parent.govt.population * parent.govt.taxrate}
War Bonds:
War Bond Interest:

Military:
Personnel Costs: {parent.army.soldiers * parent.army.salary}

Technology:
Research Budget: {parent.tech.budget}
        """


class technology:
    def __init__(
        self,
        progress=0,
        points=0,
        budget=0,
    ):
        self.progress = progress
        self.points = points
        self.budget = budget


class countries:
    def __init__(
        self,
        govt,
        econ,
        tech,
        army,
        name,
        id,
        symbol,
    ):
        self.govt = govt
        self.econ = econ
        self.tech = tech
        self.army = army
        self.name = name
        self.id = id
        self.symbol = symbol

    def turn(self):
        self.econ.update(self)
        self.govt.update()
        while True:
            print("new turn")
            actionInput = input("What's your next move?: ")
            action = actionInput.split(" ")
            if len(action) > 1:
                for i in nations:
                    if i.name == action[1]:
                        subject = i
            match action[0]:
                case "attack":
                    self.attack(subject)
                case "fortify":
                    # come back maybe least priority
                    pass
                case "research":
                    if action[1] == "shop":  # working on all the reports 10/26/2024
                        print(
                            """
tanks = 100 points and 20 progress                              
ipad = 2 points and 1 child   
                              """
                        )

                    self.tech.budget += int(action[1])
                    print(f"Research and Development budget set to {self.tech.budget}")
                case "recruit":
                    if action[1] * self.army.salary > self.econ.money:
                        print(
                            f"You can not afford to pay {action[1]} soldiers. The max you can afford is {round(self.econ.money/self.army.salary)}"
                        )
                        break
                    self.army.soldiers += action[1]
                    print(
                        f"you recruited {action[1]} soldiers, reducing your monthly income by ${action[1] * self.army.salary}"
                    )
                case "tax":
                    self.govt.taxrate = action[1]
                    print(f"Taxes have been set to {action[1]}%")
                    print(
                        f"Tax revenue increased to {self.govt.population * self.govt.taxrate}"
                    )
                case "economy":
                    
                case "army":
                    print(str(self.army))
                case "government":
                    print(str(self.govt))
                case "map":
                    showpolmap(str(0.01))
                case "end":
                    # end turn behavior
                    break
                case "escape":
                    raise
                case _:
                    print(f"command '{action[0]}' not found")

    def attack(self, defender):
        attackpower = self.army.morale * self.tech.points
        defendpower = defender.army.morale * defender.tech.points
        print(self.army.soldiers * attackpower + defender.army.soldiers * defendpower)


france = countries(
    government(population=40_000_000, alliance="allies"),
    economy(money=150_000_000_000),
    technology(),
    military(soldiers=4_000_000),
    name="france",
    id=0,
    symbol="#",
)
uk = countries(
    government(population=45_000_000, alliance="allies"),
    economy(money=225_000_000_000),
    technology(),
    military(soldiers=730_000),
    name="uk",
    id=1,
    symbol="&;",
)
serbia = countries(
    government(population=4_500_000, alliance="allies"),
    economy(money=8_000_000),
    technology(),
    military(soldiers=707_000),
    name="serbia",
    id=2,
    symbol="^",
)
russia = countries(
    government(population=167_000_000, alliance="allies"),
    economy(money=232_000_000),
    technology(),
    military(soldiers=5_500_000),
    name="russia",
    id=3,
    symbol="!",
)
italy = countries(
    government(population=36_000_000, alliance="allies"),
    economy(money=70_000_000),
    technology(),
    military(soldiers=1_200_000),
    name="italy",
    id=4,
    symbol="*",
)
austriahungary = countries(
    government(population=52_000_000, alliance="axis"),
    economy(money=120_000_000_000),
    technology(),
    military(soldiers=3_000_000),
    name="austriahungary",
    id=5,
    symbol="(",
)
germany = countries(
    government(population=68_000_000, alliance="axis"),
    economy(money=237_000_000_000),
    technology(),
    military(soldiers=3_800_000),
    name="germany",
    id=6,
    symbol="$",
)
bulgaria = countries(
    government(population=4_700_000, alliance="axis"),
    economy(money=11_000_000_000),
    technology(),
    military(soldiers=600_000),
    name="bulgaria",
    id=7,
    symbol="@",
)
ottomanempire = countries(
    government(population=23_000_000, alliance="axis"),
    economy(money=30_000_000_000),
    technology(),
    military(soldiers=1_000_000),
    name="ottomanempire",
    id=8,
    symbol="+",
)
# add development somehow
nations = [
    france,
    uk,
    serbia,
    russia,
    italy,
    austriahungary,
    germany,
    bulgaria,
    ottomanempire,
    #    player,
]


def showpolmap(animatetime=0):
    mapstring = ""
    if animatetime > 0:
        line = ""
        for i in map_data:
            line = ""
            time.sleep(animatetime)
            for j in i:
                if j["symbol"] == "\n":
                    continue
                line = line + j["symbol"]
            print(line)
    else:
        for i in map_data:
            for j in i:
                mapstring = mapstring + j["symbol"]
        print(mapstring)


print("Press 1 to choose France               Easy")
print("Press 2 to choose United Kingdom       Easy")
print("Press 3 to choose Serbia               Hard")
print("Press 4 to choose Russia               Medium")
print("Press 5 to choose Italy                Medium")
print("Press 6 to choose Austria Hungary      Medium")
print("Press 7 to choose Germany              Easy")
print("Press 8 to choose Bulgaria             Hard")
print("Press 9 to choose Ottoman Empire       Medium")
nationselect = int(input("Choose your nation: ")) - 1
for i in nations:
    if i.id == nationselect:
        player = i

print(f"You have chosen {player.name}")
print("Type 'tutorial' at any action point to get a tutorial.")

while True:
    player.turn()
