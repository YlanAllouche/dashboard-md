"""Template loading and rendering utilities"""

from pathlib import Path
from playlist_maker.templates.home_page import get_home_page_html


def load_template(filename):
    """Load HTML template file"""
    template_dir = Path(__file__).parent.parent / "html_templates"
    template_path = template_dir / filename

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_home_template(pywal_css, successful_files):
    """
    Render home page template with modular dashboard.

    Args:
        pywal_css: CSS variables from pywal
        successful_files: List of dicts with 'stem', 'title', 'count' keys

    Returns:
        Complete HTML string
    """
    return get_home_page_html(pywal_css, successful_files)


def render_unified_home_template(pywal_css, successful_collections):
    """
    Render unified home page with tabbed navigation.

    Videos are linked to separate pages, other content is embedded.

    Args:
        pywal_css: CSS variables from pywal
        successful_collections: Dict organized by content type

    Returns:
        str: Complete HTML string
    """
    from playlist_maker.templates.home_page import get_unified_home_page_html
    return get_unified_home_page_html(pywal_css, successful_collections)


def render_video_template(title, pywal_css, javascript):
    """Render video page template"""
    template = load_template("video.html")
    template = template.replace("{TITLE}", title)
    template = template.replace("{PYWAL_CSS}", pywal_css)
    template = template.replace("{JAVASCRIPT}", javascript)
    return template


def render_playlist_cards(successful_files):
    """Render playlist cards grid"""
    if not successful_files:
        return """
        <div class="empty-state">
            <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:36px;height:36px;display:inline;margin-right:8px;vertical-align:middle;"><path d="M3 12h18"/><path d="M12 3v18"/><circle cx="12" cy="12" r="10"/></svg> No Video Collections Found</h2>
            <p>Add some JSON files with video data to get started</p>
        </div>
 """

    html = '<div class="playlist-grid">'

    for file_info in successful_files:
        html += f"""
            <a href="{file_info['stem']}.html" class="playlist-card">
                <div class="playlist-title">{file_info['title']}</div>
                <div class="playlist-subtitle">Video Collection</div>
                <div class="playlist-stats">{file_info['count']} videos</div>
                <div class="playlist-button">View Collection </div>
            </a>
 """

    html += "</div>"
    return html
