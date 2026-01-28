"""
Unified home page JavaScript code.
Extracted for better maintainability and debugging.
"""

def get_unified_page_javascript():
    """
    Return JavaScript code for the unified home page.

    This is extracted as a separate function to avoid:
    - Complex f-string escaping issues
    - Large, difficult-to-debug strings
    - Confusion between Python and JavaScript syntax
    """
    return """
        // Video fragment loading
        let currentVideoUrl = null;

        // Video link clicks - using window-level event delegation for reliability
        window.addEventListener('click', (e) => {
            const link = e.target.closest('.video-link');
            if (link) {
                e.preventDefault();
                const videoUrl = link.dataset.videoUrl;
                if (videoUrl) {
                    loadVideoFragment(videoUrl);
                }
            }
        });

        // Load video fragment dynamically
        async function loadVideoFragment(url) {
            const listContainer = document.getElementById('video-list-container');
            const fragmentContainer = document.getElementById('video-fragment-container');
            const videosContent = document.getElementById('videos-content');

            // Show loading state
            listContainer.style.display = 'none';
            fragmentContainer.style.display = 'block';
            fragmentContainer.innerHTML = '<div style="text-align: center; padding: 3rem;">Loading...</div>';

            try {
                const response = await fetch(url);
                const html = await response.text();

                // Parse the HTML
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');

                // Extract the header (title, stats)
                const header = doc.querySelector('.header');
                const stats = doc.querySelector('#stats');
                const videoGrid = doc.querySelector('#videoGrid');
                const videoScript = doc.querySelector('script');

                // Build fragment HTML
                let fragmentHtml = '';
                if (header) {
                    fragmentHtml += '<div class="header">' + header.innerHTML + '</div>';
                }
                if (stats) {
                    fragmentHtml += '<div id="stats">' + stats.innerHTML + '</div>';
                }
                if (videoGrid) {
                    fragmentHtml += '<div class="video-grid" id="videoGrid">' + videoGrid.innerHTML + '</div>';
                }

                // Render fragment
                fragmentContainer.innerHTML = fragmentHtml;

                // Execute the video page script to initialize functionality
                if (videoScript) {
                    const script = document.createElement('script');
                    script.textContent = videoScript.textContent;
                    fragmentContainer.appendChild(script);
                }

                currentVideoUrl = url;
            } catch (error) {
                console.error('Error loading video fragment:', error);
                fragmentContainer.innerHTML = '<div style="text-align: center; padding: 3rem;">Error loading video collection. <a href="#" onclick="showVideoList()">Try again</a></div>';
            }
        }

        // Show video list
        function showVideoList() {
            const listContainer = document.getElementById('video-list-container');
            const fragmentContainer = document.getElementById('video-fragment-container');

            listContainer.style.display = 'block';
            fragmentContainer.style.display = 'none';
            fragmentContainer.innerHTML = '';
            currentVideoUrl = null;
        }

        // Tab switching
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.dataset.tab;

                // Always reset video state when switching tabs
                const listContainer = document.getElementById('video-list-container');
                const fragmentContainer = document.getElementById('video-fragment-container');

                if (listContainer && fragmentContainer) {
                    // Reset containers to initial state
                    listContainer.style.display = 'block';
                    listContainer.style.visibility = 'visible';
                    fragmentContainer.style.display = 'none';
                    fragmentContainer.innerHTML = '';
                    currentVideoUrl = null;
                }

                // Remove active class from all tabs
                document.querySelectorAll('.tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });

                // Hide all tab content
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });

                // Activate clicked tab and show content
                button.classList.add('active');
                const targetContent = document.getElementById(tabId + '-content');
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });

        // Sub-tab switching
        document.querySelectorAll('.sub-tab-button').forEach(button => {
            button.addEventListener('click', () => {
                const subTabId = button.dataset.subtab;

                // Remove active class from all sub-tabs
                const parentSubTabs = button.closest('.sub-tabs');
                parentSubTabs.querySelectorAll('.sub-tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });

                // Hide all collections
                const allCollections = document.querySelectorAll('.collection');
                allCollections.forEach(collection => {
                    collection.classList.remove('active');
                });

                // Activate clicked sub-tab and show collection
                button.classList.add('active');
                const collectionElement = document.getElementById(subTabId + '-collection');
                if (collectionElement) {
                    collectionElement.classList.add('active');
                }
            });
        });

        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', () => {
            const baseUrl = 'obsidian://advanced-uri?vault=share&eval=';
            const command = `let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.marshallAllQueries(tp);`;
            window.location.href = baseUrl + encodeURIComponent(command);
        });

        // State toggle buttons
        document.querySelectorAll('.toggle-toggle').forEach(button => {
            button.addEventListener('click', (e) => {
                const row = e.target.closest('.data-row');
                const itemId = row.dataset.id;
                const itemType = row.dataset.type;
                const isToggleActive = button.classList.contains('toggle-active');
                const isToggleFocus = button.classList.contains('toggle-focus');

                // Toggle visual state
                if (isToggleActive) {
                    button.classList.toggle('active');
                    row.classList.toggle('active');
                } else if (isToggleFocus) {
                    button.classList.toggle('focused');
                    row.classList.toggle('focused');
                }

                // Send signal to Obsidian (placeholder - implement actual Obsidian command)
                console.log(`Toggle ${isToggleActive ? 'active' : 'focus'} for ${itemType} ${itemId}`);
                // TODO: Add actual Obsidian integration command
            });
        });

        // Title link clicks - open file in nvim
        document.querySelectorAll('.title-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const file = link.dataset.file;
                const line = link.dataset.line;

                const baseUrl = 'obsidian://advanced-uri?vault=share&eval=';
                const command = 'let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.openLineInNvim("' + file + '", ' + line + ');';
                window.location.href = baseUrl + encodeURIComponent(command);
            });
        });
    """
