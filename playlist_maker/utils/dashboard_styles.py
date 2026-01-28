"""CSS styles for dashboard and sidebar components."""


def get_dashboard_css():
    """Get all dashboard-related CSS styles."""
    return """
        /* ===== LAYOUT ===== */
        .main-layout {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 2rem;
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        .main-content {
            flex: 1;
        }

        .sidebar {
            position: relative;
        }

        /* ===== TAB NAVIGATION ===== */
        .dashboard-tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid var(--color7);
            overflow-x: auto;
        }

        .dashboard-tabs button {
            padding: 0.75rem 1.5rem;
            background: transparent;
            border: none;
            color: var(--color6);
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
            white-space: nowrap;
        }

        .dashboard-tabs button:hover {
            color: var(--foreground);
        }

        .dashboard-tabs button.active {
            color: var(--color4);
            border-bottom-color: var(--color4);
        }

        /* ===== DASHBOARD WIDGETS ===== */
        .dashboard-widget {
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .dashboard-widget.active {
            display: block;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(5px);
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
            background: var(--color0);
            border: 2px solid var(--color7);
        }

        .dashboard-table thead {
            background: var(--color8);
            border-bottom: 2px solid var(--color7);
        }

        .dashboard-table th {
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: var(--color4);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .dashboard-table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--color7);
            color: var(--foreground);
        }

        .dashboard-table tbody tr:last-child td {
            border-bottom: none;
        }

        .dashboard-table tbody tr:hover {
            background: var(--color8);
        }

        /* Row styling */
        .row-label {
            font-weight: 600;
            color: var(--foreground);
            width: 100px;
        }

        .row-focus .row-label {
            color: var(--color1);
        }

        .row-active .row-label {
            color: var(--color3);
        }

        .row-planned .row-label {
            color: var(--color2);
        }

        .row-data {
            color: var(--color6);
            font-size: 0.9rem;
        }

        .row-data a {
            color: var(--color4);
            text-decoration: none;
            margin-right: 0.5rem;
            transition: color 0.2s ease;
        }

        .row-data a:hover {
            color: var(--color5);
            text-decoration: underline;
        }

        /* Nested table styling (for progress widget) */
        .dashboard-table--nested tbody tr.row-focus-sub,
        .dashboard-table--nested tbody tr.row-active-sub {
            background: var(--color8);
            font-size: 0.85rem;
        }

        .row-sublabel {
            padding-left: 2rem;
            color: var(--color6);
            font-weight: 400;
        }

        /* ===== ENTRY STYLING ===== */
        .entry {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            margin-right: 0.5rem;
            margin-bottom: 0.25rem;
            background: var(--color8);
            border-radius: 3px;
            font-size: 0.85rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 200px;
            vertical-align: middle;
        }

        .entry:hover {
            background: var(--color7);
            cursor: help;
        }

        /* Initiative types */
        .entry.initiative-work {
            border-left: 3px solid var(--color1);  /* Red for work */
        }

        .entry.initiative-study {
            border-left: 3px solid var(--color2);  /* Green for study */
        }

        /* Progress types */
        .entry.progress {
            border-left: 3px solid var(--color4);  /* Blue default */
        }

        .entry.progress-project {
            border-left: 3px solid var(--color3);  /* Yellow for projects */
        }

        .entry.progress-todo {
            border-left: 3px solid var(--color5);  /* Magenta for tasks */
        }

        /* TODO and Mind indicators */
        .entry.todo {
            border-left: 3px solid var(--color4);  /* Blue for todos */
        }

        .entry.mind {
            border-left: 3px solid var(--color5);  /* Magenta for ideas */
            font-style: italic;
            opacity: 0.8;
        }

        .entry.is-mind {
            font-style: italic;
            opacity: 0.8;
        }

        /* Empty state */
        .empty {
            color: var(--color6);
            opacity: 0.6;
        }

        /* Count badge */
        .count {
            display: inline-block;
            padding: 0.15rem 0.4rem;
            background: var(--color7);
            border-radius: 2px;
            font-size: 0.7rem;
            color: var(--foreground);
            margin-left: 0.25rem;
        }

        /* ===== PLAYLISTS SIDEBAR ===== */
        .playlists-sidebar {
            background: var(--color0);
            border: 2px solid var(--color7);
            padding: 1.5rem;
            position: sticky;
            top: 2rem;
            max-height: calc(100vh - 4rem);
            overflow-y: auto;
        }

        .sidebar-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--foreground);
            border-bottom: 2px solid var(--color7);
            padding-bottom: 0.75rem;
        }

        .playlists-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        .playlist-row {
            transition: background 0.2s ease;
        }

        .playlist-row:hover {
            background: var(--color8);
        }

        .playlist-name {
            padding: 0.5rem 0;
        }

        .playlist-name a {
            color: var(--color4);
            text-decoration: none;
            transition: color 0.2s ease;
            display: block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .playlist-name a:hover {
            color: var(--color5);
        }

        .playlist-count {
            text-align: right;
            color: var(--color6);
            padding: 0.5rem 0 0.5rem 0.5rem;
            font-size: 0.75rem;
            white-space: nowrap;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 1024px) {
            .main-layout {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }

            .playlists-sidebar {
                position: relative;
                top: auto;
                max-height: none;
                margin-top: 2rem;
            }
        }

        @media (max-width: 768px) {
            .main-layout {
                padding: 1rem 0.5rem;
            }

            .dashboard-tabs {
                gap: 0.25rem;
            }

            .dashboard-tabs button {
                padding: 0.5rem 1rem;
                font-size: 0.85rem;
            }

            .dashboard-table th,
            .dashboard-table td {
                padding: 0.5rem;
                font-size: 0.8rem;
            }

            .playlists-sidebar {
                padding: 1rem;
            }

            .sidebar-title {
                font-size: 0.95rem;
                margin-bottom: 0.75rem;
            }

            .playlists-table {
                font-size: 0.75rem;
            }
        }
    """
