/**
 * Rasterise the SVG sources in assets/img into the PNG files the social card
 * and the Apple touch icon need (SVG is not reliably supported by either).
 *
 * The site itself ships no dependencies; this is a one-off authoring tool:
 *
 *   npm install --no-save @resvg/resvg-js
 *   node tools/render-images.mjs
 */
import { Resvg } from '@resvg/resvg-js';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

const targets = [
  { src: 'assets/img/og-card.svg', out: 'assets/img/og-card.png', width: 1200 },
  { src: 'assets/img/apple-touch-icon.svg', out: 'assets/img/apple-touch-icon.png', width: 180 },
];

for (const { src, out, width } of targets) {
  const svg = readFileSync(join(root, src), 'utf8');
  const renderer = new Resvg(svg, {
    fitTo: { mode: 'width', value: width },
    font: { loadSystemFonts: true, defaultFontFamily: 'DejaVu Serif' },
  });
  writeFileSync(join(root, out), renderer.render().asPng());
  console.log(`${src} -> ${out} (${width}px wide)`);
}
