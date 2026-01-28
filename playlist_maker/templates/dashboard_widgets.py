"""Dashboard widget templates for the landing page.

Each widget represents a different view of task/initiative data.
Widgets are displayed as tabs and can be easily customized.
"""


def get_initiatives_table_widget():
    """
    Widget 1: Initiatives vs Projects table
    
    Columns: Initiative, Projects
    Rows: Focus, Active, Planned
    
    Example structure:
    ┌─────────────────┬──────────────┐
    │ Initiative      │ Projects     │
    ├─────────────────┼──────────────┤
    │ Focus           │ [links]      │
    │ Active          │ [links]      │
    │ Planned         │ [links]      │
    └─────────────────┴──────────────┘
    """
    return """
    <div class="dashboard-widget" id="initiatives-widget">
        <table class="dashboard-table">
            <thead>
                <tr>
                    <th class="col-initiative">Initiative</th>
                    <th class="col-projects">Projects</th>
                </tr>
            </thead>
            <tbody>
                <tr class="row-focus">
                    <td class="row-label">Focus</td>
                    <td class="row-data">{INITIATIVES_FOCUS}</td>
                </tr>
                <tr class="row-active">
                    <td class="row-label">Active</td>
                    <td class="row-data">{INITIATIVES_ACTIVE}</td>
                </tr>
                <tr class="row-planned">
                    <td class="row-label">Planned</td>
                    <td class="row-data">{INITIATIVES_PLANNED}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """


def get_dashboard_widget():
    """
    Widget 2: Dashboard with Initiative, TODO, and Mind columns
    
    Columns: Initiative, TODO, Mind
    Rows: Focus, Active
    
    Example structure:
    ┌─────────────────┬──────────────┬──────────────┐
    │ Initiative      │ TODO         │ Mind         │
    ├─────────────────┼──────────────┼──────────────┤
    │ Focus           │ [count/list] │ [count/list] │
    │ Active          │ [count/list] │ [count/list] │
    └─────────────────┴──────────────┴──────────────┘
    """
    return """
    <div class="dashboard-widget" id="dashboard-widget">
        <table class="dashboard-table">
            <thead>
                <tr>
                    <th class="col-initiative">Initiative</th>
                    <th class="col-todo">TODO</th>
                    <th class="col-mind">Mind</th>
                </tr>
            </thead>
            <tbody>
                <tr class="row-focus">
                    <td class="row-label">Focus</td>
                    <td class="row-data">{DASHBOARD_TODO_FOCUS}</td>
                    <td class="row-data">{DASHBOARD_MIND_FOCUS}</td>
                </tr>
                <tr class="row-active">
                    <td class="row-label">Active</td>
                    <td class="row-data">{DASHBOARD_TODO_ACTIVE}</td>
                    <td class="row-data">{DASHBOARD_MIND_ACTIVE}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """


def get_progress_widget():
    """
    Widget 3: Progress tracking with Progress and Async sub-rows
    
    Columns: Initiative, Projects
    Rows: Focus, Active
    Sub-rows per cell: Progress, Async
    
    Example structure:
    ┌─────────────────┬──────────────┐
    │ Initiative      │ Projects     │
    ├─────────────────┼──────────────┤
    │ Focus           │              │
    │ ├─ Progress     │ [data]       │
    │ └─ Async        │ [data]       │
    │ Active          │              │
    │ ├─ Progress     │ [data]       │
    │ └─ Async        │ [data]       │
    └─────────────────┴──────────────┘
    """
    return """
    <div class="dashboard-widget" id="progress-widget">
        <table class="dashboard-table dashboard-table--nested">
            <thead>
                <tr>
                    <th class="col-initiative">Initiative</th>
                    <th class="col-projects">Projects</th>
                </tr>
            </thead>
            <tbody>
                <tr class="row-focus">
                    <td class="row-label">Focus</td>
                    <td></td>
                </tr>
                <tr class="row-focus-sub row-focus-progress">
                    <td class="row-sublabel">├─ Progress</td>
                    <td class="row-data">{PROGRESS_FOCUS_PROGRESS}</td>
                </tr>
                <tr class="row-focus-sub row-focus-async">
                    <td class="row-sublabel">└─ Async</td>
                    <td class="row-data">{PROGRESS_FOCUS_ASYNC}</td>
                </tr>
                
                <tr class="row-active">
                    <td class="row-label">Active</td>
                    <td></td>
                </tr>
                <tr class="row-active-sub row-active-progress">
                    <td class="row-sublabel">├─ Progress</td>
                    <td class="row-data">{PROGRESS_ACTIVE_PROGRESS}</td>
                </tr>
                <tr class="row-active-sub row-active-async">
                    <td class="row-sublabel">└─ Async</td>
                    <td class="row-data">{PROGRESS_ACTIVE_ASYNC}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
