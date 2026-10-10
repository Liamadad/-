const fs = require('fs');
const html = fs.readFileSync('out/danci.html', 'utf8');
const script = html.slice(html.indexOf('<script>') + 8, html.lastIndexOf('</script>'));
new Function(script);                                   // syntax check of the whole page script
const logic = script.slice(0, script.indexOf('function row('));
const api = new Function(logic + '; return {W, info, dayWords, learned, dateOfStudyDay, weekWords, isLastSatOfMonth, PLAN, WEEKS, OFF};')();
const { W, info, dayWords, learned, dateOfStudyDay, weekWords, PLAN, WEEKS } = api;
const assert = (c, m) => { if (!c) { console.error('FAIL', m); process.exitCode = 1; } };
let s = 0, r = 0, dayOfRec = {};
for (let d = 1; d <= WEEKS * 5; d++) {
  const w = dayWords(d); if (!w) continue;
  assert(w.s[0] === s && w.r[0] === r, 'contiguous ' + d);
  for (let i = w.r[0]; i < w.r[1]; i++) dayOfRec[W.R[i][0]] = d;
  for (let i = w.s[0]; i < w.s[1]; i++) { const wd = W.S[i][0]; if (i >= 570) assert(dayOfRec[wd] !== undefined && dayOfRec[wd] < d, 'spell after rec ' + wd + ' day ' + d); }
  s = w.s[1]; r = w.r[1];
}
console.log('totals', s, r, 'of', W.S.length, W.R.length);
assert(s === W.S.length && r === W.R.length, 'all words scheduled');
const D = (y, m, d) => new Date(y, m - 1, d, 12);
for (const [y, m, d] of [[2026,10,10],[2026,10,12],[2026,10,16],[2026,10,17],[2026,10,18],[2027,1,4],[2027,8,16],[2027,9,27],[2027,10,15],[2027,11,1],[2027,12,31],[2028,1,2],[2028,1,3]]) {
  const it = info(D(y, m, d)); const w = it.d ? dayWords(it.d) : null;
  console.log(`${y}-${m}-${d}`, JSON.stringify(it), w ? `new ${w.s[1]-w.s[0]}+${w.r[1]-w.r[0]}` : '');
}
console.log('day1 date', dateOfStudyDay(1).toDateString(), 'day6', dateOfStudyDay(6).toDateString(), 'day320', dateOfStudyDay(320).toDateString());
console.log('week1 counts', weekWords(1).s.length, weekWords(1).r.length, 'week52', weekWords(52).s.length, weekWords(52).r.length);
// review load at a steady-state day
const it = info(D(2027, 3, 10)); let n = 0; for (const k of [1,2,4,7,15,30]) { const w = dayWords(it.d - k); if (w) n += (w.s[1]-w.s[0]) + (w.r[1]-w.r[0]); }
console.log('review words on 2027-3-10:', n);
