# CLAUDE.md — Collaboration-Area-Event-Series

This file gives Claude Code context about this project. Read it before making any changes.

## Project Overview

Automation toolkit for the **ESIP Federation** (Earth Science Information Partners) to create and manage recurring collaboration area meetings and events across two platforms:

- **Zoom** — recurring meetings via Zoom Server-to-Server OAuth API
- **WordPress** — individual calendar events via The Events Calendar Pro REST API

This project is actively used in production. The `zoom_meetings_output.csv` contains real ESIP meeting data. Be careful with any changes that affect output formats or API payloads.

---

## Repository Layout

```
scripts/                         # All runnable Python scripts
  create_zoom_recurring_meetings.py   # Primary: creates Zoom meetings from config
  create_events.py                    # Primary: creates WordPress events from config
  generate_wp_events_config.py        # Utility: Zoom config + CSV → WP events config
  map_zoom_to_event_series_config.py  # Utility: Zoom config → WP config (simpler)

examples/                        # Reference configs (safe to edit/extend)
  zoom-config.json                    # Example Zoom meeting config (5 meetings)
  events-config.json                  # Example WordPress events config
  zoom_meetings_output_example.csv    # Example CSV output format

docs/                            # Extended documentation
  ZOOM_GUIDE.md                       # Full Zoom API setup and usage guide
  README.md                           # WordPress Events full reference
  QUICKSTART.md                       # WordPress 5-minute quick start

zoom_meetings_output.csv         # Production output — real ESIP meeting data
requirements.txt                 # Python deps: only `requests >= 2.28.0`
```

---

## Key Scripts

### `create_zoom_recurring_meetings.py`
- Entry point: `--config <path>` (required), `--dry-run`, `--verbose`
- Uses `ZoomAPIClient` class for OAuth token management and API calls
- Reads a JSON config with `zoom_api` credentials + `meetings` array
- Appends results to a CSV file (default: `zoom_meetings_output.csv`)
- Supports daily, weekly, and monthly recurrence

### `create_events.py`
- Entry point: `--config <path>` (required), `--dry-run`
- Reads a JSON config with `wordpress` credentials + `event` or `events` array
- Creates non-recurring events via WordPress REST API
- WordPress does not support recurrence via the REST API — this is intentional

### `generate_wp_events_config.py`
- Entry point: `--template`, `--zoom-config`, `--zoom-output-csv`, `--output`
- Bridges Zoom and WordPress: reads Zoom config + output CSV, generates WP config
- Strips trailing ` - YYYY` from event titles
- Injects registration URLs from CSV into event descriptions as HTML

### `map_zoom_to_event_series_config.py`
- Simpler alternative to `generate_wp_events_config.py`
- Converts a single Zoom meeting config to WordPress format
- Sets venue to "Virtual - Zoom", adds standard categories

---

## Config File Formats

### Zoom Config (`examples/zoom-config.json`)
```json
{
  "zoom_api": {
    "account_id": "...",
    "client_id": "...",
    "client_secret": "..."
  },
  "output_file": "zoom_meetings_output.csv",
  "meetings": [
    {
      "host_email": "user@org.com",
      "topic": "Meeting Title",
      "start_date": "YYYY-MM-DD",
      "start_time": "HH:MM:SS",
      "duration": 60,
      "timezone": "America/New_York",
      "recurrence_type": "weekly|monthly|daily",
      "weekly_days": "2",       // weekly only: 1=Sun ... 7=Sat
      "monthly_day": 15,        // monthly only: day of month
      "end_date": "YYYY-MM-DD", // use end_date OR occurrences
      "occurrences": 10,
      "repeat_interval": 1,
      "enable_registration": true,
      ...
    }
  ]
}
```

### WordPress Config (`examples/events-config.json`)
```json
{
  "wordpress": {
    "url": "https://your-site.com",
    "username": "...",
    "app_password": "..."
  },
  "events": [
    {
      "title": "Event Title",
      "start_date": "YYYY-MM-DD HH:MM:SS",
      "end_date": "YYYY-MM-DD HH:MM:SS",
      "description": "HTML content",
      "venue": "Virtual - Zoom",
      "organizer": "Organizer Name",
      "categories": ["Collaboration Area"]
    }
  ]
}
```

---

## Development Guidelines

### When modifying scripts
- Always update the corresponding doc in `docs/` if behavior changes
- Preserve dry-run mode (`--dry-run`) in any script that makes API calls
- Keep rate limiting in place: 1s between Zoom API calls, 0.5s between WordPress calls
- Do not change the CSV output column names — external processes may depend on them
- Config file structure changes must be backward-compatible or clearly versioned

### When updating documentation
- `docs/ZOOM_GUIDE.md` — update when Zoom script behavior, config fields, or auth steps change
- `docs/README.md` — update when WordPress script behavior or config fields change
- `docs/QUICKSTART.md` — update only when the basic 5-step flow changes significantly
- `README.md` (root) — update when the overall feature set or quick-start commands change
- `scripts/README.md` — update when script interfaces (flags, inputs, outputs) change

### Credentials
- Never commit real credentials. All configs use placeholder values like `YOUR_ZOOM_ACCOUNT_ID`
- The `.gitignore` excludes `*-config.json` (non-example configs) and `.env` files
- Production configs (e.g., `zoom-meeting-2026-config.json`) should never be committed

### Python conventions
- Python 3.6+ compatible
- Use type hints for function signatures
- Follow PEP 8
- Only dependency is `requests` — do not add new dependencies without updating `requirements.txt`

---

## Common Tasks

**Add a new Zoom config field:**
1. Add handling in `create_zoom_recurring_meetings.py`
2. Add the field to `examples/zoom-config.json` with a sensible default
3. Document the field in `docs/ZOOM_GUIDE.md` (Configuration Reference table)

**Add a new WordPress event field:**
1. Add handling in `create_events.py`
2. Add the field to `examples/events-config.json`
3. Document in `docs/README.md` (Configuration Reference)

**Add a new script:**
1. Place it in `scripts/`
2. Include a module-level docstring with usage examples
3. Add an entry to `scripts/README.md`
4. Reference it from root `README.md` if it's a primary workflow

---

## External API References

- Zoom API docs: https://developers.zoom.us/docs/api/
- Zoom Server-to-Server OAuth: https://developers.zoom.us/docs/internal-apps/
- The Events Calendar REST API: available via WordPress plugin documentation
- WordPress Application Passwords: Settings > Users > Application Passwords
