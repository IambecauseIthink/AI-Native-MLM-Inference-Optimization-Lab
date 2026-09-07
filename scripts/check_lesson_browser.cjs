// Optional browser QA. Requires Playwright + its Chromium; no model/network calls.
// Usage: node scripts/check_lesson_browser.cjs /absolute/preview-directory
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
(async()=>{
 const dir=path.resolve(process.argv[2]);
 const browser=await chromium.launch({headless:true, ...(process.env.LESSON_BROWSER_CHANNEL?{channel:process.env.LESSON_BROWSER_CHANNEL}:{})});
 const page=await browser.newPage(); const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 let interactions=0;
 for(const width of [360,736])for(const colorScheme of ['light','dark'])for(let n=1;n<=6;n++){
  const id=String(n).padStart(2,'0');
  await page.setViewportSize({width,height:1000});await page.emulateMedia({colorScheme});
  await page.goto(pathToFileURL(path.join(dir,`${id}.html`)).href);
  const root=page.locator(`#lesson-${id}`);await root.locator('[data-metrics] tr').first().waitFor();
  const initial=await root.getAttribute('data-result');
  const selects=root.locator('select');
  for(let i=0;i<await selects.count();i++){
   const select=selects.nth(i),name=await select.getAttribute('name');
   const values=await select.locator('option').evaluateAll(xs=>xs.map(x=>x.value));
   const before=await select.inputValue();const choice=values.find(x=>x!==before);
   await select.selectOption(choice);
   const state=JSON.parse(await root.getAttribute('data-result'));
   if(state.parameters[name]!==Number(choice))throw new Error(`Control did not update ${id}/${name}`);
   const valid=await root.evaluate(el=>{
    const r=JSON.parse(el.dataset.result),rows=[...el.querySelectorAll('[data-metrics] tr')];
    const f=n=>Number.isInteger(n)?String(n):Number(n).toLocaleString('en-US',{maximumSignificantDigits:6});
    return rows.length===r.view.metrics.length&&rows.every((row,j)=>row.cells[0].textContent===r.view.metrics[j].label&&row.cells[1].textContent===f(r.view.metrics[j].value));
   });
   if(!valid)throw new Error(`Visible metrics mismatch ${id}`);
   await select.selectOption(before);interactions++;
  }
  if(initial!==await root.getAttribute('data-result'))throw new Error('Roundtrip mismatch');
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
  if(overflow)throw new Error(`Overflow ${id}/${width}/${colorScheme}`);
  await page.screenshot({path:path.join(dir,`${id}-${width}-${colorScheme}.png`),fullPage:true});
 }
 await browser.close();if(errors.length)throw new Error(errors.join('\n'));
 console.log(JSON.stringify({pages:24,interactions,consoleErrors:errors.length,overflow:false}));
})().catch(e=>{console.error(e);process.exit(1)});
