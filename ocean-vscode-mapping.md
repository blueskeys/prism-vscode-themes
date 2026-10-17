# T3 Code「Ocean」→ VS Code 主题复刻映射表

> 交付物：chrome 层 61 个语义键 → VS Code workbench 键的完整映射。
> 状态：**分析文档，未生成主题**。路线建议：C（chrome 层用 T3 调色板 + 语法层用内嵌 Material Theme Ocean），先做 dark。

## 1. 数据来源与验证

| 内容 | 位置 | 形态 |
|---|---|---|
| T3 界面调色板（chrome 层） | `server.asar` 内主题对象 `{id:\`ocean\`,label:\`Ocean\`,appearance:\`light\`,colors:{…},variants:{dark:{…}},sidebarArtwork:!0}` | 根 `colors` = light 值，`variants.dark` = dark 全量覆盖，共 **61 键**，全部 OKLCH |
| 窗口 chrome（每主题 4 键） | `server.asar` 内 pretty 结构 `ocean:{light:{background,foreground,accent,chrome},dark:{…}}` | OKLCH |
| 语法层 | `server.asar` 内嵌完整 VS Code 主题 `material-theme-ocean`（chunk `material-theme-ocean-CHQ94UKr.js`） | `type:dark`，**214 colors + 82 tokenColors + 16 terminal ANSI**，`editor.background #0F111A` |

验证：dark `canvas` 的 `oklch(0.242641 0.024125 250.573)` 按标准 OKLab 矩阵转 sRGB = **`#17212b`**，与截图主背景（占第一张图 71%）逐位吻合；同一转换矩阵处理的窗口 chrome 组也得到 `#17212b`，交叉验证通过。

另一个佐证方向：T3 内部存在"以 VS Code 主题的 `editor.background` 为种子推导调色板"的构建函数（报错文案：*"That VS Code theme has no editor.background color, so there is nothing to build a palette from"*），但 5 套内置主题（t3-chat / grove / ocean / ember / iris）的 OKLCH 值是**静态定义**，不是运行时推导。复刻其余 4 套主题 = 换一份 palette 输入，结构完全相同。

提取脚本与中间产物（本仓库）：
- `.tmp/extract_ocean3.py` — 从 asar 定位 Ocean 对象、解析、OKLCH→hex 转换
- `.tmp/ocean_palette.json` — 61 键 light+dark 完整色板（hex + 原始 OKLCH）
- `.tmp/material_theme_ocean.json` — 语法层完整主题 JSON

## 2. 完整色板（61 键，dark + light 对照）

| T3 键 | dark | light | 语义 |
|---|---|---|---|
| canvas | `#17212b` | `#f5f7f8` | 主画布背景 |
| chrome | `#17212b` | `#f5f7f8` | 窗口框架 |
| toolbar | `#17212b` | `#f5f7f8` | 顶部工具条背景 |
| toolbarForeground | `#fffaff` | `#241523` | 工具条文字 |
| toolbarBorder | `#36566f` | `#d8e4ee` | 工具条描边 |
| toolbarControl | `#293f52` | `#e4ecf2` | 工具条控件底 |
| toolbarControlForeground | `#fffaff` | `#241523` | 工具条控件文字 |
| toolbarControlHover | `#324e66` | `#d8e4ee` | 工具条控件 hover |
| surface | `#17212b` | `#f5f7f8` | 通用面（状态区） |
| surfaceRaised | `#333b45` | `#edeff1` | 浮起面（弹层/挂件） |
| surfaceOverlay | `#414851` | `#e8e9eb` | 更高层浮面 |
| text | `#fffaff` | `#241523` | 主文字 |
| textMuted | `#8d8f97` | `#746c75` | 次要文字 |
| border | `#405567` | `#cdd4dc` | 通用描边 |
| input | `#4f677b` | `#c0c9d4` | 输入控件底 |
| focus | `#70b9ee` | `#2672af` | 焦点环 |
| accent | `#70b9ee` | `#2672af` | 强调色（蓝） |
| accentForeground | `#241523` | `#fffaff` | 强调色上的文字（深字浅底） |
| secondary | `#293f52` | `#e4ecf2` | 次级按钮底 |
| secondaryForeground | `#fffaff` | `#241523` | 次级按钮文字 |
| muted | `#233544` | `#e8eff4` | 静默控件底 |
| mutedForeground | `#969ca6` | `#6f6873` | 静默文字（行号级） |
| placeholder | `#a4a4ac` | `#716972` | 占位符 |
| secondaryLabel | `#8d8f97` | `#746c75` | 次级标签（=textMuted） |
| iconMuted | `#8d8f97` | `#746c75` | 静默图标（=textMuted） |
| error | `#fb414a` | `#fb2c36` | 错误 |
| errorForeground | `#ff6467` | `#c10007` | 错误文字 |
| errorSurface | `#3c2630` | `#f5e6e9` | 错误底色 |
| warning | `#fe9a00` | `#fe9a00` | 警告 |
| warningForeground | `#ffb900` | `#b74b00` | 警告文字 |
| warningSurface | `#3c3424` | `#f6efe4` | 警告底色 |
| update | `#70b9ee` | `#2672af` | 信息/更新（=accent） |
| updateForeground | `#a2d2f4` | `#194a72` | 信息文字（亮 accent） |
| updateSurface | `#345269` | `#d4e1ed` | 信息底色 |
| accentSurface | `#324e66` | `#d8e4ee` | 强调底（选中焦点行） |
| accentSurfaceForeground | `#fffaff` | `#241523` | 强调底文字 |
| messageSurface | `#375871` | `#d0dfeb` | 消息/通知底 |
| messageForeground | `#fffaff` | `#241523` | 消息文字 |
| messageAction | `#5bd0d6` | `#0a6f75` | 消息动作/链接（青） |
| messageActionForeground | `#241523` | `#fffaff` | 动作按钮文字 |
| messageActionHover | `#6fd6db` | `#096267` | 动作 hover |
| codeBackground | `#252e38` | `#f0f1f3` | 内嵌代码块底 |
| codeForeground | `#fffaff` | `#241523` | 内嵌代码文字 |
| searchMatchBackground | `#8c6c1f` | `#ffde8b` | 搜索匹配（暗金） |
| searchMatchForeground | `#f5f5f5` | `#21180a` | 搜索匹配文字 |
| searchMatchActiveBackground | `#eea52b` | `#eea52b` | 当前匹配（亮橙） |
| searchMatchActiveForeground | `#21180a` | `#21180a` | 当前匹配文字 |
| sidebar | `#1e2d3b` | `#e4ecf2` | 侧栏底 |
| sidebarForeground | `#fffaff` | `#241523` | 侧栏文字 |
| sidebarMutedForeground | `#989ca5` | `#6c6570` | 侧栏静默文字 |
| sidebarControlSurface | `#424e5a` | `#d5dbe2` | 侧栏控件/分节头 |
| sidebarRowHover | `#283e50` | `#cdddea` | 侧栏行 hover |
| sidebarRowActive | `#2f495f` | `#bed4e5` | 侧栏行按下/焦点 |
| sidebarRowSelected | `#324f66` | `#b7cfe2` | 侧栏行选中 |
| sidebarBorder | `#6d757f` | `#cdd2d9` | 侧栏描边 |
| terminalBackground | `#17212b` | `#f5f7f8` | 终端底（=canvas） |
| terminalForeground | `#fffaff` | `#241523` | 终端文字（=text） |
| terminalCursor | `#70b9ee` | `#2672af` | 终端光标（=accent） |
| terminalSelection | `#36566f` | `#d0dfeb` | 终端选区 |
| terminalScrollbar | `#797c84` | `#c7c5c9` | 滚动条 |
| terminalScrollbarHover | `#9798a0` | `#b2aeb4` | 滚动条 hover |

窗口 chrome（dark）：background/chrome `#17212b`、foreground `#fffaff`、accent `#70b9ee`。light：`#f5f7f8` / `#241523` / `#2672af`。

## 3. 映射表：VS Code workbench 键 ← T3 键

按 VS Code 区域组织；写主题 JSON 时照此填值。**无标注 = 直接对应；〔判断〕= 多对一中我的取舍，可调**。

### 3.1 全局基础
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `foreground` | text `#fffaff` |
| `descriptionForeground` | textMuted `#8d8f97` |
| `focusBorder` | focus `#70b9ee` |
| `border` | border `#405567` |
| `selection.background` | terminalSelection `#36566f`〔判断：+`80` alpha〕 |
| `widget.shadow` | —〔手调：`#00000080`，T3 无阴影键〕 |

### 3.2 标题栏 / 编辑器组 / 标签
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `titleBar.activeBackground` / `titleBar.inactiveBackground` | chrome `#17212b` |
| `titleBar.activeForeground` | toolbarForeground `#fffaff` |
| `titleBar.inactiveForeground` | textMuted `#8d8f97` |
| `titleBar.border` | toolbarBorder `#36566f` |
| `editorGroupHeader.tabsBackground` | toolbar `#17212b` |
| `editorGroupHeader.tabsBorder` | toolbarBorder `#36566f` |
| `editorGroup.border` / `editorGroup.dropBackground` | toolbarBorder `#36566f` / accentSurface〔判断〕 |
| `editorGroup.emptyBackground` | canvas `#17212b` |
| `tab.activeBackground` | canvas `#17212b`〔判断：与编辑器同色，T3 标签融进画布〕 |
| `tab.activeForeground` | text `#fffaff` |
| `tab.activeBorderTop` | accent `#70b9ee`〔判断：Material 风顶边〕 |
| `tab.inactiveBackground` | toolbar `#17212b` |
| `tab.inactiveForeground` | textMuted `#8d8f97`〔判断：toolbarForeground 纯白过亮〕 |
| `tab.hoverBackground` | sidebarRowHover `#283e50`〔判断〕 |
| `tab.unfocusedActiveForeground` | textMuted `#8d8f97` |

### 3.3 编辑器
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `editor.background` | **canvas `#17212b`**（核心决策，见 §5） |
| `editor.foreground` | text `#fffaff` |
| `editorLineNumber.foreground` | mutedForeground `#969ca6` |
| `editorLineNumber.activeForeground` | text `#fffaff` |
| `editorCursor.foreground` | terminalCursor `#70b9ee` |
| `editor.selectionBackground` | terminalSelection `#36566f` |
| `editor.inactiveSelectionBackground` | muted `#233544` |
| `editor.selectionHighlightBackground` | terminalSelection + `40` alpha〔判断〕 |
| `editor.findMatchBackground` / `findMatchForeground` | searchMatchActiveBackground `#eea52b` / searchMatchActiveForeground `#21180a`（当前匹配=亮橙） |
| `editor.findMatchHighlightBackground` / `findMatchHighlightForeground` | searchMatchBackground `#8c6c1f` / searchMatchForeground `#f5f5f5`（其余匹配=暗金） |
| `editor.lineHighlightBackground` | muted `#233544`〔判断：可改不设〕 |
| `editorCodeLens.foreground` | secondaryLabel `#8d8f97` |
| `editorGhostText.foreground` | placeholder `#a4a4ac` |
| `editorWidget.background` / `editorSuggestWidget.background` / `editorHoverWidget.background` / `quickInput.background` / `debugToolBar.background` | surfaceRaised `#333b45` |
| `editorWidget.border` / `editorSuggestWidget.border` / `editorHoverWidget.border` | border `#405567` |
| `editorSuggestWidget.selectedBackground` | sidebarRowSelected `#324f66`〔判断〕 |
| `keybindingLabel.background` | surfaceOverlay `#414851` |
| `keybindingLabel.foreground` | text `#fffaff` |
| `keybindingLabel.border` / `keybindingLabel.bottomBorder` | border `#405567` |
| `editorInlayHint.background` | codeBackground `#252e38`〔判断〕 |
| `editorInlayHint.foreground` | textMuted `#8d8f97` |

### 3.4 侧栏 / 活动栏 / 列表
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `sideBar.background` / `activityBar.background` | sidebar `#1e2d3b` |
| `sideBar.foreground` / `sideBarTitle.foreground` / `activityBar.foreground` | sidebarForeground `#fffaff` |
| `sideBar.border` / `activityBar.border` | sidebarBorder `#6d757f` |
| `activityBar.inactiveForeground` | sidebarMutedForeground `#989ca5` |
| `activityBarBadge.background` | accent `#70b9ee` |
| `activityBarBadge.foreground` | accentForeground `#241523` |
| `sideBarSectionHeader.background` | sidebarControlSurface `#424e5a` |
| `sideBarSectionHeader.foreground` | sidebarForeground `#fffaff` |
| `list.hoverBackground` | sidebarRowHover `#283e50` |
| `list.focusBackground` | sidebarRowActive `#2f495f` |
| `list.activeSelectionBackground` / `list.inactiveSelectionBackground` | sidebarRowSelected `#324f66` |
| `list.activeSelectionForeground` / `list.inactiveSelectionForeground` | sidebarForeground `#fffaff` |
| `list.focusOutline` | focus `#70b9ee` |
| `quickInputList.focusBackground` | accentSurface `#324e66` |
| `quickInputList.focusForeground` | accentSurfaceForeground `#fffaff` |
| `list.errorForeground` / `list.warningForeground` | error `#fb414a` / warning `#fe9a00` |

### 3.5 按钮 / 输入 / 下拉 / 菜单
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `button.background` | accent `#70b9ee` |
| `button.foreground` | accentForeground `#241523` |
| `button.hoverBackground` | updateForeground `#a2d2f4`〔判断：同色相亮一档〕 |
| `button.secondaryBackground` | secondary `#293f52` |
| `button.secondaryForeground` | secondaryForeground `#fffaff` |
| `button.secondaryHoverBackground` | accentSurface `#324e66`〔判断〕 |
| `input.background` / `dropdown.background` | input `#4f677b` |
| `input.foreground` / `dropdown.foreground` | text `#fffaff` |
| `input.border` / `dropdown.border` | border `#405567`〔判断：可不设走无边框〕 |
| `input.placeholderForeground` | placeholder `#a4a4ac` |
| `inputOption.activeBorder` | focus `#70b9ee` |
| `dropdown.listBackground` | surfaceRaised `#333b45` |
| `checkbox.background` | input `#4f677b`〔判断〕 |
| `checkbox.border` | border `#405567` |
| `checkbox.foreground` | text `#fffaff` |
| `menu.background` | toolbarControl `#293f52` |
| `menu.foreground` | toolbarControlForeground `#fffaff` |
| `menu.selectionBackground` / `menubar.selectionBackground` | toolbarControlHover `#324e66` |
| `menu.selectionForeground` / `menubar.selectionForeground` | toolbarControlForeground `#fffaff` |
| `menu.separatorBackground` | border `#405567` |
| `toolbar.hoverBackground` | toolbarControl `#293f52` |
| `toolbar.hoverForeground` | toolbarControlForeground `#fffaff` |
| `toolbar.activeBackground` | toolbarControlHover `#324e66` |
| `progressBar.background` | accent `#70b9ee` |

### 3.6 输入校验 / 错误警告信息
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `inputValidation.errorBackground` / `errorBorder` / `errorForeground` | errorSurface `#3c2630` / error `#fb414a` / errorForeground `#ff6467` |
| `inputValidation.warningBackground` / `warningBorder` / `warningForeground` | warningSurface `#3c3424` / warning `#fe9a00` / warningForeground `#ffb900` |
| `inputValidation.infoBackground` / `infoBorder` / `infoForeground` | updateSurface `#345269` / update `#70b9ee` / updateForeground `#a2d2f4` |
| `editorError.foreground` | error `#fb414a` |
| `editorWarning.foreground` | warning `#fe9a00` |
| `editorInfo.foreground` | update `#70b9ee` |

### 3.7 通知 / 链接 / 内嵌代码
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `notifications.background` | messageSurface `#375871` |
| `notifications.foreground` | messageForeground `#fffaff` |
| `notifications.border` | border `#405567` |
| `notificationCenterHeader.background` | surfaceRaised `#333b45` |
| `notificationCenterHeader.foreground` | messageForeground `#fffaff` |
| `notificationsErrorIconForeground` | error `#fb414a` |
| `notificationsWarningIconForeground` | warning `#fe9a00` |
| `notificationsInfoIconForeground` | update `#70b9ee` |
| `notificationLink.foreground` / `textLink.foreground` | messageAction `#5bd0d6`〔判断：T3 的链接/动作是青色而非蓝〕 |
| `textLink.activeForeground` | messageActionHover `#6fd6db` |
| `textCodeBlock.background` | codeBackground `#252e38` |
| `textPreformat.foreground` | codeForeground `#fffaff` |
| `textBlockQuote.background` | surfaceRaised `#333b45`〔判断〕 |

### 3.8 终端 / 滚动条 / 状态栏 / minimap
| VS Code 键 | ← T3 键（dark 值） |
|---|---|
| `terminal.background` | terminalBackground `#17212b`（=canvas，一致性 ✓） |
| `terminal.foreground` | terminalForeground `#fffaff` |
| `terminalCursor.foreground` | terminalCursor `#70b9ee` |
| `terminal.selectionBackground` | terminalSelection `#36566f` |
| `terminal.border` | border `#405567` |
| `terminal.ansi*`（16 色） | 语法层 Material Ocean，见 §6 |
| `scrollbarSlider.background` | terminalScrollbar `#797c84` |
| `scrollbarSlider.hoverBackground` | terminalScrollbarHover `#9798a0` |
| `scrollbarSlider.activeBackground` | terminalScrollbarHover `#9798a0`〔T3 无第三档〕 |
| `minimap.background` | canvas `#17212b` |
| `minimapSlider.background` / `hoverBackground` | terminalScrollbar + alpha〔判断〕 |
| `statusBar.background` / `statusBar.noFolderBackground` | surface `#17212b` |
| `statusBar.foreground` | text `#fffaff` |
| `statusBar.border` | border `#405567` |
| `statusBar.debuggingBackground` | updateSurface `#345269`〔判断〕 |
| `statusBarItem.hoverBackground` | sidebarRowHover `#283e50`〔判断〕 |
| `statusBarItem.remoteBackground` | updateSurface `#345269`〔判断〕 |
| `breadcrumb.background` | canvas `#17212b` |
| `breadcrumb.foreground` | mutedForeground `#969ca6`〔判断〕 |
| `breadcrumb.focusForeground` / `activeSelectionForeground` | text `#fffaff` |

### 3.9 T3 键覆盖核对
61 键全部落位。仅 1 个键无 1:1 归宿：**messageActionForeground**（VS Code 通知按钮复用 `button.*`，无独立键；留作 `quickInputList.focusForeground` 备选）。iconMuted 与 sidebarMutedForeground 色值几乎相同（`#8d8f97` vs `#989ca5`），可互换。

### 3.10 必须手调的缺口（T3 无对应）
| 内容 | 建议 |
|---|---|
| 阴影类（`widget.shadow` 等） | `#00000080` 起步手调 |
| `gitDecoration.*` | 取语法层色：untracked/added `#C3E88D`、modified `#FFCB6B`、deleted `#f07178`、conflicted/branch `#F78C6C`、stageModified `#82AAFF` |
| `charts.*` | red←error、blue←accent、green←`#C3E88D`、yellow←warning、orange←`#F78C6C`、purple←`#C792EA`、foreground←text、lines←textMuted |
| `editorIndentGuide.*` / `editorWhitespace` | border/textMuted 加低 alpha |
| `merge.*` / `diffEditor.*` | Material 原值（`#64d3892c` / `#dd50742c` 系）照搬 |
| `symbolIcon.*` / `debug.*` / `testing.*` | 首版不设，吃默认；迭代再加 |

## 4. 语法层（路线 C 的第二层）

内嵌 `material-theme-ocean` 已完整导出为 `.tmp/material_theme_ocean.json`（214 + 82 + 16），token 前景色共 14 个：

| 色值 | 用途（按 token 数） |
|---|---|
| `#f07178` ×18 | 红：关键字/标签/常量 |
| `#89DDFF` ×12 | 青：属性/操作符/单位 |
| `#babed8` ×10 | 灰白：默认前景/变量 |
| `#FFCB6B` ×10 | 黄：函数/类名/参数 |
| `#82AAFF` ×7 | 蓝：变量/数字 |
| `#C3E88D` ×5 | 绿：字符串 |
| `#F78C6C` ×5 | 橙：标签/属性名 |
| `#C792EA` ×4 | 紫：关键字/控制流 |
| `#ff9cac` ×3 | 粉：重音 token |
| `#464B5D` ×3 | 暗灰：注释/行号级 |
| `#B2CCD6` ×1、`#babed890` ×1、`#916b53` ×1 | 零星 |

终端 16 ANSI：black `#000000`、red `#f07178`、green `#C3E88D`、yellow `#FFCB6B`、blue `#82AAFF`、magenta `#C792EA`、cyan `#89DDFF`、white `#ffffff`；bright 同色系（brightBlack `#464B5D`、brightWhite `#ffffff`，其余与普通档同值）。

**重要观察**：Material Ocean 自带的 workbench 色几乎全色单色——`sideBar/activityBar/statusBar/titleBar/tab/list` 的背景清一色 `#0F111A`。截图里的层次感（侧栏 `#1e2d3b`、按钮蓝、青色链接）**全部来自 chrome 层**。这直接支持路线 C 的做法：workbench 部分整体换成 §3 的映射，Material JSON 只保留 `tokenColors` + `terminal.ansi*` + 少量编辑器内色（如 `editor.selectionBackground #717CB450`、`editor.wordHighlight*`、`diffEditor.*`、`editorBracketMatch*` 等微调色）。

## 5. `editor.background` 决策点

| 选项 | 值 | 效果 |
|---|---|---|
| **A（推荐）** | `#17212b`（chrome canvas） | 整窗统一深海军蓝，与截图观感一致；T3 自己的终端背景也是 canvas（先例）。token 色在 `#0F111A` 上标定，`#17212b` 仅亮一档（OKLCH L 0.243 vs 0.21），对比度无碍 |
| B | `#0F111A`（Material 原值） | 语法层 100% 原汁，但编辑器与侧栏（`#1e2d3b`）之间会出现近黑断层，不像截图 |

## 6. 许可证

语法层是 **Material Theme**（Mattia Astorino，MIT）。T3 的 asar 内未附带它的独立 LICENSE 文件；对外发布复刻主题前，需在上游仓库（Material Theme 官方源）确认许可并在 README 署名。T3 自身的 UI 调色板（61 键）属于 T3 Code 应用本身——个人使用无虞，公开发布需再评估。

## 7. 下一步

1. 拍板路线（建议 C）与范围（建议先 dark-only，主题名 `T3 Ocean Dark`）。
2. 生成最小扩展：`package.json`（`contributes.themes`）+ `themes/t3-ocean-dark.json`（§3 映射 + §4 tokenColors/ANSI 合成）。数据都在 `.tmp/*.json`，可脚本化合成，改完 F5 即时预览。
3. light 变体：色板已在手（§2 light 列），需要时按同一映射再出一份 `T3 Ocean Light`。
4. 其余 4 套主题（Grove/Ember/Iris/T3 Chat）同流程换色板即可。
