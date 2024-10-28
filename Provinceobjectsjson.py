import json

# fmt: off
map = [['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', '%', '%', '%', '%', '%', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], [' ', ' ', ' ', '\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', '%', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '&', '&', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', '%', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '&', '&', '&', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', ' ', ' ', '&', '&', '&', '&', '&', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', ' ', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '$', '$', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', '&', '&', '&', '&', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '$', '$', '$', '$', '$', '$', '$', '$', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', ' ', ' ', ' ', ' ', '&', '&', '&', '&', '&', '&', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '&', '&', '&', '&', '&', '&', '&', '&', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '$', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '$', '$', '$', '$', '$', '$', '$', '$', '$', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '#', '#', '#', '#', '%', '%', '%', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '%', '$', '$', '$', '$', '$', '$', '$', '$', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' '], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '%', '%', '%', '%', '%', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' '], [' ', '\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '*', '*', '*', '*', '*', '*', '*', '*', '*', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '^', '^', '^', '^', '%', '%', '%', '%', '%', '@', '@', '@', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '%', '%', '%', '%', '#', '#', '#', '#', '#', '#', ' '], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', '*', '*', '*', '*', '*', '*', '*', '*', '*', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '^', '^', '^', '^', '^', '@', '@', '@', '@', '@', '@', '@', '@', '@', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', '*', '*', '*', '*', '*', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '^', '^', '^', '^', '@', '@', '@', '@', '@', '(', '(', '(', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '*', '*', '*', '*', '*', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', '*', '*', '*', '*', '*', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', '*', '*', '*', '*', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', '*', '*', '*', ' ', ' ', '*', '*', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '('], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '('], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'], ['\n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'], ['\n', ' ', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%'], ['\n', ' ', ' ', ' ', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '(', '(', '(', '(', '(', '(', '(', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%']]
# fmt: on

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

objmap = []
line = []


def coordstoobj():
    for y, l in enumerate(map):
        line = []
        for x, n in enumerate(l):
            line.append(
                {
                    "owner": symbols[n],
                    "symbol": n,
                    "terrain": "_",
                }
            )
        objmap.append(line)


coordstoobj()
print(json.dumps(objmap))

with open("ww1game\map_data.json", "w") as f:
    json.dump(objmap, f, indent=4)
