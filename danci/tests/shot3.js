const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [name, scheme, w] of [['h_375_light','light',375],['h_375_dark','dark',375]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 760 }, deviceScaleFactor: 2, colorScheme: scheme });
    const p = await ctx.newPage(); await p.clock.setFixedTime(new Date('2027-03-10T10:00:00'));
    await p.goto('file://' + process.cwd() + '/site/index.html');
    await p.click('[data-tab="spell"]'); await p.click('#shuffle'); await p.click('#cover');
    const small = await p.$$eval('button', bs => bs.filter(x => { const r = x.getBoundingClientRect(); return r.width && (r.width < 44 || r.height < 44); }).map(x => x.id || x.className || x.textContent).slice(0, 5));
    console.log(name, 'buttons under 44px:', small, 'overflow', await p.evaluate(() => document.documentElement.scrollWidth > innerWidth));
    await p.screenshot({ path: `shots/${name}.png` }); await ctx.close();
  }
  await b.close();
})();
