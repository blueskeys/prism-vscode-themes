# Prism Themes

**Prism Themes** 是一个 VS Code 主题合集。第一批收录从 [T3 Code](https://t3.dev/) 桌面应用内置主题 1:1 提取移植的 **12 套主题**（6 族 × 深/浅），附带**右下角状态栏快速切换**与 T3 风格的 Color Scheme 选择器。后续将陆续加入更多非 T3 来源的主题家族。

## 主题清单

| 族 | 深色（editor 背景） | 浅色（editor 背景） | 说明 |
|---|---|---|---|
| **T3 Ocean** | `#17212b` | `#f5f7f8` | 深海军蓝，截图同款 |
| **T3 Grove** | `#1b2821` | `#f3f7f4` | 苔绿 |
| **T3 Ember** | `#291e1a` | `#f9f7f5` | 暖褐 |
| **T3 Iris** | `#1d1929` | `#f8f7f9` | 紫罗兰 |
| **T3 Chat** | `#1f1a24` | `#fdf7fd` | T3 默认 |
| **T3 Material** | `#0F111A` | `#FAFAFA` | T3 内嵌的原版 Material Ocean / Lighter |

- 前 5 族 = **T3 界面调色板**（61 个 OKLCH 语义键逐键转换，深浅两版）负责 workbench 外观 + 侧栏/控件/终端层次，语法高亮用 T3 内嵌的 Material token 规则（82 条）。
- 第 6 族 = T3 代码查看器内嵌的原版 Material 主题，原样保留（`#0F111A` 单色 chrome）。

## 快速切换

- 状态栏**右下角**会出现 `◐ Ocean Dark` 按钮，点击弹出 12 套主题选择器（按族分组、标注深浅、当前项打勾）。
- 命令面板执行 **`Prism Themes: Quick Switch Theme`** 效果相同。
- 切换即时生效；状态栏标签会跟随任何途径的主题变更自动同步。

## 安装

上架 Marketplace 后可直接搜索 **Prism Themes** 安装，或：

```bash
code --install-extension <publisher-id>.prism-themes
```

本仓库为源码。用 VS Code 打开 `prism-themes/` 目录后 `F5` 调试预览，或：

```bash
cd prism-themes
npx @vscode/vsce package
code --install-extension prism-themes-1.0.3.vsix
```

也可以直接把 `prism-themes/` 整个目录拷到 `~/.vscode/extensions/prism-themes-1.0.3/`。

## 生成与再构建

主题 JSON 由脚本从 T3 Code 安装包（`server.asar`）提取的真实定义生成，不是目测取色：

```bash
python tools/extract_all.py       # 提取 5 族色板 + 2 套 Material 基底 → tools/data/
python tools/generate_themes.py   # 按映射表生成 12 套 themes/*.json
```

键位映射的完整说明见仓库根目录 `ocean-vscode-mapping.md`。

## 致谢与许可

- 语法 token 规则与部分编辑器内配色来自 **Material Theme**（Mattia Astorino，MIT）。
- UI 调色板（61 键 OKLCH）提取自本机安装的 T3 Code 应用，仅供个人使用；公开发布前请自行确认相关授权（见 `NOTICE`）。
