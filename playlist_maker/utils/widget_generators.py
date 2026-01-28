"""
Widget data generators.

Convert processed dashboard data into formatted HTML for widgets.
Handles styling, type indicators, and status colors.
"""

from typing import Dict, Any, List

try:
    from .dashboard_data import DashboardDataProcessor, format_entry_list_html
except ImportError:
    from dashboard_data import DashboardDataProcessor, format_entry_list_html


class WidgetDataGenerator:
    """Generate formatted widget HTML from dashboard data."""
    
    def __init__(self, data_processor: DashboardDataProcessor = None):
        """
        Initialize widget generator.
        
        Args:
            data_processor: DashboardDataProcessor instance. Creates new if None.
        """
        self.processor = data_processor or DashboardDataProcessor()
        self.data = self.processor.get_all_widget_data()
    
    # ========== INITIATIVES WIDGET ==========
    
    def get_initiatives_widget_data(self) -> Dict[str, str]:
        """
        Generate HTML for initiatives widget cells.
        
        Structure:
        ┌─────────────────┬──────────────┐
        │ Initiative      │ Projects     │
        ├─────────────────┼──────────────┤
        │ Focus           │ [HTML]       │
        │ Active          │ [HTML]       │
        │ Planned         │ [HTML]       │
        └─────────────────┴──────────────┘
        
        Returns:
            Dict with keys: focus, active, planned
            Each value is HTML string with entry tags
        """
        initiatives = self.data['initiatives']
        
        return {
            'focus': self._format_initiative_list(initiatives['focus']),
            'active': self._format_initiative_list(initiatives['active']),
            'planned': self._format_initiative_list(initiatives['planned']),
        }
    
    def _format_initiative_list(self, entries: List[Dict[str, Any]]) -> str:
        """
        Format list of initiatives with type and status styling.
        
        Args:
            entries: List of initiative dicts
        
        Returns:
            HTML string with formatted initiatives
        """
        if not entries:
            return '<span class="empty">—</span>'
        
        formatted = []
        for entry in entries:
            entry_type = entry.get('type', '').lower()  # 'work' or 'study'
            summary = entry.get('summary', 'Untitled')
            
            # Truncate if needed
            if len(summary) > 40:
                summary = summary[:37] + '...'
            
            # Create entry with type styling
            html = f'<span class="entry initiative-{entry_type}">{summary}</span>'
            formatted.append(html)
        
        return ' '.join(formatted)
    
    # ========== DASHBOARD WIDGET (TODO + MIND) ==========
    
    def get_dashboard_widget_data(self) -> Dict[str, str]:
        """
        Generate HTML for dashboard widget cells.
        
        Structure:
        ┌─────────────────┬──────────┬──────────┐
        │ Initiative      │ TODO     │ Mind     │
        ├─────────────────┼──────────┼──────────┤
        │ Focus           │ [HTML]   │ [HTML]   │
        │ Active          │ [HTML]   │ [HTML]   │
        └─────────────────┴──────────┴──────────┘
        
        Returns:
            Dict with keys: 
              todo_focus, todo_active, mind_focus, mind_active
        """
        todos = self.data['todos']
        minds = self.data['minds']
        
        return {
            'todo_focus': self._format_todo_list(todos['focus_todo']),
            'todo_active': self._format_todo_list(todos['active_todo']),
            'mind_focus': self._format_mind_list(minds['focus']),
            'mind_active': self._format_mind_list(minds['active']),
        }
    
    def _format_todo_list(self, entries: List[Dict[str, Any]]) -> str:
        """Format TODO items with count."""
        if not entries:
            return '<span class="empty">—</span>'
        
        # Show summary + count
        summary = entries[0].get('summary', 'Untitled')
        if len(summary) > 30:
            summary = summary[:27] + '...'
        
        count = len(entries)
        if count == 1:
            return f'<span class="entry todo">{summary}</span>'
        else:
            return f'<span class="entry todo">{summary}</span> <span class="count">+{count-1}</span>'
    
    def _format_mind_list(self, entries: List[Dict[str, Any]]) -> str:
        """Format mind items with count."""
        if not entries:
            return '<span class="empty">—</span>'
        
        # Show summary + count
        summary = entries[0].get('summary', 'Untitled')
        if len(summary) > 30:
            summary = summary[:27] + '...'
        
        count = len(entries)
        if count == 1:
            return f'<span class="entry mind">{summary}</span>'
        else:
            return f'<span class="entry mind">{summary}</span> <span class="count">+{count-1}</span>'
    
    # ========== PROGRESS WIDGET ==========
    
    def get_progress_widget_data(self) -> Dict[str, str]:
        """
        Generate HTML for progress widget cells.
        
        Structure:
        ┌─────────────────┬──────────────┐
        │ Initiative      │ Projects     │
        ├─────────────────┼──────────────┤
        │ Focus           │              │
        │ ├─ Progress     │ [HTML]       │
        │ └─ Async        │ [HTML]       │
        │ Active          │              │
        │ ├─ Progress     │ [HTML]       │
        │ └─ Async        │ [HTML]       │
        └─────────────────┴──────────────┘
        
        Returns:
            Dict with keys: 
              focus_progress, focus_async, active_progress, active_async
        """
        progress = self.data['progress']
        
        return {
            'focus_progress': self._format_progress_list(
                progress['focus']['progress'], 'focus'
            ),
            'focus_async': self._format_progress_list(
                progress['focus']['async'], 'focus'
            ),
            'active_progress': self._format_progress_list(
                progress['active']['progress'], 'active'
            ),
            'active_async': self._format_progress_list(
                progress['active']['async'], 'active'
            ),
        }
    
    def _format_progress_list(self, entries: List[Dict[str, Any]], status: str) -> str:
        """
        Format progress items with type and status styling.
        
        Args:
            entries: List of progress entry dicts
            status: 'focus' or 'active'
        
        Returns:
            HTML string with formatted progress items
        """
        if not entries:
            return '<span class="empty">—</span>'
        
        formatted = []
        for entry in entries[:3]:  # Show max 3 entries
            entry_type = entry.get('type', '').lower()
            summary = entry.get('summary', 'Untitled')
            
            # Truncate if needed
            if len(summary) > 30:
                summary = summary[:27] + '...'
            
            # Create entry with type styling
            html = f'<span class="entry progress progress-{entry_type}">{summary}</span>'
            formatted.append(html)
        
        count = len(entries)
        result = ' '.join(formatted)
        
        # Add count if more than shown
        if count > 3:
            result += f' <span class="count">+{count-3}</span>'
        
        return result
    
    # ========== MAIN API ==========
    
    def get_all_widget_html(self) -> Dict[str, Dict[str, str]]:
        """
        Get all widget data organized by widget type.
        
        Returns:
            Dict structure:
            {
                'initiatives': {
                    'focus': HTML,
                    'active': HTML,
                    'planned': HTML,
                },
                'dashboard': {
                    'todo_focus': HTML,
                    'todo_active': HTML,
                    'mind_focus': HTML,
                    'mind_active': HTML,
                },
                'progress': {
                    'focus_progress': HTML,
                    'focus_async': HTML,
                    'active_progress': HTML,
                    'active_async': HTML,
                }
            }
        """
        return {
            'initiatives': self.get_initiatives_widget_data(),
            'dashboard': self.get_dashboard_widget_data(),
            'progress': self.get_progress_widget_data(),
        }
    
    def get_replacement_dict(self) -> Dict[str, str]:
        """
        Get dict of all placeholders and their values for template.string.replace().
        
        Returns:
            Dict with placeholder keys and HTML values
        """
        initiatives = self.get_initiatives_widget_data()
        dashboard = self.get_dashboard_widget_data()
        progress = self.get_progress_widget_data()
        
        return {
            '{INITIATIVES_FOCUS}': initiatives['focus'],
            '{INITIATIVES_ACTIVE}': initiatives['active'],
            '{INITIATIVES_PLANNED}': initiatives['planned'],
            '{DASHBOARD_TODO_FOCUS}': dashboard['todo_focus'],
            '{DASHBOARD_TODO_ACTIVE}': dashboard['todo_active'],
            '{DASHBOARD_MIND_FOCUS}': dashboard['mind_focus'],
            '{DASHBOARD_MIND_ACTIVE}': dashboard['mind_active'],
            '{PROGRESS_FOCUS_PROGRESS}': progress['focus_progress'],
            '{PROGRESS_FOCUS_ASYNC}': progress['focus_async'],
            '{PROGRESS_ACTIVE_PROGRESS}': progress['active_progress'],
            '{PROGRESS_ACTIVE_ASYNC}': progress['active_async'],
        }
