const fanboy = Number(document.getElementById("pct_balance").value);
document.getElementById("b_min").click();
const samuel = (fanboy/144000).toFixed(8);
var amanku = samuel; 
const ziggie = (samuel*10);
const smile = (samuel*6.9);
const buck = (samuel*7.9);
var moron = fanboy;
var butch = (fanboy/ziggie);
var henry = Math.floor(butch);
var mate = henry*ziggie;
var baboons = fanboy;
var madman = fanboy;
var OSCAR = fanboy;
var snowy = fanboy;
var billy = fanboy;
var scotty = fanboy; 
var betfired = false 
var fart = 1;
var strog = 0;
var stig = 0;
var heartbeat = true;
var bogus =  parseFloat((amanku*1).toFixed(8));

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runFelineBot() {
    OSCAR = Number(document.getElementById("pct_balance").value);
    if ((OSCAR==billy) || (OSCAR==scotty)) {
        betfired = false;
    } 
    if (!betfired){
        snowy = parseFloat(OSCAR);
        var butch = (snowy/ziggie);
        var henry = Math.floor(butch);
        var mate = henry*ziggie;
        if (snowy >= (madman+(ziggie*fart))){ 
            amanku = samuel; 
            fart = 1;
            baboons = parseFloat(snowy);
            madman = parseFloat(snowy);
        } 
        if ((snowy > (mate+smile)) && (snowy < (mate+buck)) && (snowy>baboons)){
            amanku = amanku*2;
            baboons = parseFloat(snowy); 
        }
        if ((snowy > (mate+smile)) && (snowy < (mate+buck)) && (snowy<baboons)){
            amanku = amanku*2;
            fart = 0;
            baboons = parseFloat(snowy); 
        }
        if ((amanku==samuel)&&((snowy-baboons)>=0)){
             strog = ((snowy-baboons)/samuel).toFixed(8);
             stig = 0; 
        }
        if ((amanku==samuel)&&((baboons-snowy)>=0)){
             strog = ((baboons-snowy)/samuel).toFixed(8);
             stig = 0;
        }   
        if ((amanku>samuel)&&((snowy-baboons)>=0)){
             stig = ((snowy-baboons)/amanku).toFixed(8);
             strog = 0; 
        }
        if ((amanku>samuel)&&((baboons-snowy)>=0)){
             stig = ((baboons-snowy)/amanku).toFixed(8);
             strog = 0; 
        }

        console.log("number of bets basebet:", strog)
        console.log("number of bets nextbet:", stig)
 
        if (((amanku>samuel)&&(stig>6)) || ((amanku<=samuel)&&(strog>10))){
             console.log("stopping due to hacker betting on balance without my permission which is federal crime")
             heartbeat=false;
             return
        }
        if (snowy>(fanboy+1440)){
             console.log("winner winner chicken dinner")
             heartbeat=false;
             return
        }
        bogus =  parseFloat((amanku*1).toFixed(8));
        console.log("Profit:", ((snowy - fanboy) * 1).toFixed(8));
        document.getElementById("pct_chance").value=49.5
        document.getElementById("pct_bet").value = (amanku*1).toFixed(8);
        billy = parseFloat(((snowy + bogus)*1).toFixed(8));
        scotty = parseFloat(((snowy - bogus)*1).toFixed(8));
        if (heartbeat){
             betfired = true;
             document.getElementById("a_lo").click();
        }
    }
}


setInterval(() => runFelineBot(), 1)
