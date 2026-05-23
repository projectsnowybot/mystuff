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
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineScript, QWebEngineSettings, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from bs4 import BeautifulSoup

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-audio-output"
logging.getLogger("PyQt5").setLevel(logging.CRITICAL)

u = input("Enter username: ")
p = getpass.getpass("Enter password: ")

URL = "https://just-dice.com"
STATE_FILE = ".snowybot.json"


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
        
        self.neXtbet = 0.0
        self.bolux = 0.0
        self.oldsevensbalance = 0.0
        self.oldupbalance = 0.0
        self.olddownbalance = 0.0
        self.basetimes = 1
        self.basebet = 0.0
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
        
        # Connection management flag
        self.is_reconnecting = False

        # Browser Setup
        self.browser_view = QWebEngineView()
        
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)

        self.channel = QWebChannel()
        self.bridge_object = WebBridge(self.evaluate_financial_sync)
        self.channel.registerObject("pyBridge", self.bridge_object)
        self.browser_view.page().setWebChannel(self.channel)

        # Monitor connection failures and load status changes
        self.browser_view.page().loadFinished.connect(self.handle_load_finished)

        self.bet_in_flight = False
        self.last_activity_time = time.time()

        self.engine_timer = QTimer()
        self.engine_timer.timeout.connect(self.process_tick)

        self.heartbeat = True
        self.log("System initialized. Running in Headless Server Mode...")
        self.browser_view.setUrl(QUrl(URL))
        
        QTimer.singleShot(35000, self.kjool_look)

    def log(self, msg):
        print(f"{msg}")

    def handle_load_finished(self, success):
        if not success:
            self.log("🚨 Network interface changed or link dropped. Pausing engine...")
            self.trigger_network_reconnect()

    def trigger_network_reconnect(self):
        if self.is_reconnecting:
            return
            
        self.is_reconnecting = True
        self.is_running = False
        self.engine_timer.stop()
        self.bet_in_flight = False
        
        self.prev_balance = None
        self.prev_wins = None
        self.prev_losses = None
        
        self.log("📡 Scheduling page reload in 10 seconds...")
        QTimer.singleShot(10000, self.execute_reconnect_retry)

    def execute_reconnect_retry(self):
        self.log("🔄 Executing interface reload...")
        self.browser_view.reload()
        QTimer.singleShot(20000, self.verify_reconnection_status)

    def verify_reconnection_status(self):
        self.browser_view.page().runJavaScript(
            "document.getElementsByClassName('name_button').length", 
            self.confirm_reconnect_page_state
        )

    def confirm_reconnect_page_state(self, result):
            self.log("🟢 Connection trying. Loading state coordinates...")
            self.is_reconnecting = False
            self.kjool_look()

    def kjool_look(self):
        if self.is_reconnecting: 
            return
        try: 
           self.browser_view.page().runJavaScript("document.getElementsByClassName('name_button')[0].click()")
        except Exception as e:
           pass
        self.log("Analyzing interface state parameters...")
        self.betfired = False
        QTimer.singleShot(5000, self.inject_login)

    def inject_login(self):
        if self.is_reconnecting: return
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
        QTimer.singleShot(12000, self.start_post_login_scrapers)

    def start_post_login_scrapers(self):
        if self.is_reconnecting: 
            return
        self.log("🔓 Login pipeline finalized. Initializing data trackers...")
        self.deploy_dom_observer()

    def check_ready(self):
        if self.is_reconnecting: return
        page = self.browser_view.page()
        page.runJavaScript(
            "document.getElementById('pct_balance') ? document.getElementById('pct_balance').value : null", 
            self.handle_python_value_read
        )

    def handle_python_value_read(self, val):
        if self.is_reconnecting: 
            return
        if val is None or str(val) == "null" or str(val).strip() == "":
            print("⏳ Balance element value unreadable. Retrying...")
            QTimer.singleShot(2000, self.trigger_network_reconnect)
            return

        try:
            cleaned_val = "".join(c for c in str(val) if c.isdigit() or c in ".-")
            balance = float(cleaned_val)
            
            #self.log(f"🎯 Value Extracted successfully: {balance:.8f}")
            self.balnce = str(balance)
            
            if not self.is_running:
                self.verify_login()
                
        except Exception as e:
            print(f"⚠️ Value parser failure: {e}")
            QTimer.singleShot(2000, self.check_ready)

    def verify_login(self):
        if self.is_reconnecting: return
        try:
            balance = float(self.balnce)
        except Exception as e:
            QTimer.singleShot(5000, self.check_ready)
            return
   
        self.log(f"✅ Active Balance Confirmed: {balance:.8f}")
        self.setup_state(balance)
        QTimer.singleShot(1500, self.toggle_engine)

    def deploy_wins(self):
        if self.is_reconnecting: return
        self.browser_view.page().runJavaScript("document.getElementById('wins').innerText.replace(/,/g, '')", self.winning_wins)
   
    def deploy_loss(self):
        if self.is_reconnecting: return
        self.browser_view.page().runJavaScript("document.getElementById('losses').innerText.replace(/,/g, '')", self.lossing_loses)

    def deploy_balance(self): 
        if self.is_reconnecting: return
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
        if self.is_reconnecting: return
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
                "neXtbet": self.neXtbet, "basebet": self.basebet, "oldsevensbalance": self.oldsevensbalance, "oldupbalance": self.oldupbalance, "olddownbalance": self.olddownbalance, "basetimes": self.basetimes,
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
            self.basebet = 0.00000001
        elif self.state_data:
            self.basebet = self.state_data.get("basebet")
        else:
            self.basebet = round(balance / 144000, 8)
        
        self.tens = self.basebet * 10.0
        self.sevens = self.basebet * 6.9
        self.eights = self.basebet * 7.9
        self.uppers = 6.9
        self.downers = 2.9

    def setup_state(self, real_bal):
        self.calculate_units(real_bal)
        self.state_data = self.load_state_file()
        
        if self.state_data:
            self.log("📂 Resuming tracking matrices from cache registry...")
            self.neXtbet = self.state_data.get("neXtbet", self.basebet)
            self.basetimes = int(self.state_data.get("basetimes", 1))
            self.initial_balance = self.state_data.get("initial_balance", real_bal)
            last_saved = self.state_data.get("last_balance", real_bal)
            drift = real_bal - last_saved
            self.tracked_balance = round(self.state_data.get("tracked_balance", real_bal) + drift, 8)
            self.next_compound = self.state_data.get("next_compound", self.tracked_balance * 1.24)
            self.shadow = 0.0
            self.lowertens = round(((math.floor(self.tracked_balance / self.tens))* self.tens), 8)
            
            # Auto-align target anchors on resume to protect against small sync slips
            self.oldsevensbalance = self.state_data.get("oldsevensbalance", self.tracked_balance)
            self.oldupbalance = self.state_data.get("oldupbalance", self.lowertens)
            self.olddownbalance = self.state_data.get("olddownbalance", self.lowertens)
            self.log(f"⚖️ Deviation Corrected: {drift:.8f}")
        else:
            self.log("🆕 Zero-baseline initialization execution...")
            self.neXtbet = self.basebet
            self.basetimes = 1
            self.shadow = 0.0
            self.tracked_balance = real_bal
            self.initial_balance = real_bal
            self.lowertens = round(((math.floor(self.tracked_balance / self.tens))* self.tens), 8)
            self.next_compound = self.tracked_balance * 1.24
            self.oldsevensbalance = float(self.lowertens) 
            self.oldupbalance = float(self.lowertens) 
            self.olddownbalance = float(self.lowertens)
        
        self.last_balance = real_bal

    def load_state_file(self):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                keys = ["neXtbet", "basebet", "oldsevensbalance", "oldupbalance", "olddownbalance", "tracked_balance", "initial_balance", "last_balance", "next_compound", "uppers", "downers"]
                for k in keys:
                    if k in data: data[k] = float(data[k])
                return data
        except: 
            return None

    def toggle_engine(self):
        if self.is_reconnecting: return
        self.is_running = True
        self.log(f"🚀 ENGINE ONLINE. Operational Unit: {self.neXtbet:.8f}")
        
        self.last_change_time = time.time()
        self.last_activity_time = time.time()
        self.heartbeat = True
        self.bet_in_flight = False  
        
        QTimer.singleShot(1000, self.process_tick) 

    def lol_poop(self):
        self.trigger_network_reconnect()

    def process_tick(self):
        if self.is_reconnecting or not self.is_running: 
            return
            
        self.evaluate_financial_sync()
        if time.time() - self.last_activity_time > 45:
            self.last_activity_time = time.time()
            self.lol_poop()
            return
            
        if self.heartbeat and (not self.bet_in_flight) and (self.tracked_balance != self.shadow):
            self.last_activity_time = time.time()
            self.lowertens = round(((math.floor(self.tracked_balance / self.tens))* self.tens), 8)
            if (self.tracked_balance >= (self.oldupbalance+(self.tens*self.basetimes))):
                self.neXtbet = self.basebet
                self.basetimes = 1 
                self.oldsevensbalance = float(self.lowertens)
                self.oldupbalance = float(self.lowertens) 
            if ((self.tracked_balance > (self.lowertens + self.sevens)) and (self.tracked_balance < (self.lowertens + self.eights)) and (self.tracked_balance > self.oldsevensbalance)):
                self.neXtbet = round((self.neXtbet * 2), 8)
                self.oldsevensbalance = float(self.tracked_balance)  
            if ((self.tracked_balance > (self.lowertens + self.sevens)) and (self.tracked_balance < (self.lowertens + self.eights)) and (self.tracked_balance < self.oldsevensbalance)):
                self.neXtbet = round((self.neXtbet * 2), 8)
                self.basetimes = 0
                self.oldsevensbalance = float(self.tracked_balance)       
            if ((self.tracked_balance >= (self.oldsevensbalance + (self.neXtbet * 10))) or (self.tracked_balance <= (self.oldsevensbalance - (self.neXtbet * 10)))):
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
                    pct_bet.value = '{self.neXtbet:.8f}';
                    a_lo.click();
                }}
            }})();
            """
            self.browser_view.page().runJavaScript(jsfool)
        QTimer.singleShot(150, self.process_tick) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = BotEngine()
    bot.hide()  
    sys.exit(app.exec_())
