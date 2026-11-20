// gta6-meme-x-01 entry program.
//
// Copies POST.json from the repository root to the output directory.
// That is all it does: the house reads the post itself from X.
//
// Run the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// No network, no wall clock, no files outside the repository.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const repoDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(repoDir, "POST.json");
const dst = join(outDir, "POST.json");

try {
  if (!existsSync(src)) {
    console.error(`POST.json not found in the repository: ${src}`);
    process.exit(1);
  }
  mkdirSync(outDir, { recursive: true });
  copyFileSync(src, dst);
} catch (err) {
  console.error(`failed to copy ${src} to ${dst}: ${err.message}`);
  process.exit(1);
}
