# Quick Start Guide

This guide will help you get started with creating recurring events in WordPress using The Events Calendar Pro API.

## Step 1: Prerequisites

1. **WordPress Setup**
   - WordPress site with The Events Calendar Pro plugin installed
   - REST API enabled (enabled by default)
   - Permalinks enabled (Settings → Permalinks)

2. **Authentication**
   - Create an Application Password in WordPress:
     - Go to Users → Profile
     - Scroll to "Application Passwords"
     - Enter a name (e.g., "Event Series Script")
     - Click "Add New Application Password"
     - Copy the generated password

3. **Development Environment**
   - Python 3.6+
   - Install dependencies: `pip install requests`

## Step 2: Create Your Configuration File

Copy one of the example configurations:

```bash
# For a simple test
cp examples/simple-config.json my-config.json

# For multiple events
cp examples/event-series-config.json my-config.json
```

Edit `my-config.json` with your details:
- Replace `wordpress_url` with your WordPress site URL
- Replace `username` with your WordPress username
- Replace `app_password` with your Application Password
- Customize the events array with your events

## Step 3: Test Your Configuration

Run a dry-run to verify your configuration (Python only):

```bash
python scripts/create_recurring_events.py --config my-config.json --dry-run
```

This will show what would be created without actually creating events.

## Step 4: Create Your Events

```bash
# Basic usage
python scripts/create_recurring_events.py --config my-config.json

# With verbose output to see details
python scripts/create_recurring_events.py --config my-config.json --verbose
```

## Step 5: Verify in WordPress

1. Log in to your WordPress admin panel
2. Go to Events → All Events
3. You should see your newly created recurring events

## Common Issues

### "Authentication failed"
- Double-check your username and application password
- Ensure you're using an Application Password, not your regular password
- Verify your user has permission to create events

### "API endpoint not found"
- Verify The Events Calendar Pro plugin is installed and activated
- Check that permalinks are enabled
- Test the API: visit `https://your-site.com/wp-json/`

### "Invalid date format"
- Dates must be in YYYY-MM-DD format (e.g., 2024-01-15)
- Times must be in HH:MM:SS format (e.g., 14:30:00)

### "Invalid recurrence_day"
- Must be in format: "first Monday", "second Tuesday", etc.
- Valid positions: first, second, third, fourth, last
- Valid days: Monday through Sunday

## Tips

1. **Start Small**: Test with one event first using the simple config
2. **Use Dry-Run**: Always test with `--dry-run` before creating events
3. **Check Dates**: Ensure start_date comes before end_date
4. **Backup**: Consider backing up your WordPress database before bulk operations
5. **Rate Limiting**: The script includes a 0.5-second delay between requests to avoid overwhelming your server

## Example: Creating Monthly Team Meetings

Here's a complete example for creating a monthly team meeting:

```json
{
  "wordpress_url": "https://mycompany.com",
  "username": "admin",
  "app_password": "abcd efgh ijkl mnop qrst uvwx",
  "events": [
    {
      "title": "Monthly Team Sync",
      "description": "Regular monthly team meeting to discuss progress and plans",
      "start_date": "2024-01-08",
      "end_date": "2024-12-31",
      "start_time": "10:00:00",
      "end_time": "11:00:00",
      "recurrence_pattern": "MONTHLY",
      "recurrence_day": "first Monday",
      "venue": "Conference Room A",
      "organizer": "Team Lead",
      "categories": ["Team Meeting", "Internal"]
    }
  ]
}
```

Save this as `team-meetings.json` and run:

```bash
python scripts/create_recurring_events.py --config team-meetings.json --dry-run
```

If everything looks good, create the events:

```bash
python scripts/create_recurring_events.py --config team-meetings.json
```

## Next Steps

- Read the [full documentation](README.md) for advanced features
- Check out more examples in the `examples/` directory
- Customize event fields like venues, organizers, and categories
- Create multiple event series in a single configuration file

## Support

If you encounter issues:
1. Check the troubleshooting section in docs/README.md
2. Verify your configuration with dry-run mode
3. Enable verbose output for detailed error messages
4. Open an issue on GitHub with your error details
