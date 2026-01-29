"""SVG icon definitions for the playlist maker"""


class SVGIcons:
    """Collection of SVG icons used in the UI"""

    STAR_FILLED = '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 10.26 24 10.26 17.55 16.52 19.64 24.78 12 19.52 4.36 24.78 6.45 16.52 0 10.26 8.91 10.26 12 2"/></svg>'
    STAR_EMPTY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="12 2 15.09 10.26 24 10.26 17.55 16.52 19.64 24.78 12 19.52 4.36 24.78 6.45 16.52 0 10.26 8.91 10.26 12 2"/></svg>'
    CHECK = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>'
    CIRCLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>'
    CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
    USER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
    CALENDAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
    INBOX = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-7l-2 5H9l-2-5H2"/><path d="M5.45 5.11L2 12v6a2 2 0 002 2h16a2 2 0 002-2v-6l-3.45-6.89A2 2 0 0016.88 4H7.12a2 2 0 00-1.67 1.11z"/></svg>'
    CHECKMARK_ALT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>'
    FILM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/></svg>'
    EYE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>'
    STATS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'
    QUESTION_MARK = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>'

    # Status icon mapping
    STATUS_ICONS = {
        '?': QUESTION_MARK,
        'w': QUESTION_MARK,
        't': QUESTION_MARK,
    }

    # Tag icons
    FOCUS = '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/></svg>'
    FUN = '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><path d="M2 12a10 10 0 0110-10 10 10 0 0110 10 10 10 0 01-10 10A10 10 0 012 12z"/><path d="M9 8a1 1 0 011-1h2a1 1 0 011 1v3a1 1 0 01-1 1h-2a1 1 0 01-1-1V8z" fill="white"/><path d="M14 9a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 01-1 1h-2a1 1 0 01-1-1V9z" fill="white"/></svg>'
    TV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><polyline points="17 2 12 7 7 2"/></svg>'
    WALK = '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px;"><circle cx="12" cy="3" r="2"/><path d="M12 8v2m0 0l-4 4m4-4l4 4m0 0v3a2 2 0 01-4 0v-1a2 2 0 00-4 0v1a2 2 0 01-4 0v-3"/></svg>'
    BED = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M2 4v16a2 2 0 002 2h16a2 2 0 002-2V4"/><line x1="2" y1="9" x2="22" y2="9"/><rect x="2" y="4" width="20" height="5"/></svg>'
    TECH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="2" y1="17" x2="22" y2="17"/><line x1="6" y1="21" x2="18" y2="21"/></svg>'

    @staticmethod
    def get_all_tag_glyphs():
        """Return mapping of tag names to their SVG glyphs"""
        return {
            'focus': SVGIcons.FOCUS,
            'entertain': SVGIcons.FUN,
            'tv': SVGIcons.TV,
            'walk': SVGIcons.WALK,
            'bed': SVGIcons.BED,
            'tech': SVGIcons.TECH,
        }

    @staticmethod
    def get_status_icon(status: str):
        """Get SVG icon for a status value, returns None if no icon defined"""
        return SVGIcons.STATUS_ICONS.get(status)
