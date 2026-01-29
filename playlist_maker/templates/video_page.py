"""Video collection page template"""


def get_video_page_html(title, pywal_css, json_data):
    """Generate the video collection page HTML"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
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
            padding-bottom: 56.25%;
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
            border-radius: 0;
            font-size: 0.75rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 3px;
            border: 1px solid var(--color7);
        }}

        .youtube-link-badge {{
            background: var(--color0);
            color: var(--foreground);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--color7);
            text-decoration: none;
            transition: all 0.2s;
            margin: 0 8px;
        }}

        .youtube-link-badge:hover {{
            border-color: var(--color4);
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
                            <a href="${{createYouTubeLink(video.locator)}}" class="youtube-link-badge" target="_blank" rel="noopener noreferrer" title="Open in YouTube">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-link-icon lucide-link" style="width:14px;height:14px;display:inline;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                            </a>
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
            statsElement.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin-right:4px;vertical-align:middle;"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg> ${{totalVideos}} videos • 
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin:0 4px 0 4px;vertical-align:middle;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${{formatDuration(totalDuration)}} total
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
