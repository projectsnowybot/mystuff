const {
    Builder: e,
    By: t
} = require("selenium-webdriver"), firefox = require("selenium-webdriver/firefox"), fs = require("fs"), readline = require("readline");
let config = {
        url: "https://just-dice.com",
        div: 320,
        binary: "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        gecko: "C:\\Users\\snowy\\geckodriver.exe"
    },
    bot = {
        nextBet: 0,
        snowy: 0,
        tens: 0,
        sevens: 0,
        eights: 0,
        oldSevBal: 0,
        oldDownBal: 0,
        oldUpBal: 0,
        floorTens: 0,
        feasle: 0,
        marker: 0,
        markThree: 0,
        liveBal: 0
    },
    self = {
        startBal: 0,
        oldBal: 0
    },
    stateLoaded = !1,
    userCreds = null,
    passCreds = null,
    code2FA = null,
    temporarySessionBalance = 0;

function ask(e, t = !1) {
    let l = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    return new Promise(o => {
        t && process.stdin.on("data", function t(o) {
            ["\n", "\r", "\x04"].includes(o += "") ? process.stdin.off("data", t) : (readline.clearLine(process.stdout, 0), readline.cursorTo(process.stdout, 0), process.stdout.write(e + "*".repeat(l.line.length)))
        }), l.question(e, e => {
            l.close(), o(e)
        })
    })
}(async function runAutomationPipeline() {
    try {
        fs.existsSync("snow_state.json") ? (bot = JSON.parse(fs.readFileSync("snow_state.json", "utf8")), stateLoaded = !0, console.log("📂 Previous state profile detected!")) : console.log("Fresh session profile initialization.")
    } catch (l) {
        console.log("⚠️ State extraction failure.")
    }
    let o, a = await new e().forBrowser("firefox").setFirefoxOptions(new firefox.Options().setBinary(config.binary).addArguments("--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage")).setFirefoxService(new firefox.ServiceBuilder(config.gecko)).build();
    console.log(`🌐 Connecting to instance: ${config.url}`), await a.manage().window().maximize();
    while (true) {
        try {
            await a.get(config.url);
            break;
        } catch (err) {
            console.log("❌ Connection failed. Retrying...");
            await new Promise(e => setTimeout(e, 5000));
        }
    }
    console.log("⏳ Waiting 32s for scripts..."), await new Promise(e => setTimeout(e, 32e3));
    try {
        await a.findElement(t.css("a.fancybox-item.fancybox-close")).click();
    } catch (n) {}
    await new Promise(e => setTimeout(e, 5e3)), await a.executeScript(() => {
        let e = document.querySelector('ul.tabs a[href="#account"]');
        e && (e.scrollIntoView({
            block: "center"
        }), e.focus(), e.dispatchEvent(new KeyboardEvent("keydown", {
            key: "Enter",
            code: "Enter",
            keyCode: 13,
            which: 13,
            bubbles: !0
        })), e.click())
    }), await new Promise(e => setTimeout(e, 2e3));
    if (!userCreds) {
        userCreds = await ask("👤 Username: ");
        passCreds = await ask("🔑 Password: ", !0);
        console.log();
        code2FA = await ask("🛡️ 2FA Code: ", !0);
        console.log();
    }
    try {
        await (await a.findElement(t.id("myuser"))).sendKeys(userCreds), await (await a.findElement(t.id("mypass"))).sendKeys(passCreds), code2FA.trim() && await (await a.findElement(t.id("mycode"))).sendKeys(code2FA.trim()), await a.executeScript(() => {
            let e = Array.from(document.querySelectorAll("input, button, a")).find(e => "login" === (e.value || e.innerText || "").toLowerCase().trim());
            e && e.click()
        })
    } catch (b) {}
    for (let d = 32; d > 0; d--) {
        readline.clearLine(process.stdout, 0);
        readline.cursorTo(process.stdout, 0);
        process.stdout.write(`⏳ Syncing layout... ${d}s remaining`);
        await new Promise(e => setTimeout(e, 1000));
    }
    console.log("\n🚀 Launching automation loop structure...");
    let f = !1,
        lastBalanceChangeTime = Date.now(),
        shouldTriggerReload = !1;
    await a.executeScript(e => {
        window.__snowy_bet_signal = !1, window.__snowy_next_bet_amount = "0.00000000", window.__latest_snow_state = null;
        (async () => {
            let t = () => {
                let e = document.getElementById("pct_balance");
                if (!e) return null;
                let t = (e.value || e.innerText || e.textContent || "").trim();
                return "" === t || t.toLowerCase().includes("loading") ? null : parseFloat(t.replace(/[^0-9.]/g, ""))
            };
            for (;;) {
                if (!window.__snowy_bet_signal) {
                    await new Promise(e => setTimeout(e, 1));
                    continue
                }
                let l = document.getElementById("pct_bet"),
                    o = document.getElementById("pct_chance"),
                    a = document.getElementById("a_lo");
                if (l && o && a) {
                    let n = t();
                    if (null === n) {
                        await new Promise(e => setTimeout(e, 1));
                        continue
                    }
                    l.focus();
                    l.value = window.__snowy_next_bet_amount, l.dispatchEvent(new Event("input", {
                        bubbles: !0
                    })), l.dispatchEvent(new Event("change", {
                        bubbles: !0
                    })), l.dispatchEvent(new KeyboardEvent("keydown", {
                        key: "Enter",
                        code: "Enter",
                        keyCode: 13,
                        which: 13,
                        bubbles: !0
                    })), o.focus();
                    o.value = e, o.dispatchEvent(new Event("input", {
                        bubbles: !0
                    })), o.dispatchEvent(new Event("change", {
                        bubbles: !0
                    })), o.dispatchEvent(new KeyboardEvent("keydown", {
                        key: "Enter",
                        code: "Enter",
                        keyCode: 13,
                        which: 13,
                        bubbles: !0
                    })), a.classList.remove("invalid"), a.click(), window.__snowy_bet_signal = !1;
                    let s = !1;
                    for (; !s;) {
                        await new Promise(e => setTimeout(e, 1));
                        let i = t();
                        null !== i && i !== n && (s = !0, window.__latest_snow_state = i.toString())
                    }
                } else await new Promise(e => setTimeout(e, 100))
            }
        })()
    }, "49.5");
    for (;;) try {
        if (f && (Date.now() - lastBalanceChangeTime > 55000)) {
            console.log("\n🛑 [TIMEOUT] Reloading driver...");
            shouldTriggerReload = !0;
            break;
        }
        let c = f ? await a.executeScript(() => {
            let e = window.__latest_snow_state;
            return window.__latest_snow_state = null, e
        }) : await a.executeScript(() => {
            let e = document.getElementById("pct_balance");
            return e ? (e.value || e.innerText || e.textContent || "").trim().replace(/[^0-9.]/g, "") : null
        });
        if (!c) {
            await new Promise(e => setTimeout(e, 1));
            continue
        }
        if (bot.liveBal = parseFloat(c), bot.liveBal >= 14400) {
            console.log(`\n🎉 Target Reached! Balance: ${bot.liveBal.toFixed(8)}`);
            break
        }
        if (bot.liveBal > 0) {
            let outcome = "⚪ SYNC";
            if (f) {
                outcome = bot.liveBal > self.oldBal ? "🟢 WIN" : bot.liveBal < self.oldBal ? "🔴 LOSS" : "⚪ SYNC";
                lastBalanceChangeTime = Date.now();
            } else {
                console.log("🚀 Loop active.");
                f = !0, lastBalanceChangeTime = Date.now();
                if (self.startBal === 0) self.startBal = bot.liveBal;
                self.oldBal = temporarySessionBalance > 0 && temporarySessionBalance !== bot.liveBal ? temporarySessionBalance : bot.liveBal;
            }
            if (!bot.snowy || !bot.oldDownBal || !bot.oldUpBal) {
                bot.snowy = self.startBal / config.div, bot.feasle = bot.snowy, bot.tens = 10 * bot.snowy, bot.sevens = 6.9 * bot.snowy, bot.eights = 7.9 * bot.snowy, bot.oldDownBal = self.startBal - bot.tens, bot.oldUpBal = self.startBal, bot.nextBet = bot.snowy
            }
            bot.floorTens = Math.floor(bot.liveBal / bot.tens) * bot.tens;
            if ((bot.liveBal-(bot.oldDownBal+(bot.nextBet * 2)))<=0) {
                bot.marker = parseFloat(bot.oldDownBal + bot.tens);
                bot.markThree = parseFloat(bot.oldDownBal + bot.tens);
                bot.nextBet = 0;
                bot.oldSevBal = parseFloat(bot.floorTens);
                bot.oldUpBal = parseFloat((Math.floor(bot.liveBal / bot.tens) + 1) * bot.tens);
                while (true) {
                    if (bot.marker > (bot.markThree + (bot.feasle * 6.9))) {
                        bot.feasle = bot.feasle * 2;
                        bot.markThree = parseFloat(bot.marker);
                        bot.marker = bot.marker + bot.feasle;
                    } else if (bot.marker >= bot.liveBal) {
                        bot.marker = parseFloat(bot.oldDownBal + bot.tens);
                        bot.markThree = parseFloat(bot.oldDownBal + bot.tens);
                        bot.nextBet = parseFloat(bot.feasle);
                        bot.feasle = bot.snowy;
                        break;
                    } else {
                        bot.marker = bot.marker + bot.feasle;
                    }
                }
                await new Promise(res => {
                    let checkInterval = setInterval(() => {
                        if (bot.nextBet > 0) {
                            clearInterval(checkInterval);
                            res();
                        }
                    }, 10);
                });
            }
            if (bot.liveBal < bot.oldDownBal) {
                bot.nextBet = bot.snowy;
                bot.oldSevBal = parseFloat(bot.floorTens);
                bot.oldDownBal = parseFloat(bot.floorTens);
                bot.oldUpBal = parseFloat(bot.floorTens);
            }
            if (bot.liveBal >= (bot.oldUpBal + (bot.tens * 6))){
                bot.nextBet = bot.snowy;
                bot.oldSevBal = parseFloat(bot.floorTens);
                bot.oldUpBal = parseFloat(bot.floorTens);
            }
            if (bot.liveBal > (bot.floorTens + bot.sevens) && bot.liveBal < (bot.floorTens + bot.eights) && bot.liveBal !== bot.oldSevBal) {
                bot.nextBet = Number((bot.nextBet * 2).toFixed(8));
                bot.oldSevBal = parseFloat(bot.liveBal);
            }
            let totalProfit = bot.liveBal - self.startBal;
            console.log(`[${outcome}] Bet: ${bot.nextBet.toFixed(8)} | Balance: ${bot.liveBal.toFixed(8)} | Profit: ${totalProfit >= 0 ? "+" : ""}${totalProfit.toFixed(8)}`), self.oldBal = bot.liveBal, temporarySessionBalance = bot.liveBal, fs.writeFileSync("snow_state.json", JSON.stringify(bot)), await a.executeScript(e => {
                window.__snowy_next_bet_amount = e, window.__snowy_bet_signal = !0
            }, bot.nextBet.toFixed(8))
        }
    } catch (w) {
        await new Promise(e => setTimeout(e, 1))
    }
    try {
        await a.quit()
    } catch (err) {}
    if (shouldTriggerReload) {
        console.log("🔄 Restarting instance...");
        stateLoaded = !1;
        await runAutomationPipeline();
    }
})();