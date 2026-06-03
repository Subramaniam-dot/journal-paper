#!/usr/bin/env node
// Generate the conditional flow-matching posterior illustration as D3-composed SVG.
// The figure is intentionally visual-first: sparse labels, vector paths, and no axes.

import * as d3 from "d3";
import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, "figures");
mkdirSync(outDir, { recursive: true });

const svgPath = join(outDir, "fig_method_cfm.svg");
const pdfPath = join(outDir, "fig_method_cfm.pdf");

const W = 1900;
const H = 560;
const PDF_W_PT = 515.5;
const PDF_H_PT = +(PDF_W_PT * H / W).toFixed(2);
const EXPORT_SCALE = +(PDF_W_PT / W).toFixed(8);
const C = {
  ink: "#1f2528",
  muted: "#5c656b",
  faint: "#e8edf0",
  base: "#9aa3a8",
  baseDark: "#6e777c",
  blue: "#0072B2",
  blue2: "#E5F1F8",
  green: "#1b6b2a",
  green2: "#dfeee4",
  green3: "#74a878",
  amber: "#D55E00",
  orange2: "#FBE9DD",
  gold: "#c8951f",
  hair: "#BDBDBD",
  rfInk: "#4D4D4D",
  wall: "#f7f9fa",
};

const rng = d3.randomLcg(0.31827);
const line = d3.line().curve(d3.curveBasis);

function esc(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function attrs(obj = {}) {
  return Object.entries(obj)
    .filter(([, v]) => v !== undefined && v !== null)
    .map(([k, v]) => `${k}="${esc(v)}"`)
    .join(" ");
}

function tag(name, attr = {}, body = "") {
  const a = attrs(attr);
  return body === "" ? `<${name}${a ? " " + a : ""}/>` : `<${name}${a ? " " + a : ""}>${body}</${name}>`;
}

function wordTspans(s, firstAttrs = {}) {
  const words = String(s).trim().split(/\s+/).filter(Boolean);
  return words.map((word, i) =>
    tag("tspan", i === 0 ? firstAttrs : { dx: "0.32em" }, esc(word))
  ).join("");
}

function text(x, y, s, cls = "label", more = {}) {
  return tag("text", { x, y, class: cls, ...more }, wordTspans(s));
}

function multiline(x, y, lines, cls = "small", more = {}) {
  const body = lines.map((l, i) => wordTspans(l, { x, dy: i === 0 ? 0 : 30 })).join("");
  return tag("text", { x, y, class: cls, ...more }, body);
}

function rect(x, y, width, height, more = {}) {
  return tag("rect", { x, y, width, height, ...more });
}

function circle(cx, cy, r, more = {}) {
  return tag("circle", { cx, cy, r, ...more });
}

function ellipse(cx, cy, rx, ry, more = {}) {
  return tag("ellipse", { cx, cy, rx, ry, ...more });
}

function path(d, more = {}) {
  return tag("path", { d, ...more });
}

function poly(points, more = {}) {
  return tag("polygon", { points: points.map((p) => p.join(",")).join(" "), ...more });
}

function lineTag(x1, y1, x2, y2, more = {}) {
  return tag("line", { x1, y1, x2, y2, ...more });
}

function star(cx, cy, rOuter, rInner, points = 5, more = {}) {
  const pts = [];
  for (let i = 0; i < points * 2; i++) {
    const a = -Math.PI / 2 + (i * Math.PI) / points;
    const r = i % 2 === 0 ? rOuter : rInner;
    pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
  }
  return poly(pts, more);
}

function cube(x, y, w, h, dx, dy, opts = {}) {
  const {
    fill = "#ffffff",
    side = "#f6f8f8",
    top = "#fbfcfc",
    stroke = "#70787d",
    opacity = 1,
    dash = "",
  } = opts;
  const back = [[x + dx, y + dy], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + dx, y + h + dy]];
  const front = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
  const pieces = [];
  pieces.push(poly([back[0], back[1], front[1], front[0]], { fill: top, stroke, "stroke-width": 2.2, opacity, "stroke-dasharray": dash }));
  pieces.push(poly([front[1], back[1], back[2], front[2]], { fill: side, stroke, "stroke-width": 2.2, opacity, "stroke-dasharray": dash }));
  pieces.push(poly(front, { fill, stroke, "stroke-width": 2.2, opacity, "stroke-dasharray": dash }));
  pieces.push(tag("line", { x1: front[0][0], y1: front[0][1], x2: back[0][0], y2: back[0][1], stroke, "stroke-width": 2.2, opacity, "stroke-dasharray": dash }));
  pieces.push(tag("line", { x1: front[2][0], y1: front[2][1], x2: back[2][0], y2: back[2][1], stroke, "stroke-width": 2.2, opacity, "stroke-dasharray": dash }));
  return pieces.join("");
}

function pointInCube(x, y, w, h, dx, dy, u, v, z) {
  return [x + u * w + z * dx, y + v * h + z * dy];
}

function sampleInEllipse(cx, cy, rx, ry, rot = 0) {
  const a = rng() * Math.PI * 2;
  const r = Math.sqrt(rng());
  const x = Math.cos(a) * r * rx;
  const y = Math.sin(a) * r * ry;
  const cr = Math.cos(rot);
  const sr = Math.sin(rot);
  return [cx + x * cr - y * sr, cy + x * sr + y * cr];
}

function conditionCuboid(x, y, scale = 0.39) {
  const cx = x + 125;
  const cy = y + 150;
  const hx = 136.5;
  const hy = 139.0;
  const hz = 190.0;
  const antLong = 120.0;
  const antShort = 26.25;

  function p3(px, py, pz) {
    return [
      cx + scale * (0.55 * px + 0.45 * pz),
      cy + scale * (-0.05 * px + 0.18 * pz - 0.95 * py),
    ];
  }

  function poly3(points, more = {}) {
    return poly(points.map(([a, b, c]) => p3(a, b, c)), more);
  }

  function line3(a, b, more = {}) {
    const u = p3(...a);
    const v = p3(...b);
    return lineTag(u[0], u[1], v[0], v[1], more);
  }

  function patchOnWall(wall, y0) {
    const hl = antLong / 2;
    const hs = antShort / 2;
    let pts;
    if (wall === "-z" || wall === "+z") {
      const zz = wall === "-z" ? -hz : hz;
      pts = [[-hs, y0 - hl, zz], [hs, y0 - hl, zz], [hs, y0 + hl, zz], [-hs, y0 + hl, zz]];
    } else {
      const xx = wall === "+x" ? hx : -hx;
      pts = [[xx, y0 - hl, -hs], [xx, y0 + hl, -hs], [xx, y0 + hl, hs], [xx, y0 - hl, hs]];
    }
    return poly3(pts, { fill: C.blue, stroke: C.rfInk, "stroke-width": 1.05, opacity: 0.96 });
  }

  const corners = [
    [-hx, -hy, -hz], [hx, -hy, -hz], [hx, -hy, hz], [-hx, -hy, hz],
    [-hx, hy, -hz], [hx, hy, -hz], [hx, hy, hz], [-hx, hy, hz],
  ];
  const edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  const tx = p3(0, 0, 0);

  return tag("g", {}, [
    poly3([[-hx, hy, -hz], [hx, hy, -hz], [hx, hy, hz], [-hx, hy, hz]], {
      fill: "#f7f9fa",
      stroke: C.rfInk,
      "stroke-width": 0.95,
      opacity: 0.40,
    }),
    poly3([[-hx, -hy, -hz], [hx, -hy, -hz], [hx, -hy, hz], [-hx, -hy, hz]], {
      fill: "#eeeeee",
      stroke: C.rfInk,
      "stroke-width": 0.95,
      opacity: 0.20,
    }),
    ...edges.map(([a, b]) => line3(corners[a], corners[b], {
      stroke: C.rfInk,
      "stroke-width": 1.05,
      opacity: 0.68,
    })),
    patchOnWall("-z", 67.5),
    patchOnWall("-x", -72.5),
    patchOnWall("+x", 67.5),
    patchOnWall("+z", -72.5),
    ellipse(tx[0], tx[1], 48, 19, { fill: "none", stroke: C.blue, "stroke-width": 1.0, opacity: 0.36 }),
    ellipse(tx[0], tx[1], 31, 12, { fill: "none", stroke: C.blue, "stroke-width": 1.0, opacity: 0.42 }),
    ellipse(tx[0], tx[1], 16, 7, { fill: C.orange2, stroke: C.amber, "stroke-width": 1.15 }),
    lineTag(tx[0] - 10, tx[1], tx[0] + 10, tx[1], { stroke: C.amber, "stroke-width": 1.05 }),
    text(tx[0], tx[1] + 4, "Tx", "cond-mini", { "text-anchor": "middle", fill: C.amber }),
  ].join(""));
}

function miniSParams(x, y) {
  const w = 124;
  const h = 70;
  const px = x + 13;
  const py = y + 23;
  const pw = w - 26;
  const ph = 33;
  const traces = d3.range(4).map((k) => {
    const pts = d3.range(34).map((i) => [
      px + i * (pw / 33),
      py + ph * 0.55 - 7 * Math.sin(i / 5 + k * 0.55) + k * 2.1,
    ]);
    return path(line(pts), {
      fill: "none",
      stroke: k === 0 ? C.amber : C.blue,
      "stroke-width": 1.15,
      opacity: k === 0 ? 0.95 : 0.62,
    });
  });
  return tag("g", {}, [
    rect(x, y, w, h, { rx: 4, fill: "#ffffff", stroke: C.hair, "stroke-width": 1.05 }),
    text(x + w / 2, y + 17, "S_i5(f)", "cond-mini", {
      "text-anchor": "middle",
      fill: C.rfInk,
      textLength: 64,
      lengthAdjust: "spacingAndGlyphs",
    }),
    lineTag(px, py + ph, px + pw, py + ph, { stroke: C.rfInk, "stroke-width": 0.8, opacity: 0.65 }),
    ...traces,
  ].join(""));
}

function miniFeatureVector(x, y) {
  const w = 124;
  const h = 60;
  const gx = x + 13;
  const gy = y + 29;
  const groups = [
    [22, C.blue],
    [18, C.amber],
    [22, C.blue],
    [18, C.amber],
    [20, C.blue],
  ];
  let cursor = gx;
  const cells = [];
  for (const [gw, color] of groups) {
    cells.push(rect(cursor, gy, gw, 16, { fill: color, opacity: 0.13, stroke: color, "stroke-width": 0.9 }));
    for (let i = 1; i < Math.floor(gw / 7); i++) {
      cells.push(lineTag(cursor + i * 7, gy, cursor + i * 7, gy + 16, { stroke: color, "stroke-width": 0.65, opacity: 0.35 }));
    }
    cursor += gw;
  }
  return tag("g", {}, [
    rect(x, y, w, h, { rx: 4, fill: "#ffffff", stroke: C.hair, "stroke-width": 1.05 }),
    text(x + w / 2, y + 18, "x_RF, 180-D", "cond-mini", {
      "text-anchor": "middle",
      fill: C.blue,
      textLength: 104,
      lengthAdjust: "spacingAndGlyphs",
    }),
    ...cells,
  ].join(""));
}

const baseCube = { x: 475, y: 220, w: 245, h: 150, dx: 92, dy: -62 };
const postCube = { x: 1280, y: 214, w: 300, h: 160, dx: 102, dy: -62 };
const baseOut = [baseCube.x + baseCube.w + 24, baseCube.y + 76];
const postIn = [postCube.x + 70, postCube.y + 80];
const postCenter = [postCube.x + 185, postCube.y + 78];

let svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${PDF_W_PT}pt" height="${PDF_H_PT}pt" viewBox="0 0 ${PDF_W_PT} ${PDF_H_PT}">
<defs>
  <linearGradient id="flowStroke" x1="0%" x2="100%" y1="0%" y2="0%">
    <stop offset="0%" stop-color="${C.baseDark}" stop-opacity="0.50"/>
    <stop offset="42%" stop-color="${C.blue}" stop-opacity="0.46"/>
    <stop offset="100%" stop-color="${C.green}" stop-opacity="0.62"/>
  </linearGradient>
  <linearGradient id="ribbon" x1="0%" x2="100%" y1="0%" y2="0%">
    <stop offset="0%" stop-color="${C.blue}" stop-opacity="0.08"/>
    <stop offset="65%" stop-color="${C.blue}" stop-opacity="0.10"/>
    <stop offset="100%" stop-color="${C.green}" stop-opacity="0.12"/>
  </linearGradient>
  <radialGradient id="posteriorGlow" cx="50%" cy="50%" r="58%">
    <stop offset="0%" stop-color="${C.green3}" stop-opacity="0.33"/>
    <stop offset="100%" stop-color="${C.green3}" stop-opacity="0"/>
  </radialGradient>
  <marker id="arrowGreen" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
    <path d="M2,2 L10,6 L2,10 Z" fill="${C.green}"/>
  </marker>
  <marker id="arrowBlue" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
    <path d="M2,2 L8,5 L2,8 Z" fill="${C.blue}"/>
  </marker>
  <style>
    .label { font: 700 30px Arial, Helvetica, sans-serif; fill: ${C.ink}; }
    .small { font: 26px Arial, Helvetica, sans-serif; fill: ${C.muted}; }
    .tiny { font: 26px Arial, Helvetica, sans-serif; fill: ${C.muted}; }
    .stage { font: 700 28px Arial, Helvetica, sans-serif; fill: ${C.ink}; }
    .cond-mini { font: 700 26px Arial, Helvetica, sans-serif; fill: ${C.rfInk}; }
    .math { font: italic 26px "Times New Roman", Times, serif; fill: ${C.ink}; }
  </style>
</defs>
<g transform="scale(${EXPORT_SCALE})">
`;

// Measurement condition: compact signal flow from Tx/Rx geometry to RF features.
svg += tag("g", { id: "condition" }, [
  conditionCuboid(48, 86, 0.39),
  path(line([[244, 237], [270, 237], [292, 175]]), {
    fill: "none",
    stroke: C.rfInk,
    "stroke-width": 1.35,
    "stroke-linecap": "round",
    "marker-end": "url(#arrowBlue)",
    opacity: 0.72,
  }),
  miniSParams(304, 132),
  path(line([[366, 203], [366, 215], [366, 233]]), {
    fill: "none",
    stroke: C.rfInk,
    "stroke-width": 1.25,
    "stroke-linecap": "round",
    "marker-end": "url(#arrowBlue)",
    opacity: 0.70,
  }),
  miniFeatureVector(304, 234),
  text(246, 381, "RF condition c", "stage", { "text-anchor": "middle" }),
  text(246, 412, "Tx/Rx -> S-parameters -> x_RF", "tiny", { "text-anchor": "middle" }),
].join(""));

// Base cuboid and samples.
let baseDots = "";
const basePts = [];
for (let i = 0; i < 92; i++) {
  const u = rng();
  const v = rng();
  const z = rng();
  const p = pointInCube(baseCube.x, baseCube.y, baseCube.w, baseCube.h, baseCube.dx, baseCube.dy, u, v, z);
  basePts.push(p);
  baseDots += circle(p[0].toFixed(1), p[1].toFixed(1), 5.3, { fill: C.base, opacity: 0.42 });
}
svg += tag("g", { id: "base" }, [
  cube(baseCube.x, baseCube.y, baseCube.w, baseCube.h, baseCube.dx, baseCube.dy, {
    fill: "rgba(255,255,255,0.38)",
    side: "rgba(245,248,250,0.48)",
    top: "rgba(251,252,252,0.52)",
    stroke: "#778086",
  }),
  baseDots,
  text(610, 423, "bounded base", "stage", { "text-anchor": "middle" }),
  text(610, 452, "uniform in volume", "small", { "text-anchor": "middle" }),
].join(""));

// Flow ribbon and trajectories.
const ribbonTop = line([
  [baseOut[0] - 30, baseOut[1] - 60],
  [850, 138],
  [1040, 132],
  [postIn[0] + 60, postIn[1] - 53],
]);
const ribbonBottom = line([
  [postIn[0] + 60, postIn[1] + 58],
  [1040, 330],
  [850, 330],
  [baseOut[0] - 30, baseOut[1] + 62],
]);
svg += path(`${ribbonTop} L ${ribbonBottom.slice(1)} Z`, { fill: "url(#ribbon)", stroke: "none" });

let flows = "";
const postPts = [];
for (let i = 0; i < 125; i++) {
  const p = sampleInEllipse(postCenter[0], postCenter[1], 132, 40, -0.05);
  postPts.push(p);
}
for (let i = 0; i < 34; i++) {
  const s = basePts[Math.floor(rng() * basePts.length)];
  const e = postPts[Math.floor(rng() * postPts.length)];
  const lift = (rng() - 0.5) * 74;
  const d = line([
    [s[0] + 12, s[1]],
    [790 + rng() * 80, 210 + lift],
    [1035 + rng() * 80, 205 - lift * 0.35],
    [e[0] - 12, e[1]],
  ]);
  flows += path(d, {
    fill: "none",
    stroke: "url(#flowStroke)",
    "stroke-width": 3.0 + rng() * 1.8,
    opacity: 0.48,
    "stroke-linecap": "round",
  });
}
const mainFlow = line([[baseOut[0], baseOut[1]], [870, 178], [1055, 176], [postCenter[0] - 85, postCenter[1]]]);
svg += tag("g", { id: "flow" }, [
  flows,
  path(mainFlow, {
    fill: "none",
    stroke: C.green,
    "stroke-width": 5.8,
    opacity: 0.90,
    "stroke-linecap": "round",
    "marker-end": "url(#arrowGreen)",
  }),
  text(990, 145, "learned flow", "stage", { "text-anchor": "middle", fill: C.green }),
].join(""));

// Short conditioning cue. Keep it local to avoid crossing the base cloud.
const condD = line([[468, 215], [500, 215]]);
svg += path(condD, {
  fill: "none",
  stroke: C.blue,
  "stroke-width": 2.6,
  "stroke-dasharray": "6 7",
  opacity: 0.72,
  "marker-end": "url(#arrowBlue)",
});

// Posterior cuboid, cloud, credible contours, and mean.
let postDots = "";
for (const [x, y] of postPts) {
  postDots += circle(x.toFixed(1), y.toFixed(1), 5.2, { fill: C.green, opacity: 0.46 });
}
svg += tag("g", { id: "posterior" }, [
  cube(postCube.x, postCube.y, postCube.w, postCube.h, postCube.dx, postCube.dy, {
    fill: "rgba(255,255,255,0.30)",
    side: "rgba(237,246,239,0.38)",
    top: "rgba(252,253,251,0.50)",
    stroke: "#75807a",
    opacity: 0.54,
    dash: "8 7",
  }),
  ellipse(postCenter[0], postCenter[1], 250, 92, { fill: "url(#posteriorGlow)", stroke: "none" }),
  ellipse(postCenter[0], postCenter[1], 92, 28, { fill: "none", stroke: C.green, "stroke-width": 3.2, opacity: 0.96, transform: `rotate(-3 ${postCenter[0]} ${postCenter[1]})` }),
  ellipse(postCenter[0], postCenter[1], 143, 43, { fill: "none", stroke: C.green, "stroke-width": 2.6, opacity: 0.72, transform: `rotate(-3 ${postCenter[0]} ${postCenter[1]})` }),
  ellipse(postCenter[0], postCenter[1], 185, 58, { fill: "none", stroke: C.green, "stroke-width": 2.2, opacity: 0.48, transform: `rotate(-3 ${postCenter[0]} ${postCenter[1]})` }),
  postDots,
  star(postCenter[0] + 2, postCenter[1] - 3, 25, 11, 5, { fill: "#111", stroke: "#111", "stroke-width": 1.2 }),
  text(1430, 423, "posterior p(x|c)", "stage", { "text-anchor": "middle", fill: C.green }),
  text(1430, 452, "samples + credible regions", "small", { "text-anchor": "middle", fill: C.green }),
  multiline(1670, 178, ["50 / 90 / 95%", "credible regions"], "small", { "text-anchor": "start", fill: C.green }),
  multiline(1670, 286, ["mean", "point estimate"], "small", { "text-anchor": "start", fill: C.ink }),
  tag("line", { x1: 1626, y1: 281, x2: postCenter[0] + 28, y2: postCenter[1] - 2, stroke: C.ink, "stroke-width": 2.0, opacity: 0.65 }),
].join(""));

// Minimal time axis.
svg += tag("g", { id: "time" }, [
  tag("line", { x1: 610, y1: 500, x2: 1430, y2: 500, stroke: "#737a7d", "stroke-width": 2.1 }),
  tag("line", { x1: 610, y1: 488, x2: 610, y2: 512, stroke: "#737a7d", "stroke-width": 2.1 }),
  tag("line", { x1: 1430, y1: 488, x2: 1430, y2: 512, stroke: "#737a7d", "stroke-width": 2.1 }),
  text(610, 535, "t = 0", "tiny", { "text-anchor": "middle" }),
  text(1015, 535, "Euler ODE sampling", "tiny", { "text-anchor": "middle" }),
  text(1430, 535, "t = 1", "tiny", { "text-anchor": "middle" }),
].join(""));

svg += `</g>\n</svg>\n`;

writeFileSync(svgPath, svg);
execFileSync("rsvg-convert", ["-f", "pdf", "-o", pdfPath, svgPath], { stdio: "inherit" });
console.log(`wrote ${svgPath}`);
console.log(`wrote ${pdfPath}`);
