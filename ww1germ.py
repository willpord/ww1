import math
import time
import random
import json

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
    "!": "insurgency",
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
        stability=100,
        targetstability=100,
        provincecount=0,
        Parent=None,
    ):
        self.population = population
        self.alliance = alliance
        self.taxrate = taxerate
        self.stability = stability
        self.targetstability = targetstability
        self.provincecount = provincecount
        self.Parent = Parent

    def start_insurgency(self):
        provincecount, allprovince = find_total_provinces(self.Parent, returnall=True)
        startingtile = random.choice(allprovince)
        map_data[startingtile[1]][startingtile[0]]["symbol"] = insurgency.symbol
        map_data[startingtile[1]][startingtile[0]]["owner"] = insurgency
        insurgency.army.soldiers += (self.Parent.Govt.population / 10) / provincecount
        print("An insurgency has begun (by force)!")

    def update(self):
        # fmt: off
        # bread prices, war deaths, 
        self.taxrate /= 100
        taxdebuff = self.targetstability = 1 - (1 / 100) * (self.taxrate + 20) ** 2 + 10 # quadratic
        taxdebuff = (100) / (1 + 0.93 ** (self.taxrate + math.sqrt(self.taxrate + 0.93) - 50))  # normalize (better imo)
        self.targetstability = 100 - taxdebuff # - everything else too but mostly taxes i think
        
        self.taxrate *= 100
        # fmt: on
        # add other factors to stability, add domestic politics

    def new_turn(self):
        self.update()
        self.stability = self.stability + (self.targetstability - self.stability) * 0.6
        if self.stability < 25 and random.randint(0, 100) < self.stability:
            self.Parent.Govt.start_insurgency()
            print("An insurgency has begun!")

    def __str__(self):
        return f"""
Government Report:
Population Estimate: {"{:,}".format(self.population)}
Tax Rate: {self.taxrate}%
Stability: {round(self.stability, 2)}%
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
            self.Parent.army.soldiers * self.Parent.army.salary
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
Military Personnel Costs: ${"{:,}".format(self.Parent.army.soldiers * self.Parent.army.salary)}
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
        self.combat_bonus = 1
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
        army,
        name,
        id,
        symbol,
        is_player=False,
    ):
        self.Govt = Govt
        self.Econ = Econ
        self.Tech = Tech
        self.army = army
        self.name = name
        self.id = id
        self.symbol = symbol
        self.is_player = is_player

        self.Econ.Parent = self
        self.Govt.Parent = self

    def turn(self):
        global turn_number
        self.Econ.new_turn()
        self.Govt.new_turn()
        self.Tech.new_turn()
        self.army.new_turn()
        print(f"Turn {turn_number}")
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
                case "insurgency":
                    self.Govt.start_insurgency()
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
                    if action[1].isnumeric() == True:
                        self.Tech.budget = int(action[1])
                        print(
                            "Research and Development budget set to {:,}".format(
                                self.Tech.budget
                            )
                        )
                case "recruit":
                    if int(action[1]) * self.army.salary > self.Econ.money:
                        print(
                            "You can not afford to pay {:,} soldiers. The max you can afford is {:,} soldiers".format(
                                int(action[1]),
                                round(self.Econ.money / self.army.salary),
                            )
                        )
                        break
                    self.army.soldiers += int(action[1])
                    print(
                        "you recruited {:,} soldiers, reducing your monthly income by ${:,}".format(
                            int(action[1]), int(action[1]) * self.army.salary
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
                    print(str(self.army))
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
                    quit()
                case _:
                    print(f"command '{action[0]}' not found")

    def attack(self, defender, force):
        if force > self.army.soldiers:
            print("You do not have that many soldiers, but infinite soldiers for debug")
        if find_total_provinces(defender) == 0:
            print(f"{defender.name} has been defeated")
        # problem area vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # fmt: off
        attack_power = force * self.Tech.combat_bonus * random.uniform(0.5, 0.8)
        if defender.army.soldiers <= 0:
            print(f"{defender.name} has 0 soldiers; iron out this exception once this function makes some semblance of sense (making their soldiers 1)")
            defender.army.soldiers
            return
        defender_power = defender.army.soldiers / 5 * defender.Tech.combat_bonus * random.uniform(0.5, 0.8)
        # fmt: on

        ratio = attack_power / defender_power
        atkloss = min(round(attack_power / ratio), force)
        defloss = round(defender_power * ratio)  # calculate casualties
        print(f"Ratio: {ratio}")

        frontline_power[self][defender] += ratio
        frontline_power[defender][self] -= ratio
        province_gain = 0

        # find the number of provinces gained
        province_gain = math.floor(frontline_power[self][defender])
        frontline_power[self][defender] = frontline_power[self][defender] - math.floor(
            frontline_power[self][defender]
        )
        frontline_power[defender][self] = frontline_power[defender][self] + math.floor(
            frontline_power[defender][self]
        )

        # problem area ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        for i in range(
            province_gain
        ):  # find and transfer ownership of conqured provinces to player
            neighbors = findborders(self.symbol, defender.symbol)
            if len(neighbors) <= 0:
                break
            randomprovince = neighbors[random.randint(0, len(neighbors) - 1)]
            map_data[randomprovince[0]][randomprovince[1]]["owner"] = self
            map_data[randomprovince[0]][randomprovince[1]]["symbol"] = self.symbol
        self.army.soldiers -= atkloss
        defender.army.soldiers -= defloss
        print("You lost {:,} soldiers".format(atkloss))
        print(
            defender.name.capitalize(), "lost {:,} soldiers".format(defloss)
        )  # output results of battle

        print(f"You have conqured {province_gain} provinces (supposedly)")


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


a = random.uniform


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
insurgency = countries(
    government(population=0, alliance="insurgency"),
    Economy(money=0),
    Technology(),
    military(soldiers=0),
    name="insurgency",
    id=9,
    symbol="!",
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
    insurgency,
]

frontline_power = dict()
for i in nations:
    frontline_power[i] = dict()
    for n in nations:
        frontline_power[i][n] = 0


def find_total_provinces(
    target,
    returnall=False,
):
    allprovinces = []
    count = 0
    for y, i in enumerate(map_data):
        for x, j in enumerate(i):
            if j["symbol"] == target.symbol:
                if returnall:
                    allprovinces.append((x, y))
                count += 1
    if returnall:
        return (count, allprovinces)
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
player.is_player = True

print(f"You have chosen {player.name}")
print("Type 'tutorial' at any action point to get a tutorial.")

turn_number = 0
while True:
    turn_number += 1
    player.turn()
while False:
    turn_number += 1
    france.turn()
    uk.turn()
    serbia.turn()
    russia.turn()
    italy.turn()
    austriahungary.turn()
    germany.turn()
    bulgaria.turn()
    ottomanempire.turn()
