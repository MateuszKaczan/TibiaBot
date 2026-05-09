import pyautogui as pg
import time

pg.useImageNotFoundException(False)


print("Za 5 sekund pokaże pozycję kursora...")
time.sleep(5)

while True:
    x, y = pg.position()
    print(f"Pozycja kursora: X={x:4d}  Y={y:4d}   |   Naciśnij Ctrl+C aby zatrzymać")
    time.sleep(0.5)


# venv\Scripts\activate
# py main.py


flags = [
    {"path": "./images/flags/flag_6.png", "wait": 5},
    {"path": "./images/flags/flag_1.png", "wait": 3},
    {"path": "./images/flags/flag_4.png", "wait": 2},
    {"path": "./images/flags/flag_1.png", "wait": 1},
    {"path": "./images/flags/flag_2.png", "wait": 6},
    {"path": "./images/flags/flag_3.png", "wait": 5},
    {"path": "./images/flags/flag_5.png", "wait": 4},
    {"path": "./images/flags/flag_7.png", "wait": 4},
    {"path": "./imtfages/flags/flag_8.png", "wait": 3},
    # {"path": "./images/flags/flag_2.png", "wait": 2},
    # {"path": "./images/flags/flag_6.png", "wait": 15},
    # {"path": "./images/flags/flag_5.png", "wait": 10},
    # {"path": "./images/flags/flag_8.png", "wait": 10},
    # {"path": "./images/flags/flag_3.png", "wait": 10},
    # {"path": "./images/flags/flag_2.png", "wait": 10},
    # {"path": "flag_5.png", "wait": 7},
]

items = [
    {"path": "./images/items/mace.png"},
    {"path": "./images/items/sword.png"},
    {"path": "./images/items/ham.png"},
]

MAPA_REGION = (1751, 27, 106, 106)
BATTLE_REGION = (1560, 27, 180, 310)
BACKPACK_REGION = (1744, 462, 172, 439)

MANA_REGION = (856, 28, 250, 12)
HEALTH_REGION_LOW = (260, 28, 100, 10)
HEALTH_REGION_NOT_FULL = (535, 28, 160, 10)

STATUS_REGION = (1752, 286, 100, 9)

RED_COLOR = (233, 0, 0)
PINK_COLOR = (186, 96, 96)
colors = [RED_COLOR, PINK_COLOR]

# x = 3330
x = 1591
y = 362

# -------------------- life healing -------------------------


def HealCharacter():
    # print("HealCharacter")
    if CheckHPIsLow() == True:
        pg.press("F1")

    if CheckManaIsOK() == True and CheckHPIsNotFull() == True:
        pg.press("F2")

    if CheckManaIsOK() == False and CheckHPIsNotFull() == True:
        pg.press("F4")

    EatCharacter()


def CheckHPIsLow():
    # print("CheckManaIsOK")
    check = pg.locateOnScreen(
        "./images/bar_black.png", confidence=0.95, region=HEALTH_REGION_LOW
    )
    # print("CheckHPIsLow check: ")

    try:
        if check is not None:
            # print("CheckHPIsLow True")
            # pg.screenshot("CheckHPIsLowTrue.png", region=HEALTH_REGION_LOW)
            return True
        else:
            # pg.screenshot("CheckHPIsLowFalse.png", region=HEALTH_REGION_LOW)
            # print("CheckHPIsLow False")
            return False

    except Exception as e:
        print("Wystąpił błąd przy CheckHPIsLow:", e)
        return False


def CheckHPIsNotFull():
    # print("CheckManaIsOK")
    check = pg.locateOnScreen(
        "./images/bar_black.png", confidence=0.95, region=HEALTH_REGION_NOT_FULL
    )
    # print("CheckHPIsLow check: ")

    try:
        if check is not None:
            # pg.screenshot("hpRegionNOTFULLTrue.png", region=HEALTH_REGION_NOT_FULL)
            # print("CheckHPIsNotFull True")
            return True
        else:
            # pg.screenshot("manaRegionFalse.png", region=MANA_REGION)
            # pg.screenshot("hpRegionNOTFULLFalse.png", region=HEALTH_REGION_NOT_FULL)
            # print("CheckHPIsNotFull False")
            return False

    except Exception as e:
        # print("Wystąpił błąd przy CheckManaIsOK:", e)
        return False


def CheckManaIsOK():
    # print("CheckManaIsOK")
    check = pg.locateOnScreen(
        "./images/bar_blue.png", confidence=0.95, region=MANA_REGION
    )
    # print("CheckManaIsOK check:")

    try:
        if check is not None:
            # pg.screenshot("manaRegionTrue.png", region=MANA_REGION)
            # print("CheckManaIsOK True")
            return True
        else:
            # pg.screenshot("manaRegionFalse.png", region=MANA_REGION)
            # print("CheckManaIsOK False")
            return False

    except Exception as e:
        print("Wystąpił błąd przy CheckManaIsOK:", e)
        return False


def EatCharacter():
    if CheckChaacterIsHungry:
        pg.press("F7")


def CheckChaacterIsHungry():
    check = pg.locateOnScreen(
        "./images/hungry_sign.png", confidence=0.95, region=STATUS_REGION
    )

    if check is not None:
        return True
    else:
        return False


def ThereAreMonsters():
    try:
        # pg.screenshot("test.png", region=BATTLE_REGION)
        check = pg.locateOnScreen(
            "./images/BattleList.png", confidence=0.95, region=BATTLE_REGION
        )

        if check is None:
            # print("wykrylo monstery 222")
            pg.screenshot("ThereAreMonstersTrue.png", region=BATTLE_REGION)
            return True
        else:
            pg.screenshot("ThereAreMonstersFalse.png", region=BATTLE_REGION)
            # print("battle list jest puste")
            return False
    except Exception as e:
        # print("battle list wykrylo monstery 333")
        # print("Wystąpił błąd przy wykrywaniu monsterów:", e)
        return True


def kill_monster():
    # If monster.png is False, not found it, means that monster is on my battle
    # so it's necessary to attack

    while ThereAreMonsters() == True:
        pg.press("t")
        pg.sleep(1)
        pg.press("f")

        if Are3LeonsOnBattleField() == True:
            pg.sleep(1)
            pg.press("F5")

        HealCharacter()

        # Verify both red and pink colors in the x,y pixel

        # print(colors)
        for color in colors:
            while pg.pixelMatchesColor(x, y, color, tolerance=50):
                # print("Still attacking")
                pg.sleep(1)

        # print("Monster died")


def Are3LeonsOnBattleField():
    check = pg.locateOnScreen(
        "./images/monsters/lions.png", confidence=0.9, region=BATTLE_REGION
    )

    # print("Are3LeonsOnBattleField Check:")
    try:
        if check is not None:
            # print("Are3LeonsOnBattleFieldTrue:")
            # pg.screenshot("BattleRegion3LionsTrue.png", region=BATTLE_REGION)
            return True
        else:
            # print("Are3LeonsOnBattleFieldFalse:")
            # pg.screenshot("BattleRegion3LionsFalse.png", region=BATTLE_REGION)
            return False
    except Exception as e:
        print("Are3LeonsOnBattleFieldException:", e)
        return False


def check_flag(flag_path, wait):
    # Search for flags on the minimap
    # pg.screenshot("maparegion.png", region=MAPA_REGION)
    box = pg.locateOnScreen(flag_path, confidence=0.7, region=MAPA_REGION)
    if box:
        print("going to flag : ", flag_path)
        moveMouseToPointAndClick(box)
        # print("check_flag sleep 5: ")

        # time.sleep(5)

        # Sprawdź potwory

        print("check_flag wait: ", wait)
        pg.sleep(wait)
        kill_monster()
    else:
        print(f"Flag {flag_path} not found")


def moveMouseToPointAndClick(box):
    x, y = pg.center(box)
    pg.moveTo(x, y, 0.2)
    pg.sleep(0.2)
    pg.click()
    # back cursor to center of screen
    pg.sleep(0.2)
    pg.moveTo(1300, 400, 0.2)


def run():

    kill_monster()
    # print("flags:", flags)
    for item in flags:
        check_flag(item["path"], item["wait"])
        # kill the monsters around, maybe we're trapped and can't go to the flag
        # Ideally is to add some check if the character arrived to the flag, if not go again
        # but lets just add 2 more seconds
        check_flag(item["path"], 2)
        removeItemFromBackPack()


# ------------------------------------- remove items ---------------------------


def removeItemFromBackPack():
    # print("removeItemFromBackPack")
    # checkItem = pg.locateOnScreen(
    #     "./images/mace.png", confidence=0.8, region=BATTLE_REGION
    # )

    for item in items:
        # print("item_path: ", item)
        while ThereAreItems(item["path"]) is not None:
            box = ThereAreItems(item["path"])
            moveMouseToPointAndDropToCenter(box)


def ThereAreItems(item_path):
    try:
        # pg.screenshot("itemsRegion.png", region=BACKPACK_REGION)
        box = pg.locateOnScreen(item_path, confidence=0.8, region=BACKPACK_REGION)
        #         box = pg.locateOnScreen(
        #     "./images/items/mace.png", confidence=0.8, region=BACKPACK_REGION
        # )

        if box is None:
            # print("nie znaleziono itemu")
            return None
        else:
            # print("wykrylo item")
            return box

    except Exception as e:
        print("battle list wykrylo monstery 333")
        print("Wystąpił błąd przy wykrywaniu itemu: ", e)
        return None


def moveMouseToPointAndDropToCenter(box):
    x, y = pg.center(box)
    pg.moveTo(x, y, 0.2)
    pg.sleep(0.1)
    pg.dragTo(782, 481, duration=0.5)  # duration to czas trwania ruchu w sekundach

    # back cursor to center of screen
    pg.sleep(0.1)
    pg.moveTo(1300, 400, 0.2)  # wsporzedne postaci


while True:
    run()
