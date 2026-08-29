const whisker = parseFloat(((document.getElementById("pct_balance").value)*1).toFixed(8));
var becance = parseFloat(whisker)
var garfield = parseFloat(whisker)
var nobter = parseFloat((whisker/1000).toFixed(8));
var kool = parseFloat(nobter);
var frockter = parseFloat(nobter);
var tens = nobter*10;
var xix = nobter*60;
var sevens = nobter*6.9;
var eights = nobter*7.9;
var popie = whisker;
var wreggle = parseFloat(((Math.floor(whisker/tens))*tens));
var voxxy = parseFloat(whisker);
var farts = 0;
var slut = parseFloat((frockter*1).toFixed(8));
var mookie = document.getElementById("pct_balance").value;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}



async function runFelineBot() {
  while (true){
  mookie = parseFloat(((document.getElementById("pct_balance").value)*1).toFixed(8));
  if ((mookie==(((becance+slut)*1).toFixed(8))) || (mookie==(((becance-slut)*1).toFixed(8))) || (farts<=1)){
        becance = parseFloat(mookie);
    if ((becance-(frockter*9))<nobter){
        console.log("handbrake time");
        frockter = parseFloat(nobter);
        wreggle = parseFloat(((Math.floor(becance/tens))*tens));
        voxxy = parseFloat(becance);
    }
    if (becance>=(voxxy+xix)){
        console.log("upper handbrake time");
        frockter = parseFloat(nobter);
        wreggle = parseFloat(((Math.floor(becance/tens))*tens));
        voxxy = parseFloat(becance);
    }
    if (becance>(garfield*2)){
        nobter = (nobter*2);
        tens = nobter*10;
        xix = nobter*60;
        sevens = nobter*6.9;
        eights = nobter*7.9;
        frockter = parseFloat(nobter);
        wreggle = parseFloat(((Math.floor(becance/tens))*tens));
        voxxy = parseFloat(becance);
    }
    if ((becance>(((Math.floor(becance/tens))*tens)+sevens))&&(becance<(((Math.floor(becance/tens))*tens)+eights))&&(becance!==wreggle)){
        frockter = (frockter*2);
        wreggle = parseFloat(becance);
        console.log("doubling")
    }
    if (becance>=(whisker*144)){
        console.log("winner winner chicken dinner");
        return false;
    }
    slut = parseFloat((frockter*1).toFixed(8));
    console.log("bet:", frockter, "balance:", becance)
    document.getElementById("b_min").click();
    document.getElementById("pct_chance").value = 49.5;
    document.getElementById("pct_bet").value = (slut*1).toFixed(8);
    popie = becance;
    farts = farts+1;
    document.getElementById("a_lo").click();
    }
  await sleep(1000);
  }
}


runFelineBot();
