// Video data from JSON file
const videoData = {VIDEO_DATA};

const placeholderThumbnails = ['🎬', '📺', '🎥', '🎞️', '📹', '🎪', '🎭', '🎨', '🎯', '🎲'];

// Tag definitions with SVG glyphs and labels
const tagDefinitions = [
    { name: 'focus', glyph: '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/></svg>', label: 'Focus' },
    { name: 'entertain', glyph: '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><path d="M2 12a10 10 0 0110-10 10 10 0 0110 10 10 10 0 01-10 10A10 10 0 012 12z"/><path d="M9 8a1 1 0 011-1h2a1 1 0 011 1v3a1 1 0 01-1 1h-2a1 1 0 01-1-1V8z" fill="white"/><path d="M14 9a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 01-1 1h-2a1 1 0 01-1-1V9z" fill="white"/></svg>', label: 'Fun' },
    { name: 'tv', glyph: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><polyline points="17 2 12 7 7 2"/></svg>', label: 'TV' },
    { name: 'walk', glyph: '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><circle cx="12" cy="3" r="2"/><path d="M12 8v2m0 0l-4 4m4-4l4 4m0 0v3a2 2 0 01-4 0v-1a2 2 0 00-4 0v1a2 2 0 01-4 0v-3"/></svg>', label: 'Walk' },
    { name: 'bed', glyph: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M2 4v16a2 2 0 002 2h16a2 2 0 002-2V4"/><line x1="2" y1="9" x2="22" y2="9"/><rect x="2" y="4" width="20" height="5"/></svg>', label: 'Bed' },
    { name: 'tech', glyph: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="2" y1="17" x2="22" y2="17"/><line x1="6" y1="21" x2="18" y2="21"/></svg>', label: 'Tech' }
];

function createObsidianLink(command) {
    const baseUrl = 'obsidian://advanced-uri?vault=share&eval=';
    return baseUrl + encodeURIComponent(command);
}

function createPlayLink(locator) {
    const command = `app.plugins.plugins["templater-obsidian"].templater.current_functions_object.user.captureMdPlay("${locator}")`;
    return createObsidianLink(command);
}

function createInboxWatchedToggleLink(id) {
    const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.toggleInbox(tp, "${id}");tp.user.toggleWatched(tp,"${id}");`;
    return createObsidianLink(command);
}

function createInboxToggleLink(id) {
    const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.toggleInbox(tp,"${id}");`;
    return createObsidianLink(command);
}

function createTagToggleLink(id, tag) {
    const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.toggleTag(tp,"${id}", "${tag}");`;
    return createObsidianLink(command);
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
    });
}

function createTagToggles(video) {
    return tagDefinitions.map(tagDef => {
        const isActive = video.tags?.includes(tagDef.name);
        const statusSvg = isActive ? '<svg viewBox="0 0 24 24" fill="currentColor" style="width:12px;height:12px;"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>' : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><circle cx="12" cy="12" r="10"/></svg>';
        const statusClass = isActive ? 'active' : 'inactive';
        const link = createTagToggleLink(video.id, tagDef.name);
        
        return `<a href="${link}" class="tag-toggle ${statusClass}" title="${tagDef.name}: ${isActive ? 'Active' : 'Inactive'}">
            <span style="display:inline-flex;align-items:center;gap:3px;">
                <span style="width:12px;height:12px;display:inline-flex;">${statusSvg}</span>
                <span style="width:14px;height:14px;display:inline-flex;">${tagDef.glyph}</span>
            </span> ${tagDef.label}
        </a>`;
    }).join('');
}

function createVideoCard(video, index) {
    const isInboxActive = video.tags?.includes('inbox');
    const isWatched = video.watched;
    const isStarred = video.tags?.includes('starred');
    const watchedClass = isWatched ? 'watched' : '';

    const thumbnailContent = video.thumbnail
        ? `<img src="${video.thumbnail}" alt="${video.summary}" class="thumbnail" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
           <div class="placeholder-thumbnail" style="display: none;">${placeholderThumbnails[index % placeholderThumbnails.length]}</div>`
        : `<div class="placeholder-thumbnail">${placeholderThumbnails[index % placeholderThumbnails.length]}</div>`;

    const playLink = createPlayLink(video.locator);
    const inboxWatchedLink = createInboxWatchedToggleLink(video.id);
    const inboxLink = createInboxToggleLink(video.id);
    const starredLink = createTagToggleLink(video.id, 'starred');

    return `
        <div class="video-card ${watchedClass}" data-id="${video.id}">
            <div class="thumbnail-container">
                <a href="${playLink}" class="thumbnail-link">
                    ${thumbnailContent}
                    <div class="play-button">
                        <svg viewBox="0 0 24 24" fill="currentColor" style="width:48px;height:48px;">
                            <polygon points="5 3 19 12 5 21 5 3"/>
                        </svg>
                    </div>
                </a>
                <a href="${starredLink}" class="starred-button ${isStarred ? 'active' : 'inactive'}" title="Toggle starred">
                    <span style="display:inline-flex;align-items:center;justify-content:center;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="${isStarred ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-star-icon lucide-star" style="width:20px;height:20px;"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/></svg>
                    </span>
                </a>
                <div class="duration-badge">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:2px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${formatDuration(video.duration)}
                </div>
                <div class="watched-indicator"></div>
            </div>
            <div class="card-content">
                <h3 class="video-title">${video.summary}</h3>
                <div class="video-meta">
                    <span class="channel-name">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>${video.channel}
                    </span>
                    <span class="video-date">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>${formatDate(video.date)}
                    </span>
                </div>
                <div class="action-buttons">
                    <a href="${inboxWatchedLink}" class="btn btn-watched ${isWatched ? 'active' : ''}" title="Toggle watched + inbox">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M20 6L9 17l-5-5"/></svg> Watched
                    </a>
                    <a href="${inboxLink}" class="btn btn-inbox ${isInboxActive ? 'active' : ''}" title="Toggle inbox only">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M22 12h-7l-2 5H9l-2-5H2"/><path d="M5.45 5.11L2 12v6a2 2 0 002 2h16a2 2 0 002-2v-6l-3.45-6.89A2 2 0 0016.88 4H7.12a2 2 0 00-1.67 1.11z"/></svg> Inbox
                    </a>
                </div>
                <div class="tag-toggles">
                    ${createTagToggles(video)}
                </div>
            </div>
        </div>
    `;
}

function renderStats() {
    const totalVideos = videoData.length;
    const watchedVideos = videoData.filter(v => v.watched).length;
    const totalDuration = videoData.reduce((sum, v) => sum + v.duration, 0);
    const watchedDuration = videoData.filter(v => v.watched).reduce((sum, v) => sum + v.duration, 0);
    
    const statsElement = document.getElementById('stats');
    statsElement.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin-right:4px;vertical-align:middle;"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg> ${totalVideos} videos • 
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin:0 4px 0 4px;vertical-align:middle;"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg> ${watchedVideos} watched • 
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;display:inline;margin:0 4px 0 4px;vertical-align:middle;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${formatDuration(totalDuration)} total • 
        <svg viewBox="0 0 24 24" fill="currentColor" style="width:16px;height:16px;display:inline;margin:0 4px 0 4px;vertical-align:middle;"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg> ${formatDuration(watchedDuration)} watched
    `;
}

function renderVideos() {
    const videoGrid = document.getElementById('videoGrid');
    videoGrid.innerHTML = videoData.map((video, index) => createVideoCard(video, index)).join('');
}

// Initialize the page
renderStats();
renderVideos();
