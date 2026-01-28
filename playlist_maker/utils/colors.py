"""Color handling and pywal integration"""

from pathlib import Path


def extract_pywal_colors():
    """Load colors from ~/.cache/wal/colors.css"""
    try:
        colors_css = Path.home() / ".cache" / "wal" / "colors.css"
        if colors_css.exists():
            with open(colors_css, "r", encoding="utf-8") as f:
                return f.read()
    except Exception:
        pass

    # Default fallback CSS
    return """
    :root {
        --wallpaper: url("None");
        --background: #1a1a2e;
        --foreground: #ffffff;
        --cursor: #ffffff;
        --color0: #000000;
        --color1: #ee5396;
        --color2: #5eca89;
        --color3: #f0c674;
        --color4: #668ee8;
        --color5: #a78bfa;
        --color6: #2dd4bf;
        --color7: #ffffff;
        --color8: #666666;
        --color9: #ee5396;
        --color10: #5eca89;
        --color11: #f0c674;
        --color12: #668ee8;
        --color13: #a78bfa;
        --color14: #2dd4bf;
        --color15: #ffffff;
    }
    """
