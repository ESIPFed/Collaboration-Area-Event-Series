# Scripts Directory

This directory contains automation scripts for creating events and meetings.

## Available Scripts

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

### 2. create_events.py

**Purpose:** Create single or multiple non-recurring events in WordPress using The Events Calendar Pro API

**Use Case:**
- WordPress site with The Events Calendar Pro plugin
- Creating one event or many events from one config file
- Works with the REST API without recurrence rules

**Quick start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Create events
python create_events.py --config ../examples/simple-config.json
```

**Features:**
- ✅ WordPress REST API integration
- ✅ Single event or bulk event creation
- ✅ Custom venues and organizers
- ✅ Categories support

---

### 3. generate_wp_events_config.py

**Purpose:** Generate a WordPress events config from Zoom config + Zoom output CSV

**Use Case:**
- You have `zoom-meeting-2026-config.json` with meeting definitions
- You have `zoom_meetings_output.csv` with `registration_url` values
- You want `wp-events-2026-config.json` in the same framework as `examples/events-config.json`

**Quick start:**
```bash
python generate_wp_events_config.py \
	--template ../examples/events-config.json \
	--zoom-config ../zoom-meeting-2026-config.json \
	--zoom-output-csv ../zoom_meetings_output.csv \
	--output ../wp-events-2026-config.json
```

**Behavior notes:**
- ✅ Removes trailing ` - 2026` from event titles
- ✅ Sets event description to standard registration HTML content
- ✅ Replaces registration link per matching `meeting_topic` from CSV

---

## Comparison

| Feature | Zoom Script | WordPress Script |
|---------|-------------|------------------|
| Platform | Zoom Meetings | WordPress Events |
| Multi-user | ✅ Yes | ❌ No |
| Recurrence Types | Daily/Weekly/Monthly | N/A (single events) |
| Registration | ✅ Automatic | Depends on plugin |
| Output Format | CSV file | WordPress database |
| Best For | Virtual meetings | Website calendar events |

## Support

- Zoom Script Issues: See [Zoom Guide](../docs/ZOOM_GUIDE.md)
- WordPress Script Issues: See [Main Documentation](../docs/README.md)
