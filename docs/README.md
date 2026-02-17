# Events Calendar Pro API - Event Creation Scripts

This repository contains scripts and utilities for creating one or many WordPress events using The Events Calendar Pro REST API.

## Features

- ✅ Create one event or many events from a single configuration file
- ✅ Supports both `event` (single) and `events` (multiple) config shapes
- ✅ Unique event names for each event
- ✅ Customizable start/end dates and times
- ✅ Support for venues, organizers, and categories
- ✅ Dry-run mode for testing
- ✅ Verbose output for debugging

## Requirements

- Python 3.6 or higher
- `requests` library: `pip install requests`
- WordPress site with The Events Calendar Pro plugin installed
- REST API enabled on WordPress
- Application password for authentication

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ESIPFed/Collaboration-Area-Event-Series.git
   cd Collaboration-Area-Event-Series
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

## Configuration

Create a JSON configuration file with your WordPress credentials and event details.
See `examples/events-config.json` for a multi-event example.

### Configuration Structure

```json
{
  "wordpress_url": "https://your-wordpress-site.com",
  "username": "your-username",
  "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx",
  "events": [
    {
      "title": "Event Name",
      "description": "Event description",
      "start_date": "2024-01-08",
      "end_date": "2024-01-08",
      "start_time": "14:00:00",
      "end_time": "15:00:00",
      "venue": "Virtual - Zoom",
      "organizer": "Organization Name",
      "categories": ["Category1", "Category2"]
    }
  ]
}
```

### Required Fields

- `wordpress_url`: Your WordPress site URL
- `username`: WordPress username
- `app_password`: Application password (see Setup Guide below)
- Either `events`: Array of event objects, or `event`: single event object

### Event Object Fields

**Required:**
- `title`: Event title/name (string)
- `start_date`: Event start date in YYYY-MM-DD format
- `end_date`: Event end date in YYYY-MM-DD format
- `start_time`: Event start time in HH:MM:SS format
- `end_time`: Event end time in HH:MM:SS format

**Optional:**
- `description`: Event description (string)
- `venue`: Venue name (string)
- `organizer`: Organizer name (string)
- `categories`: Array of category names

## Usage

### Python Script

```bash
# Basic usage
python scripts/create_events.py --config examples/events-config.json

# Dry run (test without creating events)
python scripts/create_events.py --config examples/events-config.json --dry-run

# Verbose output
python scripts/create_events.py --config examples/events-config.json --verbose

# Display help
python scripts/create_events.py --help
```

### Generate Config from Zoom Inputs

```bash
python scripts/generate_wp_events_config.py \
  --template examples/events-config.json \
  --zoom-config zoom-meeting-2026-config.json \
  --zoom-output-csv zoom_meetings_output.csv \
  --output wp-events-2026-config.json
```

This generator:
- uses `examples/events-config.json` as the framework,
- maps meetings from Zoom config into WordPress `events`,
- strips trailing ` - 2026` from titles,
- injects standardized registration HTML into each event description,
- and uses `registration_url` matched by `meeting_topic` from `zoom_meetings_output.csv`.

The generated description includes:
- `.registration-note` with registration requirement text,
- `.footer-note` with calendar/update guidance,
- `.annual-reset-note` with annual re-registration guidance.

## Setup Guide

### Creating an Application Password in WordPress

1. Log in to your WordPress admin panel
2. Go to **Users** → **Profile**
3. Scroll down to **Application Passwords**
4. Enter a name for the application (e.g., "Event Series Script")
5. Click **Add New Application Password**
6. Copy the generated password (it will look like: `xxxx xxxx xxxx xxxx xxxx xxxx`)
7. Use this password in your configuration file

### Enabling REST API

The REST API is enabled by default in WordPress. If you're having issues:

1. Check that permalinks are enabled (Settings → Permalinks)
2. Ensure The Events Calendar Pro plugin is installed and activated
3. Test the API endpoint: `https://your-site.com/wp-json/tribe/events/v1/events`

## Examples

### Example 1: Single Event

```json
{
  "wordpress_url": "https://example.com",
  "username": "admin",
  "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx",
  "event": {
    "title": "Team Meeting",
    "description": "Regular team sync meeting",
    "start_date": "2024-01-08",
    "end_date": "2024-01-08",
    "start_time": "10:00:00",
    "end_time": "11:00:00"
  }
}
```

### Example 2: Multiple Events

See `examples/events-config.json` for a complete example with multiple events.

## Troubleshooting

### Authentication Errors

- Verify your username and application password are correct
- Ensure the application password includes spaces as shown
- Check that your user account has permission to create events

### API Endpoint Not Found

- Verify The Events Calendar Pro plugin is installed and activated
- Check that permalinks are enabled in WordPress
- Test the API endpoint in your browser: `https://your-site.com/wp-json/`

### Events Not Creating

- Run with verbose mode to see detailed error messages
- Check WordPress error logs
- Verify date/time formats are correct (YYYY-MM-DD and HH:MM:SS)

### Connection Timeouts

- The script includes a 0.5-second delay between requests
- If you have many events, the script may take time to complete
- Check your server's rate limiting settings

## API Reference

This script uses The Events Calendar Pro REST API. Key endpoints:

- **Create Event**: `POST /wp-json/tribe/events/v1/events`
- **Get Events**: `GET /wp-json/tribe/events/v1/events`
- **Update Event**: `PUT /wp-json/tribe/events/v1/events/{id}`
- **Delete Event**: `DELETE /wp-json/tribe/events/v1/events/{id}`

For more information, see [The Events Calendar REST API documentation](https://theeventscalendar.com/knowledgebase/k/rest-api/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Check The Events Calendar Pro documentation
- Review WordPress REST API documentation

## Version History

### 1.1.0 (2026-02-17)
- Added `scripts/create_events.py` for non-recurring event creation via REST API
- Added support for single `event` and multi `events` config formats
- Updated documentation and examples
