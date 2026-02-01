"""Common row components for table-based rendering.

Row Structure Convention (all types):
1. Extra field cell(s) - type-specific metadata (always FIRST)
2. Title cell - displays main content (title/summary)
3. Action cell - active/focus toggle buttons (except calendar)

Field Mapping by Type:
- Tasks: status → title → active/focus
- Calendar: date → status → title → location → (no actions)
- Projects: status → title → active/focus
- Notes: status → title (+ description) → active/focus
"""

from ..utils.svg_icons import SVGIcons


def get_table_styles():
    """
    Return CSS styles for table rendering.

    Returns:
        str: CSS string
    """
    return """
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
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
    }

    /* Base table styles */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 2rem;
        background: var(--bg-paper);
        border-radius: 2px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border-light);
    }

    .data-row {
        border-bottom: 1px solid var(--border-light);
        background: var(--bg-paper);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .data-row:last-child {
        border-bottom: none;
    }

    /* State styles */
    .data-row.active {
        background: var(--bg-light);
    }

    .data-row.focused {
        background: linear-gradient(135deg, rgba(201, 162, 39, 0.08) 0%, var(--bg-light) 100%);
        border-left: 3px solid var(--accent-primary);
    }

    .data-row.active.focused {
        background: linear-gradient(135deg, rgba(201, 162, 39, 0.12) 0%, var(--bg-light) 100%);
        border-left: 3px solid var(--accent-primary);
    }

    .data-row:hover {
        background: var(--bg-cream);
        transform: translateX(2px);
    }

    /* Column styles */
    .status-cell {
        padding: 0.625rem 1rem;
        width: 140px;
        vertical-align: middle;
    }

    .status-icon-cell {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.625rem 1rem;
        width: 140px;
        vertical-align: middle;
    }

    .status-icon-cell svg {
        width: 18px;
        height: 18px;
        color: var(--text-dark-secondary);
    }

    .status-icon-cell[data-status="w"] svg {
        color: #c23645;
    }

    .status-icon-cell[data-status="t"] svg {
        color: #6b4c9a;
    }

    .status-icon-cell[data-status="current"] svg {
        color: #2d6a4f;
    }

    .status-icon-cell[data-status=" "] svg {
        color: #9ca3af;
    }

    .status-icon-cell[data-status="work"] svg {
        color: #6366f1;
    }

    .status-icon-cell[data-status="/"] svg {
        color: #9ca3af;
    }

    .status-icon-cell[data-status="?"] svg {
        color: #f59e0b;
    }

    .status-icon-cell[data-status="x"] svg {
        color: #10b981;
    }

    .status-icon-cell[data-status="<"] svg {
        color: #ec4899;
    }

    .status-icon-cell[data-status=">"] svg {
        color: #8b5cf6;
    }

    .status-icon-cell[data-status="note"] svg {
        color: #3b82f6;
    }

    .status-icon-cell[data-status="focus"] svg {
        color: #f97316;
    }

    .status-icon-cell[data-status="empty"] svg {
        color: #9ca3af;
    }

    .status-icon-cell[data-status="pending"] svg {
        color: #f59e0b;
    }

    .status-icon-cell[data-status="none"] svg {
        color: #9ca3af;
    }

    .status-icon-cell[data-status="active"] svg {
        color: #10b981;
    }

    .status-icon-cell[data-status="*"] svg {
        color: #06b6d4;
    }

    .status-icon-cell[data-status="!"] svg {
        color: #ef4444;
    }

    .status-icon-cell[data-status="a"] svg {
        color: #84cc16;
    }

    .status-icon-cell[data-status="bookmark"] svg {
        color: #8b5cf6;
    }

    .status-icon-cell[data-status="project"] svg {
        color: #f97316;
    }

    .scheduled-cell {
        padding: 0.625rem 1rem;
        width: 140px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8125rem;
        color: var(--text-dark-secondary);
    }

    .scheduled-cell svg {
        width: 14px;
        height: 14px;
        color: var(--text-dark-muted);
        margin-right: 6px;
        vertical-align: text-bottom;
    }

    .location-cell {
        padding: 0.625rem 1rem;
        width: 140px;
        font-size: 0.875rem;
        color: var(--text-dark-secondary);
        font-weight: 300;
    }

    .workspace-cell {
        padding: 0.625rem 1rem;
        width: 140px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-dark-secondary);
    }

    .title-cell {
        padding: 0.625rem 1rem;
        min-width: 280px;
    }

    .title {
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 0.125rem;
        color: var(--text-dark-primary);
    }

    .description {
        font-size: 0.75rem;
        color: var(--text-dark-muted);
        font-weight: 300;
        line-height: 1.3;
    }

    .action-cell {
        padding: 0.625rem 1rem;
        text-align: right;
        white-space: nowrap;
    }

    .toggle-toggle {
        padding: 0.375rem 0.75rem;
        background: transparent;
        border: 1px solid var(--border-light);
        border-radius: 2px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-left: 0.375rem;
        font-size: 0.6875rem;
        font-weight: 600;
        font-family: 'Source Sans Pro', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-dark-secondary);
    }

    .toggle-toggle:hover {
        border-color: var(--border-medium);
        color: var(--text-dark-primary);
        background: var(--bg-light);
        transform: translateY(-1px);
    }

    .toggle-toggle.active {
        background: var(--bg-dark);
        border-color: var(--bg-dark);
        color: var(--text-light-primary);
        box-shadow: 0 2px 8px rgba(26, 26, 26, 0.2);
    }

    .toggle-toggle.focused {
        background: linear-gradient(135deg, var(--accent-primary) 0%, #a68a1f 100%);
        border-color: var(--accent-primary);
        color: var(--bg-paper);
        box-shadow: 0 2px 8px rgba(201, 162, 39, 0.25);
    }

    .title-link {
        color: var(--text-dark-primary);
        text-decoration: none;
        cursor: pointer;
        transition: color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .title-link:hover {
        color: var(--accent-primary);
    }

    .title-link .title {
        font-weight: 600;
    }

    /* Collection styles */
    .collection {
        margin-bottom: 3rem;
        opacity: 0;
        animation: fadeSlideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    .collection.active {
        display: block;
    }

    @keyframes fadeSlideIn {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .collection h3 {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: var(--text-dark-primary);
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-light);
        letter-spacing: -0.01em;
        position: relative;
    }

    .collection h3::after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 0;
        width: 60px;
        height: 2px;
        background: var(--accent-primary);
    }

    .empty-message {
        text-align: center;
        padding: 3rem 2rem;
        color: var(--text-dark-muted);
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 0.9375rem;
        font-style: italic;
    }


    """


def create_status_cell(status):
    """
    Create a status cell with optional icon or text.

    Args:
        status: Status value string

    Returns:
        str: HTML for status cell
    """
    icon = SVGIcons.get_status_icon(status)
    if icon:
        return f"""
        <td class="status-cell status-icon-cell" data-status="{status}">
            {icon}
        </td>"""
    else:
        return f"""
        <td class="status-cell">
            {status}
        </td>"""


def create_title_cell(title, description="", file="", line=1):
    """
    Create a title cell with optional description.

    Args:
        title: Title text
        description: Optional description text
        file: File path for Obsidian link (optional)
        line: Line number for Obsidian link (default: 1)

    Returns:
        str: HTML for title cell
    """
    if file:
        title_link = f'<a href="#" class="title-link" data-file="{file}" data-line="{line}">{title}</a>'
    else:
        title_link = f'<div class="title">{title}</div>'

    html = f"""<td class="title-cell">
        {title_link}"""

    if description:
        html += f"""<div class="description">{description}</div>"""

    html += """</td>"""
    return html


def create_state_toggles_html(item_id, is_active=False, is_focused=False):
    """
    Create active/focus toggle buttons.

    Args:
        item_id: Item identifier
        is_active: Whether item is currently active
        is_focused: Whether item is currently focused

    Returns:
        str: HTML for toggle buttons
    """
    active_class = "active" if is_active else "inactive"
    focused_class = "focused" if is_focused else "unfocused"

    return f"""
    <td class="action-cell">
        <button class="toggle-toggle toggle-active {active_class}" data-id="{item_id}" title="Toggle active">
            Active
        </button>
        <button class="toggle-toggle toggle-focus {focused_class}" data-id="{item_id}" title="Toggle focus">
            Focus
        </button>
    </td>"""


def _render_collection_base(
    collection_info, content_type, empty_message, rows_html, is_first=False
):
    """
    Base function for rendering any collection as a table.

    Args:
        collection_info: Dict with 'title', 'stem', and 'data' keys
        content_type: Type of collection ('task', 'calendar', 'project')
        empty_message: Message to show when no data
        rows_html: HTML string for table rows
        is_first: Whether this is the first collection (makes it active)

    Returns:
        str: HTML for collection table
    """
    is_active = "active" if is_first else ""

    return f"""
    <section class="collection {is_active}" data-type="{content_type}" data-title="{collection_info['title']}" id="{collection_info['stem']}-collection">
        <h3>{collection_info['title']}</h3>
        <table class="data-table {content_type}-table">
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </section>"""


def _render_empty_collection(
    collection_info, content_type, empty_message, is_first=False
):
    """
    Render an empty collection.

    Args:
        collection_info: Dict with 'title', 'stem' keys
        content_type: Type of collection
        empty_message: Message to display
        is_first: Whether this is the first collection (makes it active)

    Returns:
        str: HTML for empty collection
    """
    is_active = "active" if is_first else ""

    return f"""
    <section class="collection {is_active}" data-type="{content_type}" data-title="{collection_info['title']}" id="{collection_info['stem']}-collection">
        <h3>{collection_info['title']}</h3>
        <div class="empty-message">{empty_message}</div>
    </section>"""


def render_task_collection(collection_info, is_first=False):
    """
    Render a single task collection as a table.

    Row structure:
    1. Status cell (extra field - FIRST)
    2. Title cell (task title - as link)
    3. Action cell (active/focus toggles)

    Args:
        collection_info: Dict with 'title' and 'data' keys
        is_first: Whether this is the first collection (makes it active)

    Returns:
        str: HTML for task collection table
    """
    tasks = collection_info.get("data", [])

    if not tasks:
        return _render_empty_collection(
            collection_info, "task", "No tasks found", is_first
        )

    rows_html = ""
    for task in tasks:
        status = task.get("status", "")
        title_cell = create_title_cell(
            task.get("title", ""), "", task.get("file", ""), task.get("line", 1)
        )

        metadata_html = create_status_cell(status)

        toggles_html = create_state_toggles_html(
            task["id"], task.get("active", False), task.get("focus", False)
        )

        row_html = f"""
    <tr class="data-row" data-id="{task['id']}" data-type="task">
        {metadata_html}
        {title_cell}
        {toggles_html}
    </tr>"""
        rows_html += row_html

    return _render_collection_base(
        collection_info, "task", "No tasks found", rows_html, is_first
    )


def render_calendar_collection(collection_info, is_first=False):
    """
    Render a single calendar collection as a table.

    Row structure:
    1. Scheduled cell (extra field - FIRST: date)
    2. Status cell (extra field)
    3. Title cell (event title - as link)
    4. Location cell (extra field)
    5. Action cell (empty - no active/focus toggles)

    Args:
        collection_info: Dict with 'title' and 'data' keys
        is_first: Whether this is the first collection (makes it active)

    Returns:
        str: HTML for calendar collection table
    """
    events = collection_info.get("data", [])

    if not events:
        return _render_empty_collection(
            collection_info, "calendar", "No events found", is_first
        )

    rows_html = ""
    for event in events:
        title_cell = create_title_cell(
            event.get("title", ""), "", event.get("file", ""), event.get("line", 1)
        )
        scheduled = event.get("scheduled", "")
        scheduled = event.get("scheduled", "")
        location = event.get("location", "")
        status = event.get("status", "")

        extra_fields_html = f"""
        <td class="scheduled-cell">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            {scheduled}
        </td>{create_status_cell(status)}"""

        location_html = f"""
        <td class="location-cell">
            {location}
        </td>"""

        rows_html += f"""
    <tr class="data-row" data-id="{event['id']}" data-type="calendar">
        {extra_fields_html}
        {title_cell}
        {location_html}
        <td class="action-cell"></td>
    </tr>"""

    return _render_collection_base(
        collection_info, "calendar", "No events found", rows_html, is_first
    )


def render_project_collection(collection_info, is_first=False):
    """
    Render a single project collection as a table.

    Row structure:
    1. Status cell (extra field - FIRST)
    2. Title cell (project title - as link)
    3. Action cell (active/focus toggles)

    Args:
        collection_info: Dict with 'title' and 'data' keys
        is_first: Whether this is the first collection (makes it active)

    Returns:
        str: HTML for project collection table
    """
    projects = collection_info.get("data", [])

    if not projects:
        return _render_empty_collection(
            collection_info, "project", "No projects found", is_first
        )

    rows_html = ""
    for project in projects:
        title_cell = create_title_cell(
            project.get("title", ""),
            "",
            project.get("file", ""),
            project.get("line", 1),
        )
        status = project.get("status", "")

        metadata_html = create_status_cell(status)

        toggles_html = create_state_toggles_html(
            project["id"], project.get("active", False), project.get("focus", False)
        )

        rows_html += f"""
    <tr class="data-row" data-id="{project['id']}" data-type="project">
        {metadata_html}
        {title_cell}
        {toggles_html}
    </tr>"""

    return _render_collection_base(
        collection_info, "project", "No projects found", rows_html, is_first
    )


def render_notes_collection(collection_info, is_first=False):
    """
    Render a single notes collection as a table.

    Row structure:
    1. Status cell (extra field - FIRST)
    2. Title cell (note title + description - as link)
    3. Action cell (active/focus toggles)

    Args:
        collection_info: Dict with 'title' and 'data' keys
        is_first: Whether this is the first collection (makes it active)

    Returns:
        str: HTML for notes collection table
    """
    notes = collection_info.get("data", [])

    if not notes:
        return _render_empty_collection(
            collection_info, "notes", "No notes found", is_first
        )

    rows_html = ""
    for note in notes:
        title_cell = create_title_cell(
            note.get("title", ""),
            note.get("description", ""),
            note.get("file", ""),
            note.get("line", 1),
        )
        status = note.get("status", "active")

        metadata_html = create_status_cell(status)

        toggles_html = create_state_toggles_html(
            note["id"], note.get("active", False), note.get("focus", False)
        )

        rows_html += f"""
    <tr class="data-row" data-id="{note['id']}" data-type="notes">
        {metadata_html}
        {title_cell}
        {toggles_html}
    </tr>"""

    return _render_collection_base(
        collection_info, "notes", "No notes found", rows_html, is_first
    )
