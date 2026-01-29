"""CSS styles for dashboard and sidebar components."""


def get_dashboard_css():
    """Get all dashboard-related CSS styles."""
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

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Source Sans Pro', sans-serif;
            background: var(--bg-light);
            color: var(--text-dark-primary);
            line-height: 1.6;
            position: relative;
            overflow-x: hidden;
            min-height: 100vh;
        }

        /* ===== LAYOUT ===== */
        .main-layout {
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: 2.5rem;
            max-width: 1500px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
            position: relative;
            z-index: 1;
        }

        .main-content {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .sidebar {
            position: relative;
        }

        /* ===== PAGE HEADER ===== */
        .page-header {
            text-align: center;
            padding: 4rem 3rem;
            background: var(--bg-paper);
            position: relative;
            overflow: hidden;
            border-radius: 2px;
            border: 1px solid var(--border-light);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .page-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-tertiary) 100%);
        }

        .page-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--text-dark-primary);
            letter-spacing: -0.02em;
            position: relative;
        }

        .page-header p {
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.875rem;
            color: var(--text-dark-secondary);
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-weight: 500;
            position: relative;
        }

        /* ===== TAB NAVIGATION ===== */
        .dashboard-tabs {
            display: flex;
            gap: 0.25rem;
            padding: 0.5rem;
            background: var(--bg-paper);
            border-radius: 4px;
            overflow-x: auto;
            border: 1px solid var(--border-light);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }

        .dashboard-tabs button {
            padding: 0.75rem 1.5rem;
            background: transparent;
            border: none;
            color: var(--text-dark-muted);
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.8125rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-radius: 2px;
            position: relative;
        }

        .dashboard-tabs button:hover {
            color: var(--text-dark-primary);
            background: var(--bg-light);
        }

        .dashboard-tabs button.active {
            color: var(--bg-paper);
            background: var(--bg-dark);
        }

        /* ===== DASHBOARD WIDGETS ===== */
        .dashboard-widget {
            display: none;
            animation: fadeSlideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .dashboard-widget.active {
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

        /* ===== TABLES ===== */
        .dashboard-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-paper);
            border-radius: 2px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-light);
        }

        .dashboard-table thead {
            background: var(--bg-dark);
            border-bottom: 1px solid var(--border-light);
        }

        .dashboard-table th {
            padding: 1.25rem 1.5rem;
            text-align: left;
            font-family: 'Source Sans Pro', sans-serif;
            font-weight: 600;
            font-size: 0.6875rem;
            color: var(--text-light-secondary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .dashboard-table td {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-light);
            color: var(--text-dark-primary);
            font-size: 0.875rem;
            vertical-align: middle;
            transition: background 0.2s ease;
        }

        .dashboard-table tbody tr:last-child td {
            border-bottom: none;
        }

        .dashboard-table tbody tr:hover {
            background: var(--bg-cream);
        }

        /* Row styling */
        .row-label {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
            font-size: 0.75rem;
            color: var(--text-dark-primary);
            width: 140px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .row-focus .row-label {
            color: var(--accent-quaternary);
        }

        .row-active .row-label {
            color: var(--accent-primary);
        }

        .row-planned .row-label {
            color: var(--accent-secondary);
        }

        .row-data {
            color: var(--text-dark-secondary);
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.875rem;
            font-weight: 300;
        }

        .row-data a {
            color: var(--accent-primary);
            text-decoration: none;
            margin-right: 0.75rem;
            font-weight: 500;
            transition: color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .row-data a:hover {
            color: var(--accent-secondary);
        }

        /* Nested table styling (for progress widget) */
        .dashboard-table--nested tbody tr.row-focus-sub,
        .dashboard-table--nested tbody tr.row-active-sub {
            background: var(--bg-cream);
        }

        .row-sublabel {
            padding-left: 2.5rem;
            color: var(--text-dark-muted);
            font-weight: 300;
            font-size: 0.8125rem;
        }

        /* ===== ENTRY STYLING ===== */
        .entry {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 0.875rem;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
            background: var(--bg-light);
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.8125rem;
            font-weight: 400;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 240px;
            vertical-align: middle;
            border-radius: 2px;
            border: 1px solid var(--border-light);
            position: relative;
            transition: all 0.2s ease;
        }

        .entry::before {
            content: '';
            position: absolute;
            left: 0;
            top: 6px;
            bottom: 6px;
            width: 2px;
            border-radius: 1px;
        }

        .entry:hover {
            border-color: var(--border-medium);
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        /* Initiative types */
        .entry.initiative-work::before {
            background: var(--accent-quaternary);
        }

        .entry.initiative-study::before {
            background: var(--accent-secondary);
        }

        /* Progress types */
        .entry.progress::before {
            background: var(--accent-tertiary);
        }

        .entry.progress-project::before {
            background: var(--accent-primary);
        }

        .entry.progress-todo::before {
            background: var(--accent-secondary);
        }

        /* TODO and Mind indicators */
        .entry.todo::before {
            background: var(--accent-tertiary);
        }

        .entry.mind {
            color: var(--accent-quaternary);
            font-style: italic;
            border-color: rgba(194, 54, 69, 0.15);
        }

        .entry.mind::before {
            background: var(--accent-quaternary);
        }

        .entry.is-mind {
            color: var(--accent-quaternary);
        }

        /* Empty state */
        .empty {
            color: var(--text-dark-muted);
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.875rem;
            font-weight: 300;
            font-style: italic;
            padding: 1rem;
        }

        /* Count badge */
        .count {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.625rem;
            background: var(--bg-dark);
            border: 1px solid var(--border-light);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.6875rem;
            font-weight: 500;
            color: var(--text-light-secondary);
            margin-left: 0.5rem;
            border-radius: 2px;
        }

        /* ===== PLAYLISTS SIDEBAR ===== */
        .playlists-sidebar {
            background: var(--bg-paper);
            border-radius: 2px;
            padding: 0;
            position: sticky;
            top: 2rem;
            max-height: calc(100vh - 4rem);
            overflow-y: auto;
            border: 1px solid var(--border-light);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .sidebar-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.125rem;
            font-weight: 600;
            padding: 1.5rem;
            color: var(--text-dark-primary);
            border-bottom: 1px solid var(--border-light);
            text-transform: none;
            letter-spacing: 0.02em;
            position: relative;
        }

        .sidebar-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 1.5rem;
            right: 1.5rem;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-primary) 0%, transparent 100%);
        }

        .playlists-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Source Sans Pro', sans-serif;
        }

        .playlist-row {
            transition: all 0.2s ease;
            border-bottom: 1px solid var(--border-light);
        }

        .playlist-row:hover {
            background: var(--bg-cream);
        }

        .playlist-row:last-child {
            border-bottom: none;
        }

        .playlist-name {
            padding: 1rem 1.5rem;
        }

        .playlist-name a {
            color: var(--text-dark-primary);
            text-decoration: none;
            transition: color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .playlist-name a:hover {
            color: var(--accent-primary);
        }

        .playlist-count {
            text-align: right;
            color: var(--text-dark-muted);
            padding: 1rem 1.5rem 1rem 1rem;
            font-size: 0.75rem;
            font-weight: 400;
            white-space: nowrap;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 1024px) {
            .main-layout {
                grid-template-columns: 1fr;
                gap: 2rem;
            }

            .playlists-sidebar {
                position: relative;
                top: auto;
                max-height: 400px;
            }
        }

        @media (max-width: 768px) {
            .main-layout {
                padding: 1.5rem 1rem;
            }

            .page-header {
                padding: 2.5rem 1.5rem;
            }

            .page-header h1 {
                font-size: 2.25rem;
            }

            .dashboard-tabs {
                gap: 0;
            }

            .dashboard-tabs button {
                padding: 0.625rem 1rem;
                font-size: 0.75rem;
            }

            .dashboard-table th,
            .dashboard-table td {
                padding: 0.875rem 1rem;
                font-size: 0.8125rem;
            }

            .playlists-sidebar {
                max-height: 350px;
            }

            .sidebar-title {
                padding: 1.25rem;
                font-size: 1rem;
            }

            .playlists-table {
                font-size: 0.8125rem;
            }
        }
    """
