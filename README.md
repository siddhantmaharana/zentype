# zentype

A minimal typing app for practicing with your own text — copy something, paste it in, and type. Modeled on the reading/typing experience of [Typersguild](https://typersguild.com), scoped down to a local, single-user, single-file app.

## Features

- **Continuous-scroll reader** — type through a document paragraph by paragraph, like reading a book. Completed paragraphs stay on screen with their stats frozen beneath them (`⚡ wpm · ⊘ accuracy · 🏆 xp`); upcoming text stays visible, dimmed, ahead of the cursor.
- **Section detection** — markdown headers or short standalone lines (`CHAPTER II`, `What is a GPT model?`) are recognized as section breaks, shown inline in the flow, and award a small XP bonus just for reaching them.
- **Floating toolbar** — prev/next section, table of contents, a Quick Settings drawer, a Focus Sounds ambient noise generator, Zen Mode, and restart.
- **XP & progress** — every paragraph and header earns XP; a session XP counter lives in the top bar alongside live WPM/accuracy/time.
- **Autosave & resume** — progress is saved per-paragraph to `localStorage`, keyed by document content. Reopen the same file later and it resumes exactly where you left off.
- **Training controls** (Quick Settings) — Ignore Capitalization, Stop on Error, Auto Skip Symbols, and Training Mode (backtrack N words on a mistake).
- **Typing sounds** — synthesized mechanical-click and error-buzz feedback (no bundled audio files), toggle and volumes in Quick Settings.
- **Explicit pause** — press `Esc` to freeze the timer and dim the text; any key or click resumes without being typed. Idle for 5s and it auto-pauses the same way, but the next keystroke resumes and counts normally.
- **Paste to start** — copy any text and `Ctrl+V` on the welcome screen; dropping a `.txt`/`.md` file works too.
- **Font size control** — adjust font size (A− / A+) from the top bar or Quick Settings.
- **Markdown stripping** — headings, bold, links, code blocks, Obsidian wikilinks, and tags are stripped so you type plain prose; headers are kept as section markers rather than discarded.

## Usage

### Browser
1. Open `index.html` in Chrome or Firefox
2. Copy some text, then press `Ctrl+V` (or drag & drop a `.txt`/`.md` file)
3. Start typing — the current paragraph is highlighted; finish it to move to the next

### Desktop app
```bash
pip install -r requirements.txt
python3 main.py
```

## Deploy

Static file, no build step, no backend — GitHub Pages serves `index.html` as-is.

1. Push `main` to GitHub (`origin` is already `github.com/siddhantmaharana/zentype`)
2. Repo → **Settings → Pages** → Source: **Deploy from a branch** → Branch: `main`, folder `/ (root)` → **Save**
3. Live at `https://siddhantmaharana.github.io/zentype/` within a minute or two

Progress still lives in the browser's `localStorage`, just scoped to that URL instead of a local `file://` path — more reliably persistent across sessions than `file://` storage, but still per-browser, per-device, with no account and no cross-device sync (that would need a backend — see [Not in this build](#not-in-this-build)). The desktop app (`python3 main.py`) works the same regardless of whether Pages is enabled.

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Backspace` | Delete last character |
| `Esc` | Pause / close an open drawer |
| `Ctrl+V` | Paste text (welcome screen only) |

Click the **zentype** wordmark any time to return to the paste screen.

## Stats

- **WPM** — words per minute for the current paragraph, calculated on correctly typed characters only
- **Accuracy** — correct characters ÷ total keystrokes (including backspace corrections), per paragraph
- **XP** — awarded per completed paragraph (scaled to length and accuracy) and per section header reached
- **Time** — active typing time for the current paragraph; idle and paused periods excluded

## Not in this build

Document library/dashboard, full Settings page, theme picker, multiple sound-pack choices (one synthesized click/error sound each, not a curated pack picker), on-screen keyboard visualizer, vocabulary collection, digraph mistake analysis, PDF/EPUB/DOCX ingestion, and any account/sync backend (progress stays local to each browser) are cut from this pass — see `v2_0.md` for the full spec this is scoped down from.

## Changelog

### 2026-08-31 — Typer view rewrite
- Continuous-scroll, paragraph-by-paragraph reader replaces fixed pagination
- Section detection with inline headers, floating toolbar (TOC, Quick Settings, Focus Sounds, Zen Mode, restart)
- Per-paragraph XP scoring; progress autosaves and resumes via `localStorage`
- Explicit pause (`Esc`) and idle auto-pause now share one timing mechanism
- Training controls: Ignore Capitalization, Stop on Error, Auto Skip Symbols, backtrack-on-error
- Synthesized typing-click and error-buzz sounds (Web Audio, no bundled assets), volumes in Quick Settings
- Removed: Reading Mode, the page/result-screen modal, and the open file/open folder buttons + native file dialogs — paste (or drag & drop) is now the only way in, and `main.py` no longer needs a JS↔Python API at all
- Removed: bottom button bar; restart moved into the floating toolbar, and the wordmark now doubles as a "back to paste screen" button
- Removed: per-document Notes drawer

### 2026-04-01 — Fonts & reading mode
- Brighter font colors
- Reading mode toggle (scrollable, non-typing view)

### 2026-03-24 — Basic app
- Drag-and-drop `.txt`/`.md` files, paginated navigation
- Live WPM/accuracy/timer
- Known issues at the time: timer never paused, rendering size was inconsistent, no persisted progress
