"""Data validation and processing"""

from pathlib import Path
import re
import os

# Content type configuration
CONTENT_TYPE_RULES = {
    "video": {
        "priority": 1,
        "required_fields": ["id", "summary", "duration", "channel", "date", "locator"],
        "optional_fields": ["thumbnail", "watched", "tags"],
        "type_field_value": "Note",
        "status_field_value": "youtube",
        "validator": "validate_video_data"
    },
    "calendar": {
        "priority": 2,
        "required_fields": ["id", "title", "scheduled"],
        "optional_fields": ["location", "description", "status", "attendees"],
        "type_field_value": None,
        "validator": "validate_calendar_data"
    },
    "project": {
        "priority": 3,
        "required_fields": ["file", "summary"],
        "optional_fields": ["workspace", "class", "status", "progress", "due_date", "active", "focus"],
        "type_field_value": "note",
        "status_field_value": "current",
        "validator": "validate_project_data"
    },
    "task": {
        "priority": 4,
        "required_fields": ["file", "summary"],
        "optional_fields": ["status", "description", "due_date", "priority", "active", "focus"],
        "type_field_value": "task",
        "validator": "validate_task_data"
    },
    "notes": {
        "priority": 5,
        "required_fields": ["file", "summary"],
        "optional_fields": ["workspace", "class", "status", "description", "active", "focus"],
        "type_field_value": "note",
        "status_field_value": None,
        "validator": "validate_notes_data"
    }
}


def detect_content_type(data):
    """
    Detect the content type based on data structure.

    Args:
        data: Parsed JSON data (should be a list)

    Returns:
        str: Content type ("video", "task", "calendar", "project")
    """
    if not isinstance(data, list) or len(data) == 0:
        return "task"

    sample_items = [item for item in data[:5] if isinstance(item, dict)]

    if len(sample_items) == 0:
        return "task"

    # First, check for scheduled field or calendar type (calendar takes priority)
    scheduled_count = 0
    for item in sample_items:
        if "scheduled" in item:
            scheduled_count += 1
        elif item.get("type") == "calendar":
            scheduled_count += 1

    if scheduled_count >= len(sample_items) * 0.5:
        return "calendar"

    # Then check for type-based detection
    sorted_types = sorted(CONTENT_TYPE_RULES.items(), key=lambda x: x[1]["priority"])

    for type_name, type_config in sorted_types:
        if type_config["type_field_value"] is None:
            continue

        type_field_value = type_config["type_field_value"]
        status_field_value = type_config.get("status_field_value")

        matching_items = 0
        for item in sample_items:
            if item.get("type") == type_field_value:
                if status_field_value is None or item.get("status") == status_field_value:
                    matching_items += 1

        if matching_items >= len(sample_items) * 0.5:
            return type_name

    return "task"


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


def validate_task_data(data):
    """
    Validate that the JSON data is suitable for task processing.

    Args:
        data: Parsed JSON data

    Returns:
        tuple: (is_valid, reason)
    """
    if not isinstance(data, list):
        return False, "Not a list"

    if len(data) == 0:
        return False, "Empty list"

    valid_items = 0

    for item in data[:5]:
        if not isinstance(item, dict):
            continue

        if item.get("type") == "task" and "file" in item and "summary" in item:
            valid_items += 1

    if valid_items == 0:
        return False, "No valid task items found"

    return True, "Valid task data"


def validate_calendar_data(data):
    """
    Validate that the JSON data is suitable for calendar processing.

    Args:
        data: Parsed JSON data

    Returns:
        tuple: (is_valid, reason)
    """
    if not isinstance(data, list):
        return False, "Not a list"

    if len(data) == 0:
        return False, "Empty list"

    valid_items = 0

    for item in data[:5]:
        if not isinstance(item, dict):
            continue

        if "scheduled" in item or item.get("type") == "calendar":
            valid_items += 1

    if valid_items == 0:
        return False, "No valid calendar items found"

    return True, "Valid calendar data"


def validate_project_data(data):
    """
    Validate that the JSON data is suitable for project processing.

    Args:
        data: Parsed JSON data

    Returns:
        tuple: (is_valid, reason)
    """
    if not isinstance(data, list):
        return False, "Not a list"

    if len(data) == 0:
        return False, "Empty list"

    valid_items = 0

    for item in data[:5]:
        if not isinstance(item, dict):
            continue

        if item.get("type") == "note" and item.get("status") == "current":
            valid_items += 1

    if valid_items == 0:
        return False, "No valid project items found"

    return True, "Valid project data"


def sanitize_task_data(data):
    """
    Clean and ensure task data has all required fields with defaults.

    Args:
        data: Parsed JSON data

    Returns:
        list: List of sanitized task dictionaries
    """
    sanitized = []

    for item in data:
        if not isinstance(item, dict):
            continue

        if item.get("type") != "task":
            continue

        file_path = item.get("file", "")
        summary = item.get("summary", "")

        if not file_path or not summary:
            continue

        import os
        id_value = os.path.splitext(os.path.basename(file_path))[0]

        active_match = re.search(r'\[active::\s*(\w+)\]', summary)
        focus_match = re.search(r'\[focus::\s*(\w+)\]', summary)
        date_match = re.search(r'\[date::\s*([^\]]+)\]', summary)

        is_active = active_match and active_match.group(1).lower() in ["true", "yes", "1"]
        is_focused = focus_match and focus_match.group(1).lower() in ["true", "yes", "1"]
        due_date = date_match.group(1) if date_match else ""

        clean_summary = re.sub(r'\s*\[.*?\]', '', summary).strip()
        line = item.get("line", 1)

        sanitized_item = {
            "id": str(id_value),
            "title": str(clean_summary),
            "status": str(item.get("status", "pending").strip()),
            "description": "",
            "due_date": str(due_date),
            "priority": str("normal"),
            "active": bool(is_active),
            "focus": bool(is_focused),
            "file": str(file_path),
            "line": int(line)
        }

        if not sanitized_item["id"]:
            continue

        sanitized.append(sanitized_item)

    return sanitized


def sanitize_calendar_data(data):
    """
    Clean and ensure calendar data has all required fields with defaults.

    Args:
        data: Parsed JSON data

    Returns:
        list: List of sanitized event dictionaries
    """
    sanitized = []

    for item in data:
        if not isinstance(item, dict):
            continue

        file_path = item.get("file", "")
        summary = item.get("summary", "")
        scheduled = item.get("scheduled", "")

        if not scheduled:
            scheduled_match = re.search(r'\[scheduled::\s*([^\]]+)\]', summary)
            scheduled = scheduled_match.group(1) if scheduled_match else ""

        if not scheduled:
            scheduled = item.get("date", "")

        if not scheduled:
            continue

        import os
        id_value = os.path.splitext(os.path.basename(file_path))[0]

        location = item.get("location", "")
        if not location:
            location_match = re.search(r'\[location::\s*([^\]]+)\]', summary)
            location = location_match.group(1) if location_match else ""

        clean_summary = re.sub(r'\s*\[[^]]*\]', '', summary).strip()
        line = item.get("line", 1)

        sanitized_item = {
            "id": str(id_value),
            "title": str(clean_summary),
            "scheduled": str(scheduled),
            "location": str(location),
            "status": str(item.get("status", "scheduled")),
            "description": item.get("description", ""),
            "attendees": item.get("attendees", []) if isinstance(item.get("attendees"), list) else [],
            "file": str(file_path),
            "line": int(line)
        }

        if not sanitized_item["id"]:
            continue

        sanitized.append(sanitized_item)

    return sanitized


def sanitize_project_data(data):
    """
    Clean and ensure project data has all required fields with defaults.

    Args:
        data: Parsed JSON data

    Returns:
        list: List of sanitized project dictionaries
    """
    sanitized = []

    for item in data:
        if not isinstance(item, dict):
            continue

        if item.get("type") != "note" or item.get("status") != "current":
            continue

        file_path = item.get("file", "")
        summary = item.get("summary", "")

        if not file_path or not summary:
            continue

        import os
        id_value = os.path.splitext(os.path.basename(file_path))[0]
        line = item.get("line", 1)

        sanitized_item = {
            "id": str(id_value),
            "title": str(summary),
            "workspace": str(""),
            "class": str(""),
            "status": str("in-progress"),
            "progress": int(0),
            "due_date": str(""),
            "description": "",
            "active": bool(True),
            "focus": bool(False),
            "file": str(file_path),
            "line": int(line)
        }

        if not sanitized_item["id"]:
            continue

        sanitized.append(sanitized_item)

    return sanitized


def validate_notes_data(data):
    """
    Validate that the JSON data is suitable for notes processing.

    Args:
        data: Parsed JSON data

    Returns:
        tuple: (is_valid, reason)
    """
    if not isinstance(data, list):
        return False, "Not a list"

    if len(data) == 0:
        return False, "Empty list"

    valid_items = 0

    for item in data[:5]:
        if not isinstance(item, dict):
            continue

        if item.get("type") == "note":
            valid_items += 1

    if valid_items == 0:
        return False, "No valid notes items found"

    return True, "Valid notes data"


def sanitize_notes_data(data):
    """
    Clean and ensure notes data has all required fields with defaults.

    Args:
        data: Parsed JSON data

    Returns:
        list: List of sanitized note dictionaries
    """
    sanitized = []

    for item in data:
        if not isinstance(item, dict):
            continue

        if item.get("type") != "note":
            continue

        file_path = item.get("file", "")
        summary = item.get("summary", "")

        if not file_path or not summary:
            continue

        import os
        id_value = os.path.splitext(os.path.basename(file_path))[0]

        description_match = re.search(r'\[description::\s*([^\]]+)\]', summary)
        description = description_match.group(1) if description_match else ""
        
        clean_summary = re.sub(r'\s*\[description::\s*[^\]]+\]', '', summary).strip()

        active_match = re.search(r'\[active::\s*(\w+)\]', summary)
        focus_match = re.search(r'\[focus::\s*(\w+)\]', summary)
        line = item.get("line", 1)

        is_active = active_match and active_match.group(1).lower() in ["true", "yes", "1"]
        is_focused = focus_match and focus_match.group(1).lower() in ["true", "yes", "1"]

        sanitized_item = {
            "id": str(id_value),
            "title": str(clean_summary),
            "description": str(description),
            "status": str(item.get("status", "active")),
            "active": bool(is_active),
            "focus": bool(is_focused),
            "file": str(file_path),
            "line": int(line)
        }

        if not sanitized_item["id"]:
            continue

        sanitized.append(sanitized_item)

    return sanitized


def validate_and_sanitize(data, content_type):
    """
    Route data to appropriate validator and sanitizer based on content type.

    Args:
        data: Parsed JSON data
        content_type: Content type string ("video", "task", "calendar", "project", "notes")

    Returns:
        tuple: (sanitized_data, is_valid, reason)
    """
    validators = {
        "video": validate_video_data,
        "task": validate_task_data,
        "calendar": validate_calendar_data,
        "project": validate_project_data,
        "notes": validate_notes_data
    }

    sanitizers = {
        "video": sanitize_video_data,
        "task": sanitize_task_data,
        "calendar": sanitize_calendar_data,
        "project": sanitize_project_data,
        "notes": sanitize_notes_data
    }

    validator = validators.get(content_type)
    sanitizer = sanitizers.get(content_type)

    if not validator or not sanitizer:
        return [], False, f"Unknown content type: {content_type}"

    is_valid, reason = validator(data)

    if not is_valid:
        return [], False, reason

    sanitized = sanitizer(data)
    return sanitized, True, reason
