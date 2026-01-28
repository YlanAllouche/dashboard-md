"""Playlist Maker - Generate video collection dashboards from JSON data"""

import json
import sys
from pathlib import Path

# Import from local modules
from playlist_maker.utils.colors import extract_pywal_colors
from playlist_maker.utils.templates import render_unified_home_template, load_template
from playlist_maker.data import format_title, detect_content_type, validate_and_sanitize


def generate_unified_home_page(output_dir, successful_collections):
    """
    Generate a unified index.html with tabbed navigation for all content types.

    Videos are linked to separate pages, other types are embedded.
    """
    pywal_css = extract_pywal_colors()

    home_html = render_unified_home_template(pywal_css, successful_collections)

    home_path = output_dir / "index.html"
    with open(home_path, "w", encoding="utf-8") as f:
        f.write(home_html)

    print(f"\nGenerated unified home page: {home_path}")


def generate_home_page(output_dir, successful_files):
    """Generate a home page that lists all available playlists"""
    # Sort by title
    successful_files.sort(key=lambda x: x["title"])

    # Get pywal colors
    pywal_css = extract_pywal_colors()

    # Render home template with modular dashboard
    home_html = render_home_template(pywal_css, successful_files)

    return home_html


def generate_html(json_data, title):
    """Generate the complete HTML with embedded JSON data"""
    # Get pywal colors
    pywal_css = extract_pywal_colors()

    # Load JavaScript template
    javascript_template = load_template("video.js")

    # Convert json_data to JSON string
    json_str = json.dumps(json_data, indent=8)

    # Format JavaScript with video data (use replace to avoid format string issues)
    javascript = javascript_template.replace("{VIDEO_DATA}", json_str)

    from playlist_maker.utils.templates import render_video_template
    # Render video template
    html_template = render_video_template(title, pywal_css, javascript)

    return html_template


def main():
    # Hardcoded folder path
    folder_path = Path.home() / "share" / "_tmp"

    # Check if folder exists
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' not found.")
        print("Please create the folder or update the hardcoded path in the script.")
        sys.exit(1)

    print(f"Scanning folder: {folder_path}")

    # Find all JSON files
    json_files = list(folder_path.glob("*.json"))

    if not json_files:
        print("No JSON files found in the folder.")
        sys.exit(1)

    print(f"Found {len(json_files)} JSON files")

    # New structure: organize by content type
    successful_collections = {
        "video": [],
        "task": [],
        "calendar": [],
        "project": [],
        "notes": []
    }

    failed_files = []

    # Process each JSON file
    for json_file_path in json_files:
        filename = json_file_path.name
        stem = json_file_path.stem
        title = format_title(stem)

        print(f"\nProcessing: {filename}")

        try:
            # Read and parse JSON
            with open(json_file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            # Detect content type
            content_type = detect_content_type(json_data)
            print(f"  Detected type: {content_type}")

            # Validate and sanitize using router
            sanitized_data, is_valid, reason = validate_and_sanitize(json_data, content_type)

            if not is_valid:
                print(f"  Skipped: {reason}")
                failed_files.append({"filename": filename, "reason": reason})
                continue

            if len(sanitized_data) == 0:
                print(f"  Skipped: No valid items after sanitization")
                failed_files.append({"filename": filename, "reason": "No valid items"})
                continue

            # Generate separate HTML for video collections
            if content_type == "video":
                html_content = generate_html(sanitized_data, title)
                output_path = folder_path / f"{stem}.html"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"  Generated: {output_path.name}")

            # Store in collections dict for home page
            successful_collections[content_type].append({
                "filename": filename,
                "stem": stem,
                "title": title,
                "type": content_type,
                "count": len(sanitized_data),
                "data": sanitized_data
            })

            print(f"  Items: {len(sanitized_data)}")

        except json.JSONDecodeError as e:
            reason = f"Invalid JSON: {str(e)[:50]}..."
            print(f"  Failed: {reason}")
            failed_files.append({"filename": filename, "reason": reason})
            continue
        except Exception as e:
            reason = f"Error: {str(e)[:50]}..."
            print(f"  Failed: {reason}")
            failed_files.append({"filename": filename, "reason": reason})
            continue

    # Generate unified home page
    generate_unified_home_page(folder_path, successful_collections)

    # Summary
    print(f"\nSummary:")
    for content_type, collections in successful_collections.items():
        if collections:
            print(f"  {content_type.capitalize()}: {len(collections)} collections, {sum(c['count'] for c in collections)} total items")

    if failed_files:
        print(f"\nSkipped files:")
        for file_info in failed_files:
            print(f"  • {file_info['filename']}: {file_info['reason']}")


if __name__ == "__main__":
    main()
