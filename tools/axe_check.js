const puppeteer = require('puppeteer');
const axeSource = require('axe-core').source;
const fs = require('fs');

(async () => {
  const url = process.argv[2] || 'http://127.0.0.1:8000/';
  console.log(`Running accessibility check against ${url}`);
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  try {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });
    // inject axe
    await page.evaluate(axeSource);
    const results = await page.evaluate(async () => {
      return await axe.run(document, {
        runOnly: {
          type: 'tag',
          values: ['wcag2aa', 'best-practice']
        }
      });
    });

    const outFile = 'a11y-report.json';
    fs.writeFileSync(outFile, JSON.stringify(results, null, 2));
    console.log(`Accessibility scan complete. Results saved to ${outFile}`);
    console.log('Violations summary:');
    results.violations.forEach(v => {
      console.log(`- ${v.id}: ${v.description} (impact: ${v.impact}) -- ${v.nodes.length} nodes`);
    });
    if (results.violations.length === 0) console.log('No violations found for the tested page.');
  } catch (err) {
    console.error('Error running accessibility check:', err);
    process.exitCode = 2;
  } finally {
    await browser.close();
  }
})();
