const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

const FAMILY_ORDER = ['t3-code', 't3-chat', 'grove', 'ocean', 'ember', 'iris'];
const FAMILY_LABEL = {
  't3-code': 'T3 Code', 't3-chat': 'T3 Chat', grove: 'Grove',
  ocean: 'Ocean', ember: 'Ember', iris: 'Iris', material: 'Material',
};
// map picker family id -> actual VS Code theme family id
const FAMILY_TO_THEME = {
  't3-code': 'ocean',
  't3-chat': 't3-chat',
  grove: 'grove', ocean: 'ocean', ember: 'ember', iris: 'iris', material: 'material',
};
const THEME_TO_FAMILY = Object.fromEntries(Object.entries(FAMILY_TO_THEME).map(([k, v]) => [v, k]));

// the contributed VS Code theme labels in package.json use these exact prefixes
// (note: "T3 Chat" not "T3 T3 Chat" — the "T3 " prefix is already in the family label for chat)
const THEME_LABEL_PREFIX = {
  't3-chat': 'T3 Chat',
  grove: 'T3 Grove',
  ocean: 'T3 Ocean',
  ember: 'T3 Ember',
  iris: 'T3 Iris',
  material: 'T3 Material',
};

function themeLabel(themeFid, variant) {
  return `${THEME_LABEL_PREFIX[themeFid]} ${variant === 'dark' ? 'Dark' : 'Light'}`;
}
function parseTheme(label) {
  if (!label) return null;
  const m = /^(T3 .+?) (Dark|Light)$/.exec(label);
  if (!m) return null;
  const themeFid = Object.keys(THEME_LABEL_PREFIX).find(tf => THEME_LABEL_PREFIX[tf] === m[1]);
  if (!themeFid) return null;
  return { themeFamily: themeFid, family: THEME_TO_FAMILY[themeFid] || themeFid, variant: m[2].toLowerCase() };
}
const currentTheme = () => vscode.workspace.getConfiguration('workbench').get('colorTheme', '');

let palettes = null;
function loadPalettes(ctx) {
  if (!palettes) {
    try { palettes = JSON.parse(fs.readFileSync(path.join(ctx.extensionPath, 'palettes.json'), 'utf8')); }
    catch { palettes = {}; }
  }
  return palettes;
}

// ---------- gradient orbs (pixel-tuned to T3 Code screenshots) ----------
const ORBS = {
  't3-code': {
    light: `radial-gradient(circle at 32% 30%, #ffffff 0%, #f4f6fa 38%, #d8dcef 62%, #b8c4e8 100%)`,
    dark:  `radial-gradient(circle at 32% 30%, #2a3247 0%, #161a28 40%, #0b0e18 70%, #04060c 100%)`,
  },
  't3-chat': {
    light: `radial-gradient(circle at 32% 30%, #ffd6ea 0%, #ff9dc9 30%, #ec4899 60%, #a3004c 100%)`,
    dark:  `radial-gradient(circle at 32% 30%, #d1357e 0%, #8e1a4f 40%, #4a0525 75%, #1f0210 100%)`,
  },
  grove: {
    light: `radial-gradient(circle at 32% 30%, #f0fdf4 0%, #d3f3e0 30%, #69d69a 65%, #1b7d50 100%)`,
    dark:  `radial-gradient(circle at 32% 30%, #5db67e 0%, #2f7a4d 40%, #143a23 75%, #071a0f 100%)`,
  },
  ocean: {
    light: `radial-gradient(circle at 32% 30%, #f0f7fc 0%, #d4e7f5 30%, #70b9ee 65%, #2672af 100%)`,
    dark:  `radial-gradient(circle at 32% 30%, #5a9fd6 0%, #2a5d8c 40%, #12304d 75%, #060f1a 100%)`,
  },
  ember: {
    light: `radial-gradient(circle at 32% 30%, #fef3e8 0%, #fadbbf 30%, #f09a64 65%, #ae552a 100%)`,
    dark:  `radial-gradient(circle at 32% 30%, #d67c45 0%, #8a4a25 40%, #46240f 75%, #1c0e05 100%)`,
  },
  iris: {
    light: `radial-gradient(circle at 32% 30%, #f5efff 0%, #e3d5fa 30%, #b288f0 65%, #7253b9 100%)`,
    dark:  `radial-gradient(circle at 32% 30%, #9d7df2 0%, #60489c 40%, #2d2050 75%, #120a24 100%)`,
  },
};

// ---------- mini-app preview used inside System / Light / Dark scheme cards ----------
function miniApp(variant) {
  const isLight = variant === 'light';
  const col = isLight ? {
    frame: '#eef1f5', side: '#ffffff', canvas: '#f7f9fb',
    pill: '#d4dce4', line: '#c2cdd8', line2: '#d8e0e8',
    cardBg: '#ffffff', cardBorder: '#e2e8ee',
    dotOn: '#34a853',
    msgBg: '#eef2f6', msgLine: '#c2cdd8',
    toggle: '#14b8a6',
  } : {
    frame: '#131a26', side: '#1a2433', canvas: '#0d1420',
    pill: '#2c3a4d', line: '#3b4a5e', line2: '#2a3648',
    cardBg: '#1c2635', cardBorder: '#2c3a4d',
    dotOn: '#34a853',
    msgBg: '#18202e', msgLine: '#2a3648',
    toggle: '#14b8a6',
  };
  return `<div class="mini" style="background:${col.frame}">
    <div class="mn-side" style="background:${col.side}">
      <i style="background:${col.pill};width:52%"></i>
      <i style="background:${col.pill};width:74%"></i>
      <i style="background:${col.pill};width:64%"></i>
    </div>
    <div class="mn-main" style="background:${col.canvas}">
      <i class="mn-pill" style="background:${col.pill}"></i>
      <i class="mn-line" style="background:${col.line};width:52%"></i>
      <i class="mn-line" style="background:${col.line2};width:38%"></i>
      <div class="mn-card" style="background:${col.cardBg};border-color:${col.cardBorder}">
        <div class="mn-row"><b style="background:${col.dotOn}"></b><i style="background:${col.line2};width:70%"></i></div>
        <div class="mn-row"><b style="background:${col.dotOn}"></b><i style="background:${col.line2};width:55%"></i></div>
        <div class="mn-row"><b style="background:#d97706"></b><i style="background:${col.line2};width:62%"></i></div>
      </div>
      <div class="mn-msg" style="background:${col.msgBg}">
        <i style="background:${col.msgLine}"></i>
        <span class="mn-toggle" style="background:${col.toggle}"></span>
      </div>
    </div>
  </div>`;
}

function miniAppSystem() {
  return `<div class="mini system">
    <div class="half">${miniApp('light')}</div>
    <div class="half">${miniApp('dark')}</div>
  </div>`;
}

function schemeCard(id, label, activeScheme) {
  const on = id === activeScheme;
  const body = id === 'system' ? miniAppSystem() : miniApp(id);
  return `<button class="scheme${on ? ' on' : ''}" data-scheme="${id}">
    <div class="sc-frame">${body}</div>
    <div class="sc-cap">${label}</div>
  </button>`;
}

function themeCard(fid, state) {
  const on = fid === state.family;
  const label = FAMILY_LABEL[fid];
  const lightOrb = ORBS[fid].light;
  const darkOrb = ORBS[fid].dark;
  const lightOn = on && state.variant === 'light';
  const darkOn = on && state.variant === 'dark';
  const sunSvg = `<svg viewBox="0 0 16 16" width="9" height="9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="8" cy="8" r="3.2"/><path d="M8 1.5v1.6M8 12.9v1.6M14.5 8h-1.6M3.1 8H1.5M12.6 3.4l-1.1 1.1M4.5 11.5l-1.1 1.1M12.6 12.6l-1.1-1.1M4.5 4.5L3.4 3.4"/></svg>`;
  const moonSvg = `<svg viewBox="0 0 16 16" width="9" height="9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13.5 9.5A5.5 5.5 0 1 1 6.5 2.5a4.4 4.4 0 0 0 7 7z"/></svg>`;
  return `<button class="theme${on ? ' on' : ''}" data-family="${fid}">
    <div class="orbs">
      <span class="orb${lightOn ? ' on' : ''}" data-family="${fid}" data-variant="light" style="background:${lightOrb}">
        ${lightOn ? `<span class="badge">${sunSvg}</span>` : ''}
      </span>
      <span class="orb${darkOn ? ' on' : ''}" data-family="${fid}" data-variant="dark" style="background:${darkOrb}">
        ${darkOn ? `<span class="badge">${moonSvg}</span>` : ''}
      </span>
    </div>
    <div class="t-meta">
      <span class="t-name">${label}</span>
      <span class="t-act">
        <svg width="11" height="11" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="5" y="5" width="9" height="9" rx="1.5"></rect>
          <path d="M11 5V3.5A1.5 1.5 0 0 0 9.5 2H3.5A1.5 1.5 0 0 0 2 3.5v6A1.5 1.5 0 0 0 3.5 11H5"></path>
        </svg>
      </span>
    </div>
  </button>`;
}

function pickerHtml(state) {
  // read current variant's palette so the modal itself follows the active theme
  const pal = ((palettes[state.themeFamily] || {})[state.variant]) || {};
  const isLight = state.variant === 'light';
  const BG = pal.canvas || (isLight ? '#f5f7f8' : '#0b1119');
  const PANEL = pal.sidebar || (isLight ? '#ffffff' : '#121a26');
  const BORDER = pal.border || (isLight ? '#cbd5d1' : '#1a2332');
  const BORDER_HOVER = isLight ? '#94a8b8' : '#2a3a4f';
  const TEXT = pal.text || (isLight ? '#241523' : '#e6eef7');
  const MUTED = pal.sidebarMutedForeground || (isLight ? '#6b666c' : '#7b8a9c');
  const ACCENT = pal.accent || (isLight ? '#2672af' : '#4da3ff');
  const OVERLAY_BG = isLight ? 'rgba(180, 190, 200, .55)' : 'rgba(4, 8, 14, .72)';
  const SHADOW = isLight ? '0 24px 80px rgba(30, 40, 60, .18)' : '0 24px 80px rgba(0, 0, 0, .6)';

  const schemeCards = [
    schemeCard('system', 'System', state.scheme),
    schemeCard('light', 'Light', state.scheme),
    schemeCard('dark', 'Dark', state.scheme),
  ].join('');

  const themeCards = FAMILY_ORDER.map(fid => themeCard(fid, state)).join('');

  return `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; height: 100vh; overflow: hidden;
    font-family: var(--vscode-font-family, "Segoe UI", system-ui, sans-serif);
    color: ${TEXT}; font-size: 12px; background: transparent; }

  /* ---------- modal overlay ---------- */
  .overlay { position: fixed; inset: 0; background: ${OVERLAY_BG};
    backdrop-filter: blur(2px); display: flex; align-items: center; justify-content: center;
    animation: fade .12s ease; }
  @keyframes fade { from { opacity: 0 } to { opacity: 1 } }
  @keyframes pop { from { opacity: 0; transform: scale(.96) translateY(8px) }
                   to   { opacity: 1; transform: scale(1) translateY(0) } }

  /* ---------- modal card ---------- */
  .modal { width: 560px; max-width: calc(100vw - 32px); max-height: calc(100vh - 32px);
    background: ${BG}; border: 1px solid ${BORDER}; border-radius: 12px;
    box-shadow: ${SHADOW}, 0 0 0 1px rgba(255, 255, 255, .02);
    overflow: hidden; padding: 16px 18px 18px;
    animation: pop .18s cubic-bezier(.2, .9, .3, 1.2); }

  h2 { font-size: 11px; font-weight: 500; color: ${MUTED}; margin: 0 0 10px; letter-spacing: .01em; }
  section { margin-bottom: 18px; }
  section:last-child { margin-bottom: 0; }

  /* ---------- Color scheme cards ---------- */
  .schemes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .scheme { all: unset; cursor: pointer; display: block; background: ${PANEL};
    border: 1px solid ${BORDER}; border-radius: 9px; overflow: hidden;
    transition: border-color .15s ease; }
  .scheme:hover { border-color: ${BORDER_HOVER}; }
  .scheme.on { border-color: ${ACCENT}; }
  .sc-frame { aspect-ratio: 16 / 9.5; overflow: hidden; }
  .sc-cap { padding: 8px 4px 9px; text-align: center; color: ${MUTED};
    font-size: 11px; font-weight: 400; }
  .scheme.on .sc-cap { color: ${TEXT}; }

  /* ---------- mini-app preview ---------- */
  .mini { width: 100%; height: 100%; display: flex; }
  .mini.system { display: flex; }
  .mini.system .half { flex: 1; overflow: hidden; position: relative; }
  .mini.system .half .mini { position: absolute; inset: 0; width: 200%; }
  .mini.system .half:last-child .mini { left: -100%; }
  .mn-side { width: 22%; display: flex; flex-direction: column; gap: 4px;
    padding: 7px 6px; }
  .mn-side i { display: block; height: 5px; border-radius: 2.5px; }
  .mn-main { flex: 1; padding: 8px 9px; display: flex; flex-direction: column;
    gap: 5px; position: relative; }
  .mn-pill { display: block; height: 5px; width: 30%; border-radius: 2.5px;
    align-self: center; margin-bottom: 2px; }
  .mn-line { display: block; height: 5px; border-radius: 2.5px; }
  .mn-card { position: absolute; top: 7px; right: 7px; width: 32%; padding: 5px 6px;
    border: 1px solid; border-radius: 6px; display: flex; flex-direction: column; gap: 4px; }
  .mn-row { display: flex; align-items: center; gap: 4px; }
  .mn-row b { width: 3px; height: 3px; border-radius: 50%; display: block; flex-shrink: 0; }
  .mn-row i { height: 3px; border-radius: 1.5px; display: block; }
  .mn-msg { margin-top: auto; display: flex; align-items: center; gap: 6px;
    padding: 5px 7px; border-radius: 6px; }
  .mn-msg i { flex: 1; height: 4px; border-radius: 2px; display: block; }
  .mn-toggle { width: 9px; height: 9px; border-radius: 50%; display: block; flex-shrink: 0; }

  /* ---------- Themes grid ---------- */
  .themes-head { display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 12px; }
  .themes-head h2 { margin: 0; }

  .themes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .theme { all: unset; cursor: pointer; display: flex; flex-direction: column;
    background: ${PANEL}; border: 1px solid ${BORDER}; border-radius: 9px;
    padding: 14px 12px 10px; transition: border-color .15s ease; }
  .theme:hover { border-color: ${BORDER_HOVER}; }
  .theme.on { border-color: ${ACCENT}; }

  .orbs { display: flex; gap: 12px; justify-content: center; padding: 2px 0 4px; }
  .orb { position: relative; width: 36px; height: 36px; border-radius: 50%;
    display: block; cursor: pointer; }
  .orb.on::before { content: ''; position: absolute; inset: -3px; border-radius: 50%;
    border: 1.5px solid ${ACCENT}; pointer-events: none; }
  .orb .badge { position: absolute; right: -2px; bottom: -2px; width: 13px; height: 13px;
    border-radius: 50%; background: ${PANEL}; border: 1.5px solid ${ACCENT};
    display: flex; align-items: center; justify-content: center;
    color: ${ACCENT}; pointer-events: none; }
  .orb .badge svg { width: 7px; height: 7px; }

  .t-meta { display: flex; align-items: center; justify-content: space-between;
    margin-top: auto; padding-top: 4px; }
  .t-name { font-size: 11.5px; font-weight: 500; color: ${TEXT}; }
  .t-act { color: ${MUTED}; display: inline-flex; padding: 2px; border-radius: 4px; }
  .t-act svg { width: 10px; height: 10px; }
  .theme:hover .t-act { color: ${TEXT}; }
</style></head><body>
<div class="overlay" id="overlay">
  <div class="modal" id="modal">
    <section>
      <h2>Color scheme</h2>
      <div class="schemes">${schemeCards}</div>
    </section>

    <section>
      <div class="themes-head">
        <h2>Themes</h2>
      </div>
      <div class="themes">${themeCards}</div>
    </section>
  </div>
</div>
<script>
  const vscode = acquireVsCodeApi();
  document.getElementById('overlay').addEventListener('click', e => {
    if (e.target.id === 'overlay') vscode.postMessage({ type: 'close' });
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') vscode.postMessage({ type: 'close' });
  });
  document.querySelectorAll('.scheme').forEach(el =>
    el.addEventListener('click', () => vscode.postMessage({ type: 'scheme', scheme: el.dataset.scheme })));
  document.querySelectorAll('.orb').forEach(el =>
    el.addEventListener('click', e => {
      e.stopPropagation();
      vscode.postMessage({ type: 'apply', family: el.dataset.family, variant: el.dataset.variant });
    }));
  document.querySelectorAll('.theme').forEach(el =>
    el.addEventListener('click', () => vscode.postMessage({ type: 'family', family: el.dataset.family })));
</script></body></html>`;
}

function activate(context) {
  loadPalettes(context);

  const item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, -1);
  item.name = 'Prism Themes';
  item.command = 'prismThemes.openPicker';

  function refresh() {
    const t = parseTheme(currentTheme());
    if (t) {
      item.text = `$(color-mode) ${FAMILY_LABEL[t.themeFamily]} ${t.variant === 'dark' ? 'Dark' : 'Light'}`;
      item.tooltip = 'Prism Themes — 点击打开 Color scheme';
    } else {
      item.text = '$(color-mode) Prism';
      item.tooltip = 'Prism Themes — 点击打开 Color scheme';
    }
    item.show();
  }

  let panel = null;
  // lastApplied lets us render the new selection immediately, without waiting
  // for the configuration-change event to round-trip.
  let lastApplied = null;
  function currentState() {
    const cur = parseTheme(currentTheme()) || lastApplied;
    if (cur) {
      return { family: cur.family, themeFamily: cur.themeFamily, variant: cur.variant, scheme: cur.variant };
    }
    return { family: 'ocean', themeFamily: 'ocean', variant: 'dark', scheme: 'dark' };
  }
  function render() {
    if (panel) {
      panel.webview.html = pickerHtml(currentState());
      panel.title = 'Color scheme';
    }
  }

  context.subscriptions.push(
    vscode.commands.registerCommand('prismThemes.openPicker', () => {
      panel = vscode.window.createWebviewPanel('prismThemePicker', 'Color scheme',
        { viewColumn: vscode.ViewColumn.Active, preserveFocus: false }, { enableScripts: true });
      render();
      panel.webview.onDidReceiveMessage(async msg => {
        const st = currentState();
        if (msg.type === 'scheme') {
          let variant = msg.scheme;
          if (variant === 'system') {
            const isDark = vscode.window.activeColorTheme.kind === vscode.ColorThemeKind.Dark
              || vscode.window.activeColorTheme.kind === vscode.ColorThemeKind.HighContrast;
            variant = isDark ? 'dark' : 'light';
          }
          await apply(themeLabel(st.themeFamily, variant));
          lastApplied = { family: st.family, themeFamily: st.themeFamily, variant, scheme: msg.scheme };
          render();
        } else if (msg.type === 'apply') {
          const themeFid = FAMILY_TO_THEME[msg.family] || msg.family;
          await apply(themeLabel(themeFid, msg.variant));
          lastApplied = { family: msg.family, themeFamily: themeFid, variant: msg.variant, scheme: msg.variant };
          render();
        } else if (msg.type === 'family') {
          const themeFid = FAMILY_TO_THEME[msg.family] || msg.family;
          await apply(themeLabel(themeFid, st.variant));
          lastApplied = { family: msg.family, themeFamily: themeFid, variant: st.variant, scheme: st.scheme };
          render();
        } else if (msg.type === 'customize') {
          vscode.commands.executeCommand('workbench.action.openSettings', 'workbench.colorCustomizations');
        } else if (msg.type === 'quickpick') {
          panel.dispose();
          vscode.commands.executeCommand('prismThemes.quickSwitch');
        } else if (msg.type === 'close') {
          panel.dispose();
        }
      });
      panel.onDidDispose(() => { panel = null; });
    }),

    vscode.commands.registerCommand('prismThemes.quickSwitch', async () => {
      const current = currentTheme();
      const picks = [];
      const seen = new Set();
      for (const pickerFid of FAMILY_ORDER) {
        const themeFid = FAMILY_TO_THEME[pickerFid];
        if (seen.has(themeFid)) continue;
        seen.add(themeFid);
        picks.push({ kind: vscode.QuickPickItemKind.Separator, label: FAMILY_LABEL[pickerFid] });
        for (const variant of ['dark', 'light']) {
          const label = themeLabel(themeFid, variant);
          picks.push({
            label: label === current ? `$(check) ${label}` : label,
            description: variant === 'dark' ? '深色' : '浅色',
            theme: label,
          });
        }
      }
      const pick = await vscode.window.showQuickPick(picks, {
        placeHolder: `当前主题：${current || '未知'} · 选择一个 Prism 主题`, matchOnDescription: true,
      });
      if (pick && pick.theme && pick.theme !== current) await apply(pick.theme);
    }),

    item,
    vscode.workspace.onDidChangeConfiguration(e => {
      if (!e.affectsConfiguration('workbench.colorTheme')) return;
      lastApplied = null;
      refresh();
      render();
    })
  );
  refresh();
}

async function apply(label) {
  await vscode.workspace.getConfiguration('workbench')
    .update('colorTheme', label, vscode.ConfigurationTarget.Global);
}

function deactivate() {}

module.exports = { activate, deactivate };
