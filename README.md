# DevTerminal 2.0 🚀

**The intelligent cross-platform terminal that every developer needs.**

Fast startup • Smart error recovery • Port management • Project switching • HTTP testing • Auto-completion

[![PyPI version](https://badge.fury.io/py/devterminal.svg)](https://badge.fury.io/py/devterminal)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Why DevTerminal?](#-why-devterminal)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
  - [Basic Commands](#basic-commands)
  - [Smart Error Recovery](#1-smart-error-recovery-)
  - [Port Manager](#2-port-manager-)
  - [Project Switcher](#3-project-switcher-)
  - [HTTP Testing](#4-http-testing-)
  - [Git Shortcuts](#5-git-shortcuts-)
  - [Auto-Completion](#6-auto-completion)
- [Configuration](#-configuration)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Why DevTerminal?

**Stop switching between 10 different tools.** DevTerminal brings everything you need into one beautiful terminal:

- ✅ **Smart Error Recovery** - Auto-fixes typos (no more "command not found")
- ✅ **Port Manager** - See what's running where, kill processes instantly
- ✅ **Project Switcher** - Jump between projects in milliseconds
- ✅ **HTTP Testing** - Test APIs without leaving terminal
- ✅ **Git Integration** - Shows branch in prompt + shortcuts
- ✅ **Auto-Completion** - Intelligent command and path completion
- ✅ **Cross-Platform** - Works on Windows, Linux, and macOS
- ✅ **Lightning Fast** - Instant startup, no lag

---

## ✨ Features

### Core Features
- 🚀 **Instant startup** - No loading screens or animations
- 🎨 **Beautiful UI** - Kali Linux-style colored prompts
- 📝 **Command history** - Persistent history with search
- 🔍 **Smart completion** - Commands, paths, and fuzzy matching
- 🌿 **Git integration** - Current branch in prompt
- 💻 **Cross-platform** - Windows, Linux, macOS support

### Developer Features
- 🛠️ **Smart Error Recovery** - Auto-suggests corrections for typos
- 🔌 **Port Manager** - Monitor and manage running ports
- ⚡ **Project Switcher** - Quick navigation between projects
- 🌐 **HTTP Testing** - Built-in API testing with pretty output
- 📦 **Project Detection** - Auto-detects Node, Python, Docker, etc.
- 🔐 **Environment Support** - Auto-detects virtual environments

---

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install devterminal
```

### From Source

```bash
git clone https://github.com/code-devkmd/devterminal.git
cd devterminal
pip install -e .
```

### Requirements

- Python 3.7 or higher
- Works on Windows, Linux, and macOS

### Dependencies

All dependencies are installed automatically:
- `prompt_toolkit` - Interactive terminal
- `rich` - Beautiful output formatting
- `colorama` - Cross-platform colors
- `pygments` - Syntax highlighting
- `psutil` - Port management

---

## 🚀 Quick Start

```bash
# Install
pip install devterminal

# Run
devterminal

# You'll see:
    ██████╗ ███████╗██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
    # ... beautiful banner ...
    
user@hostname:~/projects$ _
```

**First steps:**

```bash
# Try error recovery
$ git psuh
💡 Did you mean: git push?

# Check your ports
$ ports

# Add a project
$ proj add myapp ~/projects/my-app

# Test an API
$ http localhost:3000
```

---

## 📖 Usage Guide

### Basic Commands

All standard terminal commands work:

```bash
# Navigation
cd /path/to/directory     # Change directory
cd ~                      # Go to home directory
cd -                      # Go to previous directory
pwd                       # Print working directory

# File operations
ls                        # List files (or 'll' for detailed)
mkdir folder_name         # Create directory
touch file.txt            # Create file
rm file.txt               # Remove file
cp source dest            # Copy
mv source dest            # Move

# System
clear                     # Clear screen (or cls on Windows)
exit                      # Exit terminal (or Ctrl+D)
```

---

### 1. Smart Error Recovery 🛠️

**Never struggle with typos again.**

#### How it works:
- Detects command typos automatically
- Suggests the correct command
- One-key confirmation to run

#### Examples:

```bash
# Git typos
$ git psuh origin main
❌ Command not found: git psuh
💡 Did you mean: git push?
Run this command? [Y/n]: y
→ Running: git push origin main

# Docker typos
$ dokcer ps
💡 Did you mean: docker?

# Common mistakes
$ cd..
💡 Did you mean: cd ..?

$ claer
💡 Did you mean: clear?

$ npm rnu dev
💡 Did you mean: npm run?
```

#### Supported corrections:
- Git commands: `psuh→push`, `comit→commit`, `checkotu→checkout`
- Docker: `dokcer→docker`, `docker-comopse→docker-compose`
- Common: `cd..→cd ..`, `claer→clear`, `pyhton→python`
- And many more...

---

### 2. Port Manager 🔌

**See what's running where, manage ports effortlessly.**

#### Commands:

##### Show all active ports
```bash
$ ports

┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Port   ┃ PID    ┃ Process       ┃ Status  ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 3000   │ 12345  │ node          │ LISTEN  │
│ 5432   │ 8901   │ postgres      │ LISTEN  │
│ 8080   │ 23456  │ python        │ LISTEN  │
│ 27017  │ 34567  │ mongod        │ LISTEN  │
└────────┴────────┴───────────────┴─────────┘
```

##### Filter by process name
```bash
$ ports node

┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Port   ┃ PID    ┃ Process       ┃ Status  ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 3000   │ 12345  │ node          │ LISTEN  │
│ 3001   │ 12346  │ node          │ LISTEN  │
└────────┴────────┴───────────────┴─────────┘
```

##### Kill process on port
```bash
$ kill-port 3000

Found: node (PID: 12345) on port 3000
Kill this process? [y/N]: y
✓ Killed process on port 3000
```

#### Use cases:
- **"Port already in use"** errors → `kill-port 3000`
- **What's running?** → `ports`
- **Kill all Node processes** → `ports node` then kill each
- **Before starting dev server** → Check and clear ports

---

### 3. Project Switcher ⚡

**Jump between projects instantly with context.**

#### Commands:

##### Add a project
```bash
# Add current directory
$ proj add webapp
✓ Project 'webapp' saved

# Add specific path
$ proj add api ~/work/api-server
✓ Project 'api' saved

$ proj add mobile /Users/dev/projects/mobile-app
✓ Project 'mobile' saved
```

##### List all projects
```bash
$ proj list

┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Name    ┃ Type   ┃ Path                        ┃ Git     ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ webapp  │ node   │ ~/projects/webapp           │ main    │
│ api     │ python │ ~/work/api-server           │ develop │
│ mobile  │ node   │ /Users/dev/projects/mobile  │ feature │
└─────────┴────────┴─────────────────────────────┴─────────┘
```

##### Switch to a project
```bash
$ proj webapp

→ Switching to: webapp
Path: ~/projects/webapp
Type: node
Branch: main
💡 Virtual environment detected

# You're now in the webapp directory!
user@hostname:~/projects/webapp$
```

##### Remove a project
```bash
$ proj remove mobile
✓ Project 'mobile' removed
```

#### Auto-detection features:
- **Project type**: Node, Python, Rust, Go, Java, Ruby, PHP
- **Git branch**: Current branch if it's a git repo
- **Virtual env**: Detects venv, .venv, env folders
- **Last accessed**: Tracks when you last used it

#### Use cases:
- **Client projects**: `proj client-a`, `proj client-b`
- **Work/Personal**: `proj work-api`, `proj side-project`
- **Microservices**: `proj frontend`, `proj backend`, `proj admin`
- **Quick context switch**: Jump and see git branch + env immediately

---

### 4. HTTP Testing 🌐

**Test APIs without leaving your terminal.**

#### Commands:

##### GET Request
```bash
$ http localhost:3000/api/users

GET http://localhost:3000/api/users
Status: 200 OK

╭──────────────────────── Response Headers ────────────────────────╮
│ Content-Type        application/json; charset=utf-8              │
│ Content-Length      156                                          │
│ Date                Mon, 15 Jan 2024 10:30:00 GMT                │
╰──────────────────────────────────────────────────────────────────╯

╭──────────────────────── Response Body ───────────────────────────╮
│ [                                                                │
│   {                                                              │
│     "id": 1,                                                     │
│     "name": "John Doe",                                          │
│     "email": "john@example.com"                                  │
│   },                                                             │
│   {                                                              │
│     "id": 2,                                                     │
│     "name": "Jane Smith",                                        │
│     "email": "jane@example.com"                                  │
│   }                                                              │
│ ]                                                                │
╰──────────────────────────────────────────────────────────────────╯
```

##### POST Request
```bash
$ post localhost:3000/api/users '{"name":"Alice","email":"alice@test.com"}'

POST http://localhost:3000/api/users
Status: 201 Created

╭──────────────────────── Response Body ───────────────────────────╮
│ {                                                                │
│   "id": 3,                                                       │
│   "name": "Alice",                                               │
│   "email": "alice@test.com",                                     │
│   "created_at": "2024-01-15T10:30:00Z"                           │
│ }                                                                │
╰──────────────────────────────────────────────────────────────────╯
```

##### Headers Only
```bash
$ headers google.com

HEAD http://google.com
Status: 200

Server                  gws
Content-Type            text/html; charset=ISO-8859-1
Cache-Control           private, max-age=0
X-Frame-Options         SAMEORIGIN
```

#### Features:
- ✅ **Beautiful JSON formatting** with syntax highlighting
- ✅ **Auto HTTP/HTTPS** - Adds `http://` if missing
- ✅ **Color-coded status** - Green (2xx), Yellow (3xx), Red (4xx/5xx)
- ✅ **Works with localhost** and external APIs
- ✅ **Shows headers and body**

#### Use cases:
- **API development**: Quick endpoint testing
- **Debugging**: Check API responses
- **Server health**: `http localhost:3000/health`
- **Webhooks testing**: Test POST endpoints
- **API exploration**: Try new endpoints

---

### 5. Git Shortcuts 🌿

**Pre-configured Git aliases for faster workflow.**

```bash
# Git shortcuts (built-in)
$ gs                    # git status
$ ga                    # git add .
$ gc "message"          # git commit -m "message"
$ gp                    # git push
$ gl                    # git log --oneline
$ gd                    # git diff

# Regular git commands still work
$ git checkout -b feature
$ git merge main
$ git pull origin develop
```

#### Git branch in prompt:
```bash
# When in a git repo, branch shows in prompt
user@hostname:~/projects/webapp (main)$ 

# Color-coded branch indicator
user@hostname:~/api (develop)$ 
```

---

### 6. Auto-Completion

**Smart command and path completion.**

#### How to use:
- Press **Tab** to see completions
- Press **Right Arrow** to accept suggestion
- Type and get fuzzy matches

#### Command completion:
```bash
$ gi<TAB>
git

$ doc<TAB>
docker

$ np<TAB>
npm
```

#### Path completion:
```bash
$ cd pro<TAB>
projects/

$ cd projects/my<TAB>
projects/my-app/
projects/my-website/

# Case-insensitive fuzzy matching
$ cd MYapp<TAB>
my-app/
```

#### Features:
- ✅ Command name completion
- ✅ File and directory completion
- ✅ Case-insensitive matching
- ✅ Fuzzy matching fallback
- ✅ Shows file type metadata

---

## ⚙️ Configuration

Configuration file: `devcli/config.py`

### Customize Colors

```python
# Prompt colors
PROMPT_USER_COLOR = "ansigreen"     # User@host color
PROMPT_PATH_COLOR = "ansiblue"      # Directory color
PROMPT_GIT_COLOR = "cyan"           # Git branch color

# Available colors:
# ansigreen, ansiblue, ansired, ansiyellow, 
# ansicyan, ansimagenta, ansiwhite
```

### Customize Prompt Symbol

```python
PROMPT_SYMBOL_UNIX = "$"      # Unix/Linux/Mac
PROMPT_SYMBOL_WINDOWS = ">"   # Windows
```

### Add Custom Aliases

```python
COMMAND_ALIASES = {
    # Your custom shortcuts
    "mycommand": ["full", "command", "here"],
    "deploy": ["npm", "run", "deploy"],
    "test": ["pytest", "-v"],
}
```

### Toggle Features

```python
SHOW_BANNER = True              # Show startup banner
SHOW_GIT_BRANCH = True          # Show git branch in prompt
COMPRESS_HOME_DIR = True        # Show ~ instead of /home/user
COMPLETE_WHILE_TYPING = False   # Auto-complete as you type
```

### Add Folder Descriptions

```python
FOLDER_DESCRIPTIONS = {
    'api': 'API endpoints',
    'tests': 'Test suite',
    'docs': 'Documentation',
    'scripts': 'Build scripts',
}
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Tab** | Show completions |
| **Right Arrow** | Accept auto-suggestion |
| **Ctrl + R** | Search command history |
| **Ctrl + C** | Cancel current line |
| **Ctrl + D** | Exit terminal |
| **Ctrl + L** | Clear screen |
| **Up/Down** | Navigate history |

---

## 💡 Examples

### Daily Workflow Example

```bash
# Start your day
$ devterminal

# Check what's running
$ ports

# Switch to your project
$ proj webapp

# See current status
$ gs

# Start dev server (after killing old one)
$ kill-port 3000
$ npm run dev

# Test your API
$ http localhost:3000/api/health

# Make changes, commit
$ ga
$ gc "Add new feature"
$ gp
```

### Project Setup Example

```bash
# Add all your projects once
$ proj add frontend ~/work/frontend
$ proj add backend ~/work/backend
$ proj add mobile ~/personal/mobile-app

# Now switch instantly
$ proj frontend
$ proj backend
$ proj mobile

# List them anytime
$ proj list
```

### API Testing Example

```bash
# Test GET
$ http localhost:3000/api/users

# Test POST
$ post localhost:3000/api/users '{"name":"Test User"}'

# Check headers
$ headers api.example.com

# Test with external API
$ http jsonplaceholder.typicode.com/users/1
```

### Port Management Example

```bash
# See all ports
$ ports

# Find what Node is using
$ ports node

# Kill the blocker
$ kill-port 3000

# Verify it's gone
$ ports
```

---

## 🐛 Troubleshooting

### DevTerminal won't start

```bash
# Reinstall dependencies
pip install --upgrade devterminal

# Or from source
pip install -e . --force-reinstall
```

### Auto-completion not working

```bash
# Check config
cat devcli/config.py | grep COMPLETE_WHILE_TYPING

# Try pressing Tab twice instead of once
```

### Git branch not showing

```bash
# Make sure you're in a git repo
git status

# Check config
# In config.py, set:
SHOW_GIT_BRANCH = True
```

### Port manager showing nothing

```bash
# On Linux, you might need sudo
sudo devterminal

# Or check if psutil is installed
pip install psutil
```

### Import errors

```bash
# Install all dependencies
pip install prompt_toolkit rich colorama pygments psutil
```

### Slow startup

DevTerminal 2.0 has instant startup! If it's slow:
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Reinstall
pip uninstall devterminal
pip install devterminal
```

---

## 🤝 Contributing

We love contributions! Here's how:

### Report Bugs
Open an issue with:
- What you expected
- What happened
- Steps to reproduce
- Your OS and Python version

### Request Features
Open an issue describing:
- The feature
- Why it's useful
- Example usage

### Submit Code
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Clone
git clone https://github.com/yourusername/devterminal.git
cd devterminal

# Install in development mode
pip install -e .

# Make changes
# Test
python -m devcli.main

# Format code
black devcli/

# Submit PR
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

Built with these amazing libraries:
- [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interactive CLI
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output
- [Pygments](https://pygments.org/) - Syntax highlighting
- [psutil](https://github.com/giampaolo/psutil) - Process management
- [Colorama](https://github.com/tartley/colorama) - Cross-platform colors

---

## 📮 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/devterminal/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/devterminal/discussions)
- 📧 **Email**: your.email@example.com

---

## 🚀 What's Next?

Upcoming features:
- 🎥 Session recording and replay
- 📋 Smart clipboard manager
- 🗄️ Database quick connect
- 🤖 AI command helper
- 🔐 Secrets manager
- 📊 Command analytics

---

**Made with ❤️ by developers, for developers.**

**Star ⭐ this repo if DevTerminal makes your life easier!**