
"""
ZenType — a minimal typing app: paste your text and type.
Requires: pip install pywebview
"""

import webview
from pathlib import Path


def main():
    html_path = Path(__file__).parent / 'index.html'
    html = html_path.read_text(encoding='utf-8')

    webview.create_window(
        'ZenType',
        html=html,
        width=1280,
        height=800,
        min_size=(900, 600),
        background_color='#141414',
    )
    webview.start()


if __name__ == '__main__':
    main()
