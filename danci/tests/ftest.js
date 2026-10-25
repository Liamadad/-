const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const url = 'file://' + process.cwd() + '/site/index.html';
  const mk = async (time, scheme = 'light') => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: scheme });
    const page = await ctx.newPage();
    page.errs = []; page.on('pageerror', e => page.errs.push(e.message));
    page.reqs = []; page.on('request', r => { if (r.url().includes('youdao')) page.reqs.push(r.url()); });
    await page.clock.setFixedTime(new Date(time));
    await page.goto(url);
    return { ctx, page };
  };
  const words = p => p.$$eval('#main .panel .w .en', els => els.map(e => e.textContent.replace(/^写/, '')));
  const tabs = p => p.$$eval('#tabs .tab', els => els.map(e => e.textContent.trim()));

  // weekday
  let { ctx, page } = await mk('2027-03-10T10:00:00');
  console.log('weekday tabs', await tabs(page));
  const reviewGroups = await page.$$eval('details.group', d => d.length);
  await page.click('#shuffle');
  const flat = await page.$$eval('details.group', d => d.length);
  const revShuf = await words(page);
  console.log('review groups', reviewGroups, 'after shuffle groups', flat, 'flat words', revShuf.length);
  await page.click('[data-tab="spell"]');
  const orig = await words(page);
  await page.click('#shuffle'); const s1 = await words(page);
  await page.click('#cover'); const s2 = await words(page);
  console.log('spell orig', orig.slice(0,4), 'shuffled', s1.slice(0,4), 'same set', [...orig].sort().join()===[...s1].sort().join(), 'kept after mask', s1.join()===s2.join());
  await page.click('.say >> nth=0');
  await page.waitForTimeout(500);
  console.log('youdao requests', page.reqs.length, page.reqs[0]);
  await page.screenshot({ path: 'shots/f_spell_shuf_hide.png' });
  await page.click('#unshuffle'); const s3 = await words(page);
  console.log('unshuffle restores', s3.join()===orig.join());
  console.log('errors', page.errs);
  await ctx.close();

  // monthly saturday
  ({ ctx, page } = await mk('2026-10-31T10:00:00'));
  console.log('monthly sat tabs', await tabs(page));
  await page.click('[data-tab="month"]'); const m1 = await words(page);
  await page.click('#cover'); const m2 = await words(page);
  await page.click('#shuffle'); const m3 = await words(page);
  console.log('month count', m1.length, 'stable on mask', m1.join()===m2.join(), 'reshuffle changes', m1.join()!==m3.join());
  console.log('rules', (await page.$eval('.box', b => b.innerText)).replace(/\n/g,' | '));
  console.log('errors', page.errs); await ctx.close();

  // normal saturday, sunday after monthly, sprint saturday, sprint weekday, phase 3 weekday
  for (const t of ['2026-10-24T10:00:00','2026-11-01T10:00:00','2027-10-02T10:00:00','2027-10-05T10:00:00','2027-08-18T10:00:00']) {
    ({ ctx, page } = await mk(t));
    console.log(t.slice(0,10), await tabs(page), '|', (await page.$eval('.box h3', b => b.innerText)), '| words', (await words(page)).length, '| errors', page.errs.length);
    await ctx.close();
  }
  await browser.close();
})();
