import math
import time
import random
import json

counter = 2
nations = []

map_data = ""

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
Soldiers: {"{:,}".format(self.soldiers)}
Morale: {self.morale}%
Salary: {"{:,}".format(self.salary)}$ Per month
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
            self.stability - (1 / 100 * (self.taxrate + 20) ** 2 + 10)
        ) / 2
        # add other factors to stability, add domestic politics

    def __str__(self):
        return f"""
Government Report:
Population: {"{:,}".format(self.population)}
Tax: {self.taxrate}%
Political Unrest: {100 - self.stability}%
"""


class Economy:
    def __init__(
        self,
        money,
        income=0,
        costs=0,
        Parent=None,
    ):
        self.money = money
        self.income = income
        self.costs = costs
        self.Parent = Parent

    def update(self,):
        self.income = self.Parent.Govt.population * self.Parent.Govt.taxrate
        self.costs = self.Parent.Army.soldiers * self.Parent.Army.salary + self.Parent.Tech.budget

    def newturn(self,):
        self.update()
        self.money += self.income - self.costs
        self.update()

    def __str__(self):
        return f"""Economic report:
Total available wealth: {"{:,}".format(self.money)}
Profit: {"{:,}".format(self.income - self.costs)}
Tax Revenue: {"{:,}".format(self.Parent.Govt.population * self.Parent.Govt.taxrate)}
Costs: {"{:,}".format(self.costs)}
Personnel Costs: {"{:,}".format(self.Parent.Army.soldiers * self.Parent.Army.salary)}
Research Budget: {"{:,}".format(self.Parent.Tech.budget)}
"""


class Technology:
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
        Govt,
        Econ,
        Tech,
        Army,
        name,
        id,
        symbol,
    ):
        self.Govt = Govt
        self.Econ = Econ
        self.Tech = Tech
        self.Army = Army
        self.name = name
        self.id = id
        self.symbol = symbol

        self.Econ.Parent = self

    def turn(self):
        self.Econ.newturn()
        self.Govt.update()
        print("new turn")
        while True:
            self.Econ.update()
            actionInput = input("What's your next move?: ").lower().strip()
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
                    if action[1] == "shop":
                        print(
                            """
tanks = 100 points and 20 progress                              
ipad = 2 points and 1 child   
                              """
                        )

                    self.Tech.budget += int(action[1])
                    print(
                        "Research and Development budget set to {:,}".format(
                            self.Tech.budget
                        )
                    )
                case "recruit":
                    if int(action[1]) * self.Army.salary > self.Econ.money:
                        print(
                            "You can not afford to pay {:,} soldiers. The max you can afford is {:,} soldiers".format(
                                int(action[1]),
                                round(self.Econ.money / self.Army.salary),
                            )
                        )
                        break
                    self.Army.soldiers += int(action[1])
                    print(
                        "you recruited {:,} soldiers, reducing your monthly income by ${:,}".format(
                            int(action[1]), int(action[1]) * self.Army.salary
                        )
                    )
                case "tax":
                    self.Govt.taxrate = int(action[1])
                    print(f"Taxes have been set to {action[1]}%")
                    print(
                        "Tax revenue increased to ${:,}".format(
                            self.Govt.population * self.Govt.taxrate
                        )
                    )
                case "economy":
                    print(str(self.Econ))
                case "army":
                    print(str(self.Army))
                case "government":
                    print(str(self.Govt))
                case "map":
                    showpolmap(0.01)
                case "end":
                    # end turn behavior
                    break
                case "escape":
                    raise
                case _:
                    print(f"command '{action[0]}' not found")

    def attack(self, defender):
        attackpower = self.Army.morale * self.Tech.points
        defendpower = defender.Army.morale * defender.Tech.points
        print(self.Army.soldiers * attackpower + defender.Army.soldiers * defendpower)


france = countries(
    government(population=40_000_000, alliance="allies"),
    Economy(money=150_000_000_000),
    Technology(),
    military(soldiers=4_000_000),
    name="france",
    id=0,
    symbol="#",
)
uk = countries(
    government(population=45_000_000, alliance="allies"),
    Economy(money=225_000_000_000),
    Technology(),
    military(soldiers=730_000),
    name="uk",
    id=1,
    symbol="&;",
)
serbia = countries(
    government(population=4_500_000, alliance="allies"),
    Economy(money=8_000_000),
    Technology(),
    military(soldiers=707_000),
    name="serbia",
    id=2,
    symbol="^",
)
russia = countries(
    government(population=167_000_000, alliance="allies"),
    Economy(money=232_000_000),
    Technology(),
    military(soldiers=5_500_000),
    name="russia",
    id=3,
    symbol="!",
)
italy = countries(
    government(population=36_000_000, alliance="allies"),
    Economy(money=70_000_000),
    Technology(),
    military(soldiers=1_200_000),
    name="italy",
    id=4,
    symbol="*",
)
austriahungary = countries(
    government(population=52_000_000, alliance="axis"),
    Economy(money=120_000_000_000),
    Technology(),
    military(soldiers=3_000_000),
    name="austriahungary",
    id=5,
    symbol="(",
)
germany = countries(
    government(population=68_000_000, alliance="axis"),
    Economy(money=237_000_000_000),
    Technology(),
    military(soldiers=3_800_000),
    name="germany",
    id=6,
    symbol="$",
)
bulgaria = countries(
    government(population=4_700_000, alliance="axis"),
    Economy(money=11_000_000_000),
    Technology(),
    military(soldiers=600_000),
    name="bulgaria",
    id=7,
    symbol="@",
)
ottomanempire = countries(
    government(population=23_000_000, alliance="axis"),
    Economy(money=30_000_000_000),
    Technology(),
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
player = nations[int(input("Choose your nation: ")) - 1]

print(f"You have chosen {player.name}")
print("Type 'tutorial' at any action point to get a tutorial.")

while True:
    player.turn()
