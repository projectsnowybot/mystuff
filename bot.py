#!/usr/bin/env python3
import ast, asyncio, json, math, os, subprocess, sys, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Local bypass to prevent urllib3 crashes
os.environ["no_proxy"] = os.environ["NO_PROXY"] = (
    os.environ.get("no_proxy", "") + ",localhost,127.0.0.1,127.0.0.53,0.0.0.0"
).strip(",")
SF, LO, LE, GP = (
    "/home/snowy/bot_state.json",
    "/home/snowy/bot_output.log",
    "/home/snowy/bot_error.log",
    "/home/snowy/geckodriver",
)
(
    origiun,
    fox,
    kitty,
    bear,
    kool,
    sevens,
    eights,
    fart,
    scratchPad,
    litterbox,
    mile,
    lastLeap,
    LFV,
    yibida,
    xine,
) = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1)


def load_state():
    if os.path.exists(SF):
        try:
            with open(SF, "r") as f:
                return json.load(f)
        except:
            pass
    return None

def f8(x):
    return float(f"{x:.8f}")

def save_state(d):
    d["last_seen_timestamp"] = time.time()
    try:
        with open(SF, "w") as f:
            json.dump(d, f)
    except:
        pass


def reset_session():
    import shutil

    if os.path.exists("/home/snowy/.mozilla/firefox/bot_profile"):
        try:
            shutil.rmtree("/home/snowy/.mozilla/firefox/bot_profile")
            print("[System] Cleared old Firefox bot profile.")
        except:
            pass
    time.sleep(1)


def get_g_hosts():
    try:
        r = subprocess.check_output(
            ["gsettings", "get", "org.gnome.system.proxy", "ignore-hosts"],
            text=True,
        ).strip()
        return ast.literal_eval(r)
    except:
        return [
            "localhost",
            "127.0.0.1",
            "just-dice.com",
            "altquick.com",
            "jsdelivr.net",
            "jquery.com",
            "cloudflareinsights.com",
            "hcaptcha.com",
            "gstatic.com",
            "googleapis.com",
            "highcharts.com",
            "192.168.1.1",
        ]


def init_bot(d, u, p, c):
    print("[System] Navigating to just-dice.com...")
    d.get("https://just-dice.com")
    time.sleep(35)
    try:
        d.find_element(By.CSS_SELECTOR, "a.fancybox-item.fancybox-close").click()
    except:
        pass
    time.sleep(5)
    d.find_element(By.LINK_TEXT, "Account").click()
    time.sleep(5)
    d.find_element(By.ID, "myuser").clear()
    d.find_element(By.ID, "myuser").send_keys(u)
    d.find_element(By.ID, "mypass").clear()
    d.find_element(By.ID, "mypass").send_keys(p)
    d.find_element(By.ID, "mycode").clear()
    d.find_element(By.ID, "mycode").send_keys(c)
    d.find_element(By.ID, "myok").click()
    print("[System] Authentication submitted, waiting for login stabilization...")
    time.sleep(35)


async def awesome(d, u, p, c):
    global origiun, fox, kitty, ts, LFV, bear, mook, kool, sevens, eights, fart, scratchPad, litterbox, mile, lastLeap, xine, yibida, pile, flea, beats, folly, jolly, roger, prevbet, fugoo, heartbeat
    xine = yibida = 1
    heartbeat = True
    await asyncio.sleep(1)
    v = d.find_element(By.ID, "pct_balance").get_attribute("value")
    bal = float(v) if v else None
    if not bal or bal <= 0:
        print("[Warning] Balance check failed or zero. Refreshing session...")
        while True:
            try:
                d.refresh()
                await asyncio.sleep(35)
                await awesome(d, u, p, c)
                break
            except:
                await asyncio.sleep(2)
    else:
        d.find_element(By.ID, "b_min").click()
        await asyncio.sleep(1)
        st = load_state()
        if st:
            print("[System] Loaded previous state from disk.")
            origiun = st.get("origiun", bal)
            bear = st["bear"]
            kitty = st["kitty"]
            fart = st["fart"]
            kool = bear*10
            sevens = bear*6.9
            eights = bear*7.9
            grr = float(d.find_element(By.ID, "pct_balance").get_attribute("value"))
            fox = grr
            mile = st["mile"]
            lastLeap = st["lastLeap"]
            beats = 0
            mook = grr
            jolly = 0
            fugoo = 0
            prevbet = 0
            roger = 0
            folly = 0
            LFV = 0
            scratchPad = grr
            litterbox = grr
            ts = time.time()
        else:
            print("[System] Initializing fresh state parameters.")
            origiun = float(bal)
            fox = float(bal)
            flea = float(bal)
            bear = kitty = round(origiun / 144000, 8)
            fart = 6
            fugoo = 0
            beats = 0
            prevbet = 0
            jolly = 0
            roger = 0
            folly = 0
            LFV = 0
            mook = float(bal)
            kool = bear*10
            sevens = bear*6.9
            eights = bear*7.9
            scratchPad = fox
            litterbox = fox
            mile = ((math.floor(origiun / kool)) * kool)
            lastLeap = ((math.floor(origiun / kool)) * kool)
            ts = time.time()

        await asyncio.sleep(1)
        await runCatBot(d, u, p, c)


async def runCatBot(d, u, p, c):
     global yibida, xine, ts, fox, mook, LFV, kitty, lastLeap, scratchPad, litterbox, origiun, mile, fart, kool, bear, sevens, eights, pile, flea, beats, folly, jolly, roger, prevbet, fugoo, heartbeat
     print("[System] Bot loop started successfully.")
     yibida = xine = 1
     while (yibida==xine):
        mook = float(d.find_element(By.ID, "pct_balance").get_attribute("value"))
        await asyncio.sleep(0.01)
        if (mook!=fugoo):
            fox = float(mook)
            heartbeat = True
            if (fox >= (mile + (kool * fart))):
                lastLeap = float((math.floor(fox / kool)) * kool)
                kitty = bear
                fart = 1
                mile = float((math.floor(fox / kool)) * kool)
                print("[System] Upper handbrake triggered")

            if (
               (fox > (((math.floor(fox / kool)) * kool) + sevens))
               and (fox < (((math.floor(fox / kool)) * kool) + eights))
               and (fox > lastLeap)
            ):
                lastLeap = float(fox)
                kitty = kitty * 2

            if (
               (fox > (((math.floor(fox / kool)) * kool) + sevens))
               and (fox < (((math.floor(fox / kool)) * kool) + eights))
               and (fox < lastLeap)
            ):
                lastLeap = float(fox)
                fart = 0
                kitty = kitty * 2

            if (fox >= 14400):
                print("🔄 winner winner chicken dinner...")
                heartbeat = False
                d.quit()
                sys.exit()

            if heartbeat:
                print(
                   f"[{time.strftime('%M:%S')}] Bal: {fox:.8f} | Profit: {fox-origiun:.8f} | Bet: {kitty:.8f}"
                )
                d.find_element(By.ID, "b_min").click()
                d.find_element(By.ID, "pct_chance").clear()
                d.find_element(By.ID, "pct_chance").send_keys("49.5")
                d.find_element(By.ID, "pct_bet").clear()
                d.find_element(By.ID, "pct_bet").send_keys(f"{kitty:.8f}")
                d.find_element(By.ID, "a_lo").click()
                save_state(
                  { "origiun": origiun,
                    "fox": fox,
                    "kitty": kitty,
                    "fart": fart,
                    "mile": mile,
                    "mookie": mook,
                    "bear": bear,
                    "scratchPad": scratchPad,
                    "litterbox": litterbox,
                    "lastLeap": lastLeap,
                  }
                )
                fugoo = fox

            if fox != LFV:
                LFV = fox
                ts = time.time()
            if time.time() - ts > 55:
                print("[System] Inactivity timeout reached, refreshing page...")
                ts = time.time()
                yibida = 2
                while (yibida==2):
                    try:
                        d.refresh()
                        await asyncio.sleep(35)
                        await awesome(d, u, p, c)
                        break
                    except:
                        await asyncio.sleep(2)
            sys.stdout.flush()

def daemonize():
    """Phase 2: Disconnect from the terminal cleanly via UNIX Double-Fork."""
    print("Detaching process and launching background daemon...")
    print(f"📝 All standard output redirected to: {LO}")
    print(f"🚨 All execution errors redirected to: {LE}\n")
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
    so = open(LO, 'a+', encoding='utf-8')
    se = open(LE, 'a+', encoding='utf-8')

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


async def main_bot_loop(u, p, c):
    opt = Options()
    opt.add_argument("--headless")
    opt.set_preference("network.proxy.type", 1)
    for k in ["http", "ssl", "socks"]:
        opt.set_preference(f"network.proxy.{k}", "0.0.0.0")
        opt.set_preference(f"network.proxy.{k}_port", 1)
    wh = list(set(["localhost", "127.0.0.1", "0.0.0.0"] + get_g_hosts()))
    opt.set_preference("network.proxy.no_proxies_on", ", ".join(wh))
    print("[System] Initializing Firefox headless browser driver...")
    d = webdriver.Firefox(service=Service(GP), options=opt)
    init_bot(d, u, p, c)
    await awesome(d, u, p, c)


if __name__ == "__main__":
    reset_session()
    u = input("User: ")
    import pwinput

    p = pwinput.pwinput(prompt="Pass: ", mask="*")
    c = pwinput.pwinput(prompt="2FA: ", mask="*")
    print("please wait")
    daemonize()
    asyncio.run(main_bot_loop(u, p, c))
