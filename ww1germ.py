import math
import time
import random
import json
import matplotlib.pyplot as plt

# the game works but is like super unfinished
try:
    with open("ww1game\\map_data.json", "r") as f:
        map_data = json.load(f)
except:
    with open("map_data.json", "r") as f:
        map_data = json.load(f)

if __name__ != "__main__":
    quit()

mapcols = len(map_data[0])
maprows = len(map_data)

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
        war_deaths=[],
        morale=1,
        salary=10,  # balance salary and all these default values at some point
        parent=None,
    ):
        self.soldiers = soldiers
        self.war_deaths = war_deaths
        self.morale = morale
        self.salary = salary
        self.parent = parent

    def recruit(self, amount):
        if amount * self.parent.army.salary > self.parent.econ.money:
            self.parent.player_print(
                "You can not afford to pay {:,} soldiers. The max you can afford is {:,} soldiers".format(
                    amount,
                    round(self.parent.econ.money / self.parent.army.salary),
                )
            )
            return
        if amount > (self.parent.govt.population - amount) / 4:
            self.parent.player_print(
                "Your country can not support 1/4 of the population being soldiers"
            )
        self.parent.army.soldiers += amount
        self.parent.govt.population -= amount
        self.parent.player_print(
            "you recruited {:,} soldiers, reducing your monthly income by ${:,}".format(
                amount, amount * self.parent.army.salary
            )
        )

    def attack(self, defender, force):
        if force > self.soldiers:
            self.parent.player_print("You do not have that many soldiers")
        if find_total_provinces(defender) == 0:
            print(f"{defender.name} has been defeated")
        # problem area vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # fmt: off
        attack_power = (force / 1.1) * self.parent.tech.combat_bonus * random.uniform(0.5, 0.8)
        defender_power = defender.army.soldiers / 5 * defender.tech.combat_bonus * random.uniform(0.5, 0.8)
        if defender.army.soldiers <= 0:
            for i in find_total_provinces(defender, True)[1]:
                map_data[i[1]][i[0]]["owner"] = self.parent
                map_data[i[1]][i[0]]["symbol"] = self.parent.symbol
            nations.remove(defender)
            print(f"{defender.name.capitalize()} has been defeated!")
            return
        # fmt: on

        ratio = attack_power / defender_power
        atkloss = min(round(attack_power / (ratio + 0.01)), force)
        defloss = round(defender_power * ratio)  # calculate casualties
        self.parent.player_print(f"Ratio: {ratio}")

        frontline_power[self.parent][defender] += ratio
        frontline_power[defender][self.parent] -= ratio
        province_gain = 0
        print(frontline_power[self.parent][defender])

        # find the number of provinces gained
        province_gain = math.floor(frontline_power[self.parent][defender])
        frontline_power[self.parent][defender] = frontline_power[self.parent][
            defender
        ] - math.floor(frontline_power[self.parent][defender])
        frontline_power[defender][self.parent] = frontline_power[defender][
            self.parent
        ] + math.floor(frontline_power[defender][self.parent])

        # problem area ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        for i in range(
            province_gain
        ):  # find and transfer ownership of conqured provinces to player
            neighbors = findborders(self.parent.symbol, defender.symbol)
            if len(neighbors) <= 0:
                break
            randomprovince = neighbors[random.randint(0, len(neighbors) - 1)]
            map_data[randomprovince[0]][randomprovince[1]]["owner"] = self
            map_data[randomprovince[0]][randomprovince[1]][
                "symbol"
            ] = self.parent.symbol
            defender.govt.province_count -= 1
            defender.govt.population -= (
                defender.govt.population / defender.govt.province_count
            )
        self.soldiers -= atkloss
        defender.army.soldiers -= defloss
        self.war_deaths.append(atkloss)
        defender.army.war_deaths.append(defloss)
        self.parent.player_print("You lost {:,} soldiers".format(atkloss))
        self.parent.player_print(
            defender.name.capitalize() + " lost {:,} soldiers".format(defloss)
        )
        self.parent.player_print(
            f"You have conqured {province_gain} provinces and {round(ratio * 21,4)} miles"
        )

    def update(self):
        if (
            self.soldiers > self.parent.govt.population / 4
        ):  # maybe keep rate as adjustable variable
            self.soldiers = self.parent.govt.population / 4
        if self.soldiers < 0:
            self.soldiers = 0

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
        taxerate=0.15,
        stability=100,
        targetstability=100,
        province_count=0,
        parent=None,
    ):
        self.population = population
        self.alliance = alliance
        self.taxrate = taxerate
        self.stability = stability
        self.targetstability = targetstability
        self.province_count = province_count
        self.parent = parent

    def check_stats(self):
        if self.parent.army.soldiers <= self.population / 10:
            print(
                f"Discarded {self.parent.army.soldiers - self.population / 10} soldiers because your population cannot sustain that many"
            )
            self.parent.army.soldiers = self.population / 10

        if self.econ.money <= 0:
            print(
                "The economy has collapsed! People are revolting, your military rebelling, and your government is unstable! The longer the nation's coffers are dry, the more of the country will be lost to rebels."
            )
            for i in range(self.province_count / 2):
                self.start_insurgency()

    def start_insurgency(self):
        province_count, allprovince = find_total_provinces(self.parent, returnall=True)
        startingtile = random.choice(allprovince)
        map_data[startingtile[1]][startingtile[0]]["symbol"] = insurgency.symbol
        map_data[startingtile[1]][startingtile[0]]["owner"] = insurgency
        insurgency.army.soldiers += (self.parent.govt.population / 10) / province_count

    def update(self):
        # fmt: off
        # bread prices, war deaths,
        taxdebuff = (100) / (1 + 0.93 ** (self.taxrate + math.sqrt(self.taxrate + 0.93) - 50))  # normalize (better imo)
        
        recent_war_deaths = 0
        for i in range(min(10, len(self.parent.army.war_deaths))):
            recent_war_deaths += self.parent.army.war_deaths[-i]
        deathdebuff = recent_war_deaths / self.population


        self.targetstability = 100 - taxdebuff - deathdebuff # - everything else too but mostly taxes i think
        # fmt: on
        # add other factors to stability, add domestic politics

    def new_turn(self):
        self.update()
        self.stability = self.stability + (self.targetstability - self.stability) * 0.6

        # insurgencies
        if self.stability < 25 and random.randint(0, 100) > self.stability:
            num_insurgencies = round(
                random.randint(0, round((1 / self.stability) * 25))
            )
            for i in range(num_insurgencies):
                self.parent.govt.start_insurgency()
            print(
                "An insurgency has begun!"
                if num_insurgencies == 1
                else f"{num_insurgencies} insurgencies have begun!"
            )

    def __str__(self):
        return f"""
Government Report:
Population Estimate: {"{:,}".format(self.population)}
Tax Rate: {self.taxrate * 100}%
Stability: {round(self.stability, 2)}%
targ: {self.targetstability}
"""


class Economy:
    def __init__(
        self,
        money,
        production=0,
        income=0,
        costs=0,
        parent=None,
        development=0.8,
    ):
        self.money = money
        self.production = production
        self.income = income
        self.costs = costs
        self.parent = parent
        self.development = development

    def invest(self, investment):
        self.development += investment / 10000000 / self.development
        self.money -= investment
        self.production += (
            investment / 15 / random.uniform(0.8, 1)
        )  # adjust, how long should games be

    def tax(self, rate):
        self.parent.govt.taxrate = rate / 100
        self.parent.player_print(f"Taxes have been set to {rate}%")
        self.parent.player_print("Tax revenue increased to ${:,}".format(tax_income))

    def update(self):
        global tax_income
        tax_income = (
            self.parent.govt.population * self.development * self.parent.govt.taxrate
        )
        self.income = tax_income + self.production
        self.costs = (
            self.parent.army.soldiers * self.parent.army.salary
            + self.parent.tech.budget
        )

    def __str__(self):
        return f"""
Economic report:
Total Available Wealth:   ${"{:,}".format(round(self.money))}
Total Profit:             ${"{:,}".format(round(self.income - self.costs))}
Tax Revenue:              ${"{:,}".format(round(tax_income))}
Production Revenue:       ${"{:,}".format(round(self.production))}
Total Costs:              ${"{:,}".format(round(self.costs))}
Military Personnel Costs: ${"{:,}".format(round(self.parent.army.soldiers * self.parent.army.salary))}
Research Budget:          ${"{:,}".format(round(self.parent.tech.budget))}
"""

    def new_turn(
        self,
    ):
        self.update()
        self.money += self.income - self.costs
        self.parent.resources += self.production
        self.update()


class Technology:
    def __init__(
        self,
        progress=0,
        points=0,
        budget=0,
        combat_bonus=1,
        parent=None,
    ):
        self.progress = progress
        self.points = points
        self.budget = budget
        self.combat_bonus = combat_bonus
        self.parent = parent

    def research(self, cost):
        self.budget = cost
        self.parent.player_print(
            "Research and Development budget set to {:,}".format(self.budget)
        )

    def update(self):
        self.combat_bonus += math.sqrt(self.budget)
        pass

    def new_turn(self):
        research_gain = self.budget / 1000
        self.progress += research_gain
        self.points += research_gain / 1000

    def __str__(self):
        return f"""
Technology Report:
Current Combat Bonus: {self.combat_bonus}
"""


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
        resources=0,
        is_player=False,
    ):
        self.govt = govt
        self.econ = econ
        self.tech = tech
        self.army = army
        self.name = name
        self.id = id
        self.symbol = symbol
        self.resources = resources
        self.is_player = is_player

        self.econ.parent = self
        self.govt.parent = self
        self.army.parent = self
        self.tech.parent = self

    def player_print(self, content):
        if self.is_player:
            print(content)

    def make_decision(self):  # it is completely random rn, no i just a
        outputs = [
            "attack",
            "recruit",
            "tax",
            "end",
            "end",
            "end",
        ]
        decision = random.choice(outputs)
        subject = None
        if self.econ.money < 0:
            self.army.soldiers -= abs(self.econ.money) / self.army.salary
            self.econ.money = 0
        if self.army.soldiers < 0:
            self.army.soldiers = 0
            decision = random.choice(outputs)
        for i in nations:
            if len(findborders(self.symbol, i.symbol)) > 0:
                subject = i
        if decision == "attack":
            action = ["attack", subject, random.randint(0, int(self.army.soldiers))]
        elif decision == "recruit":
            action = [
                "recruit",
                random.randint(0, round(self.econ.money / self.army.salary)),
            ]
        elif decision == "end":
            action = ["end", None]
        elif decision == "tax":
            action = ["tax", random.randint(0, 100)]
        return action

    def turn(self):
        print(f"{self.name}'s turn:")
        global turn_number
        self.econ.new_turn()
        self.govt.new_turn()
        self.tech.new_turn()
        self.army.new_turn()
        while True:
            if self.is_player:
                subject = None
                self.econ.update()
                actionInput = input("What's your next move?: ").lower().strip()
                action = actionInput.split(" ")
                if len(action) > 1:
                    for i in nations:
                        if i.name == action[1]:
                            subject = i
            else:
                action = self.make_decision()
                subject = None
                for i in nations:
                    if i.name == action[1]:
                        subject = i
            match action[0]:
                case "insurgency":
                    self.govt.start_insurgency()
                case "attack":
                    if subject == None:
                        self.player_print(f"{action[1]} is not a country")
                        break
                    if len(action) <= 2:
                        self.player_print(
                            "Include the number of people invading after target (assuming 1 person)"
                        )
                        self.army.attack(subject, 1)
                        break
                    else:
                        self.player_print(subject)
                        self.army.attack(subject, int(action[2].replace(",", "")))
                case "research":
                    self.tech.research(int(action[1]))
                case "tech":
                    self.player_print(str(self.tech))
                case "recruit":
                    self.army.recruit(int(action[1]))
                case "tax":
                    self.econ.tax(int(action[1]))
                case "economy":
                    self.player_print(str(self.econ))
                case "invest":
                    self.econ.invest(int(action[1]))
                case "army":
                    self.player_print(str(self.army))
                case "government":
                    self.player_print(str(self.govt))
                case "map":
                    if len(action) > 1:
                        if action[1] == "terrain":
                            showpolmap(animatetime=0, display="terrain")
                        else:
                            showpolmap(animatetime=0, display="political")
                    else:
                        showpolmap(animatetime=0, display="political")
                case "tutorial":
                    self.player_print(
                        "Welcome to ww1germ.py. there is no tutorial rn my bad."
                    )
                case "end":
                    # end turn behavior
                    break
                case "name":
                    print(self.name)
                case "escape" | "python" | "clear":
                    quit()
                case _:
                    self.player_print(f"command '{action[0]}' not found")


def findborders(owner, target):
    neighbors = []
    for y in range(maprows):
        for x in range(mapcols):
            if map_data[y][x]["symbol"] == owner:
                if checkneighbors(x, y, target) == "someshitwentwrong":
                    return "someshitwentwrong"
                for i in checkneighbors(x, y, target):
                    if i in neighbors:
                        continue
                    neighbors.append(i)
    return neighbors


def checkneighbors(x, y, target):
    neighbors = []
    for dx in range(-1, 2, 2):
        if dx + x >= 111:
            continue
        for dy in range(-1, 2, 2):
            if dy + y >= 26:
                continue
            try:
                if map_data[y + dy][x + dx]["symbol"] == target:
                    neighbors.append((y + dy, x + dx))
            except:
                print(
                    f"y: {y}, dy: {dy}, rows: {maprows}, cols: {mapcols}\nx: {x}, dx: {dx}"
                )
                print(map_data[y + dy][x + dx])
                print("rompo")
                showpolmap()
                quit()
                return "someshitwentwrong"
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
    government(population=1, alliance="insurgency"),
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


def showpolmap(
    display,
    animatetime=0,
):
    mapstring = ""
    if int(animatetime) > 0:
        line = ""
        for i in map_data:
            line = ""
            time.sleep(animatetime)
            for j in i:
                if j["symbol"] == "\n":
                    continue
                if display == "terrain":
                    line = line + j["symbol"]
                else:
                    line = line + j["terrain"]
            print(line)
    else:
        for i in map_data:
            for j in i:
                if display == "terrain":
                    mapstring = mapstring + j["terrain"]
                else:
                    mapstring = mapstring + j["symbol"]
        print(mapstring)


print("Press 1 to choose France               Easy")
print(
    "Press 2 to choose United Kingdom       Easy (does not work cause they have no land borders)"
)
print("Press 3 to choose Serbia               Hard")
print("Press 4 to choose Russia               Medium")
print("Press 5 to choose Italy                Medium")
print("Press 6 to choose Austria Hungary      Medium")
print("Press 7 to choose Germany              Easy")
print("Press 8 to choose Bulgaria             Hard")
print("Press 9 to choose Ottoman Empire       Medium")
print("Press 10 to be a bot")

if __name__ == "__main__":
    player = nations[int(input("Choose your nation: ")) - 1]
    if player.name == insurgency.name:
        simulation = True
    else:
        player.is_player = True
        print(f"You have chosen {player.name}")
        print("Type 'tutorial' at any action point to get a tutorial.")

# delete this when opponent ai is a thing
for i in nations:
    i.is_player = True

turn_number = 0

graph_data = {
    "france": [],
    "germany": [],
    "serbia": [],
    "bulgaria": [],
    "austriahungary": [],
    "ottomanempire": [],
    "uk": [],
    "russia": [],
    "italy": [],
    "insurgency": [],
}


def record_soldiers():
    for i in nations:
        graph_data[i.name].append((turn_number, [i.army.soldiers, i.govt.population]))


def show_graph(nation):
    xpoints = []
    ysoldiers = []
    ypopulation = []
    ypopulationcap = []
    for i in graph_data[nation.name]:
        xpoints.append(i[0])
        ysoldiers.append(i[1][0])
        ypopulation.append(i[1][1])
        ypopulationcap.append(i[1][1] / 4)
    plt.plot(xpoints, ysoldiers)
    plt.plot(xpoints, ypopulation)
    plt.plot(xpoints, ypopulationcap)
    plt.legend(["soldiers", "population", "population cap"])
    plt.show()


if True:
    for i in range(1000):
        turn_number += 1
        print(f"Turn {turn_number}")
        france.turn()
        # uk.turn()
        serbia.turn()
        russia.turn()
        italy.turn()
        austriahungary.turn()
        germany.turn()
        bulgaria.turn()
        ottomanempire.turn()
        insurgency.turn()
        record_soldiers()
        if turn_number % 10 == 0:
            showpolmap()
            while True:
                action = input(
                    "Enter to continue, or type name of nation for to graph their stats: "
                )
                if action == "":
                    break
                for i in nations:
                    if i.name == action:
                        show_graph(i)
