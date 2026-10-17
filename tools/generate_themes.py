# -*- coding: utf-8 -*-
"""Generate 12 VS Code theme JSONs:
  5 T3 families (t3-chat/grove/ocean/ember/iris) x {light,dark}
    = chrome from T3 palette (61 keys via MAPPING) + syntax/tokens from Material base
  + 1 Material family = bundled material-theme-ocean (dark) / material-theme-lighter (light) as-is.
Mapping table documented in ocean-vscode-mapping.md."""
import json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "..", "prism-themes", "themes")
os.makedirs(OUT, exist_ok=True)

palettes = json.load(open(os.path.join(DATA, "t3_palettes.json"), encoding="utf-8"))
mt_ocean = json.load(open(os.path.join(DATA, "material_ocean.json"), encoding="utf-8"))
mt_lighter = json.load(open(os.path.join(DATA, "material_lighter.json"), encoding="utf-8"))

# ---- VS Code key -> T3 palette key [(vscode, t3key, alpha_suffix_or_None)] ----
M = [
    # global
    ("foreground", "text", None), ("descriptionForeground", "textMuted", None),
    ("focusBorder", "focus", None), ("border", "border", None),
    ("selection.background", "terminalSelection", "80"),
    ("editorWidget.border", "border", None),
    # title bar
    ("titleBar.activeBackground", "chrome", None), ("titleBar.inactiveBackground", "chrome", None),
    ("titleBar.activeForeground", "toolbarForeground", None), ("titleBar.inactiveForeground", "textMuted", None),
    ("titleBar.border", "toolbarBorder", None),
    # editor group & tabs
    ("editorGroupHeader.tabsBackground", "toolbar", None),
    ("editorGroupHeader.tabsBorder", "toolbarBorder", None),
    ("editorGroup.border", "toolbarBorder", None),
    ("editorGroup.emptyBackground", "canvas", None),
    ("editorGroup.dropBackground", "accentSurface", None),
    ("tab.activeBackground", "canvas", None), ("tab.activeForeground", "text", None),
    ("tab.activeBorderTop", "accent", None),
    ("tab.inactiveBackground", "toolbar", None), ("tab.inactiveForeground", "textMuted", None),
    ("tab.hoverBackground", "sidebarRowHover", None),
    ("tab.unfocusedActiveForeground", "textMuted", None),
    # editor
    ("editor.background", "canvas", None), ("editor.foreground", "text", None),
    ("editorLineNumber.foreground", "mutedForeground", None),
    ("editorLineNumber.activeForeground", "text", None),
    ("editorCursor.foreground", "terminalCursor", None),
    ("editor.selectionBackground", "terminalSelection", None),
    ("editor.inactiveSelectionBackground", "muted", None),
    ("editor.selectionHighlightBackground", "terminalSelection", "40"),
    ("editor.findMatchBackground", "searchMatchActiveBackground", None),
    ("editor.findMatchForeground", "searchMatchActiveForeground", None),
    ("editor.findMatchHighlightBackground", "searchMatchBackground", None),
    ("editor.findMatchHighlightForeground", "searchMatchForeground", None),
    ("editor.lineHighlightBackground", "muted", None),
    ("editorCodeLens.foreground", "secondaryLabel", None),
    ("editorGhostText.foreground", "placeholder", None),
    ("editorWidget.background", "POPOVER", None),
    ("editorSuggestWidget.background", "POPOVER", None),
    ("editorHoverWidget.background", "POPOVER", None),
    ("quickInput.background", "POPOVER", None),
    ("debugToolBar.background", "POPOVER", None),
    ("editorSuggestWidget.selectedBackground", "sidebarRowSelected", None),
    ("keybindingLabel.background", "surfaceOverlay", None),
    ("keybindingLabel.foreground", "text", None),
    ("keybindingLabel.border", "border", None), ("keybindingLabel.bottomBorder", "border", None),
    ("editorInlayHint.background", "codeBackground", None),
    ("editorInlayHint.foreground", "textMuted", None),
    ("breadcrumb.background", "canvas", None), ("breadcrumb.foreground", "mutedForeground", None),
    ("breadcrumb.focusForeground", "text", None), ("breadcrumb.activeSelectionForeground", "text", None),
    ("minimap.background", "canvas", None),
    # sidebar / activity bar / lists  (T3 file tree: muted text, selected row pops white)
    ("sideBar.background", "sidebar", None), ("activityBar.background", "sidebar", None),
    ("sideBar.foreground", "sidebarMutedForeground", None),
    ("sideBarTitle.foreground", "sidebarMutedForeground", None),
    ("sideBar.border", "sidebarBorder", None), ("activityBar.border", "sidebarBorder", None),
    ("activityBar.foreground", "sidebarMutedForeground", None),
    ("activityBar.inactiveForeground", "iconMuted", None),
    ("activityBarBadge.background", "accent", None), ("activityBarBadge.foreground", "accentForeground", None),
    ("sideBarSectionHeader.background", "sidebarControlSurface", None),
    ("sideBarSectionHeader.foreground", "sidebarForeground", None),
    ("list.hoverBackground", "sidebarRowHover", None), ("list.focusBackground", "sidebarRowActive", None),
    ("list.activeSelectionBackground", "sidebarRowSelected", None),
    ("list.inactiveSelectionBackground", "sidebarRowSelected", None),
    ("list.activeSelectionForeground", "sidebarForeground", None),
    ("list.inactiveSelectionForeground", "sidebarForeground", None),
    ("list.focusOutline", "TRANSPARENT", None),
    ("quickInputList.focusBackground", "sidebarRowActive", None),
    ("quickInputList.focusForeground", "accentSurfaceForeground", None),
    ("pickerGroup.foreground", "textMuted", None),
    # git decorations: T3's tree has no saturated name colors -> all muted, conflict gets teal
    ("gitDecoration.addedResourceForeground", "sidebarMutedForeground", None),
    ("gitDecoration.modifiedResourceForeground", "sidebarMutedForeground", None),
    ("gitDecoration.deletedResourceForeground", "textMuted", None),
    ("gitDecoration.untrackedResourceForeground", "sidebarMutedForeground", None),
    ("gitDecoration.renamedResourceForeground", "sidebarMutedForeground", None),
    ("gitDecoration.submoduleResourceForeground", "sidebarMutedForeground", None),
    ("gitDecoration.stageModifiedResourceForeground", "sidebarMutedForeground", None),
    ("gitDecoration.stageDeletedResourceForeground", "textMuted", None),
    ("gitDecoration.conflictingResourceForeground", "messageAction", None),
    ("list.errorForeground", "error", None), ("list.warningForeground", "warning", None),
    # controls
    ("button.background", "accent", None), ("button.foreground", "accentForeground", None),
    ("button.hoverBackground", "updateForeground", None),
    ("button.secondaryBackground", "secondary", None),
    ("button.secondaryForeground", "secondaryForeground", None),
    ("button.secondaryHoverBackground", "accentSurface", None),
    ("input.background", "muted", None), ("dropdown.background", "muted", None),
    ("input.foreground", "text", None), ("dropdown.foreground", "text", None),
    ("input.border", "border", None), ("dropdown.border", "border", None),
    ("input.placeholderForeground", "placeholder", None),
    ("inputOption.activeBorder", "focus", None),
    ("dropdown.listBackground", "POPOVER", None),
    ("checkbox.background", "muted", None), ("checkbox.border", "border", None),
    ("checkbox.foreground", "text", None),
    ("menu.background", "POPOVER", None), ("menu.foreground", "toolbarControlForeground", None),
    ("menu.selectionBackground", "sidebarRowHover", None),
    ("menu.selectionForeground", "toolbarControlForeground", None),
    ("menu.separatorBackground", "border", None),
    ("menubar.selectionBackground", "sidebarRowHover", None),
    ("menubar.selectionForeground", "toolbarControlForeground", None),
    ("toolbar.hoverBackground", "toolbarControl", None),
    ("toolbar.hoverForeground", "toolbarControlForeground", None),
    ("toolbar.activeBackground", "toolbarControlHover", None),
    ("progressBar.background", "accent", None),
    # validation / diagnostics
    ("inputValidation.errorBackground", "errorSurface", None),
    ("inputValidation.errorBorder", "error", None),
    ("inputValidation.errorForeground", "errorForeground", None),
    ("inputValidation.warningBackground", "warningSurface", None),
    ("inputValidation.warningBorder", "warning", None),
    ("inputValidation.warningForeground", "warningForeground", None),
    ("inputValidation.infoBackground", "updateSurface", None),
    ("inputValidation.infoBorder", "update", None),
    ("inputValidation.infoForeground", "updateForeground", None),
    ("editorError.foreground", "error", None),
    ("editorWarning.foreground", "warning", None),
    ("editorInfo.foreground", "update", None),
    # notifications / links / embedded code
    ("notifications.background", "messageSurface", None),
    ("notifications.foreground", "messageForeground", None),
    ("notifications.border", "border", None),
    ("notificationCenterHeader.background", "surfaceRaised", None),
    ("notificationCenterHeader.foreground", "messageForeground", None),
    ("notificationsErrorIconForeground", "error", None),
    ("notificationsWarningIconForeground", "warning", None),
    ("notificationsInfoIconForeground", "update", None),
    ("notificationLink.foreground", "messageAction", None),
    ("textLink.foreground", "messageAction", None),
    ("textLink.activeForeground", "messageActionHover", None),
    ("textCodeBlock.background", "codeBackground", None),
    ("textPreformat.foreground", "codeForeground", None),
    ("textBlockQuote.background", "surfaceRaised", None),
    # terminal / scrollbar / status bar / panel
    ("terminal.background", "terminalBackground", None),
    ("terminal.foreground", "terminalForeground", None),
    ("terminalCursor.foreground", "terminalCursor", None),
    ("terminal.selectionBackground", "terminalSelection", None),
    ("terminal.border", "border", None),
    ("scrollbarSlider.background", "terminalScrollbar", None),
    ("scrollbarSlider.hoverBackground", "terminalScrollbarHover", None),
    ("scrollbarSlider.activeBackground", "terminalScrollbarHover", None),
    ("statusBar.background", "surface", None), ("statusBar.foreground", "text", None),
    ("statusBar.border", "border", None), ("statusBar.noFolderBackground", "surface", None),
    ("statusBar.noFolderForeground", "text", None),
    ("statusBar.debuggingBackground", "updateSurface", None),
    ("statusBar.debuggingForeground", "text", None),
    ("statusBarItem.hoverBackground", "sidebarRowHover", None),
    ("statusBarItem.remoteBackground", "updateSurface", None),
    ("statusBarItem.remoteForeground", "text", None),
    ("panel.background", "canvas", None), ("panel.border", "border", None),
]
LITERALS = {"widget.shadow": "#00000080"}

# overlay these key prefixes from the Material base (editor-internal / decorations / ansi /
# charts) for keys we did not set ourselves -- chrome keys always win
OVERLAY_PREFIXES = (
    "terminal.ansi", "gitDecoration", "diffEditor", "merge.", "editorBracketMatch",
    "editorBracketHighlight", "editor.wordHighlight", "editorOverviewRuler", "editorGutter",
    "charts.", "editorUnnecessaryCode", "editor.findRangeHighlightBackground",
    "editor.rangeHighlightBackground", "editor.foldBackground", "editor.snippetTabstopHighlight",
    "editor.snippetFinalTabstopHighlight", "editor.symbolHighlight", "minimap.",
    "editorLineNumber.dimmedForeground", "tree.indentGuidesStroke", "editorIndentGuide",
    "editorWhitespace", "editorRuler.foreground", "symbolIcon", "editorMarkerNavigation",
    "editorLightBulb", "editorLightBulbAutoFix", "listFilterWidget", "editorUnicodeHighlight",
    "editorComments", "editorMultiCursor.", "editor.stackFrameHighlight",
    "editor.focusedStackFrameHighlight", "notebook.", "editorInlineValue",
    "editorStickyScroll.", "editorSuggestWidget", "editorHoverWidget", "debugConsole.",
    "debugIcons", "testing.", "editorTokens.", "editorGhostText.border", "scm.",
)

FAMILIES = [
    ("t3-chat", "T3 Chat"), ("grove", "T3 Grove"), ("ocean", "T3 Ocean"),
    ("ember", "T3 Ember"), ("iris", "T3 Iris"),
]

def mix(h1, h2, t=0.5):
    a = tuple(int(h1[i:i+2], 16) for i in (1, 3, 5))
    b = tuple(int(h2[i:i+2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def build_t3_theme(fid, label, variant):
    pal = palettes[fid][variant]
    base = mt_ocean if variant == "dark" else mt_lighter
    popover = mix(pal["canvas"], pal["sidebar"])  # sampled from T3's Color-scheme popover (#1a2631)
    colors = dict(LITERALS)
    colors["widget.shadow"] = "#00000080"
    for vskey, t3key, alpha in M:
        if t3key == "POPOVER":
            v = popover
        elif t3key == "TRANSPARENT":
            v = "#00000000"
        else:
            v = pal[t3key]
        colors[vskey] = v + alpha if alpha else v
    for k, v in base["colors"].items():
        if k in colors:
            continue
        if k.startswith(OVERLAY_PREFIXES):
            colors[k] = v
    return {
        "name": f"{label} {'Dark' if variant == 'dark' else 'Light'}",
        "type": "dark" if variant == "dark" else "light",
        "semanticHighlighting": True,
        "colors": colors,
        "tokenColors": base["tokenColors"],
    }

manifest = []
for fid, label in FAMILIES:
    for variant in ("light", "dark"):
        theme = build_t3_theme(fid, label, variant)
        fname = f"t3-{fid}-{variant}.json"
        json.dump(theme, open(os.path.join(OUT, fname), "w", encoding="utf-8"), indent=2)
        manifest.append((label + (" Dark" if variant == "dark" else " Light"),
                         "vs-dark" if variant == "dark" else "vs", fname, theme["colors"]["editor.background"]))
        print(f"built {fname:24s} editor.bg={theme['colors']['editor.background']}  colors={len(theme['colors'])} tokens={len(theme['tokenColors'])}")

# family 6: pure bundled Material themes
for src, fname, label in ((mt_ocean, "t3-material-dark.json", "T3 Material Dark"),
                          (mt_lighter, "t3-material-light.json", "T3 Material Light")):
    theme = copy.deepcopy(src)
    theme["name"] = label
    json.dump(theme, open(os.path.join(OUT, fname), "w", encoding="utf-8"), indent=2)
    manifest.append((label, src["type"], fname, src["colors"]["editor.background"]))
    print(f"built {fname:24s} editor.bg={src['colors']['editor.background']}  colors={len(src['colors'])} tokens={len(src['tokenColors'])}")

# emit palettes.json for the extension's webview picker (labels + the keys the picker UI needs)
PICKER_KEYS = ("canvas", "sidebar", "accent", "accentForeground", "text",
               "sidebarMutedForeground", "border", "sidebarRowHover", "sidebarRowActive",
               "sidebarRowSelected", "accentSurface", "accentSurfaceForeground", "muted",
               "messageSurface", "surfaceOverlay")
summary = {}
for fid, p in palettes.items():
    entry = {"label": p["meta"].get("label", fid)}
    for variant in ("light", "dark"):
        v = {k: p[variant][k] for k in PICKER_KEYS}
        v["popover"] = mix(v["canvas"], v["sidebar"])
        entry[variant] = v
    summary[fid] = entry

def material_variant(c):
    v = {
        "canvas": c.get("editor.background", "#0F111A"),
        "sidebar": c.get("sideBar.background", c.get("editor.background", "#0F111A")),
        "accent": c.get("activityBarBadge.background", "#80CBC4"),
        "accentForeground": c.get("activityBarBadge.foreground", "#ffffff"),
        "text": c.get("editor.foreground", "#babed8"),
        "sidebarMutedForeground": c.get("sideBar.foreground", c.get("foreground", "#babed8")),
        "border": c.get("editorGroup.border", c.get("contrastBorder", "#464B5D")),
        "sidebarRowHover": c.get("list.hoverBackground", "#1B1E2E"),
        "sidebarRowActive": c.get("list.activeSelectionBackground", "#1B1E2E"),
        "sidebarRowSelected": c.get("list.activeSelectionBackground", "#1B1E2E"),
        "accentSurface": c.get("list.activeSelectionBackground", "#1B1E2E"),
        "accentSurfaceForeground": c.get("list.activeSelectionForeground", "#ffffff"),
        "muted": c.get("input.background", "#1B1E2E"),
        "messageSurface": c.get("notifications.background", "#1B1E2E"),
        "surfaceOverlay": c.get("keybindingLabel.background", "#1B1E2E"),
    }
    v["popover"] = mix(v["canvas"], v["sidebar"])
    return v

summary["material"] = {"label": "Material",
                       "light": material_variant(mt_lighter["colors"]),
                       "dark": material_variant(mt_ocean["colors"])}
json.dump(summary, open(os.path.join(OUT, "..", "palettes.json"), "w", encoding="utf-8"), indent=1)

json.dump([{"label": l, "uiTheme": u, "path": f"themes/{f}"} for l, u, f, _ in manifest],
          open(os.path.join(DATA, "manifest.json"), "w", encoding="utf-8"), indent=2)
print("\nmanifest:", len(manifest), "themes; palettes.json written")
