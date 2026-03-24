# zentype

A minimal, keybr-inspired typing app for your Obsidian vault.

```
dark background. amber cursor. no distractions. just type.
```

## Setup

```bash
pip install pywebview
```

> **macOS**: pywebview uses WebKit natively — no extra deps.  
> **Windows**: Needs WebView2 (ships with Windows 11; install from Microsoft for older).  
> **Linux**: `sudo apt install python3-gi gir1.2-webkit2-4.0`

## Run

```bash
cd zentype
python3 main.py
```

## Usage

- **Drop** any `.md` or `.txt` file onto the window — starts immediately
- **Open file** — pick one or more markdown files via dialog
- **Open folder** — point to your Obsidian vault; picks all `.md` files (up to 100)
- **Backspace** — go back one character
- **Esc** — close modals
- **Restart** — redo current file
- **Next** — browse loaded files

## What gets stripped from your notes

The Obsidian markdown parser removes:
- YAML frontmatter (`---`)
- Wikilinks `[[Page|Alias]]` → shows alias/page name
- Embedded files `![[...]]`
- Headers, bold, italic, strikethrough (keeps the text)
- Callouts, blockquotes (keeps content)
- List markers (keeps content)
- Inline + fenced code (keeps code text)
- Obsidian tags `#topic`
- HTML tags

Paragraphs are joined into a continuous flow — no Enter key required.

## Project structure

```
zentype/
├── main.py          # Python backend + pywebview launcher
├── requirements.txt
├── README.md
└── static/
    └── index.html   # Full UI (HTML + CSS + JS, self-contained)
```

## Also works in browser

Open `static/index.html` directly in Chrome/Firefox — drag & drop works,
"open file" falls back to a browser file picker. "Open folder" requires the
desktop app.
