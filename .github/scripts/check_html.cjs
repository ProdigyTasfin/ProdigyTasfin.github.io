/* Structural HTML validation; development tooling only, never served to visitors. */
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
let HtmlValidate;
try {
  ({ HtmlValidate } = require(process.env.HTML_VALIDATE_MODULE || 'html-validate'));
} catch (_) {
  console.error('Install html-validate@10.17.0 and set HTML_VALIDATE_MODULE to its module path. See README.md.');
  process.exit(1);
}
const validator = new HtmlValidate({ rules: {
  'close-order': 'error', 'no-dup-attr': 'error', 'no-dup-id': 'error',
  'element-permitted-content': 'error', 'element-permitted-parent': 'error',
  'element-required-content': 'error', 'attribute-allowed-values': 'error',
  'unrecognized-char-ref': 'error'
} });
function files(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    if (['.git', '.github', 'node_modules'].includes(entry.name)) return [];
    const target = path.join(directory, entry.name);
    return entry.isDirectory() ? files(target) : entry.name.endsWith('.html') ? [target] : [];
  });
}
(async () => {
  const pages = files(root);
  let failed = false;
  for (const file of pages) {
    const result = await validator.validateFile(file);
    if (result.valid) continue;
    failed = true;
    result.results.forEach((item) => item.messages.forEach((message) => {
      console.error(`${path.relative(root, file)}:${message.line}:${message.column} ${message.ruleId}: ${message.message}`);
    }));
  }
  if (failed) process.exitCode = 1;
  else console.log(`PASS: ${pages.length} HTML documents; structural nesting, attributes, IDs, permitted content and character references.`);
})().catch((error) => { console.error(error.message); process.exitCode = 1; });
