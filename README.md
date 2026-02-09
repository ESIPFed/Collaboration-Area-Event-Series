# Collaboration-Area-Event-Series

Scripts and utilities for creating recurring event series in WordPress using The Events Calendar Pro API.

## Overview

This repository provides tools to automate the creation of recurring events in WordPress. Each event can have:
- Unique event name
- Specific start and end dates
- Custom time slots
- Monthly recurrence patterns (e.g., first Monday of each month)

## Quick Start

### PHP Script
```bash
php scripts/create-recurring-events.php --config=examples/event-series-config.json
```

### Python Script
```bash
python scripts/create_recurring_events.py --config examples/event-series-config.json
```

## Documentation

📚 **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes

For complete documentation, setup guides, and examples, see:
- [Full Documentation](docs/README.md)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Example Configuration](examples/event-series-config.json)

## Requirements

- WordPress with The Events Calendar Pro plugin
- REST API enabled
- Application password for authentication
- PHP 7.4+ or Python 3.6+

## Features

✅ Create multiple recurring events from a single configuration file  
✅ Monthly recurrence patterns (first/second/third/fourth/last day of week)  
✅ Unique event names for each event in the series  
✅ Customizable start/end dates and times  
✅ Support for venues, organizers, and categories  
✅ Both PHP and Python implementations  
✅ Dry-run mode for testing (Python)  

## License

MIT License - See documentation for details.
