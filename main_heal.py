import pyautogui as pg
import time

pg.useImageNotFoundException(False)
pg.PAUSE = 0.05
# venv\Scripts\activate
# py main_heal.py

# ==================== KONFIGURACJA ====================


MAPA_REGION = (1751, 27, 106, 106)
BATTLE_REGION = (1560, 27, 180, 310)
BACKPACK_REGION = (1744, 462, 172, 439)
USE_REGION = (1550, 462, 250, 639)

MANA_REGION = (850, 28, 250, 12)
MANA_REGION_NOT_FULL = (850, 28, 250, 12)
HEALTH_REGION_LOW = (295, 28, 100, 10)
HEALTH_REGION_NOT_FULL = (510, 28, 160, 10)  # od 490 - 530, bylo 500 napoczatku
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


def is_paralysed():
    return safe_locate("./images/paralysed_sign.png", STATUS_REGION, 0.95) is not None


def there_are_monsters():
    return safe_locate("./images/BattleList.png", BATTLE_REGION, 0.95) is None


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


def heal_character():
    if is_hp_not_full():
        pg.press("F1")
        pg.press("F2")
    elif is_mana_not_full():
        pg.press("F4")


# ================== KONFIGURACJA EXORI ==================

SPELL_HOTKEYS = {
    "exori gran": "f5",  # Fierce Berserk
    "exori mas": "f8",  # Groundshaker
    "exori": "f6",  # Berserk
}

COOLDOWNS = {
    "exori gran": 6.0,  # Fierce Berserk - zazwyczaj 6s po Wheel
    "exori mas": 6.0,  # Groundshaker - dostosuj do swojego Wheel (często 6s lub 5s)
    "exori": 4.0,  # Berserk - standardowo 4s
}

# Nowy priorytet (bez exori mas)
ROTATION_PRIORITY = ["exori gran", "exori", "exori mas"]

last_cast = {spell: 0.0 for spell in COOLDOWNS}


def can_cast(spell: str) -> bool:
    return time.time() - last_cast[spell] >= COOLDOWNS[spell]


def cast_exori(spell: str):
    if can_cast(spell):
        hotkey = SPELL_HOTKEYS[spell]
        pg.press(hotkey)
        last_cast[spell] = time.time()
        # print(f"   → Rzucono {spell.upper():12} ({hotkey})")
        time.sleep(0.18)
        return True
    return False


def kombinacjaObszarowychCzarow():
    """Inteligentna rotacja exori: gran → exori → min"""
    for spell in ROTATION_PRIORITY:
        if can_cast(spell):
            cast_exori(spell)
            break
    else:
        # Żaden spell nie był gotowy
        time.sleep(0.1)

    heal_character()


# ================== FUNKCJA WALKI ==================


import time

# def kill_monster():
#     first_aoe_done = False
#     last_f3_time = 0  # czas ostatniego użycia F3

#     while there_are_monsters():
#         current_time = time.time()

#         # sprawdzamy czy minęło 6 sekund
#         if current_time - last_f3_time >= 6:
#             pg.press("F3")
#             last_f3_time = current_time

#         heal_character()
#         time.sleep(0.5)

#         if not first_aoe_done:
#             print("   → Czekam 0.5s na pierwsze AoE (luring potworów)...")
#             for _ in range(1):
#                 heal_character()
#                 time.sleep(0.5)
#             first_aoe_done = True
#         else:
#             heal_character()
#             kombinacjaObszarowychCzarow()
#             time.sleep(0.8)

#         zbierajLoot()


def kill_monster():
    first_aoe_done = False
    last_f3_time = 0  # czas ostatniego użycia F3

    while there_are_monsters():
        pg.press("t")
        current_time = time.time()

        # sprawdzamy czy minęło 6 sekund
        if current_time - last_f3_time >= 16:
            # pg.press("F3")
            last_f3_time = current_time

        # Sprawdzenie czy nadal atakuje
        for color in ATTACK_COLORS:
            while pg.pixelMatchesColor(
                ATTACK_CHECK_POS[0], ATTACK_CHECK_POS[1], color, tolerance=50
            ):
                heal_character()
                time.sleep(0.5)

        # if not first_aoe_done:
        #     print("   → Czekam 0.5s na pierwsze AoE (luring potworów)...")
        #     for _ in range(1):
        #         heal_character()
        #         time.sleep(0.5)
        #     first_aoe_done = True
        # else:
        #     heal_character()
        #     # kombinacjaObszarowychCzarow()ws
        #     time.sleep(0.8)

        heal_character()
        zbierajLoot()


def zbierajLoot():
    pg.press("f")


# def kill_monster():
#     first_aoe_done = Falset

#     while there_are_monsters():
#         # pg.press("t")
#         pg.press("F3")   #  zmiana z range na mele na 12 sec

#         heal_character()
#         time.sleep(0.5)

#         if not first_aoe_done:
#             print("   → Czekam 0.5s na pierwsze AoE (luring potworów)...")
#             for _ in range(1):
#                 heal_character()
#                 time.sleep(0.5)
#             first_aoe_done = True
#         else:
#             heal_character()
#             kombinacjaObszarowychCzarow()
#             time.sleep(0.8)

#         zbierajLoot()


def zbierajLoot():
    pg.press("f")


# ================== POZOSTAŁE FUNKCJE ==================


def zjedzJedzenie():
    pg.press("f12")


def run():
    kill_monster()
    heal_character()
    # zjedzJedzenie()


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
