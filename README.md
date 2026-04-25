# 🚀 DevTerminal

[![PyPI version](https://img.shields.io/pypi/v/devterminal-cli.svg)](https://pypi.org/project/devterminal-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**DevTerminal** is an intelligent, developer-centric terminal wrapper designed to bridge the gap between Windows and Unix-like environments. Built for programmers who switch contexts frequently, it eliminates "muscle memory" errors by adapting commands in real-time.

## ✨ Key Features

- **Smart Command Adaptation:** Automatically maps Linux commands (`ls`, `cat`, `clear`, `pwd`) to Windows equivalents (`dir`, `type`, `cls`, `cd`) with optional confirmation for destructive actions.
- **Git Integration:** Real-time Git branch status directly in your prompt.
- **Live Syntax Highlighting:** Interactive coloring of commands, flags, and strings as you type.
- **Path Validation:** Fuzzy-matching suggestions for mistyped file paths or directories.
- **Persistent History:** Searchable command history saved across sessions.
- **Native Feel:** Uses standard system shells under the hood to ensure compatibility with your existing environment.

## 📥 Installation

Install DevTerminal directly from PyPI using pip:

```bash
pip install devterminal
```

## 🚀 Quick Start

Once installed, simply launch the shell by typing:

```bash
devterminal
```

## Keyboard Shortcuts

- TAB: Trigger the intelligent auto-completion engine.

- Right Arrow (→): Accept an inline suggestion (fish-style).

- Up/Down Arrows (↑/↓): Navigate through command history.

- Ctrl+C: Cancel current input.

## 🛠 Project Structure

```bash
devcli/
├── core/         # Shell logic, executor, and history management
├── completion/   # Custom auto-complete and suggestion engines
└── os_layer/     # Cross-platform adapters and detectors
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
