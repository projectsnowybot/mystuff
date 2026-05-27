const fanboy = Number(document.getElementById("pct_balance").value);
document.getElementById("b_min").click();
const samuel = (fanboy/144000).toFixed(8);
var amanku = samuel; 
const ziggie = (samuel*10);
const smile = (samuel*6.9);
const buck = (samuel*7.9);
var moron = fanboy;
var baboons = ((Math.floor(fanboy/ziggie))*ziggie);
var madman = ((Math.floor(fanboy/ziggie))*ziggie);
var OSCAR = fanboy;
var snowy = fanboy;
var billy = fanboy;
var scotty = fanboy; 
var betfired = false 
var fart = 1;
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

        if (snowy >= (madman+(ziggie*fart))){ 
            amanku = samuel; 
            fart = 1;
            baboons = ((Math.floor(snowy/ziggie))*ziggie);
            madman = ((Math.floor(snowy/ziggie))*ziggie);
        } 
        if ((snowy > (((Math.floor(snowy/ziggie))*ziggie)+smile)) && (snowy < (((Math.floor(snowy/ziggie))*ziggie)+buck)) && (snowy>baboons)){
            amanku = amanku*2;
            baboons = parseFloat(snowy); 
        }
        if ((snowy > (((Math.floor(snowy/ziggie))*ziggie)+smile)) && (snowy < (((Math.floor(snowy/ziggie))*ziggie)+buck)) && (snowy<baboons)){
            amanku = amanku*2;
            fart = 0;
            baboons = parseFloat(snowy); 
        }
        bogus =  parseFloat((amanku*1).toFixed(8));
        console.log("Profit:", ((snowy - fanboy) * 1).toFixed(8));
        document.getElementById("pct_chance").value=49.5
        document.getElementById("pct_bet").value = (amanku*1).toFixed(8);
        billy = parseFloat(((snowy + bogus)*1).toFixed(8));
        scotty = parseFloat(((snowy - bogus)*1).toFixed(8));
        betfired = true;
        document.getElementById("a_lo").click();
    }
}


setInterval(() => runFelineBot(), 1)
