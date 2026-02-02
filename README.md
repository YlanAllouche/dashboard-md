# obsi-dash

Generate HTML dashboards from Obsidian Dataview query materialization.
hyper-idiosyncratic tool templating html dashboard pages from dataview/obsidan query materialization into json files and abusing deep links for browser <=> obsidian <=> nvim communication

(Yes, clicking on any of the thumbnail would immediately play them locally in jellyfin-mpv-shim)  

https://github.com/user-attachments/assets/62c2a80a-18f8-4f7e-b6ba-0b10288a6223

## Overview

`obsi-dash` scans JSON files in `~/share/_tmp` and creates interactive HTML dashboards for viewing collections of videos, tasks, calendar events, projects, and notes. Each content type is automatically detected and rendered with appropriate templates.

## Content Types

- **Video**: YouTube/video playlists with thumbnails, duration, channel info
- **Task**: Task lists with status, priority, due dates
- **Calendar**: Scheduled events with location and attendees
- **Project**: Active project tracking
- **Notes**: Organized notes with metadata

## Installation

```bash
pip install . # -- break-system-packages
```

## Usage

Place your Obsidian Dataview JSON exports in `~/share/_tmp` (excluding files starting with `-`) and run:

```bash
cd ~/share/_tmp
python -m http.module 8008
obsi-dash # no need to be ran aftre the first time because it will be executed by the "queryAll" script as well
```

The tool will:
1. Scan the folder for JSON files
2. Auto-detect content type for each file
3. Validate and sanitize data
4. Generate individual HTML pages for video collections
5. Create a unified `index.html` with tabbed navigation

## Data Format

JSON files should follow Obsidian Dataview export structure. The tool automatically identifies content type based on field presence:

- **Video**: `id`, `summary`, `duration`, `channel`, `date`, `locator`
- **Task**: `file`, `summary`, `type: "task"`
- **Calendar**: `scheduled` field or `type: "calendar"`
- **Project**: `type: "note"`, `status: "current"`
- **Notes**: `type: "note"`

## Dependencies

- jelly_yt_play (see https://github.com/YlanAllouche/jelly_play_scripts)
-  a whole lot of js scripts in `~/share/_scripts/templates` (see https://github.com/YlanAllouche/personal-share-example)
- presence of `-tags.json` file in ~/share/_scripts
- obsidian
- obsidian plugins
    - templater
    - deeplink 
    - dataview 
- python
- nvim ran with a socket at specific path (`~/.cache/nvim/share.pipe`)

## License

MIT
