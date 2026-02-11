# Collaboration-Area-Event-Series

Scripts and utilities for creating recurring event series and meetings.

## Overview

This repository provides tools to automate the creation of recurring events and meetings across different platforms:

### 🎥 Zoom Meetings (NEW!)
Create recurring Zoom meetings with multi-user support:
- Multiple Zoom users/hosts within your organization
- Daily, weekly, and monthly recurrence patterns
- Registration enabled by default with automatic links
- Persistent CSV storage of all meeting details

### 📅 WordPress Events
Create recurring events in WordPress:
- Unique event name
- Specific start and end dates
- Custom time slots
- Monthly recurrence patterns (e.g., first Monday of each month)

## Quick Start

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
python scripts/create_recurring_events.py --config examples/event-series-config.json
```

## Documentation

### Zoom Meetings
- 📘 **[Zoom Complete Guide](docs/ZOOM_GUIDE.md)** - Full setup and usage guide
- 📄 [Example Configuration](examples/zoom-config.json)
- 📊 [Example Output CSV](examples/zoom_meetings_output_example.csv)

### WordPress Events
- 📚 **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- 📘 [Full Documentation](docs/README.md)
- 📄 [Example Configuration](examples/event-series-config.json)

## Requirements

### For Zoom Meetings
- Zoom Pro, Business, or Enterprise account
- Server-to-Server OAuth App (see [Zoom Guide](docs/ZOOM_GUIDE.md))
- Python 3.6+
- `requests` and `pyjwt` packages

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
✅ Create multiple recurring events from a single configuration file  
✅ Monthly recurrence patterns (first/second/third/fourth/last day of week)  
✅ Unique event names for each event in the series  
✅ Customizable start/end dates and times  
✅ Support for venues, organizers, and categories  
✅ Dry-run mode for testing  

## License

MIT License - See documentation for details.
