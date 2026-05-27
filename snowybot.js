const ALICE = Number(document.getElementById("pct_balance").value);
document.getElementById("b_min").click();
const bastard = (ALICE/144).toFixed(8);
var beats = bastard; 
const tenticle = (bastard*10);
const fornication = (bastard*6.9);
const greast = (bastard*7.9);
var moron = ((Math.floor(ALICE/tenticle))*tenticle)-tenticle;
var baboons = ((Math.floor(ALICE/tenticle))*tenticle);
var madman = parseFloat((Math.ceil(belance/tenticle))*tenticle);
var OSCAR = ALICE;
var belance = ALICE;
var billy = ALICE;
var scotty = ALICE; 
var hugo = 6.9;
var milly = 2.9;  
var bogus =  parseFloat((beats*1).toFixed(8));

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runFelineBot() {
    OSCAR = Number(document.getElementById("pct_balance").value);

    if ((OSCAR==billy) || (OSCAR==scotty)) {
        belance = parseFloat(OSCAR);
        if (belance>madman){
            madman = parseFloat(belance);
        }
        if ((belance-(beats*2)) <= moron){  
            beats = bastard; 
            baboons = parseFloat((Math.floor(belance/tenticle))*tenticle);
            moron = parseFloat((Math.floor(belance/tenticle))*tenticle);
            madman = parseFloat(belance); 
        }
        if ((belance>=madman) && ((belance-((beats*4)+bastard)) <= moron)){  
            beats = bastard; 
            baboons = parseFloat((Math.floor(belance/tenticle))*tenticle);
            madman = parseFloat(belance); 
        } 
        if ((belance-moron)>=(tenticle*24)){
            beats = bastard; 
            baboons = parseFloat((Math.floor(belance/tenticle))*tenticle);
            moron = parseFloat(((Math.floor(belance/tenticle))*tenticle)-tenticle);
            madman = parseFloat(belance); 
        } 
        if ((belance > (((Math.floor(belance/tenticle))*tenticle)+fornication)) && (belance < (((Math.floor(belance/tenticle))*tenticle)+greast)) && (belance!==baboons)){
            beats = beats*2;
            baboons = parseFloat(belance); 
        }
        bogus =  parseFloat((beats*1).toFixed(8));
        billy = parseFloat(((belance + bogus)*1).toFixed(8));
        scotty = parseFloat(((belance - bogus)*1).toFixed(8));
        console.log("Profit:", ((belance - ALICE) * 1).toFixed(8));
        document.getElementById("pct_chance").value=49.5
        document.getElementById("pct_bet").value = (beats*1).toFixed(8);
        document.getElementById("a_lo").click(); 
    }
}


setInterval(() => runFelineBot(), 1000)
