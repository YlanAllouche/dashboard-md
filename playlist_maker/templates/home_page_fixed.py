// Lines 586-590 with properly escaped braces
            }}}}}});

        // Title link clicks - open file in nvim
        document.querySelectorAll('.title-link').forEach(link => {{
            link.addEventListener('click', (e) => {{
                e.preventDefault();
                const file = link.dataset.file;
                const line = link.dataset.line;

                const baseUrl = 'obsidian://advanced-uri?vault=share&eval=';
                const command = 'let tp = app.plugins.plugins["templater-obsidian"].templater.current_functions_object; tp.user.openLineInNvim(tp, "' + file + '", ' + line + ');';
                window.location.href = baseUrl + encodeURIComponent(command);
            }}}}}});
        }}});
