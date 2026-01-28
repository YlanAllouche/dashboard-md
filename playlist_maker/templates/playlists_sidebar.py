"""Playlists sidebar template.

Displays playlists as a compact table on the side with links to each playlist.
"""


def get_playlists_sidebar_header():
    """Get the header for the playlists sidebar."""
    return """
    <div class="playlists-sidebar">
        <h2 class="sidebar-title">Playlists</h2>
        <table class="playlists-table">
            <tbody>
    """


def get_playlist_row(name, count, link):
    """
    Get a single playlist row.
    
    Args:
        name: Playlist name
        count: Number of videos
        link: Link to playlist page (usually stem.html)
    
    Returns:
        HTML for a single playlist table row
    """
    return f"""
                <tr class="playlist-row">
                    <td class="playlist-name"><a href="{link}">{name}</a></td>
                    <td class="playlist-count">{count}</td>
                </tr>
    """


def get_playlists_sidebar_footer():
    """Get the footer for the playlists sidebar."""
    return """
            </tbody>
        </table>
    </div>
    """
