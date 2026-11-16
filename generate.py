#!/usr/bin/env python3
"""
Generador del perfil de GitHub de Dre_Amy.

Lee config.json y crea:
  - README.md
  - assets/banner.svg, divider.svg, academic.svg, skills.svg

Solo usa la librería estándar de Python (3.8+). Ejemplos:
  python generate.py                       # usa el tema de config.json
  python generate.py --theme retro-sunset  # prueba otro tema
  python generate.py --seed 21             # cambia el cielo de estrellas
  python generate.py --list-themes         # muestra los temas disponibles
"""
import argparse
import json
import random
import sys
import textwrap
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

# ---------------------------------------------------------------- temas ----
# Cada tema define los mismos colores. Puedes sobrescribir cualquiera desde
# config.json en "palette", por ejemplo: "palette": {"secondary": "#00ffd0"}
PALETTES = {
    "dreamy-night": {
        "bg_top": "#0b1033", "bg_bottom": "#1c1255",
        "primary": "#7b5cff", "secondary": "#3df2d5",
        "warm": "#ffb27a", "pink": "#ff7ac8",
        "text": "#e9ebff", "muted": "#a3a9d6",
        "line": "#2f3680", "card": "#111749",
    },
    "retro-sunset": {
        "bg_top": "#1a0b3b", "bg_bottom": "#42115c",
        "primary": "#b06cff", "secondary": "#4de1ff",
        "warm": "#ffb347", "pink": "#ff5fa2",
        "text": "#fff1fb", "muted": "#dbb7ec",
        "line": "#5a2380", "card": "#261049",
    },
    "mint-terminal": {
        "bg_top": "#04120e", "bg_bottom": "#0b2c24",
        "primary": "#5eead4", "secondary": "#a7f3d0",
        "warm": "#fde68a", "pink": "#f9a8d4",
        "text": "#e8fff7", "muted": "#8fc9b8",
        "line": "#1c5a4b", "card": "#0a211b",
    },
    "cotton-candy": {
        "bg_top": "#1b1340", "bg_bottom": "#2f1a63",
        "primary": "#c4a7ff", "secondary": "#7ef9e0",
        "warm": "#ffd29a", "pink": "#ff9ed8",
        "text": "#fdf6ff", "muted": "#cdbcf0",
        "line": "#4b3a92", "card": "#241a55",
    },
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Trebuchet MS','Segoe UI',system-ui,Helvetica,Arial,sans-serif"

ORDINALS = {1: "1er", 2: "2do", 3: "3er", 4: "4to", 5: "5to",
            6: "6to", 7: "7mo", 8: "8vo", 9: "9no", 10: "10mo"}


def esc(s):
    return escape(str(s), quote=True)


def ordinal(n):
    return ORDINALS.get(n, f"{n}°")


# ------------------------------------------------------------ utilidades ----
def sparkle(cx, cy, r, fill, delay="0s", cls="tw"):
    d = (f"M{cx:.1f} {cy - r:.1f} Q{cx:.1f} {cy:.1f} {cx + r:.1f} {cy:.1f} "
         f"Q{cx:.1f} {cy:.1f} {cx:.1f} {cy + r:.1f} "
         f"Q{cx:.1f} {cy:.1f} {cx - r:.1f} {cy:.1f} "
         f"Q{cx:.1f} {cy:.1f} {cx:.1f} {cy - r:.1f}Z")
    return f'<path d="{d}" fill="{fill}" class="{cls}" style="animation-delay:{delay}"/>'


COMMON_CSS = (
    ".tw{animation:tw 3.4s ease-in-out infinite}"
    "@keyframes tw{0%,100%{opacity:.18}50%{opacity:1}}"
    ".fl{animation:fl 5s ease-in-out infinite}"
    "@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}"
    ".bl{animation:bl 1.1s steps(1) infinite}"
    "@keyframes bl{50%{opacity:0}}"
    ".pu{transform-box:fill-box;transform-origin:center;animation:pu 2.4s ease-out infinite}"
    "@keyframes pu{0%{transform:scale(.7);opacity:.9}100%{transform:scale(1.5);opacity:0}}"
    ".dash{animation:ds 1.4s linear infinite}"
    "@keyframes ds{to{stroke-dashoffset:-16}}"
    f".mono{{font-family:{MONO}}}"
    f".sans{{font-family:{SANS}}}"
)


def svg_open(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{esc(title)}">'
            f"<title>{esc(title)}</title><style>{COMMON_CSS}</style>")


# --------------------------------------------------------------- banner ----
def banner(cfg, p, seed):
    W, H, HORIZON, SX = 900, 320, 250, 730
    rnd = random.Random(seed)
    alias = cfg["alias"]
    size = max(34, min(72, int(560 / (max(len(alias), 1) * 0.62))))
    label = cfg.get("banner_label", "hola, soy")
    path = cfg.get("banner_path", "~/portfolio")
    line = cfg.get("banner_line", "")

    o = [svg_open(W, H, f"Banner de {alias}: {cfg['tagline']}")]
    o.append(
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["bg_top"]}"/><stop offset="1" stop-color="{p["bg_bottom"]}"/></linearGradient>'
        f'<linearGradient id="gt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p["secondary"]}"/><stop offset=".55" stop-color="{p["primary"]}"/><stop offset="1" stop-color="{p["pink"]}"/></linearGradient>'
        f'<linearGradient id="gs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["warm"]}"/><stop offset="1" stop-color="{p["pink"]}"/></linearGradient>'
        f'<radialGradient id="glow"><stop offset="0" stop-color="{p["primary"]}" stop-opacity=".55"/><stop offset="1" stop-color="{p["primary"]}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="round"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
        f'<clipPath id="floor"><rect x="0" y="{HORIZON}" width="{W}" height="{H - HORIZON}"/></clipPath>'
        f'<mask id="sunmask"><rect width="{W}" height="{HORIZON}" fill="#fff"/>'
        f'<rect x="{SX - 100}" y="{HORIZON - 52}" width="200" height="3" fill="#000"/>'
        f'<rect x="{SX - 100}" y="{HORIZON - 38}" width="200" height="4" fill="#000"/>'
        f'<rect x="{SX - 100}" y="{HORIZON - 24}" width="200" height="6" fill="#000"/>'
        f'<rect x="{SX - 100}" y="{HORIZON - 11}" width="200" height="8" fill="#000"/></mask>'
        "</defs>"
    )
    o.append('<g clip-path="url(#round)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    o.append(f'<circle cx="{SX}" cy="{HORIZON - 40}" r="190" fill="url(#glow)"/>')

    # estrellas
    for _ in range(58):
        x = rnd.uniform(12, W - 12)
        y = rnd.uniform(12, HORIZON - 14)
        delay = f"{rnd.uniform(0, 3.4):.2f}s"
        if x < 560 and y > 118:  # deja libre el área del texto
            continue
        if rnd.random() < 0.26:
            col = rnd.choice([p["secondary"], p["pink"], p["warm"], p["text"]])
            o.append(sparkle(x, y, rnd.uniform(3.5, 7), col, delay))
        else:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.6, 1.5):.2f}" '
                     f'fill="{p["text"]}" class="tw" style="animation-delay:{delay}"/>')

    # sol retro + rejilla en perspectiva
    o.append(f'<circle cx="{SX}" cy="{HORIZON - 6}" r="80" fill="url(#gs)" mask="url(#sunmask)"/>')
    o.append('<g clip-path="url(#floor)" stroke-width="1.2" opacity=".75">')
    for k in range(1, 7):
        y = HORIZON + 70 * (k / 6) ** 2
        o.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="{p["line"]}"/>')
    for j in range(-14, 15):
        o.append(f'<line x1="{SX}" y1="{HORIZON}" x2="{SX + j * 70}" y2="{H}" stroke="{p["line"]}"/>')
    o.append("</g>")
    o.append(f'<line x1="0" y1="{HORIZON}" x2="{W}" y2="{HORIZON}" stroke="{p["secondary"]}" stroke-width="1.5" opacity=".7"/>')

    # acentos de pixel art
    for (x, y, c, d) in [(612, 96, "secondary", "0s"), (846, 118, "pink", "1.1s"),
                         (800, 60, "warm", "2.2s"), (660, 168, "primary", "1.7s")]:
        o.append(f'<rect x="{x}" y="{y}" width="8" height="8" fill="{p[c]}" class="tw" style="animation-delay:{d}"/>')
    o.append(sparkle(780, 92, 16, p["secondary"], "0.4s", "tw fl"))

    # ventana de terminal
    for i, c in enumerate(["warm", "secondary", "primary"]):
        o.append(f'<circle cx="{48 + i * 18}" cy="40" r="5" fill="{p[c]}"/>')
    o.append(f'<text x="108" y="45" class="mono" font-size="13" fill="{p["muted"]}">{esc(path)}</text>')

    # textos
    o.append(sparkle(56, 100, 8, p["secondary"], "0s", "tw fl"))
    o.append(f'<text x="74" y="106" class="mono" font-size="17" fill="{p["secondary"]}">{esc(label)}</text>')
    cx = 74 + len(label) * 10.2 + 6
    o.append(f'<rect x="{cx:.0f}" y="92" width="10" height="17" fill="{p["secondary"]}" class="bl"/>')
    o.append(f'<text x="46" y="{108 + size * 0.82:.0f}" class="sans" font-size="{size}" font-weight="800" '
             f'letter-spacing="-1" fill="url(#gt)">{esc(alias)}</text>')
    ty = 108 + size * 0.82 + 40
    o.append(f'<text x="48" y="{ty:.0f}" class="sans" font-size="21" fill="{p["text"]}">{esc(cfg["tagline"])}</text>')
    if line:
        o.append(f'<text x="48" y="{ty + 28:.0f}" class="mono" font-size="14" fill="{p["muted"]}">{esc(line)}</text>')

    o.append("</g>")
    o.append(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="21.5" fill="none" stroke="{p["line"]}" stroke-width="1.5"/>')
    o.append("</svg>")
    return "".join(o)


# -------------------------------------------------------------- divider ----
def divider(cfg, p):
    W, H = 900, 28
    o = [svg_open(W, H, "Separador")]
    o.append(
        "<defs>"
        f'<linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p["secondary"]}" stop-opacity="0"/><stop offset=".5" stop-color="{p["primary"]}"/><stop offset="1" stop-color="{p["secondary"]}" stop-opacity="0"/></linearGradient>'
        "</defs>"
    )
    o.append(f'<rect x="40" y="13" width="820" height="2" rx="1" fill="url(#l)"/>')
    o.append(sparkle(450, 14, 11, p["secondary"], "0s", "tw fl"))
    o.append(sparkle(412, 14, 5, p["pink"], "0.8s"))
    o.append(sparkle(488, 14, 5, p["warm"], "1.6s"))
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------ travesía académica ----
def academic(cfg, p):
    a = cfg["academic"]
    n = max(1, int(a["cycle_current"]))
    W, H = 900, 176
    x0, x1, y = 70, 560, 96
    step = (x1 - x0) / (n - 1) if n > 1 else 0
    xs = [x0 + i * step for i in range(n)]
    title = f'{a["university"]} · {a["career"]}'

    o = [svg_open(W, H, f"Ruta académica: {ordinal(n)} ciclo en curso en {a['university']}")]
    o.append(
        "<defs>"
        f'<linearGradient id="ph" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p["primary"]}"/><stop offset="1" stop-color="{p["secondary"]}"/></linearGradient>'
        "</defs>"
    )
    o.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{p["card"]}" stroke="{p["line"]}" stroke-width="1.5"/>')
    o.append(sparkle(36, 34, 7, p["secondary"], "0s", "tw fl"))
    o.append(f'<text x="52" y="39" class="mono" font-size="14" fill="{p["muted"]}">ruta académica · {esc(title)}</text>')

    # camino recorrido y camino por venir
    o.append(f'<line x1="{xs[0]:.1f}" y1="{y}" x2="{xs[-1]:.1f}" y2="{y}" stroke="url(#ph)" stroke-width="4" stroke-linecap="round"/>')
    o.append(f'<line x1="{xs[-1]:.1f}" y1="{y}" x2="800" y2="{y}" stroke="{p["muted"]}" stroke-width="3" '
             f'stroke-dasharray="3 13" stroke-linecap="round" class="dash"/>')

    for i, x in enumerate(xs, start=1):
        if i < n:
            o.append(f'<circle cx="{x:.1f}" cy="{y}" r="13" fill="{p["primary"]}"/>')
            o.append(f'<text x="{x:.1f}" y="{y + 4.5}" text-anchor="middle" class="mono" font-size="13" font-weight="700" fill="{p["bg_top"]}">{i}</text>')
            o.append(f'<text x="{x:.1f}" y="{y + 38}" text-anchor="middle" class="mono" font-size="11" fill="{p["muted"]}">ciclo {i}</text>')
        else:
            o.append(f'<circle cx="{x:.1f}" cy="{y}" r="20" fill="none" stroke="{p["secondary"]}" stroke-width="2" class="pu"/>')
            o.append(f'<circle cx="{x:.1f}" cy="{y}" r="16" fill="{p["secondary"]}"/>')
            o.append(f'<text x="{x:.1f}" y="{y + 5}" text-anchor="middle" class="mono" font-size="15" font-weight="700" fill="{p["bg_top"]}">{i}</text>')
            o.append(f'<text x="{x:.1f}" y="{y + 42}" text-anchor="middle" class="mono" font-size="13" font-weight="700" fill="{p["secondary"]}">{ordinal(i)} ciclo</text>')
            o.append(f'<text x="{x:.1f}" y="{y + 58}" text-anchor="middle" class="mono" font-size="11" fill="{p["muted"]}">en curso</text>')

    o.append(sparkle(822, y, 17, p["warm"], "0.3s", "tw fl"))
    o.append(f'<text x="822" y="{y + 42}" text-anchor="middle" class="mono" font-size="12" fill="{p["warm"]}">{esc(a.get("next_label", "lo que sigue"))}</text>')
    o.append("</svg>")
    return "".join(o)


# ----------------------------------------------------------- habilidades ----
def skills(cfg, p):
    cats = cfg["skills"]
    accents = [p["secondary"], p["primary"], p["warm"], p["pink"]]
    W, colw, gap, pad = 900, 430, 40, 20
    inner = colw - 2 * pad
    chip_h, chip_gap = 26, 8
    cols = [0, 0]
    cards = []

    for i, (name, chips) in enumerate(cats.items()):
        rows, row, x = [], [], 0.0
        for c in chips:
            w = len(c) * 7.8 + 26
            if row and x + w > inner:
                rows.append(row)
                row, x = [], 0.0
            row.append((c, w, x))
            x += w + chip_gap
        if row:
            rows.append(row)
        h = 58 + len(rows) * (chip_h + chip_gap) + 8
        col = 0 if cols[0] <= cols[1] else 1
        cards.append((name, rows, col, cols[col], h, accents[i % len(accents)]))
        cols[col] += h + 20

    H = int(max(cols) - 20) or 60
    o = [svg_open(W, H, "Habilidades técnicas")]
    for name, rows, col, top, h, acc in cards:
        left = col * (colw + gap)
        o.append(f'<rect x="{left + 1}" y="{top + 1}" width="{colw - 2}" height="{h - 2}" rx="16" fill="{p["card"]}" stroke="{p["line"]}" stroke-width="1.5"/>')
        o.append(sparkle(left + pad + 6, top + 30, 6, acc, f"{(top % 7) / 3:.1f}s"))
        o.append(f'<text x="{left + pad + 20}" y="{top + 35}" class="mono" font-size="14" font-weight="700" fill="{acc}">{esc(name)}</text>')
        for r_i, row in enumerate(rows):
            cy = top + 52 + r_i * (chip_h + chip_gap)
            for (c, w, x) in row:
                cx = left + pad + x
                o.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{chip_h}" rx="13" fill="{p["bg_top"]}" stroke="{acc}" stroke-opacity=".6"/>')
                o.append(f'<text x="{cx + w / 2:.1f}" y="{cy + 17.5}" text-anchor="middle" class="mono" font-size="13" fill="{p["text"]}">{esc(c)}</text>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------- reconocimientos ----
def awards(cfg, p):
    items = cfg["awards"]
    n = len(items)
    W, gap, pad = 900, 24, 22
    cw = (W - gap * (n - 1)) / n
    title_w = max(12, int((cw - 2 * pad) / 8.6))
    detail_w = max(14, int((cw - 2 * pad) / 7.4))
    tone = {1: p["warm"], 2: p["secondary"], 3: p["pink"]}

    laid = []
    for it in items:
        t = textwrap.wrap(it["title"], title_w) or [""]
        d = textwrap.wrap(it.get("detail", ""), detail_w)
        laid.append((t, d))
    h_body = max(len(t) * 20 + 24 + len(d) * 17 for t, d in laid)
    H = 114 + h_body + 20

    o = [svg_open(W, H, "Reconocimientos: " + "; ".join(f'{i["place"]} lugar, {i["title"]}' for i in items))]
    for idx, (it, (t, d)) in enumerate(zip(items, laid)):
        x = idx * (cw + gap)
        acc = tone.get(it.get("n", idx + 1), p["primary"])
        o.append(f'<rect x="{x + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18" fill="{p["card"]}" stroke="{p["line"]}" stroke-width="1.5"/>')
        o.append(f'<circle cx="{x + pad + 26:.1f}" cy="52" r="28" fill="{acc}"/>')
        o.append(f'<text x="{x + pad + 26:.1f}" y="58" text-anchor="middle" class="mono" font-size="17" font-weight="700" fill="{p["bg_top"]}">{esc(it["place"])}</text>')
        o.append(f'<text x="{x + pad + 66:.1f}" y="46" class="mono" font-size="16" font-weight="700" fill="{acc}">{esc(it["place"])} lugar</text>')
        o.append(f'<text x="{x + pad + 66:.1f}" y="64" class="mono" font-size="12" fill="{p["muted"]}">{esc(it.get("scope", ""))}</text>')
        o.append(f'<text x="{x + pad + 66:.1f}" y="80" class="mono" font-size="12" fill="{p["muted"]}">{esc(it.get("date", ""))}</text>')
        o.append(sparkle(x + cw - pad - 8, 30, 7, acc, f"{idx * 0.9:.1f}s"))
        y = 122
        for line in t:
            o.append(f'<text x="{x + pad:.1f}" y="{y}" class="mono" font-size="14" font-weight="700" fill="{p["text"]}">{esc(line)}</text>')
            y += 20
        o.append(f'<text x="{x + pad:.1f}" y="{y + 2}" class="mono" font-size="12" fill="{acc}">{esc(it.get("org", ""))}</text>')
        y += 24
        for line in d:
            o.append(f'<text x="{x + pad:.1f}" y="{y}" class="mono" font-size="12" fill="{p["muted"]}">{esc(line)}</text>')
            y += 17
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- README ----
def shield_part(s):
    return quote(str(s).replace("-", "--").replace("_", "__").replace(" ", "_"), safe="_-@.")


def badge(label, value, color_hex, bg_hex, logo=None, logo_color="white", style="for-the-badge"):
    url = f"https://img.shields.io/badge/{shield_part(label)}-{shield_part(value)}-{color_hex}?style={style}&labelColor={bg_hex}"
    if logo:
        url += f"&logo={logo}&logoColor={logo_color}"
    return url


def build_readme(cfg, p, warnings):
    sec = cfg.get("sections", {})
    bg = p["bg_top"].lstrip("#")
    hx = lambda key: p.get(key, key).lstrip("#")  # acepta nombre de color o #hex
    div = '<img src="assets/divider.svg" width="100%" alt="">'
    o = []

    o.append(
        '<div align="center">\n\n'
        f'<img src="assets/banner.svg" alt="{esc(cfg["alias"])} — {esc(cfg["tagline"])}" width="100%">\n\n'
    )
    tops = []
    for b in cfg.get("badges_top", []):
        tops.append(f'![{b["label"]}]({badge(b["label"], b["value"], hx(b.get("color", "primary")), bg)})')
    if tops:
        o.append("\n".join(tops) + "\n\n")
    o.append("</div>\n")

    if sec.get("terminal", True) and cfg.get("terminal"):
        lines = []
        for step in cfg["terminal"]:
            lines.append(f'{cfg["prompt"]} {step["cmd"]}')
            lines.extend(step.get("out", []))
            lines.append("")
        o.append("\n```text\n" + "\n".join(lines).rstrip() + "\n```\n")

    for para in cfg.get("bio", []):
        o.append(para + "\n")

    if sec.get("datos_personales", True) and cfg.get("personal"):
        o.append(f"\n{div}\n\n## ✦ Datos personales\n")
        o.append("| | |\n| :-- | :-- |")
        for k, v in cfg["personal"]:
            o.append(f"| **{k}** | {v} |")
        o.append("")

    a = cfg["academic"]
    if sec.get("travesia", True):
        o.append(f"\n{div}\n\n## ✦ Travesía académica\n")
        o.append(f'<img src="assets/academic.svg" alt="Ruta académica: {ordinal(a["cycle_current"])} ciclo en curso en {esc(a["university"])}" width="100%">\n')
        since = f' · desde {a["since"]}' if a.get("since") else ""
        o.append(f'**{a["university_full"]} ({a["university"]})** · {a["career"]} · **{ordinal(a["cycle_current"])} ciclo**{since}\n')
        o.append("Mi camino por la carrera se ve en lo que voy construyendo:\n")
        for b in a.get("bullets", []):
            o.append(f"- {b}")
        o.append("")

    if sec.get("reconocimientos", True) and cfg.get("awards"):
        o.append(f"\n{div}\n\n## ✦ Reconocimientos\n")
        alt = "; ".join(f'{i["place"]} lugar en {i["title"]}' for i in cfg["awards"])
        o.append(f'<img src="assets/awards.svg" alt="Reconocimientos: {esc(alt)}" width="100%">\n')

    if sec.get("experiencia", True) and cfg.get("experience"):
        o.append(f"\n{div}\n\n## ✦ Programas y liderazgo\n")
        o.append("| Programa | Rol | Organiza | Periodo |\n| :-- | :-- | :-- | :-- |")
        for e in cfg["experience"]:
            extra = f'<br><sub>{e["detail"]}</sub>' if e.get("detail") else ""
            o.append(f'| **{e["program"]}**{extra} | {e["role"]} | {e["org"]} | {e["period"]} |')
        o.append("")

    def project_block(items, with_icon=True):
        out = []
        for pr in items:
            icon = pr.get("icon", "✦") if with_icon else "✦"
            name = f'[{pr["name"]}]({pr["url"]})' if pr.get("url") else pr["name"]
            out.append(f"### {icon} {name}\n")
            out.append(pr["description"] + "\n")
            out.append(" · ".join(f"`{s}`" for s in pr.get("stack", [])) + "\n")
        return out

    if sec.get("proyectos", True) and cfg.get("featured_projects"):
        o.append(f"\n{div}\n\n## ✦ Proyectos destacados\n")
        o.extend(project_block(cfg["featured_projects"]))

    if sec.get("github", True) and cfg.get("github_repos"):
        o.append(f"\n{div}\n\n## ✦ En mi GitHub\n")
        o.append("| Repositorio | Qué es | Stack |\n| :-- | :-- | :-- |")
        for r in cfg["github_repos"]:
            stack = " · ".join(f"`{s}`" for s in r.get("stack", []))
            o.append(f'| [**{r["name"]}**]({r["url"]}) | {r["description"]} | {stack} |')
        o.append("")

    if sec.get("habilidades", True) and cfg.get("skills"):
        o.append(f"\n{div}\n\n## ✦ Habilidades\n")
        o.append('<img src="assets/skills.svg" alt="Habilidades técnicas por categoría" width="100%">\n')
        o.append("<details>\n<summary>Ver como lista</summary>\n")
        for cat, items in cfg["skills"].items():
            o.append(f"- **{cat}:** {', '.join(items)}")
        o.append("\n</details>\n")

    if sec.get("certificaciones", True) and cfg.get("certifications"):
        o.append(f"\n{div}\n\n## ✦ Certificaciones\n")
        o.append("| Certificación | Organiza | Fecha |\n| :-- | :-- | :-- |")
        for c in cfg["certifications"]:
            title = f'[{c["title"]}]({c["url"]})' if c.get("url") else c["title"]
            o.append(f'| {title} | {c["org"]} | {c["date"]} |')
        o.append("")

    if sec.get("contacto", True):
        L = cfg["links"]
        o.append(f"\n{div}\n\n## ✦ Hablemos\n\n<div align=\"center\">\n")
        o.append(f'[![GitHub]({badge("GitHub", L["github_label"], hx("primary"), bg, "github")})]({L["github"]})')
        if L.get("linkedin"):
            o.append(f'[![LinkedIn]({badge("LinkedIn", L["linkedin_label"], hx("secondary"), bg, "linkedin")})]({L["linkedin"]})')
        else:
            warnings.append('Falta "linkedin" en config.json (links): el botón de LinkedIn se omitió.')
        if L.get("instagram"):
            o.append(f'[![Instagram]({badge("Instagram", L["instagram_label"], hx("warm"), bg, "instagram")})]({L["instagram"]})')
        if L.get("email"):
            o.append(f'[![Correo]({badge("Correo", L["email"], hx("primary"), bg, "gmail")})](mailto:{L["email"]})')
        o.append(f'\n<br>\n\n✦ &nbsp; *{cfg["closing"]}* &nbsp; ✦\n\n</div>')

    return "\n".join(o) + "\n"


# ------------------------------------------------------------------ main ----
def main():
    ap = argparse.ArgumentParser(description="Genera el README y los gráficos del perfil.")
    ap.add_argument("--config", default=str(ROOT / "config.json"))
    ap.add_argument("--theme", help="nombre del tema (ver --list-themes)")
    ap.add_argument("--seed", type=int, help="semilla del cielo de estrellas")
    ap.add_argument("--list-themes", action="store_true")
    args = ap.parse_args()

    if args.list_themes:
        for name in PALETTES:
            print(name)
        return 0

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    theme = args.theme or cfg.get("theme", "dreamy-night")
    if theme not in PALETTES:
        print(f'Tema "{theme}" no existe. Disponibles: {", ".join(PALETTES)}', file=sys.stderr)
        return 1
    p = {**PALETTES[theme], **cfg.get("palette", {})}
    seed = args.seed if args.seed is not None else cfg.get("seed", 7)

    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "banner.svg").write_text(banner(cfg, p, seed), encoding="utf-8")
    (ASSETS / "divider.svg").write_text(divider(cfg, p), encoding="utf-8")
    (ASSETS / "academic.svg").write_text(academic(cfg, p), encoding="utf-8")
    (ASSETS / "skills.svg").write_text(skills(cfg, p), encoding="utf-8")
    if cfg.get("awards"):
        (ASSETS / "awards.svg").write_text(awards(cfg, p), encoding="utf-8")

    warnings = []
    (ROOT / "README.md").write_text(build_readme(cfg, p, warnings), encoding="utf-8")

    print(f"Listo ✦ tema={theme} semilla={seed}")
    print("  README.md + assets/banner.svg, divider.svg, academic.svg, skills.svg, awards.svg")
    for w in warnings:
        print("  Aviso:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
