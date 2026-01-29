"""CSS styles for dashboard and sidebar components."""


def get_dashboard_css():
    """Get all dashboard-related CSS styles."""
    return """
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg-deep: #0c1016;
            --bg-surface: #131820;
            --bg-elevated: #1c2230;
            --bg-card: #181e28;
            --bg-subtle: rgba(255, 255, 255, 0.02);
            --border-subtle: rgba(255, 255, 255, 0.06);
            --border-medium: rgba(255, 255, 255, 0.1);
            --accent-primary: #e8c47c;
            --accent-secondary: #7eb8da;
            --accent-tertiary: #a78bfa;
            --accent-quaternary: #f472b6;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --text-subtle: #475569;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Source Sans Pro', sans-serif;
            background: linear-gradient(135deg, var(--bg-deep) 0%, #0f151e 50%, var(--bg-surface) 100%);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            opacity: 0.4;
            background: 
                radial-gradient(circle at 15% 50%, rgba(126, 184, 218, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(232, 196, 124, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(167, 139, 250, 0.03) 0%, transparent 50%);
            z-index: 0;
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
            background: var(--bg-card);
            position: relative;
            overflow: hidden;
            border-radius: 16px;
        }

        .page-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(232, 196, 124, 0.08) 0%, transparent 60%);
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .page-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            position: relative;
        }

        .page-header p {
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.875rem;
            color: var(--text-secondary);
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-weight: 500;
            position: relative;
        }

        /* ===== TAB NAVIGATION ===== */
        .dashboard-tabs {
            display: flex;
            gap: 0.25rem;
            background: var(--bg-surface);
            padding: 0.5rem;
            border-radius: 12px;
            overflow-x: auto;
            border: 1px solid var(--border-subtle);
        }

        .dashboard-tabs button {
            padding: 0.75rem 1.5rem;
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.8125rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-radius: 8px;
            position: relative;
        }

        .dashboard-tabs button:hover {
            color: var(--text-primary);
            background: var(--bg-subtle);
        }

        .dashboard-tabs button.active {
            color: var(--bg-deep);
            background: var(--accent-primary);
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
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }

        .dashboard-table thead {
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
        }

        .dashboard-table th {
            padding: 1.25rem 1.5rem;
            text-align: left;
            font-family: 'Source Sans Pro', sans-serif;
            font-weight: 600;
            font-size: 0.6875rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .dashboard-table td {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-primary);
            font-size: 0.875rem;
            vertical-align: middle;
            transition: background 0.2s ease;
        }

        .dashboard-table tbody tr:last-child td {
            border-bottom: none;
        }

        .dashboard-table tbody tr:hover {
            background: var(--bg-elevated);
        }

        /* Row styling */
        .row-label {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
            font-size: 0.75rem;
            color: var(--text-primary);
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
            color: var(--text-secondary);
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
            background: var(--bg-elevated);
        }

        .row-sublabel {
            padding-left: 2.5rem;
            color: var(--text-muted);
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
            background: var(--bg-elevated);
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 0.8125rem;
            font-weight: 400;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 240px;
            vertical-align: middle;
            border-radius: 6px;
            border: 1px solid var(--border-subtle);
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
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
            border-color: rgba(244, 114, 182, 0.2);
        }

        .entry.mind::before {
            background: var(--accent-quaternary);
        }

        .entry.is-mind {
            color: var(--accent-quaternary);
        }

        /* Empty state */
        .empty {
            color: var(--text-muted);
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
            background: var(--bg-deep);
            border: 1px solid var(--border-subtle);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.6875rem;
            font-weight: 500;
            color: var(--text-secondary);
            margin-left: 0.5rem;
            border-radius: 4px;
        }

        /* ===== PLAYLISTS SIDEBAR ===== */
        .playlists-sidebar {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 0;
            position: sticky;
            top: 2rem;
            max-height: calc(100vh - 4rem);
            overflow-y: auto;
            border: 1px solid var(--border-subtle);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }

        .sidebar-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.125rem;
            font-weight: 600;
            padding: 1.5rem;
            color: var(--text-primary);
            border-bottom: 1px solid var(--border-subtle);
            text-transform: none;
            letter-spacing: 0.02em;
            position: relative;
        }

        .playlists-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Source Sans Pro', sans-serif;
        }

        .playlist-row {
            transition: all 0.2s ease;
            border-bottom: 1px solid var(--border-subtle);
        }

        .playlist-row:hover {
            background: var(--bg-elevated);
        }

        .playlist-row:last-child {
            border-bottom: none;
        }

        .playlist-name {
            padding: 1rem 1.5rem;
        }

        .playlist-name a {
            color: var(--text-primary);
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
            color: var(--text-muted);
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
