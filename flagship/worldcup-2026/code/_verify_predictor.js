// Independent check: does the inlined WC_MODEL (used by the new "any two teams"
// predictor) reproduce the PUBLISHED match_probs.csv? If yes, the live recompute
// is model-faithful. Pure logic, no browser.
const fs = require('fs');

const INDEX = 'D:/AI/journalist agent review/phase2/project/worldcup_2026/blog_showcase_opus48_0621/index.html';
const MP    = 'D:/AI/journalist agent review/phase2/datasets/worldcup_2026/forecast_outputs/match_probs.csv';

// --- extract the WC_MODEL <script> block from the shipped index.html ---
const html = fs.readFileSync(INDEX, 'utf8');
const anchor = html.indexOf('window.WC_MODEL = (function');
const start  = html.lastIndexOf('<script>', anchor) + '<script>'.length;
const end    = html.indexOf('</script>', anchor);
const modelJs = html.slice(start, end);
global.window = {};
eval(modelJs);                 // defines window.WC_MODEL
const WC = global.window.WC_MODEL;
const D = WC.DATA;
const P = D.params;

function expGoals(eh, ea) {     // same formula the predictor ports for likely score
  const sup = P.a + P.b * (eh - ea);
  return [Math.max(0.05, (P.mu + sup) / 2), Math.max(0.05, (P.mu - sup) / 2)];
}

// --- read a few published fixtures and compare ---
const lines = fs.readFileSync(MP, 'utf8').trim().split(/\r?\n/);
const hdr = lines[0].split(',');
const col = name => hdr.indexOf(name);
const rows = lines.slice(1).map(l => l.split(','));

const samples = ['Brazil', 'USA', 'Spain', 'Germany', 'Argentina'];  // pick fixtures whose home team is one of these
let checked = 0, maxErr = 0;
console.log('fixture                         pub(H/D/A)        model(H/D/A)      pub xG    model xG   ok');
for (const r of rows) {
  const home = r[col('home')], away = r[col('away')];
  if (!samples.includes(home)) continue;
  const eh = D.elo[home], ea = D.elo[away];
  if (eh == null || ea == null) { console.log('  MISSING ELO', home, away); continue; }
  const p = WC.matchProb(eh, ea);                 // [pH,pD,pA]
  const pubH = +r[col('p_home_win')], pubD = +r[col('p_draw')], pubA = +r[col('p_away_win')];
  const [lh, la] = expGoals(eh, ea);
  const e = Math.max(Math.abs(p[0]-pubH), Math.abs(p[1]-pubD), Math.abs(p[2]-pubA));
  maxErr = Math.max(maxErr, e); checked++;
  const lbl = (home + ' v ' + away).padEnd(30);
  console.log(`${lbl}  ${pubH.toFixed(3)}/${pubD.toFixed(3)}/${pubA.toFixed(3)}   ` +
              `${p[0].toFixed(3)}/${p[1].toFixed(3)}/${p[2].toFixed(3)}   ` +
              `${(+r[col('exp_home_goals')]).toFixed(2)}/${(+r[col('exp_away_goals')]).toFixed(2)}  ` +
              `${lh.toFixed(2)}/${la.toFixed(2)}  ${e < 0.02 ? 'YES' : 'NO('+e.toFixed(3)+')'}`);
  if (checked >= 8) break;
}
console.log(`\nchecked ${checked} fixtures; max prob error = ${maxErr.toFixed(4)} (want < 0.02)`);
console.log('params:', JSON.stringify(P), '| matchProb shape:', Array.isArray(WC.matchProb(D.elo['Brazil'], D.elo['Haiti'])) ? 'array[3]' : 'object');
