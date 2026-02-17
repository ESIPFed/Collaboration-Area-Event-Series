# Scripts Directory

This directory contains automation scripts for creating recurring events and meetings.

## Available Scripts

### 0. map_zoom_to_event_series_config.py

**Purpose:** Convert a Zoom meetings config JSON into a WordPress event-series config JSON

**Use Case:**
- You already have a Zoom meetings plan (e.g., `zoom-meeting-2026-config.json`)
- You want to bootstrap a matching `event-series-config.json` for WordPress

**Quick start:**
```bash
python map_zoom_to_event_series_config.py \
	--zoom-config ../zoom-meeting-2026-config.json \
	--output ../event-series-config-from-zoom.json
```

**Behavior notes:**
- ✅ Maps monthly recurrence using `monthly_week` + `monthly_week_day`
- ✅ Maps topic/agenda/date/time/duration/timezone to event fields
- ⚠ Skips unsupported recurrence types (e.g., weekly) and reports warnings

### 1. create_zoom_recurring_meetings.py

**Purpose:** Create recurring Zoom meetings using the Zoom API

**Use Case:**
- Multiple Zoom users in your organization
- Need to create various recurring meeting schedules
- Want registration links automatically generated
- Need persistent storage of meeting details

**Documentation:** See [Zoom Guide](../docs/ZOOM_GUIDE.md)

**Quick start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Create meetings
python create_zoom_recurring_meetings.py --config ../examples/zoom-config.json
```

**Features:**
- ✅ Multi-user support (different hosts)
- ✅ Daily, weekly, and monthly recurrence
- ✅ Registration enabled by default
- ✅ Saves to CSV file
- ✅ Dry-run mode for testing

---

### 2. create_recurring_events.py

**Purpose:** Create recurring events in WordPress using The Events Calendar Pro API

**Use Case:**
- WordPress site with The Events Calendar Pro plugin
- Creating event series with custom recurrence patterns
- Monthly events on specific days (e.g., first Monday)

**Quick start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Create events
python create_recurring_events.py --config ../examples/event-series-config.json
```

**Features:**
- ✅ WordPress REST API integration
- ✅ Monthly recurrence patterns
- ✅ Custom venues and organizers
- ✅ Categories and tags support

---

## Comparison

| Feature | Zoom Script | WordPress Script |
|---------|-------------|------------------|
| Platform | Zoom Meetings | WordPress Events |
| Multi-user | ✅ Yes | ❌ No |
| Recurrence Types | Daily/Weekly/Monthly | Monthly (day patterns) |
| Registration | ✅ Automatic | Depends on plugin |
| Output Format | CSV file | WordPress database |
| Best For | Virtual meetings | Website calendar events |

## Support

- Zoom Script Issues: See [Zoom Guide](../docs/ZOOM_GUIDE.md)
- WordPress Script Issues: See [Main Documentation](../docs/README.md)
