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
    <style>
        {pywal_css}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--background);
            color: var(--foreground);
            line-height: 1.6;
            min-height: 100vh;
        }}

        .page-header {{
            text-align: center;
            padding: 2rem 1rem;
            border-bottom: 2px solid var(--color7);
            background: var(--color8);
        }}

        .page-header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .page-header p {{
            font-size: 1rem;
            opacity: 0.8;
        }}

        {get_dashboard_css()}

        @media (max-width: 768px) {{
            .page-header h1 {{
                font-size: 1.8rem;
            }}

            .page-header p {{
                font-size: 0.9rem;
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
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap">
    <style>
        {pywal_css}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--background);
            color: var(--foreground);
            line-height: 1.6;
        }}

        .tabs {{
            display: flex;
            gap: 0.5rem;
            padding: 1rem;
            background: var(--color8);
            border-bottom: 1px solid var(--color7);
            overflow-x: auto;
            align-items: center;
        }}

        .refresh-button {{
            margin-left: auto;
            padding: 0.5rem;
            background: transparent;
            color: var(--foreground);
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .refresh-button:hover {{
            color: var(--color4);
        }}

        .tab-button {{
            padding: 0.75rem 1.5rem;
            background: var(--color0);
            color: var(--foreground);
            border: 1px solid var(--color7);
            border-radius: 0;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .tab-button:hover {{
            border-color: var(--color4);
        }}

        .tab-button.active {{
            background: var(--color4);
            color: var(--color0);
            border-color: var(--color4);
        }}

        .sub-tabs {{
            display: flex;
            gap: 0.5rem;
            padding: 0.5rem 1rem 0 1rem;
            background: var(--color0);
            border-bottom: 1px solid var(--color7);
            margin-bottom: 1rem;
        }}

        .sub-tab-button {{
            padding: 0.5rem 1rem;
            background: transparent;
            color: var(--foreground);
            border: none;
            border-radius: 0;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .sub-tab-button:hover {{
            color: var(--color4);
        }}

        .sub-tab-button.active {{
            color: var(--color4);
            border-bottom: 2px solid var(--color4);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        .collection {{
            display: none;
            margin-bottom: 3rem;
        }}

        .collection.active {{
            display: block;
        }}

        .collection h3 {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--foreground);
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--color7);
        }}

        .empty-message {{
            text-align: center;
            padding: 2rem;
            opacity: 0.7;
        }}

        /* Video links */
        .collection-links {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }}

        .collection-link {{
            display: block;
            padding: 1.5rem;
            background: var(--color0);
            border: 1px solid var(--color7);
            border-radius: 0;
            text-decoration: none;
            color: var(--foreground);
            transition: all 0.2s;
        }}

        .collection-link:hover {{
            border-color: var(--color4);
        }}

        .collection-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}

        .collection-count {{
            opacity: 0.7;
            font-size: 0.9rem;
        }}

        /* Video fragment styles */
        #video-fragment-container .header {{
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
        }}

        #video-fragment-container .header h1 {{
            color: var(--foreground);
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        #video-fragment-container .header p {{
            color: var(--color7);
            font-size: 1.1rem;
        }}

        #video-fragment-container .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.5rem;
        }}

        #video-fragment-container .video-card {{
            background: var(--color0);
            border-radius: 0;
            box-shadow: none;
            transition: all 0.2s;
            overflow: hidden;
            border: 1px solid var(--color7);
        }}

        #video-fragment-container .video-card:hover {{
            border-color: var(--color4);
        }}

        #video-fragment-container .thumbnail-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            overflow: hidden;
            background: var(--color8);
            cursor: pointer;
        }}

        #video-fragment-container .thumbnail {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }}

        #video-fragment-container .video-card:hover .thumbnail {{
            transform: scale(1.05);
        }}

        #video-fragment-container .duration-badge {{
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: var(--color0);
            color: var(--foreground);
            padding: 4px 8px;
            border-radius: 0;
            font-size: 0.75rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 3px;
            border: 1px solid var(--color7);
        }}

        #video-fragment-container .card-content {{
            padding: 1rem;
        }}

        #video-fragment-container .video-title {{
            font-size: 1rem;
            font-weight: 600;
            color: var(--foreground);
            margin-bottom: 0.5rem;
            line-height: 1.4;
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
            font-size: 0.875rem;
            color: var(--color7);
        }}

        #video-fragment-container .channel-name {{
            font-weight: 500;
            color: var(--color7);
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        #video-fragment-container .video-date {{
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        #video-fragment-container .action-buttons {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

        #video-fragment-container .btn {{
            flex: 1;
            padding: 0.5rem 0.75rem;
            border: 1px solid var(--color7);
            border-radius: 0;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.025em;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            text-decoration: none;
            background: var(--color0);
            color: var(--foreground);
        }}

        #video-fragment-container .btn-inbox {{
            background: var(--color0);
            color: var(--foreground);
            border: 1px solid var(--color7);
        }}

        #video-fragment-container .btn-inbox:hover {{
            border-color: var(--color4);
        }}

        #video-fragment-container .btn-inbox.active {{
            background: var(--color4);
            color: var(--color0);
            border-color: var(--color4);
        }}

        #video-fragment-container .btn-watched {{
            background: var(--color0);
            color: var(--foreground);
            border: 1px solid var(--color7);
        }}

        #video-fragment-container .btn-watched:hover {{
            border-color: var(--color2);
        }}

        #video-fragment-container .btn-watched.active {{
            background: var(--color2);
            color: var(--color0);
            border-color: var(--color2);
        }}

        #video-fragment-container .watched-indicator {{
            position: absolute;
            top: 8px;
            left: 8px;
            width: 12px;
            height: 12px;
            background: var(--color2);
            border: 2px solid var(--color0);
            border-radius: 50%;
            opacity: 0;
            transition: opacity 0.2s;
        }}

        #video-fragment-container .video-card.watched .watched-indicator {{
            opacity: 1;
        }}

        #video-fragment-container .starred-button {{
            position: absolute;
            top: 8px;
            right: 8px;
            width: 40px;
            height: 40px;
            background: var(--color0);
            border: 2px solid var(--color7);
            border-radius: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            box-shadow: none;
        }}

        #video-fragment-container .starred-button:hover {{
            border-color: var(--color3);
        }}

        #video-fragment-container .starred-button.active {{
            color: var(--color3);
            border-color: var(--color3);
        }}

        #video-fragment-container .starred-button.inactive {{
            color: var(--color7);
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
            background: var(--color8);
            color: var(--foreground);
        }}

        #video-fragment-container .tag-toggles {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.4rem;
            margin-top: 0.5rem;
        }}

        #video-fragment-container .tag-toggle {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 3px;
            padding: 0.4rem 0.5rem;
            border-radius: 0;
            font-size: 0.75rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s;
            border: 1px solid var(--color7);
            background: var(--color0);
            color: var(--foreground);
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }}

        #video-fragment-container .tag-toggle:hover {{
            border-color: var(--color4);
        }}

        #video-fragment-container .tag-toggle.active {{
            background: var(--color2);
            border-color: var(--color2);
            color: var(--color0);
        }}

        #video-fragment-container .tag-toggle.inactive {{
            background: var(--color1);
            border-color: var(--color1);
            color: var(--color0);
        }}

        #video-fragment-container .stats {{
            margin-bottom: 2rem;
            text-align: center;
            color: var(--color7);
            font-size: 0.9rem;
        }}

        {get_table_styles()}

        @media (max-width: 768px) {{
            .tabs {{
                flex-wrap: wrap;
            }}

            .container {{
                padding: 1rem 0.5rem;
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