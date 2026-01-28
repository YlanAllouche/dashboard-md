#!/usr/bin/env python3
import json
import os
import sys
import urllib.parse
from pathlib import Path


def get_svg_icons():
    """Return a dictionary of SVG icons"""
    return {
        "play": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
        "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        "star_filled": '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 10.26 24 10.26 17.55 16.52 19.64 24.78 12 19.52 4.36 24.78 6.45 16.52 0 10.26 8.91 10.26 12 2"/></svg>',
        "star_empty": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 10.26 24 10.26 17.55 16.52 19.64 24.78 12 19.52 4.36 24.78 6.45 16.52 0 10.26 8.91 10.26 12 2"/></svg>',
        "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>',
        "inbox": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-7l-2 5H9l-2-5H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.88 4H7.12a2 2 0 0 0-1.67 1.11z"/></svg>',
        "stats": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
        "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "film": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/></svg>',
    }


def extract_pywal_colors():
    """Load colors from ~/.cache/wal/colors.css"""
    try:
        colors_css = Path.home() / ".cache" / "wal" / "colors.css"
        if colors_css.exists():
            with open(colors_css, "r", encoding="utf-8") as f:
                content = f.read()
                # Parse CSS variables
                colors = {}
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('--'):
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip().rstrip(';')
                            colors[key] = value
                return content  # Return the raw CSS to inject directly
    except Exception:
        pass
    
    # Default fallback CSS
    return """
    :root {
        --wallpaper: url("None");
        --background: #1a1a2e;
        --foreground: #ffffff;
        --cursor: #ffffff;
        --color0: #000000;
        --color1: #ee5396;
        --color2: #5eca89;
        --color3: #f0c674;
        --color4: #668ee8;
        --color5: #a78bfa;
        --color6: #2dd4bf;
        --color7: #ffffff;
        --color8: #666666;
        --color9: #ee5396;
        --color10: #5eca89;
        --color11: #f0c674;
        --color12: #668ee8;
        --color13: #a78bfa;
        --color14: #2dd4bf;
        --color15: #ffffff;
    }
    """


def format_title(filename):
    """Convert filename to a nice title format"""
    # Remove extension
    name = Path(filename).stem
    # Replace underscores and hyphens with spaces
    name = name.replace("_", " ").replace("-", " ")
    # Capitalize each word
    return " ".join(word.capitalize() for word in name.split())


def validate_video_data(data):
    """Validate that the JSON data is suitable for video processing"""
    if not isinstance(data, list):
        return False, "Not a list"

    if len(data) == 0:
        return False, "Empty list"

    # Check if at least some items have the required video fields
    required_fields = ["id", "summary", "duration", "channel", "date", "locator"]
    valid_items = 0

    for item in data[:5]:  # Check first 5 items
        if not isinstance(item, dict):
            continue

        if all(field in item for field in required_fields):
            valid_items += 1

    if valid_items == 0:
        return False, "No items with required video fields found"

    return True, "Valid video data"


def sanitize_video_data(data):
    """Clean and ensure video data has all required fields with defaults"""
    sanitized = []

    for item in data:
        if not isinstance(item, dict):
            continue

        # Check for required fields
        required_fields = ["id", "summary", "duration", "channel", "date", "locator"]
        if not all(field in item for field in required_fields):
            continue

        # Ensure all fields have proper types and defaults
        sanitized_item = {
            "id": str(item.get("id", "")),
            "summary": str(item.get("summary", "Untitled Video")),
            "duration": int(item.get("duration", 0)),
            "channel": str(item.get("channel", "Unknown Channel")),
            "date": str(item.get("date", "2024-01-01")),
            "locator": str(item.get("locator", "")),
            "thumbnail": item.get("thumbnail", ""),
            "watched": bool(item.get("watched", False)),
            "tags": item.get("tags", []) if isinstance(item.get("tags"), list) else [],
        }

        # Skip if essential fields are empty
        if not sanitized_item["id"] or not sanitized_item["locator"]:
            continue

        sanitized.append(sanitized_item)

    return sanitized


def generate_home_page(output_dir, successful_files):
    """Generate a home page that lists all available playlists"""

    # Sort by title
    successful_files.sort(key=lambda x: x["title"])
    
    # Get pywal colors
    pywal_css = extract_pywal_colors()

    home_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Collection Dashboard</title>
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

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}

        .header {{
            text-align: center;
            margin-bottom: 3rem;
            color: var(--foreground);
        }}

        .header h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            font-size: 1.2rem;
            opacity: 0.8;
        }}

        .playlist-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .playlist-card {{
            background: var(--color0);
            border-radius: 24px;
            padding: 2rem;
            text-align: center;
            box-shadow: none;
            transition: all 0.2s ease;
            text-decoration: none;
            color: var(--foreground);
            border: 2px solid var(--color7);
        }}

        .playlist-card:hover {{
            transform: none;
            border-color: var(--color4);
            background: var(--color8);
        }}

        .playlist-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }}

        .playlist-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--foreground);
            margin-bottom: 0.5rem;
        }}

        .playlist-subtitle {{
            font-size: 0.9rem;
            color: var(--color7);
            margin-bottom: 1rem;
        }}

        .playlist-stats {{
            font-size: 0.8rem;
            color: var(--color6);
            margin-bottom: 1.5rem;
        }}

        .playlist-button {{
            background: var(--color4);
            color: var(--color0);
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 16px;
            font-weight: 500;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
        }}

        .playlist-button:hover {{
            opacity: 0.8;
        }}

        .footer {{
            text-align: center;
            color: white;
            opacity: 0.8;
            margin-top: 3rem;
        }}

        .empty-state {{
            text-align: center;
            color: white;
            margin: 4rem 0;
        }}

        .empty-state h2 {{
            font-size: 2rem;
            margin-bottom: 1rem;
            opacity: 0.8;
        }}

        .empty-state p {{
            font-size: 1.1rem;
            opacity: 0.7;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem 0.5rem;
            }}

            .header h1 {{
                font-size: 2.5rem;
            }}

            .playlist-grid {{
                grid-template-columns: 1fr;
                gap: 1rem;
            }}

            .playlist-card {{
                padding: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:48px;height:48px;display:inline;margin-right:12px;vertical-align:middle;"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/></svg> Video Dashboard</h1>
            <p>Your personalized video collection manager</p>
        </div>
        
"""

    if successful_files:
        home_html += '<div class="playlist-grid">'

        # Add cards for each successful file
        playlist_icons = [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]

        for i, file_info in enumerate(successful_files):
            icon = playlist_icons[i % len(playlist_icons)]
            home_html += f"""
            <a href="{file_info['stem']}.html" class="playlist-card">
                <span class="playlist-icon">{icon}</span>
                <div class="playlist-title">{file_info['title']}</div>
                <div class="playlist-subtitle">Video Collection</div>
                <div class="playlist-stats">{file_info['count']} videos</div>
                <div class="playlist-button">View Collection </div>
            </a>
"""

        home_html += "</div>"
    else:
        home_html += """
        <div class="empty-state">
             <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:36px;height:36px;display:inline;margin-right:8px;vertical-align:middle;"><path d="M3 12h18"/><path d="M12 3v18"/><circle cx="12" cy="12" r="10"/></svg> No Video Collections Found</h2>
             <p>Add some JSON files with video data to get started</p>
         </div>
"""

    home_html += f"""
        <div class="footer">
            <p>Generated by Video Collection Manager • {len(successful_files)} collections available</p>
        </div>
    </div>
</body>
</html>"""

    return home_html


def generate_html(json_data, title):
    """Generate the complete HTML with embedded JSON data"""
    
    # Get pywal colors
    pywal_css = extract_pywal_colors()

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}

        .header {{
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
        }}

        .home-link {{
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            background: var(--color4);
            color: var(--color0);
            padding: 0.5rem 1rem;
            border-radius: 12px;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .home-link:hover {{
            opacity: 0.8;
        }}

        .header h1 {{
            color: var(--foreground);
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            color: var(--color7);
            font-size: 1.1rem;
        }}

        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.5rem;
        }}

        .video-card {{
            background: var(--color0);
            border-radius: 20px;
            box-shadow: none;
            transition: all 0.2s;
            overflow: hidden;
            border: 1px solid var(--color7);
        }}

        .video-card:hover {{
            border-color: var(--color4);
        }}

        .thumbnail-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            overflow: hidden;
            background: var(--color8);
            cursor: pointer;
        }}

        .thumbnail {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }}

        .video-card:hover .thumbnail {{
            transform: scale(1.05);
        }}

         .duration-badge {{
             position: absolute;
             bottom: 8px;
             right: 8px;
             background: var(--color0);
             color: var(--foreground);
             padding: 4px 8px;
             border-radius: 12px;
             font-size: 0.75rem;
             font-weight: 500;
             display: flex;
             align-items: center;
             gap: 3px;
             border: 1px solid var(--color7);
         }}



        .card-content {{
            padding: 1rem;
        }}

         .video-title {{
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

         .video-meta {{
             display: flex;
             justify-content: space-between;
             align-items: center;
             margin-bottom: 1rem;
             font-size: 0.875rem;
             color: var(--color7);
         }}

         .channel-name {{
             font-weight: 500;
             color: var(--color7);
             display: flex;
             align-items: center;
             gap: 5px;
         }}

         .video-date {{
             font-size: 0.8rem;
             display: flex;
            align-items: center;
            gap: 4px;
        }}

        .action-buttons {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

         .btn {{
             flex: 1;
             padding: 0.5rem 0.75rem;
             border: 1px solid var(--color7);
             border-radius: 12px;
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

         .btn-inbox {{
             background: var(--color0);
             color: var(--foreground);
             border: 1px solid var(--color7);
         }}

         .btn-inbox:hover {{
             border-color: var(--color4);
         }}

         .btn-inbox.active {{
             background: var(--color4);
             color: var(--color0);
             border-color: var(--color4);
         }}

         .btn-watched {{
             background: var(--color0);
             color: var(--foreground);
             border: 1px solid var(--color7);
         }}

         .btn-watched:hover {{
             border-color: var(--color2);
         }}

         .btn-watched.active {{
             background: var(--color2);
             color: var(--color0);
             border-color: var(--color2);
         }}

         .watched-indicator {{
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

         .video-card.watched .watched-indicator {{
             opacity: 1;
         }}

         .starred-button {{
             position: absolute;
             top: 8px;
             right: 8px;
             width: 40px;
             height: 40px;
             background: var(--color0);
             border: 2px solid var(--color7);
             border-radius: 50%;
             display: flex;
             align-items: center;
             justify-content: center;
             font-size: 1.2rem;
             cursor: pointer;
             transition: all 0.2s;
             text-decoration: none;
             box-shadow: none;
         }}

         .starred-button:hover {{
             border-color: var(--color3);
         }}

         .starred-button.active {{
             color: var(--color3);
             border-color: var(--color3);
         }}

         .starred-button.inactive {{
             color: var(--color7);
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
             background: var(--color8);
             color: var(--foreground);
         }}

        .tag-toggles {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.4rem;
            margin-top: 0.5rem;
        }}

         .tag-toggle {{
             display: flex;
             align-items: center;
             justify-content: center;
             gap: 3px;
             padding: 0.4rem 0.5rem;
             border-radius: 12px;
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

         .tag-toggle:hover {{
             border-color: var(--color4);
         }}

         .tag-toggle.active {{
             background: var(--color2);
             border-color: var(--color2);
             color: var(--color0);
         }}

         .tag-toggle.inactive {{
             background: var(--color1);
             border-color: var(--color1);
             color: var(--color0);
         }}

        .icon {{
            width: 14px;
            height: 14px;
            fill: currentColor;
        }}

        .emoji {{
            font-style: normal;
            font-size: 1em;
        }}

         .stats {{
             margin-bottom: 2rem;
             text-align: center;
             color: var(--color7);
             font-size: 0.9rem;
         }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem 0.5rem;
            }}

            .video-grid {{
                grid-template-columns: 1fr;
                gap: 1rem;
            }}

            .header h1 {{
                font-size: 2rem;
            }}

            .home-link {{
                position: static;
                transform: none;
                display: inline-block;
                margin-bottom: 1rem;
            }}

            .btn {{
                font-size: 0.75rem;
                padding: 0.4rem 0.6rem;
            }}

            .tag-toggle {{
                font-size: 0.7rem;
                padding: 0.3rem 0.4rem;
            }}

            .tag-toggles {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.3rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
         <div class="header">
             <a href="index.html" class="home-link">← Home</a>
             <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:32px;height:32px;display:inline;margin-right:8px;vertical-align:middle;"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/></svg> {title}</h1>
             <p>Manage your video collection</p>
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
        const videoData = {json.dumps(json_data, indent=8)};

        const placeholderThumbnails = ['🎬', '📺', '🎥', '🎞️', '📹', '🎪', '🎭', '🎨', '🎯', '🎲'];

        // Tag definitions with SVG glyphs and labels
        const tagDefinitions = [
            {{ name: 'focus', glyph: '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/></svg>', label: 'Focus' }},
            {{ name: 'entertain', glyph: '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><path d="M2 12a10 10 0 0110-10 10 10 0 0110 10 10 10 0 01-10 10A10 10 0 012 12z"/><path d="M9 8a1 1 0 011-1h2a1 1 0 011 1v3a1 1 0 01-1 1h-2a1 1 0 01-1-1V8z" fill="white"/><path d="M14 9a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 01-1 1h-2a1 1 0 01-1-1V9z" fill="white"/></svg>', label: 'Fun' }},
            {{ name: 'tv', glyph: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><polyline points="17 2 12 7 7 2"/></svg>', label: 'TV' }},
            {{ name: 'walk', glyph: '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><circle cx="12" cy="3" r="2"/><path d="M12 8v2m0 0l-4 4m4-4l4 4m0 0v3a2 2 0 01-4 0v-1a2 2 0 00-4 0v1a2 2 0 01-4 0v-3"/></svg>', label: 'Walk' }},
            {{ name: 'bed', glyph: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M2 4v16a2 2 0 002 2h16a2 2 0 002-2V4"/><line x1="2" y1="9" x2="22" y2="9"/><rect x="2" y="4" width="20" height="5"/></svg>', label: 'Bed' }},
            {{ name: 'tech', glyph: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="2" y1="17" x2="22" y2="17"/><line x1="6" y1="21" x2="18" y2="21"/></svg>', label: 'Tech' }}
        ];

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
                 const statusSvg = isActive ? '<svg viewBox="0 0 24 24" fill="currentColor" style="width:12px;height:12px;"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>' : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><circle cx="12" cy="12" r="10"/></svg>';
                 const statusClass = isActive ? 'active' : 'inactive';
                 const link = createTagToggleLink(video.id, tagDef.name);
                 
                 return `<a href="${{link}}" class="tag-toggle ${{statusClass}}" title="${{tagDef.name}}: ${{isActive ? 'Active' : 'Inactive'}}">
                     <span style="display:inline-flex;align-items:center;gap:3px;">
                         <span style="width:12px;height:12px;display:inline-flex;">${{statusSvg}}</span>
                         <span style="width:14px;height:14px;display:inline-flex;">${{tagDef.glyph}}</span>
                     </span> ${{tagDef.label}}
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
                             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:2px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${{formatDuration(video.duration)}}
                         </div>
                         <div class="watched-indicator"></div>
                     </div>
                     <div class="card-content">
                         <h3 class="video-title">${{video.summary}}</h3>
                         <div class="video-meta">
                             <span class="channel-name">
                                 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>${{video.channel}}
                             </span>
                             <span class="video-date">
                                 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>${{formatDate(video.date)}}
                             </span>
                         </div>
                         <div class="action-buttons">
                             <a href="${{inboxWatchedLink}}" class="btn btn-watched ${{isWatched ? 'active' : ''}}" title="Toggle watched + inbox">
                                 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M20 6L9 17l-5-5"/></svg> Watched
                             </a>
                             <a href="${{inboxLink}}" class="btn btn-inbox ${{isInboxActive ? 'active' : ''}}" title="Toggle inbox only">
                                 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M22 12h-7l-2 5H9l-2-5H2"/><path d="M5.45 5.11L2 12v6a2 2 0 002 2h16a2 2 0 002-2v-6l-3.45-6.89A2 2 0 0016.88 4H7.12a2 2 0 00-1.67 1.11z"/></svg> Inbox
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
             const watchedVideos = videoData.filter(v => v.watched).length;
             const totalDuration = videoData.reduce((sum, v) => sum + v.duration, 0);
             const watchedDuration = videoData.filter(v => v.watched).reduce((sum, v) => sum + v.duration, 0);
             
             const statsElement = document.getElementById('stats');
             statsElement.innerHTML = `
                 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin-right:4px;vertical-align:middle;"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg> ${{totalVideos}} videos • 
                 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin:0 4px 0 4px;vertical-align:middle;"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg> ${{watchedVideos}} watched • 
                 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin:0 4px 0 4px;vertical-align:middle;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${{formatDuration(totalDuration)}} total • 
                 <svg viewBox="0 0 24 24" fill="currentColor" style="width:16px;height:16px;display:inline;margin:0 4px 0 4px;vertical-align:middle;"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> ${{formatDuration(watchedDuration)}} watched
             `;
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

    return html_template


def main():
    # Hardcoded folder path
    folder_path = Path.home() / "share" / "_tmp"

    # Check if folder exists
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' not found.")
        print("Please create the folder or update the hardcoded path in the script.")
        sys.exit(1)

    print(f"Scanning folder: {folder_path}")

    # Find all JSON files
    json_files = list(folder_path.glob("*.json"))

    if not json_files:
        print("No JSON files found in the folder.")
        sys.exit(1)

    print(f"Found {len(json_files)} JSON files")

    successful_files = []
    failed_files = []

    # Process each JSON file
    for json_file_path in json_files:
        filename = json_file_path.name
        stem = json_file_path.stem
        title = format_title(stem)

        print(f"\nProcessing: {filename}")

        try:
            # Read and parse JSON
            with open(json_file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            # Validate the data
            is_valid, reason = validate_video_data(json_data)
            if not is_valid:
                print(f"  Skipped: {reason}")
                failed_files.append({"filename": filename, "reason": reason})
                continue

            # Sanitize the data
            sanitized_data = sanitize_video_data(json_data)

            if len(sanitized_data) == 0:
                print(f"  Skipped: No valid video items after sanitization")
                failed_files.append(
                    {"filename": filename, "reason": "No valid video items"}
                )
                continue

            # Generate HTML
            html_content = generate_html(sanitized_data, title)

            # Write HTML file
            output_path = folder_path / f"{stem}.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            successful_files.append(
                {
                    "filename": filename,
                    "stem": stem,
                    "title": title,
                    "count": len(sanitized_data),
                }
            )

            print(f"  Generated: {output_path.name}")
            print(f"  Videos: {len(sanitized_data)}")

        except json.JSONDecodeError as e:
            reason = f"Invalid JSON: {str(e)[:50]}..."
            print(f"  Failed: {reason}")
            failed_files.append({"filename": filename, "reason": reason})
            continue
        except Exception as e:
            reason = f"Error: {str(e)[:50]}..."
            print(f"  Failed: {reason}")
            failed_files.append({"filename": filename, "reason": reason})
            continue

    # Generate home page
    home_path = folder_path / "index.html"
    home_content = generate_home_page(folder_path, successful_files)

    with open(home_path, "w", encoding="utf-8") as f:
        f.write(home_content)

    print(f"\nGenerated home page: {home_path}")

    # Summary
    print(f"\nSummary:")
    print(f"  Successfully processed: {len(successful_files)} files")
    print(f"  Failed/Skipped: {len(failed_files)} files")

    if successful_files:
        print(f"\nAvailable collections:")
        for file_info in successful_files:
            print(f"  • {file_info['title']} ({file_info['count']} videos)")

    if failed_files:
        print(f"\nSkipped files:")
        for file_info in failed_files:
            print(f"  • {file_info['filename']}: {file_info['reason']}")


if __name__ == "__main__":
    main()
