#!/usr/bin/env node
// Standalone RF-condition signal-flow schematic for visual review.

import * as d3 from "d3";
import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, "figures");
mkdirSync(outDir, { recursive: true });

const W = 1500;
const H = 450;
const PDF_W_PT = 515.5;
const PDF_H_PT = +(PDF_W_PT * H / W).toFixed(2);
const EXPORT_SCALE = +(PDF_W_PT / W).toFixed(8);
const C = {
  ink: "#4D4D4D",
  muted: "#999999",
  hair: "#BDBDBD",
  pale: "#F7F9FA",
  blue: "#0072B2",
  blue2: "#E5F1F8",
  orange: "#D55E00",
  orange2: "#FBE9DD",
  white: "#FFFFFF",
};

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

function multiline(x, y, lines, cls = "tiny", more = {}, gap = 22) {
  const body = lines.map((l, i) => wordTspans(l, { x, dy: i === 0 ? 0 : gap })).join("");
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

function arrow(x1, y1, x2, y2, more = {}) {
  return lineTag(x1, y1, x2, y2, {
    stroke: C.ink,
    "stroke-width": 1.45,
    "stroke-linecap": "round",
    "marker-end": "url(#arrow)",
    ...more,
  });
}

function receiverGeometry(x, y, scale = 0.66) {
  const cx = x + 205;
  const cy = y + 210;
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

  function text3(point, label, more = {}) {
    const p = p3(...point);
    return text(p[0], p[1], label, "rx-label", more);
  }

  function patchOnWall(wall, y0, label, labelOffset) {
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
    return [
      poly3(pts, { fill: C.blue, stroke: C.ink, "stroke-width": 1.25, opacity: 0.96 }),
      text3(labelOffset, label, { "text-anchor": "middle" }),
    ].join("");
  }

  const corners = [
    [-hx, -hy, -hz], [hx, -hy, -hz], [hx, -hy, hz], [-hx, -hy, hz],
    [-hx, hy, -hz], [hx, hy, -hz], [hx, hy, hz], [-hx, hy, hz],
  ];
  const edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  const tx = p3(0, 0, 0);

  return tag("g", {}, [
    poly3([[-hx, hy, -hz], [hx, hy, -hz], [hx, hy, hz], [-hx, hy, hz]], {
      fill: C.pale,
      stroke: C.ink,
      "stroke-width": 1.1,
      opacity: 0.42,
    }),
    poly3([[-hx, -hy, -hz], [hx, -hy, -hz], [hx, -hy, hz], [-hx, -hy, hz]], {
      fill: "#EEEEEE",
      stroke: C.ink,
      "stroke-width": 1.1,
      opacity: 0.22,
    }),
    ...edges.map(([a, b]) => line3(corners[a], corners[b], {
      stroke: C.ink,
      "stroke-width": 1.35,
      opacity: 0.72,
    })),
    patchOnWall("-z", 67.5, "P1", [0, 116, -hz - 34]),
    patchOnWall("-x", -72.5, "P4", [-hx - 57, -72.5, 0]),
    patchOnWall("+x", 67.5, "P3", [hx + 53, 67.5, 0]),
    patchOnWall("+z", -72.5, "P2", [0, -118, hz + 39]),
    ellipse(tx[0], tx[1], 86, 34, { fill: "none", stroke: C.blue, "stroke-width": 1.25, opacity: 0.28 }),
    ellipse(tx[0], tx[1], 58, 23, { fill: "none", stroke: C.blue, "stroke-width": 1.25, opacity: 0.36 }),
    ellipse(tx[0], tx[1], 28, 12, { fill: C.orange2, stroke: C.orange, "stroke-width": 1.4 }),
    lineTag(tx[0] - 17, tx[1], tx[0] + 17, tx[1], { stroke: C.orange, "stroke-width": 1.25 }),
    text(tx[0], tx[1] + 5, "Tx", "rx-label", { "text-anchor": "middle", fill: C.orange }),
  ].join(""));
}

function sParameterBlock(x, y) {
  const w = 255;
  const h = 165;
  const plotX = x + 24;
  const plotY = y + 48;
  const plotW = w - 48;
  const plotH = 76;
  const traces = d3.range(4).map((k) => {
    const pts = d3.range(54).map((i) => [
      plotX + i * (plotW / 53),
      plotY + plotH * 0.55
        - 18 * Math.sin(i / 7 + k * 0.55)
        - 7 * Math.cos(i / 13 + k * 0.9)
        + k * 4,
    ]);
    return path(line(pts), {
      fill: "none",
      stroke: k === 0 ? C.orange : C.blue,
      "stroke-width": 1.55,
      opacity: k === 0 ? 0.95 : 0.68,
    });
  });
  return tag("g", {}, [
    rect(x, y, w, h, { rx: 4, fill: C.white, stroke: C.hair, "stroke-width": 1.25 }),
    text(x + w / 2, y + 26, "S-parameters", "block-title", { "text-anchor": "middle" }),
    lineTag(plotX, plotY + plotH, plotX + plotW, plotY + plotH, { stroke: C.ink, "stroke-width": 1.0, opacity: 0.72 }),
    lineTag(plotX, plotY + 6, plotX, plotY + plotH, { stroke: C.ink, "stroke-width": 1.0, opacity: 0.72 }),
    ...traces,
    text(x + w / 2, y + h - 17, "S_i5(f), i=1..4", "tiny", { "text-anchor": "middle" }),
  ].join(""));
}

function featureVectorBlock(x, y) {
  const w = 270;
  const h = 165;
  const groups = [
    ["RSSI", 28, C.blue],
    ["phase", 42, C.orange],
    ["slope", 38, C.blue],
    ["delay", 40, C.orange],
    ["pairs", 46, C.blue],
    ["stats", 36, C.orange],
  ];
  const gx = x + 20;
  const gy = y + 70;
  const gh = 36;
  let cursor = gx;
  const cells = [];
  for (const [idx, [label, gw, color]] of groups.entries()) {
    cells.push(rect(cursor, gy, gw, gh, { fill: color, opacity: 0.12, stroke: color, "stroke-width": 1.0 }));
    for (let i = 1; i < Math.floor(gw / 9); i++) {
      cells.push(lineTag(cursor + i * 9, gy, cursor + i * 9, gy + gh, { stroke: color, "stroke-width": 0.8, opacity: 0.35 }));
    }
    cells.push(text(cursor + gw / 2, gy + gh + (idx % 2 === 0 ? 21 : 45), label, "micro", {
      "text-anchor": "middle",
      textLength: Math.max(gw - 5, 16).toFixed(1),
      lengthAdjust: "spacingAndGlyphs",
    }));
    cursor += gw;
  }
  return tag("g", {}, [
    rect(x, y, w, h, { rx: 4, fill: C.white, stroke: C.hair, "stroke-width": 1.25 }),
    text(x + w / 2, y + 26, "180-D rich feature vector", "block-title", { "text-anchor": "middle" }),
    text(x + w / 2, y + 54, "x_RF in R^180", "feature-symbol", { "text-anchor": "middle" }),
    ...cells,
  ].join(""));
}

function posteriorCue(x, y) {
  const w = 205;
  const h = 150;
  const cx = x + 102;
  const cy = y + 82;
  return tag("g", {}, [
    rect(x, y, w, h, { rx: 4, fill: C.white, stroke: C.blue, "stroke-width": 1.35 }),
    ellipse(cx, cy, 66, 25, { fill: C.blue2, stroke: "none", opacity: 0.9 }),
    ellipse(cx, cy, 52, 19, { fill: "none", stroke: C.blue, "stroke-width": 1.35, opacity: 0.85 }),
    ellipse(cx, cy, 31, 12, { fill: "none", stroke: C.blue, "stroke-width": 1.15, opacity: 0.65 }),
    ...d3.range(16).map((i) => {
      const a = (i * 2 * Math.PI) / 16;
      const r = i % 3 === 0 ? 30 : 45;
      return circle(cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.36, 2.9, { fill: C.blue, opacity: 0.62 });
    }),
    circle(cx, cy, 4.2, { fill: C.ink, opacity: 0.9 }),
    text(cx, y + 27, "CFM posterior", "block-title", { "text-anchor": "middle" }),
    text(cx, y + h - 15, "p(x | x_RF)", "tiny", { "text-anchor": "middle" }),
  ].join(""));
}

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${PDF_W_PT}pt" height="${PDF_H_PT}pt" viewBox="0 0 ${PDF_W_PT} ${PDF_H_PT}">
<defs>
  <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
    <path d="M1,1 L7,4 L1,7 Z" fill="${C.ink}"/>
  </marker>
  <style>
    text { font-family: Arial, Helvetica, sans-serif; fill: ${C.ink}; }
    .title { font-size: 25px; font-weight: 700; }
    .subtitle { font-size: 21px; fill: ${C.muted}; }
    .block-title { font-size: 21px; font-weight: 700; }
    .feature-symbol { font-size: 21px; font-weight: 700; fill: ${C.blue}; }
    .label { font-size: 21px; font-weight: 700; }
    .small { font-size: 21px; fill: ${C.ink}; }
    .tiny { font-size: 21px; fill: ${C.muted}; }
    .micro { font-size: 21px; fill: ${C.muted}; }
    .rx-label { font-size: 21px; font-weight: 700; fill: ${C.ink}; }
  </style>
</defs>
<g transform="scale(${EXPORT_SCALE})">
<rect width="${W}" height="${H}" fill="white"/>
${text(W / 2, 42, "RF condition: measurement to posterior conditioning", "title", { "text-anchor": "middle" })}
${text(W / 2, 70, "Capsule Tx radiates to four side-wall receivers; S-parameters become the 180-D condition vector.", "subtitle", { "text-anchor": "middle" })}
${receiverGeometry(42, 46, 0.66)}
${text(248, 396, "capsule Tx inside phantom", "small", { "text-anchor": "middle" })}
${text(248, 418, "4 Rx on +/-x and +/-z side walls", "tiny", { "text-anchor": "middle" })}
${arrow(452, 216, 525, 216)}
${text(489, 197, "capture", "tiny", { "text-anchor": "middle" })}
${sParameterBlock(548, 124)}
${arrow(818, 216, 885, 216)}
${text(852, 197, "derive", "tiny", { "text-anchor": "middle" })}
${featureVectorBlock(908, 124)}
${arrow(1195, 216, 1258, 216)}
${text(1227, 197, "condition", "tiny", { "text-anchor": "middle" })}
${posteriorCue(1280, 132)}
</g>
</svg>
`;

const svgPath = join(outDir, "fig_method_condition_variants.svg");
const pdfPath = join(outDir, "fig_method_condition_variants.pdf");
writeFileSync(svgPath, svg);
execFileSync("rsvg-convert", ["-f", "pdf", "-o", pdfPath, svgPath], { stdio: "inherit" });
console.log(`wrote ${svgPath}`);
console.log(`wrote ${pdfPath}`);
