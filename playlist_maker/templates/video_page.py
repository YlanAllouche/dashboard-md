"""Video collection page template"""


def get_video_page_html(title, pywal_css, json_data):
    """Generate the video collection page HTML"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
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

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
            position: relative;
            z-index: 1;
        }}

        .header {{
            text-align: center;
            margin-bottom: 2.5rem;
            position: relative;
        }}

        .header h1 {{
            font-family: 'Playfair Display', serif;
            color: var(--text-dark-primary);
            font-size: 2.75rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }}

        .header p {{
            color: var(--text-dark-secondary);
            font-size: 0.9375rem;
            font-weight: 300;
        }}

        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 1.75rem;
        }}

        .video-card {{
            background: var(--bg-paper);
            border-radius: 2px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
            border: 1px solid var(--border-light);
            position: relative;
        }}

        .video-card:hover {{
            border-color: var(--border-medium);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}

        .thumbnail-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            overflow: hidden;
            background: var(--bg-dark-surface);
            cursor: pointer;
        }}

        .thumbnail {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .video-card:hover .thumbnail {{
            transform: scale(1.05);
        }}

        .duration-badge {{
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

        .youtube-link-badge {{
            background: var(--bg-dark);
            color: var(--text-light-primary);
            padding: 0.25rem 0.625rem;
            border-radius: 2px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--border-light);
            text-decoration: none;
            transition: all 0.2s;
            margin: 0 8px;
        }}

        .youtube-link-badge:hover {{
            border-color: var(--accent-primary);
            color: var(--text-light-primary);
        }}

        .deep-link-badge {{
            background: var(--bg-dark);
            color: var(--text-light-primary);
            padding: 0.25rem 0.625rem;
            border-radius: 2px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--border-light);
            text-decoration: none;
            transition: all 0.2s;
        }}

        .deep-link-badge:hover {{
            border-color: var(--accent-primary);
            color: var(--text-light-primary);
        }}

        .card-content {{
            padding: 1.25rem;
        }}

        .video-title {{
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

        .video-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 0.8125rem;
            color: var(--text-dark-muted);
        }}

        .channel-name {{
            font-weight: 500;
            color: var(--text-dark-secondary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .channel-name svg {{
            width: 14px;
            height: 14px;
            color: var(--text-dark-muted);
        }}

        .video-date {{
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            gap: 4px;
            font-family: 'JetBrains Mono', monospace;
        }}

        .video-date svg {{
            width: 14px;
            height: 14px;
            color: var(--text-dark-muted);
            margin-right: 4px;
            vertical-align: text-bottom;
        }}

        .action-buttons {{
            display: flex;
            gap: 0.625rem;
            margin-bottom: 1rem;
        }}

        .btn {{
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

        .btn svg {{
            width: 14px;
            height: 14px;
        }}

        .btn-inbox {{
            background: transparent;
            color: var(--text-dark-muted);
            border: 1px solid var(--border-light);
        }}

        .btn-inbox:hover {{
            border-color: var(--border-medium);
            color: var(--text-dark-primary);
            background: var(--bg-light);
        }}

        .btn-inbox.active {{
            background: var(--bg-dark);
            border-color: var(--bg-dark);
            color: var(--text-light-primary);
            box-shadow: 0 2px 8px rgba(26, 26, 26, 0.2);
        }}

        .btn-watched {{
            background: transparent;
            color: var(--text-dark-muted);
            border: 1px solid var(--border-light);
        }}

        .btn-watched:hover {{
            border-color: var(--border-medium);
            color: var(--text-dark-primary);
            background: var(--bg-light);
        }}

        .btn-watched.active {{
            background: linear-gradient(135deg, var(--accent-success) 0%, #247a5d 100%);
            border-color: var(--accent-success);
            color: var(--bg-paper);
            box-shadow: 0 2px 8px rgba(45, 139, 107, 0.25);
        }}

        .watched-indicator {{
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

        .video-card.watched .watched-indicator {{
            opacity: 1;
        }}

        .starred-button {{
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

        .starred-button:hover {{
            border-color: var(--accent-quaternary);
            transform: scale(1.1);
        }}

        .starred-button.active {{
            color: var(--accent-quaternary);
            border-color: var(--accent-quaternary);
            box-shadow: 0 4px 12px rgba(194, 54, 69, 0.2);
        }}

        .starred-button.inactive {{
            color: var(--text-dark-muted);
        }}

        .starred-button svg {{
            width: 20px;
            height: 20px;
        }}

        .placeholder-thumbnail {{
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

        .tag-toggles {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
            margin-top: 0.75rem;
        }}

        .tag-toggle {{
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

        .tag-toggle:hover {{
            border-color: var(--border-medium);
            color: var(--text-dark-primary);
            background: var(--bg-cream);
        }}

        .tag-toggle.active {{
            background: linear-gradient(135deg, var(--accent-secondary) 0%, #245e44 100%);
            border-color: var(--accent-secondary);
            color: var(--bg-paper);
            box-shadow: 0 2px 6px rgba(45, 106, 79, 0.25);
        }}

        .tag-toggle.inactive {{
            background: var(--bg-light);
            border: 1px solid var(--border-light);
            color: var(--text-dark-secondary);
        }}

        .stats {{
            margin-bottom: 2rem;
            text-align: center;
            color: var(--text-dark-secondary);
            font-size: 0.9375rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Source Sans Pro', sans-serif;
            background: linear-gradient(135deg, var(--bg-deep) 0%, #0f151e 50%, var(--bg-surface) 100%);
            color: var(--text-primary);
            line-height: 1.6;
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
            opacity: 0.4;
            background:
                radial-gradient(circle at 15% 50%, rgba(126, 184, 218, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(232, 196, 124, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(167, 139, 250, 0.03) 0%, transparent 50%);
            z-index: 0;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
            position: relative;
            z-index: 1;
        }}

        .header {{
            text-align: center;
            margin-bottom: 2.5rem;
            position: relative;
        }}

        .header h1 {{
            font-family: 'Playfair Display', serif;
            color: var(--text-primary);
            font-size: 2.75rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }}

        .header p {{
            color: var(--text-secondary);
            font-size: 0.9375rem;
            font-weight: 300;
        }}

        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 1.75rem;
        }}

        .video-card {{
            background: var(--bg-card);
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
            border: 1px solid var(--border-subtle);
            position: relative;
        }}

        .video-card:hover {{
            border-color: var(--border-medium);
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }}

        .thumbnail-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            overflow: hidden;
            background: var(--bg-elevated);
            cursor: pointer;
        }}

        .thumbnail {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .video-card:hover .thumbnail {{
            transform: scale(1.05);
        }}

        .duration-badge {{
            position: absolute;
            bottom: 12px;
            right: 12px;
            background: rgba(12, 16, 22, 0.85);
            backdrop-filter: blur(8px);
            color: var(--text-primary);
            padding: 0.375rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
            border: 1px solid var(--border-medium);
            font-family: 'JetBrains Mono', monospace;
        }}

        .youtube-link-badge {{
            background: var(--bg-elevated);
            color: var(--text-primary);
            padding: 0.25rem 0.625rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--border-subtle);
            text-decoration: none;
            transition: all 0.2s;
            margin: 0 8px;
        }}

        .youtube-link-badge:hover {{
            border-color: var(--border-medium);
            color: var(--accent-primary);
        }}

        .deep-link-badge {{
            background: var(--bg-elevated);
            color: var(--text-primary);
            padding: 0.25rem 0.625rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--border-subtle);
            text-decoration: none;
            transition: all 0.2s;
        }}

        .deep-link-badge:hover {{
            border-color: var(--border-medium);
            color: var(--accent-primary);
        }}

        .card-content {{
            padding: 1.25rem;
        }}

        .video-title {{
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .video-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 0.8125rem;
            color: var(--text-muted);
        }}

        .channel-name {{
            font-weight: 500;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .channel-name svg {{
            width: 14px;
            height: 14px;
            color: var(--text-muted);
        }}

        .video-date {{
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            gap: 4px;
            font-family: 'JetBrains Mono', monospace;
        }}

        .video-date svg {{
            width: 14px;
            height: 14px;
            color: var(--text-muted);
            margin-right: 4px;
            vertical-align: text-bottom;
        }}

        .action-buttons {{
            display: flex;
            gap: 0.625rem;
            margin-bottom: 1rem;
        }}

        .btn {{
            flex: 1;
            padding: 0.625rem 0.875rem;
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
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
            color: var(--text-muted);
            font-family: 'Source Sans Pro', sans-serif;
        }}

        .btn svg {{
            width: 14px;
            height: 14px;
        }}

        .btn-inbox {{
            background: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border-subtle);
        }}

        .btn-inbox:hover {{
            border-color: var(--border-medium);
            color: var(--text-primary);
            background: var(--bg-subtle);
        }}

        .btn-inbox.active {{
            background: linear-gradient(135deg, var(--accent-primary) 0%, #d4a84f 100%);
            border-color: var(--accent-primary);
            color: var(--bg-deep);
            box-shadow: 0 2px 8px rgba(232, 196, 124, 0.25);
        }}

        .btn-watched {{
            background: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border-subtle);
        }}

        .btn-watched:hover {{
            border-color: var(--border-medium);
            color: var(--text-primary);
            background: var(--bg-subtle);
        }}

        .btn-watched.active {{
            background: linear-gradient(135deg, var(--accent-success) 0%, #5ab86f 100%);
            border-color: var(--accent-success);
            color: var(--bg-deep);
            box-shadow: 0 2px 8px rgba(107, 207, 127, 0.25);
        }}

        .watched-indicator {{
            position: absolute;
            top: 12px;
            left: 12px;
            width: 10px;
            height: 10px;
            background: var(--accent-success);
            border: 2px solid var(--bg-card);
            border-radius: 50%;
            opacity: 0;
            transition: opacity 0.2s;
            box-shadow: 0 2px 6px rgba(107, 207, 127, 0.4);
        }}

        .video-card.watched .watched-indicator {{
            opacity: 1;
        }}

        .starred-button {{
            position: absolute;
            top: 12px;
            right: 12px;
            width: 40px;
            height: 40px;
            background: rgba(12, 16, 22, 0.85);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-medium);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }}

        .starred-button:hover {{
            border-color: var(--accent-quaternary);
            transform: scale(1.1);
        }}

        .starred-button.active {{
            color: var(--accent-quaternary);
            border-color: var(--accent-quaternary);
            box-shadow: 0 4px 12px rgba(244, 114, 182, 0.3);
        }}

        .starred-button.inactive {{
            color: var(--text-muted);
        }}

        .starred-button svg {{
            width: 20px;
            height: 20px;
        }}

        .placeholder-thumbnail {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            background: linear-gradient(135deg, var(--bg-elevated) 0%, var(--bg-card) 100%);
            color: var(--text-subtle);
        }}

        .tag-toggles {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
            margin-top: 0.75rem;
        }}

        .tag-toggle {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            padding: 0.5rem 0.625rem;
            border-radius: 6px;
            font-size: 0.6875rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--border-subtle);
            background: transparent;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-family: 'Source Sans Pro', sans-serif;
        }}

        .tag-toggle:hover {{
            border-color: var(--border-medium);
            color: var(--text-primary);
            background: var(--bg-subtle);
        }}

        .tag-toggle.active {{
            background: linear-gradient(135deg, var(--accent-secondary) 0%, #6aa8cc 100%);
            border-color: var(--accent-secondary);
            color: var(--bg-deep);
            box-shadow: 0 2px 6px rgba(126, 184, 218, 0.25);
        }}

        .tag-toggle.inactive {{
            background: transparent;
            border: 1px solid var(--border-subtle);
            color: var(--text-muted);
        }}

        .stats {{
            margin-bottom: 2rem;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.9375rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1.5rem 1rem;
            }}

            .video-grid {{
                grid-template-columns: 1fr;
                gap: 1.25rem;
            }}

            .header h1 {{
                font-size: 2rem;
            }}

            .btn {{
                font-size: 0.6875rem;
                padding: 0.5rem 0.625rem;
            }}

            .tag-toggle {{
                font-size: 0.625rem;
                padding: 0.375rem 0.5rem;
            }}

            .tag-toggles {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.375rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:32px;height:32px;display:inline;margin-right:8px;vertical-align:middle;"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/></svg> {{title}}</h1>
        </div>
        
        <div class="stats" id="stats">
            <!-- Stats will be rendered here -->
        </div>
        
        <div class="video-grid" id="videoGrid">
            <!-- Videos will be rendered here -->
        </div>
    </div>

    <script>
        // Video data from JSON file
        const videoData = {json_data};

        // Tags data from -tags.json (placeholder, will be replaced by Python)
        const tagsData = {{TAGS_DATA}};

        const placeholderThumbnails = ['🎬', '📺', '🎥', '🎞️', '📹', '🎪', '🎭', '🎨', '🎯', '🎲'];

        // Tag definitions from tagsData
        const tagDefinitions = Object.entries(tagsData).map(([name, value]) => ({{
            name,
            glyph: value,
            label: value
        }}));

        function createObsidianLink(command) {{
            const baseUrl = 'obsidian://advanced-uri?vault=share&eval=';
            return baseUrl + encodeURIComponent(command);
        }}

        function createPlayLink(locator) {{
            const command = `app.plugins.plugins["templater-obsidian"].templater.current_functions_object.user.captureMdPlay("${{locator}}")`;
            return createObsidianLink(command);
        }}

        function createInboxWatchedToggleLink(id) {{
            const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.toggleInbox(tp, "${{id}}");tp.user.toggleWatched(tp,"${{id}}");`;
            return createObsidianLink(command);
        }}

        function createInboxToggleLink(id) {{
            const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.toggleInbox(tp,"${{id}}");`;
            return createObsidianLink(command);
        }}

        function createTagToggleLink(id, tag) {{
            const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.toggleTag(tp,"${{id}}", "${{tag}}");`;
            return createObsidianLink(command);
        }}

        function createYouTubeLink(locator) {{
            return `https://youtube.com/watch?v=${{locator}}`;
        }}

        function createDeepLink(file, line) {{
            const lineStr = String(line);
            const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.openLineInNvim("${{file}}", ${{lineStr}});`;
            return createObsidianLink(command);
        }}

        function formatDuration(seconds) {{
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;
            
            if (hours > 0) {{
                return `${{hours}}:${{minutes.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }}
            return `${{minutes}}:${{secs.toString().padStart(2, '0')}}`;
        }}

        function formatDate(dateString) {{
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {{ 
                month: 'short', 
                day: 'numeric', 
                year: 'numeric' 
            }});
        }}

        function createTagToggles(video) {{
            return tagDefinitions.map(tagDef => {{
                const isActive = video.tags?.includes(tagDef.name);
                const statusClass = isActive ? 'active' : 'inactive';
                const link = createTagToggleLink(video.id, tagDef.name);
                
                return `<a href="${{link}}" class="tag-toggle ${{statusClass}}" title="${{tagDef.name}}: ${{isActive ? 'Active' : 'Inactive'}}">
                    ${{tagDef.glyph}}
                </a>`;
            }}).join('');
        }}

        function createVideoCard(video, index) {{
            const isInboxActive = video.tags?.includes('inbox');
            const isWatched = video.watched;
            const isStarred = video.tags?.includes('starred');
            const watchedClass = isWatched ? 'watched' : '';

            const thumbnailContent = video.thumbnail 
                ? `<img src="${{video.thumbnail}}" alt="${{video.summary}}" class="thumbnail" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                   <div class="placeholder-thumbnail" style="display: none;">${{placeholderThumbnails[index % placeholderThumbnails.length]}}</div>`
                : `<div class="placeholder-thumbnail">${{placeholderThumbnails[index % placeholderThumbnails.length]}}</div>`;

            const inboxWatchedLink = createInboxWatchedToggleLink(video.id);
            const inboxLink = createInboxToggleLink(video.id);
            const starredLink = createTagToggleLink(video.id, 'starred');
            const deepLink = video.file ? createDeepLink(`~/share/${{video.file}}`, video.line) : null;

            return `
                <div class="video-card ${{watchedClass}}" data-id="${{video.id}}">
                    <div class="thumbnail-container">
                        ${{thumbnailContent}}
                        <a href="${{starredLink}}" class="starred-button ${{isStarred ? 'active' : 'inactive'}}" title="Toggle starred">
                            <span style="display:inline-flex;align-items:center;justify-content:center;">
                                ${{isStarred ? '<svg viewBox="0 0 24 24" fill="currentColor" style="width:20px;height:20px;"><polygon points="12 2 15.09 10.26 24 10.26 17.55 16.52 19.64 24.78 12 19.52 4.36 24.78 6.45 16.52 0 10.26 8.91 10.26 12 2"/></svg>' : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width:20px;height:20px;"><polygon points="12 2 15.09 10.26 24 10.26 17.55 16.52 19.64 24.78 12 19.52 4.36 24.78 6.45 16.52 0 10.26 8.91 10.26 12 2"/></svg>'}}
                            </span>
                        </a>
                        <div class="duration-badge">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-clock-icon lucide-clock" style="width:14px;height:14px;display:inline;"><path d="M12 6v6l4 2"/><circle cx="12" cy="12" r="10"/></svg> ${{formatDuration(video.duration)}}
                        </div>
                        <div class="watched-indicator"></div>
                    </div>
                    <div class="card-content">
                        <h3 class="video-title">${{video.summary}}</h3>
                        <div class="video-meta">
                            <span class="channel-name">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-icon lucide-user" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>${{video.channel}}
                            </span>
                            <a href="${{createYouTubeLink(video.locator)}}" class="youtube-link-badge" title="Open in YouTube">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gauge-icon lucide-gauge" style="width:14px;height:14px;display:inline;"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>
                            </a>
                            ${{video.file ? '$<span style="color: var(--color7);">/</span> <a href="${{deepLink}}" class="deep-link-badge" title="Open in Obsidian"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-icon lucide-file" style="width:14px;height:14px;display:inline;"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/></svg></a>$' : ''}}
                            <span class="video-date">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-icon lucide-calendar" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>${{formatDate(video.date)}}
                            </span>
                        </div>
                        <div class="action-buttons">
                            <a href="${{inboxWatchedLink}}" class="btn btn-watched ${{isWatched ? 'active' : ''}}" title="Toggle watched + inbox">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-icon lucide-check" style="width:14px;height:14px;"><path d="M20 6 9 17l-5-5"/></svg> Watched
                            </a>
                            <a href="${{inboxLink}}" class="btn btn-inbox ${{isInboxActive ? 'active' : ''}}" title="Toggle inbox only">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-inbox-icon lucide-inbox" style="width:14px;height:14px;"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg> Inbox
                            </a>
                        </div>
                        <div class="tag-toggles">
                            ${{createTagToggles(video)}}
                        </div>
                    </div>
                </div>
            `;
        }}

        function renderStats() {{
            const totalVideos = videoData.length;
            const totalDuration = videoData.reduce((sum, v) => sum + v.duration, 0);

            const statsElement = document.getElementById('stats');
            statsElement.innerHTML = `${{totalVideos}} videos • ${{formatDuration(totalDuration)}} total`;
        }}

        function renderVideos() {{
            const videoGrid = document.getElementById('videoGrid');
            videoGrid.innerHTML = videoData.map((video, index) => createVideoCard(video, index)).join('');
        }}

        // Initialize the page
        renderStats();
        renderVideos();
    </script>
</body>
</html>"""
