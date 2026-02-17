# Collaboration-Area-Event-Series

Scripts and utilities for creating events and meetings.

## Overview

This repository provides tools to automate event and meeting creation across different platforms:

### 🎥 Zoom Meetings (NEW!)
Create recurring Zoom meetings with multi-user support:
- Multiple Zoom users/hosts within your organization
- Daily, weekly, and monthly recurrence patterns
- Registration enabled by default with automatic links
- Persistent CSV storage of all meeting details

### 📅 WordPress Events
Create single or multiple events in WordPress:
- Unique event name
- Specific start and end date/time
- Custom time slots
- Supports one event or many from one config file

## Quick Start

### Choose Your Guide

- **Zoom recurring meetings:** [docs/ZOOM_GUIDE.md](docs/ZOOM_GUIDE.md)
- **WordPress events:** [docs/QUICKSTART.md](docs/QUICKSTART.md) then [docs/README.md](docs/README.md)

### Zoom Meetings

```bash
# Install dependencies
pip install -r requirements.txt

# Create Zoom meetings
python scripts/create_zoom_recurring_meetings.py --config examples/zoom-config.json
```

📚 **[Zoom Setup Guide](docs/ZOOM_GUIDE.md)** - Complete guide for Zoom API setup

### WordPress Events

```bash
python scripts/create_events.py --config examples/simple-config.json

# Or generate wp-events-2026-config.json from Zoom inputs
python scripts/generate_wp_events_config.py \
	--template examples/events-config.json \
	--zoom-config zoom-meeting-2026-config.json \
	--zoom-output-csv zoom_meetings_output.csv \
	--output wp-events-2026-config.json
```

## Documentation

### Zoom Meetings
- 📘 **[Zoom Complete Guide](docs/ZOOM_GUIDE.md)** - Full setup and usage guide
- 📄 [Example Configuration](examples/zoom-config.json)
- 📊 [Example Output CSV](examples/zoom_meetings_output_example.csv)

### WordPress Events
- 📚 **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- 📘 [Full Documentation](docs/README.md)
- 📄 [Example Configuration](examples/events-config.json)

## Requirements

### For Zoom Meetings
- Zoom Pro, Business, or Enterprise account
- Server-to-Server OAuth App (see [Zoom Guide](docs/ZOOM_GUIDE.md))
- Python 3.6+
- `requests` package

### For WordPress Events
- WordPress with The Events Calendar Pro plugin
- REST API enabled
- Application password for authentication
- Python 3.6+
- `requests` package

## Features

### Zoom Meetings
✅ **Multi-user support** - Create meetings for different Zoom hosts  
✅ **Flexible recurrence** - Daily, weekly, or monthly patterns  
✅ **Registration enabled** - Automatic registration with registration links  
✅ **Persistent storage** - CSV file with all meeting details  
✅ **Configurable settings** - Full control over meeting options  
✅ **Dry-run mode** - Test configurations before creating  

### WordPress Events
✅ Create one or multiple events from a single configuration file  
✅ Unique event names for each event in the config  
✅ Customizable start/end dates and times  
✅ Support for venues, organizers, and categories  
✅ Dry-run mode for testing  

## License

MIT License - See documentation for details.
