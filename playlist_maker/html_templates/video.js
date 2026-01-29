// Video data from JSON file
const videoData = {VIDEO_DATA};

// Tags data from -tags.json
const tagsData = {TAGS_DATA};

const placeholderThumbnails = ['🎬', '📺', '🎥', '🎞️', '📹', '🎪', '🎭', '🎨', '🎯', '🎲'];

// Tag definitions from tagsData
const tagDefinitions = Object.entries(tagsData).map(([name, value]) => ({
    name,
    glyph: value,
    label: value
}));

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

function createYouTubeLink(locator) {
    return `https://youtube.com/watch?v=${locator}`;
}

function createDeepLink(file, line) {
    const lineStr = String(line);
    const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.openLineInNvim("${file}", ${lineStr});`;
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
        const statusClass = isActive ? 'active' : 'inactive';
        const link = createTagToggleLink(video.id, tagDef.name);

        return `<a href="${link}" class="tag-toggle ${statusClass}" title="${tagDef.name}: ${isActive ? 'Active' : 'Inactive'}">
            ${tagDef.glyph}
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
            const deepLink = video.file ? createDeepLink(`~/share/${video.file}`, video.line) : null;

    return `
        <div class="video-card ${watchedClass}" data-id="${video.id}">
            <div class="thumbnail-container">
                <a href="${playLink}" class="thumbnail-link">
                    ${thumbnailContent}
                </a>
                <a href="${starredLink}" class="starred-button ${isStarred ? 'active' : 'inactive'}" title="Toggle starred">
                    <span style="display:inline-flex;align-items:center;justify-content:center;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="${isStarred ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-star-icon lucide-star" style="width:20px;height:20px;"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/></svg>
                    </span>
                </a>
                <div class="duration-badge">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-clock-icon lucide-clock" style="width:14px;height:14px;display:inline;"><path d="M12 6v6l4 2"/><circle cx="12" cy="12" r="10"/></svg> ${formatDuration(video.duration)}
                </div>
                <div class="watched-indicator"></div>
            </div>
            <div class="card-content">
                <h3 class="video-title">${video.summary}</h3>
                <div class="video-meta">
                    <span class="channel-name">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-icon lucide-user" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>${video.channel}
                    </span>
                    <a href="${createYouTubeLink(video.locator)}" class="youtube-link-badge" target="_blank" rel="noopener noreferrer" title="Open in YouTube">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-link-icon lucide-link" style="width:14px;height:14px;display:inline;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                    </a>
                    ${video.file ? `<span style="color: var(--color7);">/</span> <a href="${deepLink}" class="deep-link-badge" title="Open in Obsidian"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-icon lucide-file" style="width:14px;height:14px;display:inline;"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/></svg></a>` : ''}
                    <span class="video-date">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-icon lucide-calendar" style="width:14px;height:14px;display:inline;margin-right:4px;vertical-align:middle;"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>${formatDate(video.date)}
                    </span>
                </div>
                <div class="action-buttons">
                    <a href="${inboxWatchedLink}" class="btn btn-watched ${isWatched ? 'active' : ''}" title="Toggle watched + inbox">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-icon lucide-check" style="width:14px;height:14px;"><path d="M20 6 9 17l-5-5"/></svg> Watched
                    </a>
                    <a href="${inboxLink}" class="btn btn-inbox ${isInboxActive ? 'active' : ''}" title="Toggle inbox only">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-inbox-icon lucide-inbox" style="width:14px;height:14px;"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg> Inbox
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
    const totalDuration = videoData.reduce((sum, v) => sum + v.duration, 0);
    
    const statsElement = document.getElementById('stats');
    statsElement.innerHTML = `${totalVideos} videos • ${formatDuration(totalDuration)} total`;
}

function renderVideos() {
    const videoGrid = document.getElementById('videoGrid');
    videoGrid.innerHTML = videoData.map((video, index) => createVideoCard(video, index)).join('');
}

// Initialize the page
renderStats();
renderVideos();
