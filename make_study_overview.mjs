#!/usr/bin/env node
// Generate Figure 1 as hand-composed vector SVG and export to PDF.
// The final PDF is included by LaTeX; PNG renders are for inspection only.

import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, "figures");
const svgPath = join(outDir, "fig_study_overview.svg");
const pdfPath = join(outDir, "fig_study_overview.pdf");

const W = 1800;
const H = 760;
const PDF_W_PT = 515.5;
const PDF_H_PT = +(PDF_W_PT * H / W).toFixed(2);
const EXPORT_SCALE = +(PDF_W_PT / W).toFixed(8);
const C = {
  ink: "#4D4D4D",
  muted: "#999999",
  hair: "#BDBDBD",
  panel: "#ffffff",
  pale: "#F7F9FA",
  blue: "#0072B2",
  blue2: "#E5F1F8",
  green: "#0072B2",
  green2: "#E5F1F8",
  amber: "#D55E00",
  amber2: "#FBE9DD",
  purple: "#4D4D4D",
  purple2: "#F7F9FA",
  gold: "#D55E00",
};

function esc(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function attrString(obj = {}) {
  return Object.entries(obj)
    .filter(([, v]) => v !== undefined && v !== null)
    .map(([k, v]) => `${k}="${esc(v)}"`)
    .join(" ");
}

function wordTspans(s, firstAttrs = {}) {
  const words = String(s).trim().split(/\s+/).filter(Boolean);
  return words.map((word, i) => {
    const attrs = attrString(i === 0 ? firstAttrs : { dx: "0.32em" });
    return `<tspan${attrs ? " " + attrs : ""}>${esc(word)}</tspan>`;
  }).join("");
}

function text(x, y, s, cls = "", extra = "") {
  return `<text x="${x}" y="${y}" class="${cls}" ${extra}>${wordTspans(s)}</text>`;
}

function rect(x, y, w, h, cls = "", extra = "") {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}" ${extra}/>`;
}

function line(x1, y1, x2, y2, cls = "", extra = "") {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}" ${extra}/>`;
}

function poly(points, cls = "", extra = "") {
  const p = points.map(([x, y]) => `${x},${y}`).join(" ");
  return `<polygon points="${p}" class="${cls}" ${extra}/>`;
}

function circle(x, y, r, cls = "", extra = "") {
  return `<circle cx="${x}" cy="${y}" r="${r}" class="${cls}" ${extra}/>`;
}

function ellipse(x, y, rx, ry, cls = "", extra = "") {
  return `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" class="${cls}" ${extra}/>`;
}

function path(d, cls = "", extra = "") {
  return `<path d="${d}" class="${cls}" ${extra}/>`;
}

function labelBlock(x, y, lines, cls = "small", anchor = "middle", gap = 31) {
  const tspans = lines.map((l, i) =>
    wordTspans(l, { x, dy: i === 0 ? 0 : gap })
  ).join("");
  return `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${tspans}</text>`;
}

let seed = 12;
function rand() {
  seed = (1664525 * seed + 1013904223) >>> 0;
  return seed / 2 ** 32;
}

function cloud(cx, cy, rx, ry, n, color, alpha = 0.55, dotR = 4.4) {
  let out = "";
  for (let i = 0; i < n; i++) {
    const a = 2 * Math.PI * rand();
    const r = Math.sqrt(rand());
    const x = cx + Math.cos(a) * r * rx + (rand() - 0.5) * 6;
    const y = cy + Math.sin(a) * r * ry + (rand() - 0.5) * 6;
    out += circle(x.toFixed(1), y.toFixed(1), dotR, "", `fill="${color}" opacity="${alpha}"`);
  }
  return out;
}

function arrowHead(x, y, size = 10, color = C.muted, dir = "right") {
  if (dir === "down") {
    return poly([[x, y], [x - size / 2, y - size], [x + size / 2, y - size]], "", `fill="${color}"`);
  }
  return poly([[x, y], [x - size, y - size / 2], [x - size, y + size / 2]], "", `fill="${color}"`);
}

function hArrow(x1, y, x2, color = C.muted, width = 2.2, size = 10) {
  return line(x1, y, x2 - size, y, "", `stroke="${color}" stroke-width="${width}" stroke-linecap="round"`) +
    arrowHead(x2, y, size, color, "right");
}

function downArrow(x, y1, y2, color = C.blue, width = 1.8, size = 10) {
  return line(x, y1, x, y2 - size, "", `stroke="${color}" stroke-width="${width}" stroke-linecap="round" opacity="0.68"`) +
    arrowHead(x, y2, size, color, "down");
}

const panels = [
  [45, 96, 382, 620],
  [470, 96, 382, 620],
  [895, 96, 382, 620],
  [1320, 96, 382, 620],
];

let svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${PDF_W_PT}pt" height="${PDF_H_PT}pt" viewBox="0 0 ${PDF_W_PT} ${PDF_H_PT}">
<defs>
  <style>
    text { font-family: Arial, Helvetica, sans-serif; fill: ${C.ink}; }
    .title { font-size: 34px; font-weight: 700; }
    .subtitle { font-size: 25px; fill: ${C.muted}; }
    .panel-title { font-size: 27px; font-weight: 700; }
    .panel-letter { font-size: 25px; font-weight: 700; fill: ${C.ink}; }
    .small { font-size: 25px; fill: ${C.ink}; }
    .tiny { font-size: 25px; fill: ${C.muted}; }
    .metric { font-size: 25px; font-weight: 700; }
    .metric-val { font-size: 25px; fill: ${C.muted}; }
    .cfm-label { font-size: 25px; font-weight: 700; }
    .cfm-sub { font-size: 25px; fill: ${C.muted}; }
    .panel { fill: ${C.panel}; stroke: ${C.hair}; stroke-width: 2.0; rx: 8; }
    .hair { stroke: ${C.hair}; stroke-width: 1.8; fill: none; }
    .axis { stroke: ${C.ink}; stroke-width: 1.7; fill: none; }
    .arrow { stroke: ${C.muted}; stroke-width: 2.2; fill: none; }
    .arrow-green { stroke: ${C.green}; stroke-width: 3.2; fill: none; }
    .receiver { fill: ${C.green}; stroke: #111; stroke-width: 1.4; }
    .receiver-feed { stroke: #d7a53a; stroke-width: 2.2; fill: none; stroke-linecap: round; }
    .dash { stroke-dasharray: 8 7; }
  </style>
</defs>
<g transform="scale(${EXPORT_SCALE})">
<rect width="${W}" height="${H}" fill="white"/>
`;

svg += text(W / 2, 48, "Calibrated posterior pipeline for RF capsule localization", "title", `text-anchor="middle"`);
svg += text(W / 2, 76, "full-wave simulation evidence now; physical phantom validation is the next gate", "subtitle", `text-anchor="middle"`);

for (const [i, p] of panels.entries()) {
  const [x, y, w, h] = p;
  svg += rect(x, y, w, h, "panel");
  svg += circle(x + 34, y + 34, 24, "", `fill="${C.pale}" stroke="${C.muted}" stroke-width="2"`);
  svg += text(x + 34, y + 43, "ABCD"[i], "panel-letter", `text-anchor="middle"`);
}
svg += text(123, 139, "Four-receiver RF problem", "panel-title");
svg += text(548, 139, "Full-wave data generation", "panel-title");
svg += text(973, 139, "Conditional posterior", "panel-title");
svg += text(1398, 139, "Evidence and boundary", "panel-title");

for (let i = 0; i < 3; i++) {
  const x1 = panels[i][0] + panels[i][2] + 7;
  const x2 = panels[i + 1][0] - 10;
  svg += hArrow(x1, 356, x2);
}

// Panel A: faithful CST-derived 3D receiver layout.
{
  const [x, y] = panels[0];
  const cx = x + 202, cy = y + 238, s = 0.72;
  const hx = 136.5, hy = 139.0, hz = 190.0; // mm: L/2, H/2, W/2
  const antLong = 120.0, antShort = 26.25;
  const upper = `fill="${C.green}" stroke="#111" stroke-width="1.4" opacity="0.96"`;
  const lower = `fill="${C.amber}" stroke="#111" stroke-width="1.4" opacity="0.96"`;

  function p3(px, py, pz) {
    return [
      cx + s * (0.55 * px + 0.45 * pz),
      cy + s * (-0.05 * px + 0.18 * pz - 0.95 * py),
    ];
  }
  function poly3(points, extra = "") {
    return poly(points.map(([a, b, c]) => p3(a, b, c)), "", extra);
  }
  function line3(a, b, cls = "", extra = "") {
    const u = p3(...a), v = p3(...b);
    return line(u[0], u[1], v[0], v[1], cls, extra);
  }
  function text3(a, msg, cls = "tiny", extra = "") {
    const u = p3(...a);
    return text(u[0], u[1], msg, cls, extra);
  }
  function patchOnWall(port, wall, y0, colorExtra, label, labelOffset) {
    const hl = antLong / 2, hs = antShort / 2;
    let pts;
    if (wall === "-z" || wall === "+z") {
      const zz = wall === "-z" ? -hz : hz;
      pts = [[-hs, y0 - hl, zz], [hs, y0 - hl, zz], [hs, y0 + hl, zz], [-hs, y0 + hl, zz]];
    } else {
      const xx = wall === "+x" ? hx : -hx;
      pts = [[xx, y0 - hl, -hs], [xx, y0 + hl, -hs], [xx, y0 + hl, hs], [xx, y0 - hl, hs]];
    }
    svg += poly3(pts, colorExtra);
    svg += text3(labelOffset, label, "tiny", `text-anchor="middle"`);
  }

  // No-Rx top/floor faces are drawn translucent; vertical walls remain wireframe.
  svg += poly3([[-hx, hy, -hz], [hx, hy, -hz], [hx, hy, hz], [-hx, hy, hz]],
               `fill="${C.pale}" stroke="${C.ink}" stroke-width="1.2" opacity="0.42"`);
  svg += poly3([[-hx, -hy, -hz], [hx, -hy, -hz], [hx, -hy, hz], [-hx, -hy, hz]],
               `fill="#EEEEEE" stroke="${C.ink}" stroke-width="1.2" opacity="0.26"`);

  const corners = [
    [-hx, -hy, -hz], [hx, -hy, -hz], [hx, -hy, hz], [-hx, -hy, hz],
    [-hx, hy, -hz], [hx, hy, -hz], [hx, hy, hz], [-hx, hy, hz],
  ];
  const edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  for (const [a, b] of edges) svg += line3(corners[a], corners[b], "hair", `stroke="${C.ink}" stroke-width="1.8" opacity="0.75"`);

  // Draw far-to-near for this projection.
  patchOnWall("P1", "-z", 67.5, upper, "P1", [0, 116, -hz - 34]);
  patchOnWall("P4", "-x", -72.5, lower, "P4", [-hx - 57, -72.5, 0]);
  patchOnWall("P3", "+x", 67.5, upper, "P3", [hx + 53, 67.5, 0]);
  patchOnWall("P2", "+z", -72.5, lower, "P2", [0, -118, hz + 39]);

  const tx = p3(0, 0, 0);
  svg += ellipse(tx[0], tx[1], 74, 30, "hair", `stroke="${C.blue}" opacity="0.45"`);
  svg += ellipse(tx[0], tx[1], 48, 19, "hair", `stroke="${C.blue}" opacity="0.42"`);
  svg += ellipse(tx[0], tx[1], 30, 13, "", `fill="${C.gold}" stroke="#7e5a15" stroke-width="1.4"`);
  svg += text(tx[0], tx[1] + 5, "Tx", "tiny", `text-anchor="middle"`);

  svg += labelBlock(x + 191, y + 471, ["four receivers on vertical", "side walls"], "small");
  svg += labelBlock(x + 191, y + 526, ["green: upper pair;", "orange: lower pair"], "tiny", "middle", 27);
  svg += labelBlock(x + 191, y + 578, ["top and floor faces", "have no receiver"], "tiny", "middle", 27);
}

// Panel B: CST sweep, feature vector, grouped CV.
{
  const [x, y] = panels[1];
  const px = x + 70, py = y + 122, pw = 250, ph = 122;
  svg += rect(px, py, pw, ph, "", `fill="${C.pale}" stroke="${C.hair}" stroke-width="1.5"`);
  svg += line(px + 24, py + ph - 25, px + pw - 22, py + ph - 25, "hair", `stroke="${C.ink}"`);
  svg += line(px + 24, py + 22, px + 24, py + ph - 25, "hair", `stroke="${C.ink}"`);
  for (let k = 0; k < 4; k++) {
    const col = [C.blue, C.green, C.amber, C.purple][k];
    let d = "";
    for (let i = 0; i < 70; i++) {
      const xx = px + 28 + i * 3.0;
      const yy = py + 78 - 25 * Math.sin(i / 10 + k * 0.6) - k * 6;
      d += `${i === 0 ? "M" : "L"} ${xx.toFixed(1)} ${yy.toFixed(1)} `;
    }
    svg += path(d, "", `fill="none" stroke="${col}" stroke-width="2.0" opacity="0.9"`);
  }
  svg += labelBlock(px + pw / 2, py + ph + 26, ["S-parameter sweep ->", "180-D RF features"], "tiny");
  const gx = x + 72, gy = y + 314;
  svg += rect(gx, gy, 250, 86, "", `fill="none" stroke="${C.muted}" stroke-width="1.5" stroke-dasharray="7 6"`);
  for (let i = 0; i < 72; i++) {
    const cx = gx + 16 + rand() * 218;
    const cy = gy + 13 + rand() * 60;
    const col = [C.blue, C.green, C.amber, C.purple, "#777"][i % 5];
    svg += circle(cx.toFixed(1), cy.toFixed(1), 5.1, "", `fill="${col}" opacity="0.75"`);
  }
  svg += labelBlock(gx + 125, gy + 110, ["N=3935 configurations", "position-grouped 5-fold CV"], "small");
}

// Panel C: CFM transport and posterior.
{
  const [x, y] = panels[2];
  const condY = y + 76;
  svg += rect(x + 58, condY, 266, 88, "", `rx="8" fill="${C.blue2}" stroke="${C.blue}" stroke-width="1.5" opacity="0.96"`);
  svg += text(x + 191, condY + 26, "condition c", "metric", `text-anchor="middle"`);
  svg += labelBlock(x + 191, condY + 55, ["RF measurement;", "fixed geometry"], "tiny", "middle", 25);

  const plotX = x + 42;
  const plotY = y + 188;
  const plotW = 298;
  const plotH = 300;
  const rowY = plotY + 140;
  const baseX = plotX + 66;
  const postX = plotX + 236;
  const flowX = x + 191;

  svg += rect(plotX, plotY, plotW, plotH, "", `rx="16" fill="#fbfcfc" stroke="${C.hair}" stroke-width="1.4" opacity="0.98"`);
  svg += downArrow(x + 191, condY + 90, plotY + 21);
  svg += text(flowX, plotY + 36, "learned conditional transport", "small", `text-anchor="middle"`);

  svg += ellipse(baseX, rowY, 52, 34, "", `fill="#f2f4f4" stroke="#9aa1a4" stroke-width="1.4" opacity="0.90"`);
  svg += ellipse(baseX, rowY, 34, 21, "", `fill="none" stroke="#9aa1a4" stroke-width="1.1" opacity="0.50"`);
  svg += cloud(baseX, rowY, 38, 22, 20, "#8f9698", 0.48, 5.5);

  const trajectories = [
    [-32, -18, -28, -18, -46],
    [-30, 0, -18, -7, -18],
    [-21, 18, -4, 10, 18],
    [2, -20, 10, -9, -28],
    [16, 1, 22, 2, 4],
    [25, 18, 31, 14, 28],
  ];
  for (const [i, tr] of trajectories.entries()) {
    const [sxOff, syOff, exOff, eyOff, lift] = tr;
    const sx = baseX + sxOff, sy = rowY + syOff;
    const ex = postX + exOff, ey = rowY + eyOff;
    const d = `M ${sx} ${sy} C ${flowX - 34} ${rowY + lift}, ${flowX + 34} ${rowY + lift}, ${ex} ${ey}`;
    svg += path(d, "", `fill="none" stroke="${C.blue}" stroke-width="2.1" opacity="0.55" stroke-linecap="round"`);
    if (i === 1 || i === 3 || i === 5) svg += arrowHead(ex, ey, 7, C.blue);
  }
  svg += ellipse(postX, rowY, 71, 34, "", `fill="${C.green2}" stroke="none" opacity="0.78"`);
  svg += ellipse(postX, rowY, 71, 34, "", `fill="none" stroke="${C.green}" stroke-width="2.3" opacity="0.82"`);
  svg += ellipse(postX, rowY, 44, 20, "", `fill="none" stroke="${C.green}" stroke-width="1.6" opacity="0.58"`);
  svg += cloud(postX, rowY, 49, 23, 30, C.green, 0.58, 5.4);
  svg += circle(postX, rowY, 5.6, "", `fill="${C.ink}" opacity="0.92"`);
  svg += text(postX, rowY - 45, "credible region", "tiny", `text-anchor="middle"`);

  svg += text(baseX, rowY + 72, "source", "cfm-label", `text-anchor="middle"`);
  svg += labelBlock(baseX, rowY + 99, ["noise z0,", "t=0"], "cfm-sub");
  svg += text(postX, rowY + 72, "posterior", "cfm-label", `text-anchor="middle"`);
  svg += labelBlock(postX, rowY + 99, ["samples p(x | c),", "t=1"], "cfm-sub");
}

// Panel D: evidence and future physical validation boundary.
{
  const [x, y] = panels[3];
  const cards = [
    ["Point accuracy", ["CFM 0.354 cm;", "backbone 0.340 cm"], C.blue, C.blue2],
    ["Calibration", ["cov90 = 0.970;", "cov95 = 0.975"], C.blue, C.blue2],
    ["Discrimination", ["error-spread rank", "rho approx 0.60"], C.purple, C.purple2],
    ["Modality", ["bimodal only under", "geometric ambiguity"], C.amber, C.amber2],
  ];
  for (let i = 0; i < cards.length; i++) {
    const [head, lines, col, fill] = cards[i];
    const cy = y + 103 + i * 89;
    svg += rect(x + 45, cy, 310, 82, "", `rx="8" fill="${fill}" stroke="${col}" stroke-width="1.5"`);
    svg += circle(x + 70, cy + 29, 10, "", `fill="${col}"`);
    svg += text(x + 91, cy + 25, head, "metric");
    for (const [j, valueLine] of lines.entries()) {
      svg += text(x + 91, cy + 50 + j * 24, valueLine, "metric-val");
    }
  }
  svg += rect(x + 45, y + 464, 310, 120, "", `rx="8" fill="#fff" stroke="${C.muted}" stroke-width="1.7" stroke-dasharray="9 7"`);
  svg += labelBlock(x + 200, y + 490, ["Physical phantom + SDR", "validation"], "small");
  svg += labelBlock(x + 200, y + 546, ["future gate;", "not claimed here"], "tiny", "middle", 27);
}

svg += `</g>\n</svg>\n`;

writeFileSync(svgPath, svg);
execFileSync("rsvg-convert", ["-f", "pdf", "-o", pdfPath, svgPath], { stdio: "inherit" });
console.log(`wrote ${svgPath}`);
console.log(`wrote ${pdfPath}`);
