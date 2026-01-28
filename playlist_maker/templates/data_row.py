"""Common row components for table-based rendering.

Row Structure Convention (all types):
1. Extra field cell(s) - type-specific metadata (always FIRST)
2. Title cell - displays main content (title/summary)
3. Action cell - active/focus toggle buttons (except calendar)

Field Mapping by Type:
- Tasks: status → title → active/focus
- Calendar: date → status → title → location → (no actions)
- Projects: workspace/class → title → active/focus
- Notes: status → title (+ description) → active/focus
"""


def get_table_styles():
    """
    Return CSS styles for table rendering.

    Returns:
        str: CSS string
    """
    return '''
    /* Base table styles */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 2rem;
        background: var(--color0);
        border: 1px solid var(--color7);
        border-radius: 0;
    }

    .data-row {
        border-bottom: 1px solid var(--color7);
        background: var(--color1);
        transition: all 0.2s;
    }

    .data-row:last-child {
        border-bottom: none;
    }

    /* State styles */
    .data-row.active {
        background: var(--color0);
    }

    .data-row.focused {
        background: var(--color3);
        border-left: 4px solid var(--color4);
    }

    .data-row.active.focused {
        background: var(--color3);
        border-left: 4px solid var(--color4);
        font-weight: 500;
    }

    /* Column styles */
    .status-cell {
        padding: 0.75rem 1rem;
        width: 140px;
    }

    .title-cell {
        padding: 0.75rem 1rem;
        min-width: 300px;
    }

    .title {
        font-weight: 500;
        margin-bottom: 0.25rem;
    }

    .description {
        font-size: 0.85rem;
        opacity: 0.7;
    }

    .action-cell {
        padding: 0.75rem 1rem;
        text-align: right;
        white-space: nowrap;
    }

    .toggle-toggle {
        padding: 0.4rem 0.8rem;
        background: transparent;
        border: 1px solid var(--color7);
        border-radius: 0;
        cursor: pointer;
        transition: all 0.2s;
        margin-left: 0.5rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .toggle-toggle:hover {
        border-color: var(--color4);
        color: var(--color4);
    }

    .toggle-toggle.active {
        background: var(--color2);
        border-color: var(--color2);
        color: var(--color0);
    }

    .toggle-toggle.focused {
        background: var(--color3);
        border-color: var(--color3);
        color: var(--color0);
    }

    .title-link {
        color: var(--foreground);
        text-decoration: none;
        cursor: pointer;
        transition: all 0.2s;
    }

    .title-link:hover {
        color: var(--color4);
        text-decoration: underline;
    }

    .title-link .title {
        font-weight: 500;
    }


    '''


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

    html = f'''<td class="title-cell">
        {title_link}'''

    if description:
        html += f'''<div class="description">{description}</div>'''

    html += '''</td>'''
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

    return f'''
    <td class="action-cell">
        <button class="toggle-toggle toggle-active {active_class}" data-id="{item_id}" title="Toggle active">
            Active
        </button>
        <button class="toggle-toggle toggle-focus {focused_class}" data-id="{item_id}" title="Toggle focus">
            Focus
        </button>
    </td>'''


def _render_collection_base(collection_info, content_type, empty_message, rows_html, is_first=False):
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

    return f'''
    <section class="collection {is_active}" data-type="{content_type}" data-title="{collection_info['title']}" id="{collection_info['stem']}-collection">
        <h3>{collection_info['title']}</h3>
        <table class="data-table {content_type}-table">
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </section>'''


def _render_empty_collection(collection_info, content_type, empty_message, is_first=False):
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

    return f'''
    <section class="collection {is_active}" data-type="{content_type}" data-title="{collection_info['title']}" id="{collection_info['stem']}-collection">
        <h3>{collection_info['title']}</h3>
        <div class="empty-message">{empty_message}</div>
    </section>'''


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
        return _render_empty_collection(collection_info, "task", "No tasks found", is_first)

    rows_html = ""
    for task in tasks:
        status = task.get("status", "")
        title_cell = create_title_cell(
            task.get("title", ""),
            "",
            task.get("file", ""),
            task.get("line", 1)
        )

        metadata_html = f'''
        <td class="status-cell">
            {status}
        </td>'''

        toggles_html = create_state_toggles_html(
            task["id"],
            task.get("active", False),
            task.get("focus", False)
        )

        row_html = f'''
    <tr class="data-row" data-id="{task['id']}" data-type="task">
        {metadata_html}
        {title_cell}
        {toggles_html}
    </tr>'''
        rows_html += row_html

    return _render_collection_base(collection_info, "task", "No tasks found", rows_html, is_first)


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
        return _render_empty_collection(collection_info, "calendar", "No events found", is_first)

    rows_html = ""
    for event in events:
        title_cell = create_title_cell(
            event.get("title", ""),
            "",
            event.get("file", ""),
            event.get("line", 1)
        )
        scheduled = event.get("scheduled", "")
        scheduled = event.get("scheduled", "")
        location = event.get("location", "")
        status = event.get("status", "")

        extra_fields_html = f'''
        <td class="scheduled-cell">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            {scheduled}
        </td>
        <td class="status-cell">
            {status}
        </td>'''

        location_html = f'''
        <td class="location-cell">
            {location}
        </td>'''

        rows_html += f'''
    <tr class="data-row" data-id="{event['id']}" data-type="calendar">
        {extra_fields_html}
        {title_cell}
        {location_html}
        <td class="action-cell"></td>
    </tr>'''

    return _render_collection_base(collection_info, "calendar", "No events found", rows_html, is_first)


def render_project_collection(collection_info, is_first=False):
    """
    Render a single project collection as a table.

    Row structure:
    1. Workspace/class cell (extra field - FIRST)
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
        return _render_empty_collection(collection_info, "project", "No projects found", is_first)

    rows_html = ""
    for project in projects:
        title_cell = create_title_cell(
            project.get("title", ""),
            "",
            project.get("file", ""),
            project.get("line", 1)
        )
        workspace = project.get("workspace", "")
        class_type = project.get("class", "")

        metadata_html = f'''
        <td class="workspace-cell">
            {workspace or class_type}
        </td>'''

        toggles_html = create_state_toggles_html(
            project["id"],
            project.get("active", False),
            project.get("focus", False)
        )

        rows_html += f'''
    <tr class="data-row" data-id="{project['id']}" data-type="project">
        {metadata_html}
        {title_cell}
        {toggles_html}
    </tr>'''

    return _render_collection_base(collection_info, "project", "No projects found", rows_html, is_first)


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
        return _render_empty_collection(collection_info, "notes", "No notes found", is_first)

    rows_html = ""
    for note in notes:
        title_cell = create_title_cell(
            note.get("title", ""),
            note.get("description", ""),
            note.get("file", ""),
            note.get("line", 1)
        )
        status = note.get("status", "active")

        metadata_html = f'''
        <td class="status-cell">
            {status}
        </td>'''

        toggles_html = create_state_toggles_html(
            note["id"],
            note.get("active", False),
            note.get("focus", False)
        )

        rows_html += f'''
    <tr class="data-row" data-id="{note['id']}" data-type="notes">
        {metadata_html}
        {title_cell}
        {toggles_html}
    </tr>'''

    return _render_collection_base(collection_info, "notes", "No notes found", rows_html, is_first)
