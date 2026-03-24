"""
ZenType — a minimal typing app for your Obsidian vault.
Requires: pip install pywebview
"""

import re
import sys
import webview
from pathlib import Path

# ─── Markdown / Obsidian stripping ───────────────────────────────────────────

def strip_markdown(text: str) -> str:
    """Convert Obsidian-flavored markdown to clean typeable text."""
    # YAML frontmatter
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)
    # Obsidian embedded files  ![[...]]
    text = re.sub(r'!\[\[.*?\]\]', '', text)
    # Obsidian wikilinks  [[Page|Alias]] → Alias, [[Page]] → Page
    text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
                  lambda m: m.group(2) or m.group(1), text)
    # Markdown images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Markdown links → just the label
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Headers → plain text (no # prefix)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Bold / italic / strikethrough
    text = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_\n]+)_{1,3}', r'\1', text)
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    # Fenced code blocks → keep code text
    text = re.sub(r'```\w*\n(.*?)```', r'\1', text, flags=re.DOTALL)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Obsidian callouts  > [!note]
    text = re.sub(r'^>\s*\[!\w+\][-+]?\s*', '', text, flags=re.MULTILINE)
    # Blockquotes → keep content
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # Horizontal rules
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    # List markers → keep content
    text = re.sub(r'^[ \t]*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*\d+[.)]\s+', '', text, flags=re.MULTILINE)
    # Obsidian tags  #tag
    text = re.sub(r'(?<!\w)#[\w/]+', '', text)
    # HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize whitespace: collapse inline spaces, normalize newlines
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Normalize paragraph breaks to double-space (for flow-style typing)
    text = re.sub(r'\n\n+', '  ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'  +', '  ', text)
    return text.strip()


def load_file(path: str) -> dict:
    """Read and clean a file, return dict with name + text."""
    p = Path(path)
    raw = p.read_text(encoding='utf-8')
    text = strip_markdown(raw)
    return {'name': p.stem, 'text': text, 'path': str(p)}


# ─── pywebview API ────────────────────────────────────────────────────────────

_window = None  # Set after window creation


class Api:
    def open_file(self):
        result = _window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=True,
            file_types=('Markdown (*.md)', 'Text (*.txt)', 'All files (*.*)')
        )
        if not result:
            return []
        out = []
        for path in result:
            try:
                f = load_file(path)
                if len(f['text']) >= 50:
                    out.append(f)
            except Exception:
                pass
        return out

    def open_folder(self):
        result = _window.create_file_dialog(webview.FOLDER_DIALOG)
        if not result:
            return []
        folder = Path(result[0])
        out = []
        for md in sorted(folder.rglob('*.md')):
            try:
                f = load_file(str(md))
                if len(f['text']) >= 50:
                    out.append(f)
            except Exception:
                pass
        # Cap at 100 files; sort by name
        return out[:100]

    def read_file_path(self, path: str):
        """Called when a file is drag-dropped into the window."""
        try:
            f = load_file(path)
            return {**f, 'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    global _window
    html_path = Path(__file__).parent / 'index.html'
    html = html_path.read_text(encoding='utf-8')

    api = Api()
    _window = webview.create_window(
        'ZenType',
        html=html,
        js_api=api,
        width=1280,
        height=800,
        min_size=(900, 600),
        background_color='#141414',
    )
    webview.start()


if __name__ == '__main__':
    main()
