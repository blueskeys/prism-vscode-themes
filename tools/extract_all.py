# -*- coding: utf-8 -*-
"""Extract ALL T3 theme palettes (5 families, light+dark) and the two Material base
themes (ocean=dark syntax base, lighter=light syntax base) from server.asar."""
import re, math, json, os

ASAR = r"C:\Users\renjunjie\AppData\Local\Programs\t3code\resources\server.asar"
OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)
text = open(ASAR, "rb").read().decode("latin-1")

def balanced(s, start):
    depth, i, n = 0, start, len(s)
    in_str, q = False, ""
    while i < n:
        c = s[i]
        if in_str:
            if c == "\\":
                i += 2; continue
            if c == q: in_str = False
        else:
            if c in "\"'`": in_str, q = True, c
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: return i + 1
        i += 1
    return -1

def parse_pairs(s):
    out, i, n = [], 0, len(s)
    while i < n:
        m = re.compile(r"\s*['\"`]?([\w$-]+)['\"`]?\s*:").match(s, i)
        if not m:
            i += 1; continue
        key, i = m.group(1), m.end()
        depth, start, in_str, q = 0, i, False, ""
        while i < n:
            c = s[i]
            if in_str:
                if c == "\\":
                    i += 2; continue
                if c == q: in_str = False
            else:
                if c in "\"'`": in_str, q = True, c
                elif c in "{[(": depth += 1
                elif c in "}])":
                    if depth == 0: break
                    depth -= 1
                elif c == "," and depth == 0: break
            i += 1
        out.append((key, s[start:i].strip()))
        if i < n and s[i] == ",": i += 1
    return out

def oklch_to_rgb255(L, C, H):
    a = C * math.cos(math.radians(H)); b = C * math.sin(math.radians(H))
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    r = +4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bl = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    def gam(u):
        u = min(1.0, max(0.0, u))
        return 12.92*u if u <= 0.0031308 else 1.055*u**(1/2.4) - 0.055
    return round(gam(r)*255), round(gam(g)*255), round(gam(bl)*255)

def conv(v):
    v = v.strip().strip("\"'`")
    m = re.match(r"oklch\(\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*(?:/\s*([\d.]+)\s*)?\)", v)
    if m:
        r, g, b = oklch_to_rgb255(*(float(m.group(i)) for i in (1, 2, 3)))
        return f"#{r:02x}{g:02x}{b:02x}"
    if re.match(r"#[0-9a-fA-F]{3,8}$", v):
        return v.lower()
    return v

# ---- 5 family palettes ----
palettes = {}
for m in re.finditer(r"\{id:`([\w-]+)`,label:`([^`]*)`", text):
    fid = m.group(1)
    if fid not in ("t3-chat", "grove", "ocean", "ember", "iris"):
        continue
    root = text[m.start():balanced(text, m.start()) - 1]
    pairs = parse_pairs(root)
    meta = {k: v.strip("`\"'") for k, v in pairs if k not in ("colors", "variants")}
    colors = dict(parse_pairs(next(v for k, v in pairs if k == "colors").strip("{} ")))
    variants = parse_pairs(next(v for k, v in pairs if k == "variants").strip("{} "))
    dark = {}
    for k, v in variants:
        if k == "dark":
            for kk, vv in parse_pairs(v.strip("{} ")):
                dark[kk] = vv.strip("`\"'")
    palettes[fid] = {
        "meta": meta,
        "light": {k: conv(v) for k, v in colors.items()},
        "dark": {k: conv(v) for k, v in dark.items()},
    }
    print(f"{fid:8s} label={meta.get('label'):9s} light={len(colors)} keys  dark={len(dark)} keys  canvas d/l={palettes[fid]['dark'].get('canvas')}/{palettes[fid]['light'].get('canvas')}")

# sanity: all families share the same 61 keys
keys0 = set(palettes["ocean"]["light"])
for fid, p in palettes.items():
    assert set(p["light"]) == keys0 and set(p["dark"]) == keys0, f"key mismatch in {fid}"
print("all families share", len(keys0), "keys ✓")

# ---- material base themes (JSON precedes its own sourceMappingURL marker) ----
def extract_vs_theme(marker):
    m = re.search(re.escape(marker), text)
    s = text.rindex("JSON.parse(`", 0, m.start())
    start = s + len("JSON.parse(`")
    end = text.index("`)", start)
    return json.loads(text[start:end].encode("latin-1").decode("unicode_escape"))

mt_ocean = extract_vs_theme("material-theme-ocean-CHQ94UKr.js.map")
mt_lighter = extract_vs_theme("material-theme-lighter-uhdI0v04.js.map")
print("ocean:", mt_ocean["name"], mt_ocean["type"], "editor.bg", mt_ocean["colors"]["editor.background"])
print("lighter:", mt_lighter["name"], mt_lighter["type"], "editor.bg", mt_lighter["colors"]["editor.background"])

json.dump(palettes, open(os.path.join(OUT, "t3_palettes.json"), "w", encoding="utf-8"), indent=2)
json.dump(mt_ocean, open(os.path.join(OUT, "material_ocean.json"), "w", encoding="utf-8"), indent=2)
json.dump(mt_lighter, open(os.path.join(OUT, "material_lighter.json"), "w", encoding="utf-8"), indent=2)
print("saved to tools/data/")
