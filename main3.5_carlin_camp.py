import pyautogui as pg
import time


pg.useImageNotFoundException(False)
pg.PAUSE = 0.05

# print("Za 5 sekund pokaże pozycję kursora...")
# time.sleep(5)
# ==================== KONFIGURACJA ====================

# venv\Scripts\activate
# py main3.5_hero_cave.py


flags = [
    # -------------------- heros --------------------------
    {"path": "./images/flags/flag_1.png", "wait": 15},
    {"path": "./images/flags/flag_2.png", "wait": 5},
    {"path": "./images/flags/flag_3.png", "wait": 8},
    {"path": "./images/flags/flag_7.png", "wait": 5},
    {"path": "./images/flags/flag_4.png", "wait": 5},
    {"path": "./images/flags/flag_8.png", "wait": 5},
    {"path": "./images/flags/flag_5.png", "wait": 5},
    {"path": "./images/flags/flag_6.png", "wait": 10},
    # {"path": "./images/flags/flag_5.png", "wait": 6},
    # {"path": "./images/flags/flag_4.png", "wait": 4},
    # --------------------------------ssssssssssssssssassssssswd--------------
]

MAPA_REGION = (1751, 27, 106, 106)
BATTLE_REGION = (1560, 27, 180, 310)
BACKPACK_REGION = (1744, 462, 172, 439)
USE_REGION = (1550, 462, 250, 639)

MANA_REGION = (850, 28, 250, 12)
MANA_REGION_NOT_FULL = (850, 28, 250, 12)
HEALTH_REGION_LOW = (295, 28, 100, 10)
# HEALTH_REGION_NOT_FULL = (535, 28, 160, 10)
HEALTH_REGION_NOT_FULL = (480, 28, 160, 10)
# HEALTH_REGION_NOT_FULL = (470, 28, 160, 10)
STATUS_REGION = (1752, 286, 100, 9)

ATTACK_COLORS = [(233, 0, 0), (186, 96, 96)]
ATTACK_CHECK_POS = (1591, 362)

GOLD_IMAGE = r"./images/items/100gold.png"
USE_IMAGE = r"./images/items/use.png"


# ==================== BEZPIECZNE FUNKCJE ====================


def safe_locate(image_path, region=None, confidence=0.95):
    try:
        if region:
            return pg.locateOnScreen(image_path, region=region, confidence=confidence)
        return pg.locateOnScreen(image_path, confidence=confidence)
    except Exception:
        return None


# def is_hp_low():
#     return safe_locate("./images/bar_black.png", HEALTH_REGION_LOW, 0.95) is not None


def is_hp_not_full():
    return (
        safe_locate("./images/bar_black.png", HEALTH_REGION_NOT_FULL, 0.95) is not None
    )


def is_mana_not_full():
    return safe_locate("./images/bar_black.png", MANA_REGION_NOT_FULL, 0.95) is not None


def is_mana_ok():
    return safe_locate("./images/bar_blue.png", MANA_REGION, 0.95) is not None


def is_hungry():
    return safe_locate("./images/hungry_sign.png", STATUS_REGION, 0.95) is not None


def there_are_monsters():
    return safe_locate("./images/BattleList.png", BATTLE_REGION, 0.95) is None


def are_2_monsters():
    return are_2_or_more_monsters() or are_2_or_more_monsters_low_hp()


def are_2_or_more_monsters():
    return (
        safe_locate("./images/monsters/battle_3_or_more.png", BATTLE_REGION, 0.9)
        is not None
    )


def are_2_or_more_monsters_low_hp():
    return (
        safe_locate("./images/monsters/battle_3_or_more_low_hp.png", BATTLE_REGION, 0.9)
        is not None
    )


# def are_3_or_more_monsters():
#     """Zwraca True jeśli na battle liście są 3 lub więcej potworów"""
#     # Szukamy obrazka zawierającego minimum 3 wiersze potworów
#     box = safe_locate(
#         "./images/monsters/battle_3_or_more.png", region=BATTLE_REGION, confidence=0.5
#     )  # możesz zmienić na 0.82-0.88

#     if box:
#         # Opcjonalnie: możesz dodać log z pozycją
#         # print(f"   → Wykryto 3+ potworów na pozycji {box}")
#         return True
#     return False


def heal_character():
    print("heal_character")
    if is_hp_not_full():
        print("heal_character here11")
        pg.press("F1")
        pg.press("F2")
    elif is_mana_not_full():
        pg.press("F4")
        print("heal_character here22")
    #     pg.press("F2")
    # else:
    # if is_hungry():
    #     print("   [HUNGRY] Postać jest głodna! → naciskam F7")
    #     pg.press("F7")


def kill_monster():

    first_aoe_done = False

    while there_are_monsters():
        pg.press("t")

        for color in ATTACK_COLORS:
            while pg.pixelMatchesColor(
                ATTACK_CHECK_POS[0], ATTACK_CHECK_POS[1], color, tolerance=50
            ):
                heal_character()  # ← leczenie też działa podczas ataku!
                time.sleep(0.5)

        if not first_aoe_done:
            print("   → Czekam 1.5s na pierwsze AoE (luring potworów)...")
            for _ in range(3):  # 6 × 0.5s = max 3 sekundy
                heal_character()  # ← leczenie działa w tym czasie!
                time.sleep(0.5)
            first_aoe_done = True

        # Normalny cykl AoE (wszystkie kolejne)
        else:
            heal_character()
            kombinacjaObszarowychCzarow()
            time.sleep(0.8)  # krótka pauza po rzucie czaru

        # Czekanie aż skończy atakować

        zbierajLoot()


def zbierajLoot():
    pg.press("f")


def kombinacjaObszarowychCzarow():
    pg.press("F6")
    time.sleep(0.5)
    pg.press("F5")
    time.sleep(0.2)
    print("   → Rzucono F5 (obszarowy czar)")
    heal_character()


def change_one_gold_stack():
    """Konwertuje tylko jeden stack 100gp - szybka wersja"""
    box = safe_locate(GOLD_IMAGE, BACKPACK_REGION, 0.95)
    if not box:
        return False

    x, y = pg.center(box)
    pg.moveTo(x, y, duration=0.22)
    time.sleep(0.15)

    pg.rightClick()
    time.sleep(0.15)

    boxUse = safe_locate(USE_IMAGE, USE_REGION, 0.75)
    if not boxUse:
        return False

    ux, uy = pg.center(boxUse)
    pg.moveTo(ux, uy, duration=0.22)
    time.sleep(0.15)
    pg.click()

    pg.moveTo(1300, 400, duration=0.25)
    time.sleep(0.18)

    print("   → Przekonwertowano 1 stack 100gp")
    return True


# ==================== CHECK_FLAG ====================


def check_flag(flag_path, max_walk_time=15):
    """
    Idzie do flagi na minimapie, ignorując potwory po drodze.
    Regularnie leczy postać.
    Po dotarciu zaczyna czyszczenie potworów.
    """
    box = safe_locate(flag_path, MAPA_REGION, 0.7)
    if not box:
        print(f"Flaga {flag_path} nie znaleziona na minimapie")
        return

    print(f"Idę do flagi: {flag_path} (max {max_walk_time}s) - ignoruję potwory")

    # Klik na flagę
    x, y = pg.center(box)
    pg.moveTo(x, y, duration=0.25)
    time.sleep(0.25)
    pg.click()
    time.sleep(0.3)
    pg.moveTo(1300, 400, duration=0.2)  # bezpieczne miejsce kursora

    start_time = time.time()
    last_heal_time = start_time

    while True:
        current_time = time.time()
        elapsed = current_time - start_time

        # Warunek wyjścia - przekroczono maksymalny czas
        if elapsed > max_walk_time:
            print(f"   → Przekroczono maksymalny czas chodzenia ({max_walk_time}s)")
            break

        # === REGULARNE LECZENIE ===
        # if current_time - last_heal_time > 1:  # co ~2.5 sekundy lecz
        # last_heal_time = current_time
        heal_character()  # ← twoja funkcja leczenia

        # Opcjonalnie: zmiana stacka golda
        if not is_hp_not_full():
            change_one_gold_stack()

        # Krótka pauza między checkami (bardzo ważna dla płynności)
        time.sleep(0.5)

    # === DOTARLIŚMY (lub czas się skończył) ===
    print(f"   → Dotarłem do flagi {flag_path} - zaczynam czyszczenie")

    # Małe opóźnienie, żeby potwory zdążyły się zlurować
    time.sleep(1.0)

    # Teraz walczymy
    kill_monster()  # lub lepiej: clear_area_with_aoe()
    zbierajLoot()


# def additional_check(flag_path):
#     box = safe_locate(flag_path, MAPA_REGION, 0.7)
#     if box:
#         print(f"   → Dodatkowa próba dojścia: {flag_path}")
#         x, y = pg.center(box)
#         pg.moveTo(x, y, duration=0.2)
#         time.sleep(0.2)
#         pg.click()
#         time.sleep(0.2)
#         pg.moveTo(1300, 400, duration=0.2)
#         time.sleep(2)
#         kill_monster()
#     else:
#         print(
#             f"   → Flaga {flag_path} nie znaleziona w dodatkowej próbie (prawdopodobnie dotarł)"
#         )


def there_are_item(item_path):
    return safe_locate(item_path, BACKPACK_REGION, 0.8)


def drop_item(box):
    if not box:
        return
    x, y = pg.center(box)
    pg.moveTo(x, y, duration=0.2)
    time.sleep(0.1)
    pg.dragTo(782, 481, duration=0.5)
    time.sleep(0.1)
    pg.moveTo(1300, 400, duration=0.2)


# def isGoldForChange():
#     return safe_locate("./images/items/100gold.png", BACKPACK_REGION, 0.8)


def safe_locate(image, region=None, confidence=0.78):
    try:
        return pg.locateOnScreen(image, region=region, confidence=confidence)
    except:
        return None


def run():
    kill_monster()

    for flag in flags:
        check_flag(flag["path"], flag["wait"])
        zjedzJedzenie()


def zjedzJedzenie():
    pg.press("F7")


if __name__ == "__main__":
    print("=== BOT TIBIA v3.5 uruchomiony ===")
    print("Naciśnij Ctrl + C aby zatrzymać bota\n")

    try:
        while True:
            run()
    except KeyboardInterrupt:
        print("\n\nBot zatrzymany przez użytkownika (Ctrl+C)")
    except Exception as e:
        print(f"\nNieoczekiwany błąd: {e}")
    finally:
        print("Koniec działania bota.")
