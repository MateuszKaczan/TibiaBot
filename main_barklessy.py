import pyautogui as pg
import time

pg.useImageNotFoundException(False)
pg.PAUSE = 0.05
# venv\Scripts\activate
# main_barklessy.py
# ==================== KONFIGURACJA ====================

flags = [
    {"path": "./images/flags/flag_2.png", "wait": 5, "stops": 0},
    {"path": "./images/flags/flag_3.png", "wait": 7, "stops": 1},
    {"path": "./images/flags/flag_4.png", "wait": 10, "stops": 0, "useLeftArrow": 10},
    {"path": "./images/flags/flag_6.png", "wait": 5, "stops": 0, "useLeftArrow": 10},
    {"path": "./images/flags/flag_9.png", "wait": 4, "stops": 0},
    {"path": "./images/flags/flag_7.png", "wait": 4, "stops": 0},
    {"path": "./images/flags/flag_8.png", "wait": 9, "stops": 0},
    {"path": "./images/flags/flag_10.png", "wait": 5, "stops": 0},
]


MAPA_REGION = (1751, 27, 106, 106)
BATTLE_REGION = (1560, 27, 180, 310)
BACKPACK_REGION = (1744, 462, 172, 439)
USE_REGION = (1550, 462, 250, 639)

MANA_REGION = (850, 28, 250, 12)
MANA_REGION_NOT_FULL = (850, 28, 250, 12)
HEALTH_REGION_LOW = (295, 28, 100, 10)
HEALTH_REGION_NOT_FULL = (475, 28, 160, 10)  # od 490 - 530, bylo 500 napoczatku
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
        pg.press("F2")
        pg.press("F1")
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
ROTATION_PRIORITY = ["exori gran", "exori mas", "exori"]

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


def kill_monster():
    first_aoe_done = False

    while there_are_monsters():
        pg.press("t")

        # Sprawdzenie czy nadal atakuje
        for color in ATTACK_COLORS:
            while pg.pixelMatchesColor(
                ATTACK_CHECK_POS[0], ATTACK_CHECK_POS[1], color, tolerance=50
            ):
                heal_character()
                time.sleep(0.5)

        if not first_aoe_done:
            print("   → Czekam 0.5s na pierwsze AoE (luring potworów)...")
            for _ in range(1):
                heal_character()
                time.sleep(0.5)
            first_aoe_done = True
        else:
            heal_character()
            kombinacjaObszarowychCzarow()
            time.sleep(0.8)

        zbierajLoot()


def zbierajLoot():
    pg.press("f")


# ================== POZOSTAŁE FUNKCJE ==================


def change_one_gold_stack():
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


def check_flag(flag_path, max_walk_time=15, stops=0, leftArrowTimes=0):
    box = safe_locate(flag_path, MAPA_REGION, 0.7)
    if not box:
        print(f"Flaga {flag_path} nie znaleziona na minimapie")
        return

    print(f"→ Start do flagi: {flag_path} | wait={max_walk_time}s | stops={stops}")

    # --- Pierwsze kliknięcie ---
    click_flag(box)
    utaniHur()

    if stops == 0:
        # Bez stopów - po prostu idziemy cały czas
        print(f"   → Idę bez zatrzymywania ({max_walk_time}s)")
        time.sleep(max_walk_time)
    else:
        # Z stopami - robimy równy podział
        segment_time = max_walk_time / (stops + 1)  # np. 7 / 2 = 3.5s

        for i in range(stops + 1):  # np. przy stops=1 → 2 segmenty
            print(f"   → Segment {i+1}/{stops+1} → idę {segment_time:.1f}s")

            # Idziemy przez segment czasu
            start_segment = time.time()
            while time.time() - start_segment < segment_time:
                heal_character()
                time.sleep(0.35)

            # Jeśli to nie ostatni segment → robimy stop
            if i < stops:
                print(f"   → Stop #{i+1}/{stops} → czekam 1.5s (ESC)")
                pg.press("esc")

                # Zatrzymujemy się na stały czas (zegar podróży stoi)
                stop_start = time.time()
                while time.time() - stop_start < 1.5:  # <--- tutaj stały czas postoju
                    heal_character()
                    time.sleep(0.4)

                # Po stopie klikamy flagę ponownie
                box = safe_locate(flag_path, MAPA_REGION, 0.7)
                if box:
                    click_flag(box)

    # --- Dotarliśmy ---
    print(
        f"   → Dotarłem do flagi {flag_path} | Całkowity czas: {max_walk_time}s (+ postoje)\n"
    )

    pg.press("esc")
    time.sleep(1.5)

    kill_monster()
    zbierajLoot()

    if leftArrowTimes > 0:
        box = safe_locate(flag_path, MAPA_REGION, 0.7)
        click_flag(box)
        time.sleep(0.5)
        useLeftArrow(leftArrowTimes)


def click_flag(box):
    """Kliknięcie flagi i przesunięcie kursora w bezpieczne miejsce"""
    if not box:
        return False

    x, y = pg.center(box)
    pg.moveTo(x, y, duration=0.25)
    time.sleep(0.15)
    pg.click()
    time.sleep(0.25)
    pg.moveTo(1300, 400, duration=0.2)
    return True


def useLeftArrow(leftArrowTimes):
    for i in range(leftArrowTimes):
        pg.press("left")
        time.sleep(0.1)


def zjedzJedzenie():
    pg.press("F12")


def utaniHur():
    pg.press("F9")


def run():
    kill_monster()

    for flag in flags:
        check_flag(
            flag["path"],
            flag["wait"],
            flag.get("stops", 0),
            flag.get("useLeftArrow", 0),
        )
        zjedzJedzenie()


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
