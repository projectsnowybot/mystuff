import sys
import json
import math
import time
import getpass
import os
import logging
import re
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QTextEdit)
from PyQt5.QtCore import QTimer, QUrl, Qt, QObject, pyqtSlot, QFile, QIODevice
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineScript, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
from bs4 import BeautifulSoup

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-audio-output"
logging.getLogger("PyQt5").setLevel(logging.CRITICAL)

u = input("Enter username: ")
p = getpass.getpass("Enter password: ")

URL = "https://just-dice.com"
STATE_FILE = "bot_state.json"


class WebBridge(QObject):
    def __init__(self, target_callback):
        super().__init__()
        self.target_callback = target_callback

    @pyqtSlot(str)
    def transmit_data(self, data_json):
        self.target_callback(data_json)


class BotEngine(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dice Native Bot (Infinite Flow)")
        self.resize(1024, 768)

        # --- INTERNAL STATE (Strictly Float) ---
        self.is_running = False
        self.last_balance = 0.0
        self.initial_balance = 0.0
        self.tracked_balance = 0.0
        self.next_compound = 0.0
        self.last_change_time = time.time()
        
        self.prev_balance = None
        self.prev_wins = None
        self.prev_losses = None
        
        self.cat = 0.0
        self.bolux = 0.0
        self.felix = 0.0
        self.orgy = 0.0
        self.orgytwo = 0.0
        self.fart = 1
        self.tabby = 0.0
        self.tens = 0.0
        self.sevens = 0.0
        self.eights = 0.0
        self.betfired = False
        self.shadow = 0.0
        self.shadowtwo = 0.0
        self.yay = 0.0
        self.growl = 0.0
        self.uppers = 6.9
        self.downers = 2.9
        self.balnce = "0.0"
        self.wons = "0"
        self.losses = "0"

        # Browser Setup
        self.browser_view = QWebEngineView()
        
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)

        self.channel = QWebChannel()
        self.bridge_object = WebBridge(self.evaluate_financial_sync)
        self.channel.registerObject("pyBridge", self.bridge_object)
        self.browser_view.page().setWebChannel(self.channel)

        # Removed self.deploy_dom_observer link from here to prevent premature pre-login scanning

        self.bet_in_flight = False
        self.last_activity_time = time.time()

        self.engine_timer = QTimer()
        self.engine_timer.timeout.connect(self.process_tick)

        self.heartbeat = True
        self.log("System initialized. Running in Headless Server Mode...")
        self.browser_view.setUrl(QUrl(URL))
        
        # Give the initial site layout 35 seconds to stabilize completely before triggering our login interaction
        QTimer.singleShot(35000, self.kjool_look)

    def log(self, msg):
        print(f"{msg}")

    def kjool_look(self):
        try: 
           self.browser_view.page().runJavaScript("document.getElementsByClassName('name_button')[0].click()")
        except Exception as e:
           pass
        self.log("Analyzing interface state parameters...")
        self.betfired = False
        QTimer.singleShot(5000, self.inject_login)

    def inject_login(self):
        if not u or not p: return

        js = f"""
        (function() {{
            var usen = document.getElementById('myuser');
            var pasd = document.getElementById('mypass');
            var btn = document.getElementById('myok');
            var links = document.getElementsByTagName('a');
            for(var i=0; i<links.length; i++) {{
                if(links[i].innerText.includes('Account')) {{
                    links[i].click();
                    break;
                }}
            }}
            setTimeout(() => {{
                if(usen && pasd) {{
                    usen.value = '{u}';
                    pasd.value = '{p}';
                    if(btn) btn.click();
                }}
            }}, 1500);
        }})();
        """
        self.browser_view.page().runJavaScript(js)
        self.log("⏳ Running login handshake protocol...")
        
        # 🚨 THE FIX: Wait 12 seconds after clicking login to ensure the server finishes 
        # authentication before we ever read our first balance.
        QTimer.singleShot(12000, self.start_post_login_scrapers)

    def start_post_login_scrapers(self):
        self.log("🔓 Login pipeline finalized. Initializing data trackers...")
        self.deploy_dom_observer()

    def check_ready(self):
        page = self.browser_view.page()
        # Direct execution lookup into the DOM memory structure
        page.runJavaScript(
            "document.getElementById('pct_balance') ? document.getElementById('pct_balance').value : null", 
            self.handle_python_value_read
        )

    def handle_python_value_read(self, val):
        if val is None or str(val) == "null" or str(val).strip() == "":
            print("⏳ Balance element value unreadable. Retrying...")
            QTimer.singleShot(2000, self.check_ready)
            return

        try:
            cleaned_val = "".join(c for c in str(val) if c.isdigit() or c in ".-")
            balance = float(cleaned_val)
            
            self.balnce = str(balance)
            
            # If we aren't running yet, trigger initialization verification
            if not self.is_running:
                self.verify_login()
                
        except Exception as e:
            print(f"⚠️ Value parser failure: {e}")
            QTimer.singleShot(2000, self.check_ready)

    def verify_login(self):
        try:
            balance = float(self.balnce)
        except Exception as e:
            QTimer.singleShot(5000, self.check_ready)
            return
   
        self.log(f"✅ Active Balance Confirmed: {balance:.8f}")
        self.setup_state(balance)
        QTimer.singleShot(1500, self.toggle_engine)

    def deploy_wins(self):
        self.browser_view.page().runJavaScript("document.getElementById('wins').innerText.replaceAll(',', '')", self.winning_wins)
   
    def deploy_loss(self):
        self.browser_view.page().runJavaScript("document.getElementById('losses').innerText.replaceAll(',', '')", self.lossing_loses)

    def deploy_balance(self): 
        self.check_ready()

    def deploy_dom_observer(self):
        self.deploy_wins()
        self.deploy_loss()
        self.deploy_balance()

    def winning_wins(self, wins):
        self.wons = wins if wins else "0"
   
    def lossing_loses(self, losses):
        self.losses = losses if losses else "0"
   
    def evaluate_financial_sync(self):
        self.deploy_dom_observer()
        current_wins = float(self.wons)
        current_losses = float(self.losses)
        current_balance = float(self.balnce)

        if self.prev_balance is None:
            self.prev_balance = current_balance
            self.last_balance = current_balance
            self.prev_wins = current_wins
            self.prev_losses = current_losses
            return

        if (current_wins == 0 and current_losses == 0) and (self.prev_wins > 0 or self.prev_losses > 0):
            self.log("ℹ️ Site statistics cleared. Wiping tracking memory baseline...")
            self.prev_balance = None
            return

        if current_balance != self.prev_balance: 
            delta = current_balance - self.prev_balance
            
            self.tracked_balance = round(self.tracked_balance + delta, 8)
            self.last_balance = current_balance
            
            if self.is_running and (self.prev_wins > 0 or self.prev_losses > 0):
                if current_losses > self.prev_losses and delta > 0:
                    print("🚨 CRITICAL ANOMALY: Balance went UP on match REDS.")
                    sys.exit()
                elif current_wins > self.prev_wins and delta < 0:
                    print("🚨 CRITICAL ANOMALY: Balance went DOWN on match GREENS.")
                    sys.exit()
            sess = self.tracked_balance - self.initial_balance
            if current_losses > self.prev_losses:
                print(f"⚡Loss Confirmed: Balance decreased to {current_balance:.8f} | D: {delta:+.8f} | profit: {sess:+.8f}")
            elif current_wins > self.prev_wins:
                print(f"⚡ Win Confirmed: Balance increased to {current_balance:.8f} | D: {delta:+.8f} | profit: {sess:+.8f}")
            
            self.bet_in_flight = False
            self.last_activity_time = time.time()

            self.prev_wins = current_wins
            self.prev_losses = current_losses
            self.prev_balance = current_balance

    def save_state(self):
        try:
            data = {
                "cat": self.cat, "tabby": self.tabby, "felix": self.felix, "orgy": self.orgy, "orgytwo": self.orgytwo, "fart": self.fart,
                "tracked_balance": self.tracked_balance, "initial_balance": self.initial_balance,
                "last_balance": self.last_balance, "next_compound": self.next_compound, 
                "uppers": self.uppers, "downers": self.downers
            }
            with open(STATE_FILE, "w") as f:
                json.dump(data, f)
        except: 
            pass

    def calculate_units(self, balance):
        self.state_data = self.load_state_file()
        if balance == 0: 
            self.tabby = 0.00000001
        elif self.state_data:
            self.tabby = self.state_data.get("tabby")
        else:
            self.tabby = round(balance / 14400, 8)
        
        self.tens = self.tabby * 10.0
        self.sevens = self.tabby * 6.9
        self.eights = self.tabby * 7.9
        self.uppers = 6.9
        self.downers = 2.9

    def setup_state(self, real_bal):
        self.calculate_units(real_bal)
        self.state_data = self.load_state_file()
        
        if self.state_data:
            self.log("📂 Resuming tracking matrices from cache registry...")
            self.cat = self.state_data.get("cat", self.tabby)
            self.fart = int(self.state_data.get("fart", 1))
            self.initial_balance = self.state_data.get("initial_balance", real_bal)
            last_saved = self.state_data.get("last_balance", real_bal)
            drift = real_bal - last_saved
            self.tracked_balance = round(self.state_data.get("tracked_balance", real_bal) + drift, 8)
            self.next_compound = self.state_data.get("next_compound", self.tracked_balance * 1.24)
            self.shadow = 0.0
            self.mighty = round(((math.floor(self.tracked_balance / self.tens))* self.tens), 8)
            self.felix = self.state_data.get("felix", float(self.mighty))
            self.orgy = self.state_data.get("orgy", float(self.mighty))
            self.orgytwo = self.state_data.get("orgy", float(self.mighty))
            self.log(f"⚖️ Deviation Corrected: {drift:.8f}")
        else:
            self.log("🆕 Zero-baseline initialization execution...")
            self.cat = self.tabby
            self.fart = 1
            self.shadow = 0.0
            self.tracked_balance = real_bal
            self.initial_balance = real_bal
            self.mighty = round(((math.floor(self.tracked_balance / self.tens))* self.tens), 8)
            self.next_compound = self.tracked_balance * 1.24
            self.felix = float(self.mighty) 
            self.orgy = float(self.mighty) 
            self.orgytwo = float(self.mighty)
        
        self.last_balance = real_bal

    def load_state_file(self):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                keys = ["cat", "tabby", "felix", "orgy", "orgytwo", "tracked_balance", "initial_balance", "last_balance", "next_compound", "uppers", "downers"]
                for k in keys:
                    if k in data: data[k] = float(data[k])
                return data
        except: 
            return None

    def toggle_engine(self):
        self.is_running = True
        self.log(f"🚀 ENGINE ONLINE. Operational Unit: {self.cat:.8f}")
        
        self.last_change_time = time.time()
        self.last_activity_time = time.time()
        self.heartbeat = True
        self.bet_in_flight = False  
        
        # Fire structural action loop
        self.engine_timer.start(150)

    def lol_poop(self):
        self.log("🚨 Websocket stall caught! Re-establishing clean browser runtime context...")
        self.engine_timer.stop()
        self.bet_in_flight = False
        
        self.prev_balance = None
        self.prev_wins = None
        self.prev_losses = None
        
        self.browser_view.reload()
        QTimer.singleShot(15000, self.devils_pooped)
    
    def devils_pooped(self):
        self.kjool_look()

    def process_tick(self):
        self.evaluate_financial_sync()
        if time.time() - self.last_activity_time > 45:
            self.last_activity_time = time.time()
            self.lol_poop()
            return
        if self.heartbeat and not self.bet_in_flight:
            self.last_activity_time = time.time()
            self.mighty = round(((math.floor(self.tracked_balance / self.tens))* self.tens), 8)
            if ((self.tracked_balance > (self.mighty + self.sevens)) and (self.tracked_balance < (self.mighty + self.eights)) and (self.tracked_balance != self.felix)):
                self.cat = round((self.cat * 2), 8)
                self.felix = float(self.tracked_balance) 
            if (self.tracked_balance<self.orgytwo):
                self.orgytwo = float(self.tracked_balance) 
            if (self.tracked_balance>self.orgy):
                self.orgy = float(self.tracked_balance) 
            if (self.cat >= (self.tabby*7)): 
               if ((self.tracked_balance<=self.orgytwo) or (self.tracked_balance>=self.orgy)):
                  if (self.tracked_balance != self.felix):
                    self.cat = self.tabby
                    self.felix = float(self.mighty)
                    self.orgy = float(self.tracked_balance) 
                    self.orgytwo = float(self.tracked_balance) 
            if ((self.tracked_balance>=(self.felix+(self.cat*10))) or (self.tracked_balance<=(self.felix-(self.cat*10)))):
                self.log("hacker involved please fuck off hacker")
                self.heartbeat = False
                self.engine_timer.stop()
                return
            if (self.tracked_balance>=1440):
                self.log("winner winner chicken dinner")
                self.heartbeat = False
                self.engine_timer.stop()
                return
            self.shadow = float(self.tracked_balance) 
            self.save_state()
            self.bet_in_flight = True
            jsfool = f"""
            (function() {{
                var b_min = document.getElementById('b_min');
                var pct_chance = document.getElementById('pct_chance');
                var pct_bet = document.getElementById('pct_bet');
                var a_lo = document.getElementById('a_lo');
                
                if(b_min && pct_chance && pct_bet && a_lo) {{
                    b_min.click();
                    pct_chance.value = '49.5';
                    pct_bet.value = '{self.cat:.8f}';
                    a_lo.click();
                }}
            }})();
            """
            self.browser_view.page().runJavaScript(jsfool) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = BotEngine()
    bot.hide()  
    sys.exit(app.exec_())