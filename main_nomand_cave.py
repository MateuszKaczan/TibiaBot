import pyautogui as pg
import time

pg.useImageNotFoundException(False)
pg.PAUSE = 0.05
# venv\Scripts\activate
# py main_nomand_cave.py

# ==================== KONFIGURACJA ====================

walking_offset = -1

flags = [
    {"path": "./images/flags/flag_3.png", "wait": 6 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_4.png", "wait": 4 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_13.png", "wait": 3 + walking_offset, "attempts": 3},
    #  -----------------------
    {"path": "./images/flags/flag_5.png", "wait": 5 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_6.png", "wait": 6 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_9.png", "wait": 5 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_14.png", "wait": 8 + walking_offset, "attempts": 3},
    #  -----------------------
    {"path": "./images/flags/flag_7.png", "wait": 8 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_10.png", "wait": 4 + walking_offset, "attempts": 2},
    #  -----------------------
    {"path": "./images/flags/flag_11.png", "wait": 5.5 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_1.png", "wait": 4 + walking_offset, "attempts": 3},
    #  -----------------------
    {"path": "./images/flags/flag_12.png", "wait": 6 + walking_offset, "attempts": 3},
    #  -----------------------
    {"path": "./images/flags/flag_9.png", "wait": 5 + walking_offset, "attempts": 0},
    {"path": "./images/flags/flag_8.png", "wait": 6 + walking_offset, "attempts": 3},
    {"path": "./images/flags/flag_4.png", "wait": 3 + walking_offset, "attempts": 0},
    #  -----------------------
]

# flags = [
#     {"path": "./images/flags/flag_1.png", "wait": 4.5 + walking_offset, "attempts": 0},
#     # {"path": "./images/flags/flag_2.png", "wait": 11 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_up.png", "wait": 4.5 + walking_offset, "attempts": 3},
#     #  -----------------------
#     {"path": "./images/flags/flag_3.png", "wait": 3 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_4.png", "wait": 4 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_13.png", "wait": 3 + walking_offset, "attempts": 3},
#     #  -----------------------
#     {"path": "./images/flags/flag_5.png", "wait": 5 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_6.png", "wait": 6 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_9.png", "wait": 5 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_14.png", "wait": 8 + walking_offset, "attempts": 3},
#     #  -----------------------
#     {"path": "./images/flags/flag_7.png", "wait": 7 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_10.png", "wait": 4 + walking_offset, "attempts": 2},
#     #  -----------------------
#     {"path": "./images/flags/flag_11.png", "wait": 5.5 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_1.png", "wait": 4 + walking_offset, "attempts": 3},
#     #  -----------------------
#     {"path": "./images/flags/flag_12.png", "wait": 6 + walking_offset, "attempts": 3},
#     #  -----------------------
#     {"path": "./images/flags/flag_9.png", "wait": 5 + walking_offset, "attempts": 0},
#     {"path": "./images/flags/flag_8.png", "wait": 6 + walking_offset, "attempts": 3},
#     #  -----------------------
#     {"path": "./images/flags/flag_down.png", "wait": 4 + walking_offset, "attempts": 3},
# ]

MAPA_REGION = (1751, 27, 106, 106)
BATTLE_REGION = (1560, 27, 180, 310)
HEALTH_REGION_NOT_FULL = (475, 28, 160, 10)
MANA_REGION_NOT_FULL = (850, 28, 250, 12)
STATUS_REGION = (1752, 286, 100, 9)
CHASE_OPPONENT_REGION = (1869, 140, 45, 70)

ATTACK_COLORS = [(233, 0, 0), (186, 96, 96)]
ATTACK_CHECK_POS = (1591, 362)


# ==================== GLOBALNY COOLDOWN DLA HASTE ====================
last_haste_time = 0
HASTE_COOLDOWN = 28.0  # 20 sekund


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


def there_are_monsters():
    return safe_locate("./images/BattleList.png", BATTLE_REGION, 0.95) is None


def is_chase_opponent_off():
    return (
        safe_locate("./images/chase_opponent_off.png", STATUS_REGION, 0.95) is not None
    )


def there_is_Nomad():
    return safe_locate("images/monsters/Nomand.png", BATTLE_REGION, 0.95) is not None


def heal_character():
    if is_hp_not_full():
        use_exura()
        if is_hp_not_full():
            use_healing_potion()
    elif is_mana_not_full():
        use_mana_potion()


def use_healing_potion():
    pg.press("F1")


def use_mana_potion():
    pg.press("F4")


def use_exura():
    pg.press("F2")


def use_haste():
    pg.press("F9")


# ================== KONFIGURACJA EXORI ==================

SPELL_HOTKEYS = {
    "exori": "f6",
}

COOLDOWNS = {
    "exori": 4.0,
}

ROTATION_PRIORITY = ["exori"]

last_cast = {spell: 0.0 for spell in COOLDOWNS}


def can_cast(spell: str) -> bool:
    return time.time() - last_cast[spell] >= COOLDOWNS[spell]


def cast_exori(spell: str):
    if can_cast(spell):
        hotkey = SPELL_HOTKEYS[spell]
        pg.press(hotkey)
        last_cast[spell] = time.time()
        time.sleep(0.18)
        return True
    return False


def kombinacjaObszarowychCzarow():
    for spell in ROTATION_PRIORITY:
        if can_cast(spell):
            cast_exori(spell)
            break
    else:
        time.sleep(0.1)

    heal_character()


# ================== FUNKCJA HASTE ==================


def haste(forceHaste=False):
    global last_haste_time
    current_time = time.time()

    # Sprawdź czy minęło 20 sekund od ostatniego użycia
    if (current_time - last_haste_time >= HASTE_COOLDOWN) or forceHaste:
        use_haste()
        last_haste_time = current_time


# def haste():
#     if safe_locate("./images/haste_sign.png", STATUS_REGION, 0.95) is None:
#         pg.press("F9")


# ================== FUNKCJA WALKI ==================


def kill_monster():
    last_aoe_time = time.time()  # Czas ostatniego użycia AoE (lub startu walki)
    aoe_cooldown = 4  # Co 3.5 sekundy możesz użyć AoE

    while there_are_monsters():
        # while there_is_Nomad():
        pg.press("t")

        # Sprawdzenie czy nadal atakuje
        for color in ATTACK_COLORS:
            while pg.pixelMatchesColor(
                ATTACK_CHECK_POS[0], ATTACK_CHECK_POS[1], color, tolerance=50
            ):
                heal_character()
                time.sleep(0.2)

        # Sprawdź czy minęło 3.5 sekundy od ostatniego AoE (lub od startu walki)
        if time.time() - last_aoe_time >= aoe_cooldown:
            print(f"   → Walka trwa za długo! Używam czaru obszarowego...")
            kombinacjaObszarowychCzarow()
            last_aoe_time = time.time()  # Resetuj timer

        zbierajLoot()
        time.sleep(0.15)

        heal_character()

        zbierajLoot()
        time.sleep(0.15)  # <-- MAŁE OPOŹNIENIE NA ZBIERANIE

    zbierajLoot()
    time.sleep(0.15)


def zbierajLoot():
    pg.press("f")


# ================== POZOSTAŁE FUNKCJE ==================


def check_flag(flag_path, total_wait, attempts=0):
    remaining_walk_time = total_wait

    while remaining_walk_time > 0:

        box = safe_locate(flag_path, MAPA_REGION, 0.7)
        if not box:
            print(f"Flaga {flag_path} nie znaleziona na minimapie")
            return

        print(
            f"Idę do flagi: {flag_path} (pozostało czasu chodzenia: {remaining_walk_time:.1f}s)"
        )

        x, y = pg.center(box)
        pg.moveTo(x, y, duration=0.1)
        time.sleep(0.1)
        pg.click()
        time.sleep(0.2)
        pg.moveTo(1300, 400, duration=0.2)

        # walk_start_time = time.time()
        check_interval = 0.4

        walk_phase_time = min(3.0, remaining_walk_time)
        walked_this_phase = 0
        monsters_encountered = False

        while walked_this_phase < walk_phase_time:

            step_start = time.time()

            if there_are_monsters():

                print(f"   → Napotkałem potwora! Walczę... ({flag_path})")
                kill_monster()  # Ta funkcja powinna zwracać czas walki
                print(f"   → Potwór zabity, kontynuuję podróż do flagi {flag_path}")
                monsters_encountered = True
                # NIE przerywamy chodzenia - kontynuujemy od tego samego miejsca
                # walked_this_phase pozostaje takie jakie jest (czas już przebyty)
                continue  # Wracamy do sprawdzenia czy są kolejne potwory

            # Jeśli nie ma potworów, idź dalej (tylko jeśli nie napotkaliśmy potwora w tej iteracji)
            if not monsters_encountered:
                # Oblicz czas tego kroku (tylko jeśli faktycznie szliśmy)
                elapsed = time.time() - step_start
                print(f"   → monsters_encountered Pelapsed: ", {elapsed})

                if elapsed < 2.0:
                    walked_this_phase += elapsed

            # Reset flagi potwora na następną iterację
            monsters_encountered = False

            if walked_this_phase < walk_phase_time:
                sleep_time = min(check_interval, walk_phase_time - walked_this_phase)
                print(
                    f"   → walked_this_phase < walk_phase_time  sleep_time",
                    {sleep_time},
                )
                time.sleep(sleep_time)
                walked_this_phase += sleep_time

        # Odejmij TYLKO rzeczywisty czas chodzenia
        remaining_walk_time -= walked_this_phase

        if remaining_walk_time > 0.1:
            print(
                f"   → Kontynuuję podróż do flagi {flag_path} (pozostało {remaining_walk_time:.1f}s)..."
            )

    print(f"   → Dotarłem do flagi {flag_path} (czas chodzenia zakończony)")

    if attempts > 0:
        for attempt in range(attempts):
            print("attempts: ", attempt + 1, "/", attempts)
            additional_check(flag_path)


# def check_flag(flag_path, total_wait, attempts=0):
#     remaining_walk_time = total_wait
#     last_monster_check = time.time()
#     check_interval = 0.5  # Sprawdzaj potwory co 0.5s

#     while remaining_walk_time > 0:
#         # Znajdź i kliknij flagę TYLKO RAZ na początku
#         box = safe_locate(flag_path, MAPA_REGION, 0.7)
#         if not box:
#             print(f"Flaga {flag_path} nie znaleziona")
#             return

#         x, y = pg.center(box)
#         pg.click(x, y)

#         walk_start = time.time()

#         # Chodź aż do upłynięcia czasu LUB spotkania potwora
#         while remaining_walk_time > 0:
#             # Sprawdzaj potwory co chwilę
#             if time.time() - last_monster_check > check_interval:
#                 if there_are_monsters():
#                     print(
#                         f"Potwór! Walka... (zostalo {remaining_walk_time:.1f}s chodzenia)"
#                     )
#                     kill_monster()
#                     print("Wznawiam chodzenie")
#                     walk_start = time.time()  # Reset timera po walce
#                 last_monster_check = time.time()

#             # Odejmij czas który upłynął
#             elapsed = time.time() - walk_start
#             if elapsed > 0:
#                 remaining_walk_time -= elapsed
#                 walk_start = time.time()

#             time.sleep(0.1)  # Krótki odpoczynek

#             if remaining_walk_time <= 0:
#                 break

#         print(f"Dotarłem do flagi {flag_path}")


def additional_check(flag_path):
    box = safe_locate(flag_path, MAPA_REGION, 0.7)
    if box:
        print(f"   → Dodatkowa próba dojścia: {flag_path}")
        x, y = pg.center(box)
        pg.moveTo(x, y, duration=0.2)
        time.sleep(0.2)
        pg.click()
        time.sleep(0.2)
        pg.moveTo(1300, 400, duration=0.2)
        time.sleep(2)
        kill_monster()
    else:
        print(
            f"   → Flaga {flag_path} nie znaleziona w dodatkowej próbie (prawdopodobnie dotarł)"
        )


def zjedzJedzenie():
    pg.press("F12")


def run():
    haste(True)
    kill_monster()

    for flag in flags:
        check_flag(flag["path"], flag["wait"], flag["attempts"])
        zjedzJedzenie()
        # haste()


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
