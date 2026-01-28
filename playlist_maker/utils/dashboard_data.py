"""
Dashboard data processing and mapping.

Loads and processes JSON data files to populate dashboard widgets.
Handles overlapping entries and prioritization rules.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict


class DashboardDataProcessor:
    """Process and organize data for dashboard widgets."""
    
    def __init__(self, data_dir: str = "~/share/_tmp"):
        """
        Initialize data processor.
        
        Args:
            data_dir: Directory containing JSON data files
        """
        self.data_dir = Path(data_dir).expanduser()
        self.data = {}
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all required JSON files."""
        files = {
            'progress': 'progress.json',
            'focus': 'focus.json',
            'focus_tasks': 'focus-tasks.json',
            'focus_notes': 'focus-notes.json',
            'initiatives': 'initiatives.json',
            'current_tasks': 'current-tasks.json',
            'current_projects': 'current-projects.json',
            'current_images': 'current-images.json',
            'current_wonders': 'current-wonders.json',
        }
        
        for key, filename in files.items():
            filepath = self.data_dir / filename
            try:
                if filepath.exists():
                    with open(filepath) as f:
                        self.data[key] = json.load(f)
                else:
                    self.data[key] = []
            except Exception as e:
                print(f"Warning: Could not load {filename}: {e}")
                self.data[key] = []
    
    # ========== INITIATIVE DATA ==========
    
    def get_initiatives_by_status(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get initiatives organized by status (focus, active, planned).
        
        Rules:
        - Type: 'work' (red) or 'study' (green)
        - Status: 'focus', 'active', or other/none (planned)
        - Differentiate work vs study with CSS
        
        Returns:
            Dict with keys: 'focus', 'active', 'planned'
            Each contains list of initiative dicts
        """
        initiatives = self.data.get('initiatives', [])
        
        result = {
            'focus': [],
            'active': [],
            'planned': []
        }
        
        for item in initiatives:
            status = item.get('status', '').lower()
            
            # Normalize dates to 'planned'
            if status and status.startswith('202'):
                status = 'planned'
            elif status == 'none':
                status = 'planned'
            elif not status:
                status = 'planned'
            
            entry = {
                'type': item.get('type'),  # 'work' or 'study'
                'summary': item.get('summary'),
                'file': item.get('file'),
                'raw_status': item.get('status'),
            }
            
            result[status].append(entry)
        
        return result
    
    # ========== TODO/TASK DATA ==========
    
    def get_todos_by_status(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get TODO items organized by status (focus, active).
        
        Rules:
        - Combine: focus-tasks, focus-notes, current-tasks, current-projects
        - Status 'w', '?', 't' = "mind" (experimental/thoughts)
        - Normal status = "todo" (action items)
        - Focus overrides active
        
        Returns:
            Dict with keys: 'focus_todo', 'focus_mind', 'active_todo', 'active_mind'
        """
        result = {
            'focus_todo': [],
            'focus_mind': [],
            'active_todo': [],
            'active_mind': []
        }
        
        # Focus items (with mind/todo split)
        focus_items = self.data.get('focus', [])
        focus_tasks = self.data.get('focus_tasks', [])
        focus_notes = self.data.get('focus_notes', [])
        
        # Process focus files
        for item in focus_items:
            if item.get('type') == 'file':
                # Check if it's a "mind" entry (w, ?, t status)
                is_mind = item.get('status') in ['w', '?', 't']
                key = 'focus_mind' if is_mind else 'focus_todo'
                result[key].append({
                    'summary': item.get('summary'),
                    'file': item.get('file'),
                    'is_mind': is_mind,
                })
        
        # Process focus-tasks
        for item in focus_tasks:
            is_mind = item.get('status') in ['w', '?', 't']
            key = 'focus_mind' if is_mind else 'focus_todo'
            result[key].append({
                'summary': item.get('summary'),
                'file': item.get('file'),
                'is_mind': is_mind,
            })
        
        # Process focus-notes
        for item in focus_notes:
            is_mind = item.get('status') in ['w', '?', 't', '*']
            key = 'focus_mind' if is_mind else 'focus_todo'
            result[key].append({
                'summary': item.get('summary'),
                'file': item.get('file'),
                'is_mind': is_mind,
            })
        
        # Active items (current-tasks and current-projects)
        current_tasks = self.data.get('current_tasks', [])
        current_projects = self.data.get('current_projects', [])
        
        for item in current_tasks + current_projects:
            result['active_todo'].append({
                'summary': item.get('summary'),
                'file': item.get('file'),
                'is_mind': False,
            })
        
        return result
    
    # ========== MIND/IDEAS DATA ==========
    
    def get_minds_by_status(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get "mind" items (ideas, wonders, images).
        
        Rules:
        - Focus: from focus items with w/? /t status
        - Active: from current-images, current-wonders
        
        Returns:
            Dict with keys: 'focus', 'active'
        """
        result = {
            'focus': [],
            'active': []
        }
        
        # Focus mind items (already captured in todos)
        focus_items = self.data.get('focus', [])
        for item in focus_items:
            if item.get('type') == 'file' and item.get('status') in ['w', '?', 't']:
                result['focus'].append({
                    'summary': item.get('summary'),
                    'file': item.get('file'),
                })
        
        # Active mind items
        current_images = self.data.get('current_images', [])
        current_wonders = self.data.get('current_wonders', [])
        
        for item in current_images + current_wonders:
            result['active'].append({
                'summary': item.get('summary'),
                'file': item.get('file'),
            })
        
        return result
    
    # ========== PROGRESS DATA ==========
    
    def get_progress_by_status(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Get progress items with progress/async split.
        
        Rules:
        - Progress items: those marked as "in progress"
        - Async: those with no clear progress indicator
        - Status: 'focus', 'active', or other
        - Type indicates category: project, TODO, task
        
        Returns:
            Dict structure:
            {
                'focus': {
                    'progress': [...],
                    'async': [...]
                },
                'active': {
                    'progress': [...],
                    'async': [...]
                }
            }
        """
        progress_items = self.data.get('progress', [])
        
        result = {
            'focus': {
                'progress': [],
                'async': []
            },
            'active': {
                'progress': [],
                'async': []
            }
        }
        
        for item in progress_items:
            status = item.get('status', '').lower()
            
            # Determine category
            entry = {
                'type': item.get('type'),  # project, TODO, task, etc.
                'summary': item.get('summary'),
                'file': item.get('file'),
            }
            
            # Categorize by status
            if status == 'focus':
                # Focus items go to progress by default
                result['focus']['progress'].append(entry)
            elif status == 'active':
                # Active items also go to progress
                result['active']['progress'].append(entry)
            else:
                # Pending/other items are "async"
                if status == 'focus':
                    result['focus']['async'].append(entry)
                else:
                    result['active']['async'].append(entry)
        
        return result
    
    # ========== AGGREGATION ==========
    
    def get_all_widget_data(self) -> Dict[str, Any]:
        """
        Get all data organized for widget display.
        
        Returns:
            Complete widget data structure
        """
        return {
            'initiatives': self.get_initiatives_by_status(),
            'todos': self.get_todos_by_status(),
            'minds': self.get_minds_by_status(),
            'progress': self.get_progress_by_status(),
        }


def format_entry_html(entry: Dict[str, Any], include_type: bool = False) -> str:
    """
    Format a single entry as HTML link/text.
    
    Args:
        entry: Dict with 'summary' and optional 'file'
        include_type: If True, include type badge
    
    Returns:
        HTML string for the entry
    """
    summary = entry.get('summary', 'Untitled')
    entry_type = entry.get('type', '').upper()
    is_mind = entry.get('is_mind', False)
    
    # Truncate long summaries
    if len(summary) > 50:
        summary = summary[:47] + '...'
    
    # Build HTML
    html = f'<span class="entry' 
    if include_type and entry_type:
        html += f' type-{entry_type.lower()}'
    if is_mind:
        html += ' is-mind'
    html += f'">{summary}</span>'
    
    return html


def format_entry_list_html(entries: List[Dict[str, Any]], include_type: bool = False) -> str:
    """
    Format multiple entries as HTML.
    
    Args:
        entries: List of entry dicts
        include_type: If True, include type badges
    
    Returns:
        HTML string with all entries
    """
    if not entries:
        return '<span class="empty">—</span>'
    
    formatted = [format_entry_html(e, include_type) for e in entries]
    return ' '.join(formatted)
