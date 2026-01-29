"""Home page template with modular dashboard and sidebar components."""

try:
    from .dashboard_widgets import (
        get_initiatives_table_widget,
        get_dashboard_widget,
        get_progress_widget,
    )
    from .playlists_sidebar import (
        get_playlists_sidebar_header,
        get_playlist_row,
        get_playlists_sidebar_footer,
    )
    from ..utils.dashboard_styles import get_dashboard_css
    from ..utils.widget_generators import WidgetDataGenerator
except ImportError:
    # Fallback for development/testing
    from dashboard_widgets import (
        get_initiatives_table_widget,
        get_dashboard_widget,
        get_progress_widget,
    )
    from playlists_sidebar import (
        get_playlists_sidebar_header,
        get_playlist_row,
        get_playlists_sidebar_footer,
    )
    from dashboard_styles import get_dashboard_css
    from widget_generators import WidgetDataGenerator


def get_home_page_header(pywal_css):
    """Generate the home page header with styles."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 14 4-4'/%3E%3Cpath d='M3.34 19a10 10 0 1 1 17.32 0'/%3E%3C/svg%3E">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
    <style>
        {pywal_css}

        :root {{
            --bg-light: #f8f7f4;
            --bg-cream: #f1efea;
            --bg-paper: #ffffff;
            --bg-dark: #1a1a1a;
            --bg-dark-elevated: #2a2a2a;
            --bg-dark-surface: #1e1e1e;
            --border-light: rgba(0, 0, 0, 0.06);
            --border-medium: rgba(0, 0, 0, 0.1);
            --border-dark: rgba(255, 255, 255, 0.08);
            --accent-primary: #c9a227;
            --accent-secondary: #2d6a4f;
            --accent-tertiary: #6b4c9a;
            --accent-quaternary: #c23645;
            --accent-success: #2d8b6b;
            --text-dark-primary: #1a1a1a;
            --text-dark-secondary: #4a4a4a;
            --text-dark-muted: #6b6b6b;
            --text-light-primary: #f8f7f4;
            --text-light-secondary: #d4d3d0;
            --text-light-muted: #a8a6a0;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Source Sans Pro', sans-serif;
            background: linear-gradient(180deg, var(--bg-cream) 0%, var(--bg-light) 100%);
            color: var(--text-dark-primary);
            line-height: 1.6;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            opacity: 0.5;
            background:
                radial-gradient(circle at 15% 30%, rgba(45, 106, 79, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 85% 70%, rgba(201, 162, 39, 0.02) 0%, transparent 50%);
            z-index: 0;
        }}

        .page-header {{
            text-align: center;
            padding: 4rem 3rem;
            background: var(--bg-paper);
            position: relative;
            overflow: hidden;
            border-radius: 2px;
            margin-bottom: 2rem;
            border: 1px solid var(--border-light);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .page-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-tertiary) 100%);
        }}

        .page-header h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--text-dark-primary);
            letter-spacing: -0.02em;
            position: relative;
        }}

        .page-header p {{
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.875rem;
            color: var(--text-dark-secondary);
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-weight: 500;
            position: relative;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Source Sans Pro', sans-serif;
            background: var(--bg-light);
            color: var(--text-dark-primary);
            line-height: 1.6;
            position: relative;
            overflow-x: hidden;
            min-height: 100vh;
        }}

        .page-header {{
            text-align: center;
            padding: 4rem 3rem;
            background: var(--bg-card);
            position: relative;
            overflow: hidden;
            border-radius: 16px;
            margin-bottom: 2rem;
        }}

        .page-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(232, 196, 124, 0.08) 0%, transparent 60%);
            animation: rotate 20s linear infinite;
        }}

        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}

        .page-header h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            position: relative;
        }}

        .page-header p {{
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.875rem;
            color: var(--text-secondary);
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-weight: 500;
            position: relative;
        }}

        {get_dashboard_css()}

        @media (max-width: 768px) {{
            .page-header {{
                padding: 2.5rem 1.5rem;
            }}

            .page-header h1 {{
                font-size: 2rem;
            }}

            .page-header p {{
                font-size: 0.75rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="page-header">
        <h1>Dashboard</h1>
        <p>Your personal dashboard and playlist manager</p>
    </div>

    <div class="main-layout">
        <div class="main-content">
"""


def get_dashboard_tabs():
    """Generate the tab navigation for dashboard widgets."""
    return """
            <div class="dashboard-tabs">
                <button class="tab-btn active" data-tab="initiatives-widget">
                    Initiatives
                </button>
                <button class="tab-btn" data-tab="dashboard-widget">
                    Dashboard
                </button>
                <button class="tab-btn" data-tab="progress-widget">
                    Progress
                </button>
            </div>
"""


def get_dashboard_widgets_html():
    """Generate all dashboard widgets."""
    return f"""
            {get_initiatives_table_widget()}
            {get_dashboard_widget()}
            {get_progress_widget()}
"""


def get_playlists_sidebar_html(successful_files):
    """
    Generate the playlists sidebar with playlist list.
    
    Args:
        successful_files: List of dicts with 'stem', 'title', 'count' keys
    
    Returns:
        HTML string for the playlists sidebar
    """
    if not successful_files:
        return f"""
        <div class="sidebar">
            {get_playlists_sidebar_header()}
            <div style="color: var(--color6); text-align: center; padding: 1rem;">
                <p>No playlists available</p>
            </div>
        </div>
        """
    
    html = f"""
        <div class="sidebar">
            {get_playlists_sidebar_header()}
"""
    
    for file_info in successful_files:
        link = f"{file_info['stem']}.html"
        name = file_info['title']
        count = file_info['count']
        html += get_playlist_row(name, count, link)
    
    html += f"""
            {get_playlists_sidebar_footer()}
"""
    
    return html


def get_home_page_footer():
    """Generate the home page footer with script includes."""
    return """
        </div>
        <script src="dashboard.js"></script>
    </div>
</body>
</html>
"""


def get_home_page_html(pywal_css, successful_files):
    """
    Generate the complete home page HTML.
    
    Assembles all modular components into a cohesive layout with:
    - Dashboard widgets in tabs (main content)
    - Playlists sidebar (right side)
    
    Populates widget placeholders with actual data from JSON files.
    
    Args:
        pywal_css: CSS variables from pywal
        successful_files: List of successfully processed playlist files
    
    Returns:
        Complete HTML string with populated widgets
    """
    # Generate widget data from JSON files
    try:
        widget_generator = WidgetDataGenerator()
        replacements = widget_generator.get_replacement_dict()
    except Exception as e:
        print(f"Warning: Could not generate widget data: {e}")
        # Use empty placeholders if data generation fails
        replacements = {
            '{INITIATIVES_FOCUS}': '<span class="empty">No data</span>',
            '{INITIATIVES_ACTIVE}': '<span class="empty">No data</span>',
            '{INITIATIVES_PLANNED}': '<span class="empty">No data</span>',
            '{DASHBOARD_TODO_FOCUS}': '<span class="empty">No data</span>',
            '{DASHBOARD_TODO_ACTIVE}': '<span class="empty">No data</span>',
            '{DASHBOARD_MIND_FOCUS}': '<span class="empty">No data</span>',
            '{DASHBOARD_MIND_ACTIVE}': '<span class="empty">No data</span>',
            '{PROGRESS_FOCUS_PROGRESS}': '<span class="empty">No data</span>',
            '{PROGRESS_FOCUS_ASYNC}': '<span class="empty">No data</span>',
            '{PROGRESS_ACTIVE_PROGRESS}': '<span class="empty">No data</span>',
            '{PROGRESS_ACTIVE_ASYNC}': '<span class="empty">No data</span>',
        }
    
    # Build HTML
    html = (
        get_home_page_header(pywal_css)
        + get_dashboard_tabs()
        + get_dashboard_widgets_html()
        + get_playlists_sidebar_html(successful_files)
        + get_home_page_footer()
    )
    
    # Replace placeholders with actual data
    for placeholder, content in replacements.items():
        html = html.replace(placeholder, content)

    return html


def get_unified_home_page_html(pywal_css, successful_collections):
    """
    Generate complete unified home page HTML.

    Args:
        pywal_css: CSS variables from pywal
        successful_collections: Dict with collections by type

    Returns:
        str: Complete HTML
    """
    from .data_row import (
        render_task_collection,
        render_calendar_collection,
        render_project_collection,
        render_notes_collection,
        get_table_styles
    )
    from .unified_page_js import get_unified_page_javascript

    tabs_html = _build_tabs_html(successful_collections)
    video_links_html = _build_video_links_html(successful_collections.get("video", []))
    task_subtabs_html = _build_sub_tabs_html(successful_collections.get("task", []), "task")
    project_subtabs_html = _build_sub_tabs_html(successful_collections.get("project", []), "project")
    calendar_subtabs_html = _build_sub_tabs_html(successful_collections.get("calendar", []), "calendar")
    notes_subtabs_html = _build_sub_tabs_html(successful_collections.get("notes", []), "notes")

    embedded_content = {}
    embedded_content["tasks"] = "\n".join([
        render_task_collection(coll, idx == 0)
        for idx, coll in enumerate(successful_collections.get("task", []))
    ])

    embedded_content["calendar"] = "\n".join([
        render_calendar_collection(coll, idx == 0)
        for idx, coll in enumerate(successful_collections.get("calendar", []))
    ])

    embedded_content["projects"] = "\n".join([
        render_project_collection(coll, idx == 0)
        for idx, coll in enumerate(successful_collections.get("project", []))
    ])

    embedded_content["notes"] = "\n".join([
        render_notes_collection(coll, idx == 0)
        for idx, coll in enumerate(successful_collections.get("notes", []))
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 14 4-4'/%3E%3Cpath d='M3.34 19a10 10 0 1 1 17.32 0'/%3E%3C/svg%3E">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
    <style>
        {pywal_css}

        :root {{
            --bg-light: #f8f7f4;
            --bg-cream: #f1efea;
            --bg-paper: #ffffff;
            --bg-dark: #1a1a1a;
            --bg-dark-elevated: #2a2a2a;
            --bg-dark-surface: #1e1e1e;
            --border-light: rgba(0, 0, 0, 0.06);
            --border-medium: rgba(0, 0, 0, 0.1);
            --border-dark: rgba(255, 255, 255, 0.08);
            --accent-primary: #c9a227;
            --accent-secondary: #2d6a4f;
            --accent-tertiary: #6b4c9a;
            --accent-quaternary: #c23645;
            --accent-success: #2d8b6b;
            --text-dark-primary: #1a1a1a;
            --text-dark-secondary: #4a4a4a;
            --text-dark-muted: #6b6b6b;
            --text-light-primary: #f8f7f4;
            --text-light-secondary: #d4d3d0;
            --text-light-muted: #a8a6a0;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
 
        body {{
            font-family: 'Source Sans Pro', sans-serif;
            background: var(--bg-light);
            color: var(--text-dark-primary);
            line-height: 1.6;
            position: relative;
            overflow-x: hidden;
            min-height: 100vh;
        }}

        .tabs {{
            display: flex;
            gap: 0.25rem;
            padding: 0.625rem;
            background: var(--bg-paper);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            margin-bottom: 1.5rem;
            overflow-x: auto;
            align-items: center;
            position: relative;
            z-index: 1;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }}

        .refresh-button {{
            margin-left: auto;
            padding: 0.625rem;
            background: transparent;
            color: var(--text-dark-muted);
            border: 1px solid var(--border-light);
            border-radius: 2px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .refresh-button:hover {{
            color: var(--accent-primary);
            border-color: var(--border-medium);
            background: var(--bg-light);
        }}

        .tab-button {{
            padding: 0.75rem 1.5rem;
            background: transparent;
            color: var(--text-dark-muted);
            border: none;
            border-radius: 2px;
            cursor: pointer;
            font-size: 0.8125rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-family: 'Source Sans Pro', sans-serif;
            white-space: nowrap;
        }}

        .tab-button:hover {{
            color: var(--text-dark-primary);
            background: var(--bg-light);
        }}

        .tab-button.active {{
            background: var(--bg-dark);
            color: var(--text-light-primary);
        }}

        .sub-tabs {{
            display: flex;
            gap: 0.25rem;
            padding: 0.5rem 1rem 0 1rem;
            background: var(--bg-paper);
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 1.5rem;
            border-radius: 4px 4px 0 0;
        }}

        .sub-tab-button {{
            padding: 0.625rem 1.25rem;
            background: var(--bg-light);
            color: var(--text-dark-secondary);
            border: 1px solid var(--border-light);
            border-radius: 2px;
            cursor: pointer;
            font-size: 0.8125rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Source Sans Pro', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .sub-tab-button:hover {{
            color: var(--text-dark-primary);
            background: var(--bg-cream);
            border-color: var(--border-medium);
        }}

        .sub-tab-button.active {{
            color: var(--text-light-primary);
            background: var(--bg-dark);
            border-color: var(--bg-dark);
            box-shadow: 0 2px 8px rgba(26, 26, 26, 0.15);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
            position: relative;
            z-index: 1;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
            animation: fadeSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes fadeSlideIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .collection {{
            display: none;
            margin-bottom: 3rem;
        }}

        .collection.active {{
            display: block;
        }}

        .collection h3 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: var(--text-dark-primary);
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-light);
            letter-spacing: -0.01em;
            position: relative;
        }}

        .collection h3::after {{
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 60px;
            height: 2px;
            background: var(--accent-primary);
        }}

        .empty-message {{
            text-align: center;
            padding: 3rem 2rem;
            color: var(--text-dark-muted);
            font-style: italic;
            font-size: 0.9375rem;
        }}

        /* Video links */
        .collection-links {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }}

        .collection-link {{
            display: block;
            padding: 1.75rem;
            background: var(--bg-paper);
            border: 1px solid var(--border-light);
            border-radius: 2px;
            text-decoration: none;
            color: var(--text-dark-primary);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        }}

        .collection-link::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .collection-link:hover {{
            border-color: var(--border-medium);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}

        .collection-link:hover::before {{
            opacity: 1;
        }}

        .collection-title {{
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            font-family: 'Playfair Display', serif;
            color: var(--text-dark-primary);
        }}

        .collection-count {{
            color: var(--text-dark-muted);
            font-size: 0.8125rem;
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Video fragment styles */
        #video-fragment-container .header {{
            text-align: center;
            margin-bottom: 2.5rem;
            position: relative;
        }}

        #video-fragment-container .header h1 {{
            font-family: 'Playfair Display', serif;
            color: var(--text-dark-primary);
            font-size: 2.75rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }}

        #video-fragment-container .header p {{
            color: var(--text-dark-secondary);
            font-size: 0.9375rem;
            font-weight: 300;
        }}

        #video-fragment-container .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 1.75rem;
        }}

        #video-fragment-container .video-card {{
            background: var(--bg-paper);
            border-radius: 2px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
            border: 1px solid var(--border-light);
            position: relative;
        }}

        #video-fragment-container .video-card:hover {{
            border-color: var(--border-medium);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}

        #video-fragment-container .thumbnail-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            overflow: hidden;
            background: var(--bg-dark-surface);
            cursor: pointer;
        }}

        #video-fragment-container .thumbnail {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        #video-fragment-container .video-card:hover .thumbnail {{
            transform: scale(1.05);
        }}

        #video-fragment-container .duration-badge {{
            position: absolute;
            bottom: 12px;
            right: 12px;
            background: var(--bg-dark);
            color: var(--text-light-primary);
            padding: 0.375rem 0.75rem;
            border-radius: 2px;
            font-size: 0.75rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
            border: 1px solid var(--border-dark);
            font-family: 'JetBrains Mono', monospace;
        }}

        #video-fragment-container .card-content {{
            padding: 1.25rem;
        }}

        #video-fragment-container .video-title {{
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-dark-primary);
            margin-bottom: 0.75rem;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        #video-fragment-container .video-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 0.8125rem;
            color: var(--text-dark-muted);
        }}

        #video-fragment-container .channel-name {{
            font-weight: 500;
            color: var(--text-dark-secondary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        #video-fragment-container .channel-name svg {{
            width: 14px;
            height: 14px;
            color: var(--text-dark-muted);
        }}

        #video-fragment-container .video-date {{
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            gap: 4px;
            font-family: 'JetBrains Mono', monospace;
        }}

        #video-fragment-container .action-buttons {{
            display: flex;
            gap: 0.625rem;
            margin-bottom: 1rem;
        }}

        #video-fragment-container .btn {{
            flex: 1;
            padding: 0.625rem 0.875rem;
            border: 1px solid var(--border-light);
            border-radius: 2px;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            text-decoration: none;
            background: transparent;
            color: var(--text-dark-muted);
            font-family: 'Source Sans Pro', sans-serif;
        }}

        #video-fragment-container .btn svg {{
            width: 14px;
            height: 14px;
        }}

        #video-fragment-container .btn-inbox {{
            background: transparent;
            color: var(--text-dark-muted);
            border: 1px solid var(--border-light);
        }}

        #video-fragment-container .btn-inbox:hover {{
            border-color: var(--border-medium);
            color: var(--text-dark-primary);
            background: var(--bg-light);
        }}

        #video-fragment-container .btn-inbox.active {{
            background: var(--bg-dark);
            border-color: var(--bg-dark);
            color: var(--text-light-primary);
            box-shadow: 0 2px 8px rgba(26, 26, 26, 0.2);
        }}

        #video-fragment-container .btn-watched {{
            background: transparent;
            color: var(--text-dark-muted);
            border: 1px solid var(--border-light);
        }}

        #video-fragment-container .btn-watched:hover {{
            border-color: var(--border-medium);
            color: var(--text-dark-primary);
            background: var(--bg-light);
        }}

        #video-fragment-container .btn-watched.active {{
            background: linear-gradient(135deg, var(--accent-success) 0%, #247a5d 100%);
            border-color: var(--accent-success);
            color: var(--bg-paper);
            box-shadow: 0 2px 8px rgba(45, 139, 107, 0.25);
        }}

        #video-fragment-container .watched-indicator {{
            position: absolute;
            top: 12px;
            left: 12px;
            width: 10px;
            height: 10px;
            background: var(--accent-success);
            border: 2px solid var(--bg-paper);
            border-radius: 50%;
            opacity: 0;
            transition: opacity 0.2s;
            box-shadow: 0 2px 6px rgba(45, 139, 107, 0.3);
        }}

        #video-fragment-container .video-card.watched .watched-indicator {{
            opacity: 1;
        }}

        #video-fragment-container .starred-button {{
            position: absolute;
            top: 12px;
            right: 12px;
            width: 40px;
            height: 40px;
            background: var(--bg-paper);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-light);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
        }}

        #video-fragment-container .starred-button:hover {{
            border-color: var(--accent-quaternary);
            transform: scale(1.1);
        }}

        #video-fragment-container .starred-button.active {{
            color: var(--accent-quaternary);
            border-color: var(--accent-quaternary);
            box-shadow: 0 4px 12px rgba(194, 54, 69, 0.2);
        }}

        #video-fragment-container .starred-button.inactive {{
            color: var(--text-dark-muted);
        }}

        #video-fragment-container .starred-button svg {{
            width: 20px;
            height: 20px;
        }}

        #video-fragment-container .placeholder-thumbnail {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            background: linear-gradient(135deg, var(--bg-dark-surface) 0%, var(--bg-dark-elevated) 100%);
            color: var(--text-dark-muted);
        }}

        #video-fragment-container .tag-toggles {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
            margin-top: 0.75rem;
        }}

        #video-fragment-container .tag-toggle {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            padding: 0.25rem 0.5rem;
            border-radius: 2px;
            font-size: 1.25rem;
            font-weight: 400;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--border-light);
            background: var(--bg-light);
            color: var(--text-dark-secondary);
            line-height: 1;
        }}

        #video-fragment-container .tag-toggle:hover {{
            border-color: var(--border-medium);
            color: var(--text-dark-primary);
            background: var(--bg-cream);
        }}

        #video-fragment-container .tag-toggle.active {{
            background: linear-gradient(135deg, var(--accent-secondary) 0%, #245e44 100%);
            border-color: var(--accent-secondary);
            color: var(--bg-paper);
            box-shadow: 0 2px 6px rgba(45, 106, 79, 0.25);
        }}

        #video-fragment-container .tag-toggle.inactive {{
            background: var(--bg-light);
            border: 1px solid var(--border-light);
            color: var(--text-dark-secondary);
        }}

        #video-fragment-container .stats {{
            margin-bottom: 2rem;
            text-align: center;
            color: var(--text-dark-secondary);
            font-size: 0.9375rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
        }}

        {get_table_styles()}

        @media (max-width: 768px) {{
            .tabs {{
                flex-wrap: wrap;
                padding: 0.5rem;
            }}

            .container {{
                padding: 1rem 0.75rem;
            }}

            #video-fragment-container .header h1 {{
                font-size: 2rem;
            }}

            #video-fragment-container .video-grid {{
                grid-template-columns: 1fr;
                gap: 1.25rem;
            }}

            .collection-links {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="tabs">
        {tabs_html}
        <button id="refresh-btn" class="refresh-button" title="Refresh all data">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-rotate-ccw-icon lucide-rotate-ccw"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
        </button>
    </div>

    <div class="container">
        <div class="tab-content active" id="videos-content">
            <div id="video-list-container">
                {video_links_html if video_links_html else '<div class="empty-message">No video collections found</div>'}
            </div>
            <div id="video-fragment-container" style="display: none;">
                <!-- Video fragment content will be rendered here -->
            </div>
        </div>

        <div class="tab-content" id="tasks-content">
            <div class="sub-tabs" id="tasks-subtabs">
                {task_subtabs_html if task_subtabs_html else ''}
            </div>
            {embedded_content["tasks"] if embedded_content["tasks"] else '<div class="empty-message">No tasks found</div>'}
        </div>

        <div class="tab-content" id="calendar-content">
            <div class="sub-tabs" id="calendar-subtabs">
                {calendar_subtabs_html if calendar_subtabs_html else ''}
            </div>
            {embedded_content["calendar"] if embedded_content["calendar"] else '<div class="empty-message">No calendar events found</div>'}
        </div>

        <div class="tab-content" id="projects-content">
            <div class="sub-tabs" id="projects-subtabs">
                {project_subtabs_html if project_subtabs_html else ''}
            </div>
            {embedded_content["projects"] if embedded_content["projects"] else '<div class="empty-message">No projects found</div>'}
        </div>

        <div class="tab-content" id="notes-content">
            <div class="sub-tabs" id="notes-subtabs">
                {notes_subtabs_html if notes_subtabs_html else ''}
            </div>
            {embedded_content["notes"] if embedded_content["notes"] else '<div class="empty-message">No notes found</div>'}
        </div>
    </div>

    <script>
        {get_unified_page_javascript()}
     </script>
</body>
</html>"""


def _build_tabs_html(successful_collections):
    """Build tab buttons HTML."""
    tabs = []

    video_count = len(successful_collections.get("video", []))
    tabs.append(f'''
    <button class="tab-button active" data-tab="videos">
        Videos ({video_count})
    </button>''')

    task_count = len(successful_collections.get("task", []))
    if task_count > 0:
        tabs.append(f'''
    <button class="tab-button" data-tab="tasks">
        Tasks ({task_count})
    </button>''')

    calendar_count = len(successful_collections.get("calendar", []))
    if calendar_count > 0:
        tabs.append(f'''
    <button class="tab-button" data-tab="calendar">
        Calendar ({calendar_count})
    </button>''')

    project_count = len(successful_collections.get("project", []))
    if project_count > 0:
        tabs.append(f'''
    <button class="tab-button" data-tab="projects">
        Projects ({project_count})
    </button>''')

    notes_count = len(successful_collections.get("notes", []))
    if notes_count > 0:
        tabs.append(f'''
    <button class="tab-button" data-tab="notes">
        Notes ({notes_count})
    </button>''')

    return "\n".join(tabs)


def _build_video_links_html(video_collections):
    """Build video collection links HTML."""
    if not video_collections:
        return ""

    links = []
    for collection in video_collections:
        title = collection['title']
        # Remove " Videos" suffix if present
        if title.endswith(' Videos'):
            title = title[:-7]

        links.append(f'''
        <a href="#" data-video-url="{collection['stem']}.html" class="collection-link video-link">
            <div class="collection-title">{title}</div>
            <div class="collection-count">{collection['count']} videos</div>
        </a>''')

    return f'<div class="collection-links">\n' + "\n".join(links) + '\n</div>'


def _build_sub_tabs_html(collections, content_type):
    """Build sub-tab buttons HTML for tasks or projects."""
    if not collections:
        return ""

    tabs = []
    for idx, collection in enumerate(collections):
        if idx == 0:
            tabs.append(f'''
        <button class="sub-tab-button active" data-subtab="{collection['stem']}" data-type="{content_type}">
            {collection['title']}
        </button>''')
        else:
            tabs.append(f'''
        <button class="sub-tab-button" data-subtab="{collection['stem']}" data-type="{content_type}">
            {collection['title']}
        </button>''')

    return "\n".join(tabs)