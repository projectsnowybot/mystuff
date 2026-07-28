#!/usr/bin/env python3
import getpass
import json
import math
import os
import socket
import subprocess
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service



# Forced absolute storage path inside your isolated container user directory
STATE_FILE = "/home/kickpi/bot_state.json"

# --- CONFIGURATION PATHS ---
LOG_OUTPUT = "/home/kickpi/bot_output.log"
LOG_ERROR = "/home/kickpi/bot_error.log"
GECKODRIVER_PATH = "/home/kickpi/geckodriver"

# Global tracking variables for the bot logic
origiun = 0.0
fox = 0.0
kitty = 0.0
bear = 0.0
kool = 0.0
sevens = 0.0
eights = 0.0
fart = 1
scratchPad = 0.0
litterbox = 0.0
mile = 0.0
lastLeap = 0.0
LAST_FOX_VALUE = 0.0
yibida = 1
xine = 1

# ---------------------------
# STATE FILE FUNCTIONS
# ---------------------------
def load_state():
    """Loads the state file. Returns None if it doesn't exist or is invalid."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                print("🔄 Found state file. Attempting recovery...")
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ State file was corrupted. Starting fresh.")
    return None


def save_state(state_dict):
    """Saves current global variables to the state file securely inside the container."""
    state_dict["last_seen_timestamp"] = time.time()
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state_dict, f, indent=4)
            f.flush()
    except PermissionError:
        print(f"❌ Permission Denied! Cannot write to {STATE_FILE} inside sandbox container.")
    except Exception as e:
        print(f"⚠️ Failed to save state file: {e}")


def f8(x):
    return float(f"{x:.8f}")


def reset_session():
    """Wipes previous session data, cookies, or cache."""
    print("🧹 Wiping previous session data and clearing cookies...")
    import shutil
    if os.path.exists('/home/kickpi/.mozilla/firefox/bot_profile'):
         try:
             shutil.rmtree('/home/kickpi/.mozilla/firefox/bot_profile')
         except Exception as e:
             print(f"Note: Could not clear profile dir: {e}")
    time.sleep(1)


def initialize_bot_process(driver, someone, logmein, mecode):
    """Handles browser loading, logging in, and setting up dashboard."""
    print("\n🌐 Page loading, please wait...")
    driver.get("https://just-dice.com")
    time.sleep(35)
    print("✅ Page loaded successfully!")

    try:
        popup = driver.find_element(By.CSS_SELECTOR, "a.fancybox-item.fancybox-close")
        popup.click()
    except NoSuchElementException:
        pass

    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Account").click()
    time.sleep(5)

    print("🔑 Logging in now, please wait...")
    driver.find_element(By.ID, "myuser").clear()
    time.sleep(1)
    driver.find_element(By.ID, "myuser").send_keys(someone)
    time.sleep(1)
    driver.find_element(By.ID, "mypass").clear()
    time.sleep(1)
    driver.find_element(By.ID, "mypass").send_keys(logmein)
    time.sleep(1)
    driver.find_element(By.ID, "mycode").clear()
    time.sleep(1)
    driver.find_element(By.ID, "mycode").send_keys(mecode)
    time.sleep(1)
    driver.find_element(By.ID, "myok").click()

    print("⏳ Waiting for login to complete and dashboard to load...")
    time.sleep(35)


def awesome(driver, someone, logmein, mecode):
    global origiun, fox, kitty, bear, kool, sevens, eights, fart, scratchPad, litterbox, mile, lastLeap, xine, yibida, pile, flea, beats, folly, jolly, roger
    xine = 1
    yibida = 1
    print("⏳ Metrics to resolve...")
    time.sleep(1)
    
    raw_val = driver.find_element(By.ID, "pct_balance").get_attribute("value")
    if raw_val:
        ui_balance = float(raw_val)
    else:
        ui_balance = None

    if ui_balance is None or ui_balance <= 0:
        time.sleep(1)
        print("failed to fetch balance")
        should_continue = False
        while True:
                try:
                    # Try to refresh. If this fails, it jumps straight to 'except' and loops back.
                    driver.refresh()
                    print("refreshing please wait")
                    # If refresh succeeds, wait and run the function
                    time.sleep(35)
                    awesome(driver, someone, logmein, mecode)
                    # If everything completes without error, exit the loop
                    break
                except Exception as e:
                    print(f"Connection or execution failed ({e}). Refreshing again...")
                    # Optional short pause so it doesn't slam the browser instantly on failure
                    time.sleep(2)
                    # The loop automatically goes back to the top to try driver.refresh() again
    else:
        print("balance fetched")
        should_continue = True

    if should_continue:
        time.sleep(1)
        driver.find_element(By.ID, "b_min").click()
        time.sleep(1)

        saved_state = load_state()
        if saved_state:
            print(f"🚨 Bot was offline for a while. Restoring previous state...")
            origiun = saved_state.get("origiun", ui_balance)
            kitty = saved_state["kitty"]
            bear = saved_state["bear"]
            kool = bear * 10
            sevens = bear * 6.9
            eights = bear * 7.9
            fart = saved_state["fart"]
            scratchPad = saved_state["scratchPad"]
            litterbox = saved_state["litterbox"]
            pile = saved_state["pile"]
            flea = saved_state["flea"]
            bocance = driver.find_element(By.ID, "pct_balance").get_attribute("value")
            viagra = float(bocance)
            beats = saved_state["beats"]
            fox = float(viagra)
            jolly = (flea-fox)
            roger = (bear*beats)
            folly = (jolly+roger)
            mookie = float(viagra)
            scratchPad = float(viagra)
            litterbox = float(viagra)
            mile = saved_state["mile"]
            lastLeap = saved_state["lastLeap"]
        else:
            print("🚀 Fresh start. Calculating base initial variables.")
            origiun = float(ui_balance)
            fox = origiun
            flea = origiun
            yobbo = origiun / 144000
            bear = round(yobbo, 8)
            kitty = bear
            fart = 1
            beats = False
            jolly = (flea-fox)
            roger = (bear*beats)
            folly = (jolly+roger)
            kool = bear * 10
            sevens = bear * 6.9
            eights = bear * 7.9
            scratchPad = float(fox)
            litterbox = float(fox)
            lastLeap = (math.floor(origiun / kool)) * kool
            pile = (((math.floor(flea / kool)) * kool)-kool)
            mile = float(fox)
            
        runCatBot(driver, someone, logmein, mecode)


def runCatBot(driver, someone, logmein, mecode):
    global yibida, xine, fox, LAST_FOX_VALUE, kitty, lastLeap, scratchPad, litterbox, origiun, mile, fart, kool, bear, sevens, eights, pile, flea, beats, folly, jolly, roger
    LAST_FOX_CHANGE_TIMESTAMP = time.time()

    while (yibida == xine):
        time.sleep(0.001)
        becance = driver.find_element(By.ID, "pct_balance").get_attribute("value")
        mookie = float(becance)

        if ((((mookie - scratchPad)<=(bear/10)) and ((mookie - scratchPad)>=0)) or (((mookie - litterbox)<=(bear/10)) and ((mookie - litterbox)>=0))):
            fox = float(mookie)
            heartbeat = True
            if (fox>flea):
                kitty = bear
                flea = float(fox)
                print("[System] upper handbrake triggered")

            if (fox>mile):
                print("upper")
                beats = True
                mile = float(fox)

            if (fox<mile):
                beats = False
                mile = float(fox)

            if (fox<flea and not beats):
                kitty = float((flea-fox)/2)

            if fox >= 1000:
                print("🔄 winner winner chicken dinner...")
                driver.quit()
                sys.exit()

            if fox >= (origiun * 1.1):
                print("🔄 Refreshing page, target for compound achieved but resetting progress variables...")
                if os.path.exists(STATE_FILE):
                    os.remove(STATE_FILE)
                    driver.refresh()
                    time.sleep(35)
                    awesome(driver, someone, logmein, mecode)

            if heartbeat:
                netTreats = f8(fox - origiun)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Balance: {fox:.8f} | Profit: {netTreats:.8f} | Next Bet: {kitty:.8f}")

                scratchPad = round((fox + kitty), 8)
                litterbox = round((fox - kitty), 8)

                driver.find_element(By.ID, "pct_chance").clear()
                driver.find_element(By.ID, "pct_chance").send_keys("49.5")

                driver.find_element(By.ID, "pct_bet").clear()
                driver.find_element(By.ID, "pct_bet").send_keys(f"{kitty:.8f}")

                driver.find_element(By.ID, "a_lo").click()

                current_state = {
                    "origiun": origiun,
                    "fox": fox,
                    "kitty": kitty,
                    "fart": fart,
                    "mile": mile,
                    "mookie": mookie,
                    "bear": bear,
                    "beats": beats,
                    "pile": pile,
                    "flea": flea,
                    "scratchPad": scratchPad,
                    "litterbox": litterbox,
                    "lastLeap": lastLeap,
                }
                save_state(current_state)

        if fox != LAST_FOX_VALUE:
            LAST_FOX_VALUE = float(fox)
            LAST_FOX_CHANGE_TIMESTAMP = time.time()

        time_since_fox_changed = time.time() - LAST_FOX_CHANGE_TIMESTAMP
        if time_since_fox_changed > 55:
            print(f"\n🚨 [WATCHDOG] 'fox' hasn't changed in {round(time_since_fox_changed, 1)} seconds! Page likely hung.")
            print("🔄 Refreshing page, but preserving variables...")
            LAST_FOX_CHANGE_TIMESTAMP = time.time()
            yibida = 2
            while (yibida==2):
                try:
                    # Try to refresh. If this fails, it jumps straight to 'except' and loops back.
                    driver.refresh()
                    # If refresh succeeds, wait and run the function
                    time.sleep(35)
                    awesome(driver, someone, logmein, mecode)
                    # If everything completes without error, exit the loop
                    break
                except Exception as e:
                    print(f"Connection or execution failed ({e}). Refreshing again...")
                    # Optional short pause so it doesn't slam the browser instantly on failure
                    time.sleep(2) 
                    # The loop automatically goes back to the top to try driver.refresh() again

        sys.stdout.flush()                      


def daemonize():
    """Phase 2: Disconnect from the terminal cleanly via UNIX Double-Fork."""
    print("Detaching process and launching background daemon...")
    print(f"📝 All standard output redirected to: {LOG_OUTPUT}")
    print(f"🚨 All execution errors redirected to: {LOG_ERROR}\n")
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(f"❌ Fork #1 failed: {e}", file=sys.stderr)
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(f"❌ Fork #2 failed: {e}", file=sys.stderr)
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()

    si = open(os.devnull, 'r')
    so = open(LOG_OUTPUT, 'a+', encoding='utf-8')
    se = open(LOG_ERROR, 'a+', encoding='utf-8')
    
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def interactive_login():
    """Phase 1: Collect credentials cleanly from terminal."""
    print("🔐 --- Just-Dice Bot Security Portal ---")
    someone = input("Enter your username for just-dice.com: ")
    import pwinput
    logmein = pwinput.pwinput(prompt="Enter your password for just-dice.com: ", mask="*")
    mecode = pwinput.pwinput(prompt="Enter your 2FA code for just-dice or press Enter if blank: ", mask="*")
    return someone, logmein, mecode



def main_bot_loop(someone, logmein, mecode):
    """Phase 3: Fire up selenium and start processing inside the background daemon."""
    print(f"\n🚀 Daemon successfully started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    sys.stdout.flush()

    # Selenium initialization MUST happen here (Post-Fork)
    options = Options()
    options.add_argument("--headless")
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)

    initialize_bot_process(driver, someone, logmein, mecode)
    awesome(driver, someone, logmein, mecode)


if __name__ == "__main__":
    reset_session()
    someone, logmein, mecode = interactive_login()
    daemonize()
    main_bot_loop(someone, logmein, mecode)
