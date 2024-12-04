import math
import time
import random
import json

counter = 2
nations = []

with open("ww1game\map_data.json", "r") as f:
    map_data = json.load(f)

symbols = {
    "&": "uk",
    "$": "germany",
    "^": "serbia",
    "*": "italy",
    "@": "bulgaria",
    "#": "france",
    "!": "russia",
    "(": "austriahungary",
    "+": "ottomanempire",
    "\n": "newline",
    "%": "neutral",
    " ": "ocean",
}


class military:
    def __init__(
        self,
        soldiers,
        morale=1,
        salary=10,  # balance salary and all these default values at some point
        provincedefence=dict(),
    ):
        self.soldiers = soldiers
        self.morale = morale
        self.salary = salary
        self.provincedefence = provincedefence

    def update(self):
        pass

    def new_turn(self):
        pass

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
        stability=0,
        targetstability=100,
        provincecount=0,
    ):
        self.population = population
        self.alliance = alliance
        self.taxrate = taxerate
        self.stability = stability
        self.targetstability = targetstability
        self.provincecount = provincecount

    def update(
        self,
    ):
        self.targetstability = (1 / 100) * (self.taxrate + 20) ** 2 + 10
        # add other factors to stability, add domestic politics

    def new_turn(self):
        self.stability = self.stability + (self.targetstability - self.stability) * 0.6

    def __str__(self):
        return f"""
Government Report:
Population Estimate: {"{:,}".format(self.population)}
Tax Rate: {self.taxrate}%
Political Unrest: {round(self.stability, 2)}%
targ: {self.targetstability}
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

    def update(
        self,
    ):
        self.income = self.Parent.Govt.population * self.Parent.Govt.taxrate
        self.costs = (
            self.Parent.Army.soldiers * self.Parent.Army.salary
            + self.Parent.Tech.budget
        )

    def new_turn(
        self,
    ):
        self.update()
        self.money += self.income - self.costs
        self.update()

    def __str__(self):
        return f"""
Economic report:
Total Available Wealth: ${"{:,}".format(self.money)}
Total Profit: ${"{:,}".format(self.income - self.costs)}
Tax Revenue: ${"{:,}".format(self.Parent.Govt.population * self.Parent.Govt.taxrate)}
Total Costs: ${"{:,}".format(self.costs)}
Military Personnel Costs: ${"{:,}".format(self.Parent.Army.soldiers * self.Parent.Army.salary)}
Research Budget: ${"{:,}".format(self.Parent.Tech.budget)}
"""


class Technology:
    def __init__(
        self,
        progress=0,
        points=0,
        budget=0,
        combat_bonus=1,
    ):
        self.progress = progress
        self.points = points
        self.budget = budget
        self.combat_bonus = combat_bonus

    def update(self):
        pass

    def new_turn(self):
        research_gain = self.budget / 1000
        self.progress += research_gain
        self.points += research_gain / 1000


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
        self.Econ.new_turn()
        self.Govt.new_turn()
        self.Tech.new_turn()
        self.Army.new_turn()
        print("new turn")
        while True:
            subject = None
            self.Econ.update()
            actionInput = input("What's your next move?: ").lower().strip()
            action = actionInput.split(" ")
            if len(action) > 1:
                for i in nations:
                    if i.name == action[1]:
                        subject = i
            match action[0]:
                case "attack":
                    if subject == None:
                        print(f"{action[1]} is not a country")
                        break
                    if len(action) <= 2:
                        print(
                            "Include the number of people invading after target (assuming 1 person)"
                        )
                        self.attack(subject, 1)
                        break
                    else:
                        print(subject)
                        self.attack(subject, int(action[2].replace(",", "")))
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

                    elif action[1].isnumeric() == True:
                        self.Tech.budget = int(action[1])
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
                    if len(action) > 1:
                        showpolmap()
                    else:
                        showpolmap(0.01)
                case "tutorial":
                    print("Welcome to ww1germ.py. there is no tutorial rn my bad.")
                case "end":
                    # end turn behavior
                    break
                case "escape" | "python" | "clear":
                    raise ""
                case _:
                    print(f"command '{action[0]}' not found")

    def attack(self, defender, force):
        if force > self.Army.soldiers:
            print("You do not have that many soldiers, but infinite soldiers for debug")
        if findtotalprovinces(defender) == 0:
            print(f"{defender.name} has been defeated")
        # problem area vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # fmt: off
        attackpower = force * self.Tech.combat_bonus * random.uniform(0.5, 0.8)
        if defender.Army.soldiers <= 0:
            print(f"{defender.name} has 0 soldiers; iron out this exception once this function makes some semblance of sense")
            return
        defenderpower = defender.Army.soldiers / 5 * defender.Tech.combat_bonus * random.uniform(0.5, 0.8)
        # fmt: on

        ratio = attackpower / defenderpower
        atkloss = min(round(attackpower / ratio), force)
        defloss = round(defenderpower * ratio)  # calculate casualties
        print(f"Ratio: {ratio}")

        frontlinepower[self][defender] += ratio
        frontlinepower[defender][self] -= ratio
        provincegain = 0

        # find the number of provinces gained
        provincegain = math.floor(frontlinepower[self][defender])
        frontlinepower[self][defender] = frontlinepower[self][defender] - math.floor(
            frontlinepower[self][defender]
        )
        frontlinepower[defender][self] = frontlinepower[defender][self] + math.floor(
            frontlinepower[defender][self]
        )

        # problem area ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        for i in range(
            provincegain
        ):  # find and transfer ownership of conqured provinces to player
            neighbors = findborders(self.symbol, defender.symbol)
            if len(neighbors) <= 0:
                break
            randomprovince = neighbors[random.randint(0, len(neighbors) - 1)]
            map_data[randomprovince[0]][randomprovince[1]]["owner"] = self
            map_data[randomprovince[0]][randomprovince[1]]["symbol"] = self.symbol
        self.Army.soldiers -= atkloss
        defender.Army.soldiers -= defloss
        print("You lost {:,} soldiers".format(atkloss))
        print(
            defender.name.capitalize(), "lost {:,} soldiers".format(defloss)
        )  # output results of battle

        print(f"You have conqured {provincegain} provinces (supposedly)")


def findborders(owner, target):
    neighbors = []
    rows = len(map_data)
    cols = len(map_data[0])
    for y in range(rows):
        for x in range(cols):
            if map_data[y][x]["symbol"] == owner:
                for i in checkneighbors(x, y, target):
                    if i in neighbors:
                        continue
                    neighbors.append(i)
    return neighbors


def checkneighbors(x, y, target):
    neighbors = []
    for dx in range(-1, 2, 2):
        for dy in range(-1, 2, 2):
            if map_data[y + dy][x + dx]["symbol"] == target:
                neighbors.append((y + dy, x + dx))
    return neighbors


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
]

frontlinepower = dict()
for i in nations:
    frontlinepower[i] = dict()
    for n in nations:
        frontlinepower[i][n] = 0


def findtotalprovinces(target):
    count = 0
    for i in map_data:
        for j in i:
            if j["symbol"] == target.symbol:
                count += 1
    return count


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
