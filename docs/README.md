# Events Calendar Pro API - Recurring Events Scripts

This repository contains scripts and utilities for creating recurring event series in WordPress using The Events Calendar Pro REST API. Each event can have a unique name and recur monthly on specific days (e.g., first Monday of each month).

## Features

- ✅ Create multiple recurring events from a single configuration file
- ✅ Support for monthly recurrence patterns (first/second/third/fourth/last day of week)
- ✅ Unique event names for each event in the series
- ✅ Customizable start/end dates and times
- ✅ Support for venues, organizers, and categories
- ✅ Both PHP and Python implementations available
- ✅ Dry-run mode for testing (Python version)
- ✅ Verbose output for debugging

## Requirements

### For PHP Script

- PHP 7.4 or higher
- cURL extension enabled
- WordPress site with The Events Calendar Pro plugin installed
- REST API enabled on WordPress
- Application password for authentication

### For Python Script

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

2. For Python users, install dependencies:
   ```bash
   pip install requests
   ```

## Configuration

Create a JSON configuration file with your WordPress credentials and event details. See `examples/event-series-config.json` for a complete example.

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
      "end_date": "2024-12-31",
      "start_time": "14:00:00",
      "end_time": "15:00:00",
      "recurrence_pattern": "MONTHLY",
      "recurrence_day": "first Monday",
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
- `events`: Array of event objects

### Event Object Fields

**Required:**
- `title`: Event title/name (string)
- `start_date`: First occurrence date in YYYY-MM-DD format
- `end_date`: Last occurrence date in YYYY-MM-DD format
- `start_time`: Event start time in HH:MM:SS format
- `end_time`: Event end time in HH:MM:SS format

**Optional:**
- `description`: Event description (string)
- `recurrence_pattern`: Currently supports "MONTHLY" (default)
- `recurrence_day`: Day pattern like "first Monday", "second Tuesday", etc.
- `venue`: Venue name (string)
- `organizer`: Organizer name (string)
- `categories`: Array of category names

### Recurrence Day Format

The `recurrence_day` field accepts patterns like:
- `first Monday` - First Monday of each month
- `second Tuesday` - Second Tuesday of each month
- `third Wednesday` - Third Wednesday of each month
- `fourth Thursday` - Fourth Thursday of each month
- `last Friday` - Last Friday of each month

## Usage

### PHP Script

```bash
# Basic usage
php scripts/create-recurring-events.php --config=examples/event-series-config.json

# Display help
php scripts/create-recurring-events.php --help
```

### Python Script

```bash
# Basic usage
python scripts/create_recurring_events.py --config examples/event-series-config.json

# Dry run (test without creating events)
python scripts/create_recurring_events.py --config examples/event-series-config.json --dry-run

# Verbose output
python scripts/create_recurring_events.py --config examples/event-series-config.json --verbose

# Display help
python scripts/create_recurring_events.py --help
```

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

### Example 1: Single Recurring Event

```json
{
  "wordpress_url": "https://example.com",
  "username": "admin",
  "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx",
  "events": [
    {
      "title": "Monthly Team Meeting",
      "description": "Regular team sync meeting",
      "start_date": "2024-01-08",
      "end_date": "2024-12-31",
      "start_time": "10:00:00",
      "end_time": "11:00:00",
      "recurrence_day": "first Monday"
    }
  ]
}
```

### Example 2: Multiple Event Series

See `examples/event-series-config.json` for a complete example with multiple events.

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
- Ensure recurrence_day format is valid

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

### 1.0.0 (2024-01-01)
- Initial release
- PHP script for creating recurring events
- Python script with dry-run and verbose modes
- Example configuration files
- Comprehensive documentation
