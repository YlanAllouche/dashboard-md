"""Common row components for table-based rendering."""


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


    '''


def create_title_cell(title, description=""):
    """
    Create a title cell with optional description.

    Args:
        title: Title text
        description: Optional description text

    Returns:
        str: HTML for title cell
    """
    html = f'''<td class="title-cell">
        <div class="title">{title}</div>'''

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


def _render_collection_base(collection_info, content_type, empty_message, rows_html):
    """
    Base function for rendering any collection as a table.

    Args:
        collection_info: Dict with 'title', 'stem', and 'data' keys
        content_type: Type of collection ('task', 'calendar', 'project')
        empty_message: Message to show when no data
        rows_html: HTML string for table rows

    Returns:
        str: HTML for collection table
    """
    is_active = "active" if collection_info.get("stem") == collection_info.get("stem", "").split("-")[0] else ""

    return f'''
    <section class="collection {is_active}" data-type="{content_type}" data-title="{collection_info['title']}" id="{collection_info['stem']}-collection">
        <h3>{collection_info['title']}</h3>
        <table class="data-table {content_type}-table">
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </section>'''


def _render_empty_collection(collection_info, content_type, empty_message):
    """
    Render an empty collection.

    Args:
        collection_info: Dict with 'title', 'stem' keys
        content_type: Type of collection
        empty_message: Message to display

    Returns:
        str: HTML for empty collection
    """
    is_active = "active" if collection_info.get("stem") == collection_info.get("stem", "").split("-")[0] else ""

    return f'''
    <section class="collection {is_active}" data-type="{content_type}" data-title="{collection_info['title']}" id="{collection_info['stem']}-collection">
        <h3>{collection_info['title']}</h3>
        <div class="empty-message">{empty_message}</div>
    </section>'''


def render_task_collection(collection_info):
    """
    Render a single task collection as a table.

    Args:
        collection_info: Dict with 'title' and 'data' keys

    Returns:
        str: HTML for task collection table
    """
    tasks = collection_info.get("data", [])

    if not tasks:
        return _render_empty_collection(collection_info, "task", "No tasks found")

    rows_html = ""
    for task in tasks:
        title_cell = create_title_cell(task.get("title", ""), "")
        due_date = task.get("due_date", "")

        metadata_html = f'''
        <td class="metadata-cell">
            {due_date}
        </td>'''

        toggles_html = create_state_toggles_html(
            task["id"],
            task.get("active", False),
            task.get("focus", False)
        )

        row_html = f'''
    <tr class="data-row" data-id="{task['id']}" data-type="task">
        {title_cell}
        {metadata_html}
        {toggles_html}
    </tr>'''
        rows_html += row_html

    return _render_collection_base(collection_info, "task", "No tasks found", rows_html)


def render_calendar_collection(collection_info):
    """
    Render a single calendar collection as a table.

    Args:
        collection_info: Dict with 'title' and 'data' keys

    Returns:
        str: HTML for calendar collection table
    """
    events = collection_info.get("data", [])

    if not events:
        return _render_empty_collection(collection_info, "calendar", "No events found")

    rows_html = ""
    for event in events:
        title_cell = create_title_cell(event.get("title", ""), "")
        scheduled = event.get("scheduled", "")
        location = event.get("location", "")

        metadata_html = f'''
        <td class="scheduled-cell">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            {scheduled}
        </td>
        <td class="location-cell">
            {location}
        </td>'''

        rows_html += f'''
    <tr class="data-row" data-id="{event['id']}" data-type="calendar">
        {title_cell}
        {metadata_html}
        <td class="action-cell"></td>
    </tr>'''

    return _render_collection_base(collection_info, "calendar", "No events found", rows_html)


def render_project_collection(collection_info):
    """
    Render a single project collection as a table.

    Args:
        collection_info: Dict with 'title' and 'data' keys

    Returns:
        str: HTML for project collection table
    """
    projects = collection_info.get("data", [])

    if not projects:
        return _render_empty_collection(collection_info, "project", "No projects found")

    rows_html = ""
    for project in projects:
        title_cell = create_title_cell(project.get("title", ""), "")
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
        {title_cell}
        {metadata_html}
        {toggles_html}
    </tr>'''

    return _render_collection_base(collection_info, "project", "No projects found", rows_html)
