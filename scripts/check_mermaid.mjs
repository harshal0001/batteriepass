// Parse every ```mermaid block in the given Markdown files with Mermaid's own parser.
//
// Documentation guard, run in CI (.github/workflows/docs-check.yml). No browser: Mermaid
// is loaded in Node with a minimal DOM, so the check needs neither Chromium nor
// mermaid-cli, which is what made the first version of this step fail on the runner.
//
//   npm install --no-save --prefix /tmp/mmcheck mermaid@11 jsdom dompurify
//   cp scripts/check_mermaid.mjs /tmp/mmcheck/ && node /tmp/mmcheck/check_mermaid.mjs README.md docs/**/*.md
//
// Exit code 1 if any diagram fails to parse. Prints file and the first line of the error.

import fs from "node:fs";
import path from "node:path";
import { JSDOM } from "jsdom";

const dom = new JSDOM("<!doctype html><html><body></body></html>");
globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.DOMPurify = (await import("dompurify")).default(dom.window);
const mermaid = (await import("mermaid")).default;
mermaid.initialize({ startOnLoad: false });

const files = process.argv.slice(2).filter((f) => f.endsWith(".md") && fs.existsSync(f));
if (files.length === 0) {
  console.log("no markdown files to check");
  process.exit(0);
}

let total = 0;
let failed = 0;
const fence = /```mermaid[^\n]*\n([\s\S]*?)```/g;

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  let match;
  let index = 0;
  while ((match = fence.exec(text))) {
    index += 1;
    total += 1;
    try {
      await mermaid.parse(match[1]);
    } catch (err) {
      failed += 1;
      const first = String(err?.message ?? err).split("\n")[0];
      console.log(`FAIL ${path.relative(process.cwd(), file)} (diagram ${index}): ${first}`);
    }
  }
}

console.log(`${total} diagram(s) in ${files.length} file(s), ${failed} failed`);
process.exit(failed ? 1 : 0);
