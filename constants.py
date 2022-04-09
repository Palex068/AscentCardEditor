varaibles = open("data/varaibles.txt", "r+")

# Бинды

HK_EXIT = "Ctrl+W"
HK_EXIT_BIND = "<Control-w>"

HK_OPEN = "Ctrl+O"
HK_OPEN_BIND = "<Control-o>"

# Шрифты

MAINFONT = ("Arial", 11)
SUBFONT = ("Courier New", 12)

# Цветовая тема

CT_MAIN = ["#a0a0a0", "#0e0211", "#e2f0ff", "#4b5c2b"]
CT_SUB = ["#d0d0d0", "#1e1122", "#f1f8ff", "#808f65"]
CT_EXTRA = ["#ffffff", "#2e2032", "#ffffff", "#aab498"]
CT_TEXT = ["#000000", "#ffffff", "#000000", "#ffffff"]
CT = 0

# Значения карт

COLORS = varaibles.readline().split(", ")
CARDTYPES = varaibles.readline().split(", ")
FRACTIONS = varaibles.readline()[0:-1].split(", ")
CREATURETYPES = varaibles.readline()[0:-1].split(", ")
ORDERTYPES = varaibles.readline().split(", ")
RELICTYPES = varaibles.readline().split(", ")
KEYWORDS = varaibles.readline()[0:-1].split(", ")

CARDSUBTYPES = [" — "]
CARDSUBTYPES.append(ORDERTYPES[-1])
for i in ORDERTYPES:
    CARDSUBTYPES.append(i)
for i in RELICTYPES:
    CARDSUBTYPES.append(i)
for i in FRACTIONS:
    CARDSUBTYPES.append(i)
CARDSUBTYPES.append(ORDERTYPES[-1])
for i in CREATURETYPES:
    for j in FRACTIONS:
        CARDSUBTYPES.append(i + " — " + j)

varaibles.close()

keywords = open("data/keywords.txt", "r+")

INSERTABLE_KEYWORDS = {}

line = keywords.readline()

while line != "":

    line = line[0:-1].split("=")
    INSERTABLE_KEYWORDS[line[0]] = line[1]

    line = keywords.readline()

keywords.close()