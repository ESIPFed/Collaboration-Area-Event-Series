# Zoom Recurring Meetings API Script

Complete guide for creating recurring Zoom meetings using the Zoom API with support for multiple users in your organization.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output](#output)
- [Troubleshooting](#troubleshooting)

## Overview

This script automates the creation of recurring Zoom meetings for multiple users within your organization. Key features include:

✅ **Multiple User Support** - Create meetings for different Zoom users/emails in your workspace  
✅ **Flexible Recurrence** - Daily, weekly, or monthly recurring patterns  
✅ **Registration Enabled** - Registration activated by default with auto-approval  
✅ **Persistent Storage** - Meeting details and registration links saved to CSV file  
✅ **Configurable Settings** - Full control over meeting settings, security, and scheduling  
✅ **Dry Run Mode** - Test configurations before creating actual meetings  

## Prerequisites

### 1. Zoom Account Requirements

- Zoom Pro, Business, or Enterprise account
- Admin access or appropriate permissions to create meetings for users
- Server-to-Server OAuth App credentials

### 2. System Requirements

- Python 3.6 or higher
- Internet connection
- Required Python packages (see installation)

### 3. Zoom App Setup

You need to create a Server-to-Server OAuth app in the Zoom Marketplace:

#### Step-by-Step Zoom App Creation:

1. **Go to Zoom App Marketplace**
   - Navigate to https://marketplace.zoom.us/
   - Sign in with your Zoom admin account

2. **Create Server-to-Server OAuth App**
   - Click "Develop" → "Build App"
   - Select "Server-to-Server OAuth"
   - Click "Create"

3. **Configure App Information**
   - App Name: "Recurring Meetings Creator" (or your choice)
   - Company Name: Your organization name
   - Developer Contact: Your email
   - Click "Continue"

4. **Get Your Credentials**
   - You'll see three important credentials:
     - **Account ID** - Your Zoom account identifier
     - **Client ID** - OAuth client identifier
     - **Client Secret** - OAuth client secret
   - ⚠️ **IMPORTANT**: Copy and save these credentials securely!

5. **Add Scopes (Permissions)**
   - Click on "Scopes" tab
   - Add the following scopes:
     - `meeting:write:admin` - Create meetings for any user
     - `meeting:read:admin` - Read meeting information
     - `user:read:admin` - Read user information
     - `user:read:user` - Read basic user profile information
   - Click "Continue"

6. **Activate the App**
   - Review your app settings
   - Click "Activate"

## Setup

### 1. Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests
```

### 2. Prepare Configuration File

Create a JSON configuration file with your Zoom credentials and meeting details:

```bash
# Copy the example configuration
cp examples/zoom-config.json my-meetings-config.json

# Edit with your credentials and meeting details
nano my-meetings-config.json
```

## Configuration

### Configuration File Structure

```json
{
  "zoom_api": {
    "account_id": "YOUR_ZOOM_ACCOUNT_ID",
    "client_id": "YOUR_OAUTH_CLIENT_ID",
    "client_secret": "YOUR_OAUTH_CLIENT_SECRET"
  },
  "output_file": "zoom_meetings_output.csv",
  "meetings": [
    {
      "host_email": "user@yourorganization.com",
      "topic": "Meeting Title",
      "agenda": "Meeting description",
      "start_date": "2026-03-01",
      "start_time": "10:00:00",
      "duration": 60,
      "timezone": "America/New_York",
      "recurrence_type": "weekly",
      "weekly_days": "2",
      "end_date": "2026-12-31",
      "enable_registration": true
    }
  ]
}
```

### Configuration Reference

#### Zoom API Settings

| Field | Required | Description |
|-------|----------|-------------|
| `account_id` | Yes | Your Zoom Account ID from the OAuth app |
| `client_id` | Yes | OAuth Client ID from the OAuth app |
| `client_secret` | Yes | OAuth Client Secret from the OAuth app |

#### Output Settings

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `output_file` | No | `zoom_meetings.csv` | Path to CSV file for saving meeting details |

#### Meeting Settings

##### Basic Settings (Required)

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| `host_email` | Yes | Email | Email of Zoom user who will host the meeting |
| `topic` | Yes | String | Meeting title/name |
| `start_date` | Yes | YYYY-MM-DD | Start date for the recurring series |
| `start_time` | Yes | HH:MM:SS | Start time in 24-hour format |

##### Scheduling Settings

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `duration` | No | 60 | Meeting duration in minutes |
| `timezone` | No | UTC | Timezone (e.g., "America/New_York", "Europe/London") |
| `agenda` | No | "" | Meeting description/agenda |

##### Recurrence Settings

| Field | Required | Options | Description |
|-------|----------|---------|-------------|
| `recurrence_type` | Yes | `daily`, `weekly`, `monthly` | Type of recurrence pattern |
| `repeat_interval` | No | 1 | Repeat every N days/weeks/months |
| `end_date` | No* | YYYY-MM-DD | Last date for the series |
| `occurrences` | No* | Number | Number of occurrences (alternative to end_date) |

*At least one of `end_date` or `occurrences` should be specified

**For Weekly Recurrence:**

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| `weekly_days` | No | String | Days of week: "1"=Sunday, "2"=Monday, ..., "7"=Saturday<br>Multiple days: "1,3,5" |

**For Monthly Recurrence:**

| Field | Required | Format | Description |
|-------|----------|--------|-------------|
| `monthly_day` | No | 1-31 | Day of the month for the meeting |

##### Registration Settings

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `enable_registration` | No | true | Enable/disable registration |
| `approval_type` | No | 0 | 0=auto approve, 1=manual, 2=no registration |
| `registration_type` | No | 1 | 1=register once for all, 2=register for each, 3=one occurrence |

##### Meeting Settings

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `host_video` | No | true | Start with host video on |
| `participant_video` | No | true | Start with participant video on |
| `join_before_host` | No | false | Allow participants to join before host |
| `mute_upon_entry` | No | true | Mute participants upon entry |
| `waiting_room` | No | true | Enable waiting room |
| `password` | No | - | Meeting password |
| `watermark` | No | false | Enable watermark |
| `auto_recording` | No | none | `none`, `local`, or `cloud` |
| `audio` | No | both | `both`, `telephony`, or `voip` |
| `meeting_authentication` | No | false | Require authentication to join |

## Usage

### Basic Usage

Create meetings from your configuration file:

```bash
python scripts/create_zoom_recurring_meetings.py --config my-meetings-config.json
```

### Dry Run Mode

Test your configuration without creating actual meetings:

```bash
python scripts/create_zoom_recurring_meetings.py --config my-meetings-config.json --dry-run
```

This will show you exactly what would be created without making any API calls.

### Verbose Mode

Get detailed output during creation:

```bash
python scripts/create_zoom_recurring_meetings.py --config my-meetings-config.json --verbose
```

Note: verbose mode attempts to verify each host with `GET /users/{email}`. If your app token does not include user-read scopes (`user:read:user:admin` and `user:read:user`), the script now skips only that verification step and still proceeds with meeting creation.

### Combined Options

```bash
python scripts/create_zoom_recurring_meetings.py \
  --config my-meetings-config.json \
  --dry-run \
  --verbose
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--config` | - | Path to JSON configuration file (required) |
| `--dry-run` | - | Preview what would be created without creating |
| `--verbose` | `-v` | Enable verbose output with detailed information |
| `--help` | `-h` | Show help message and exit |

## Output

### Console Output

The script provides clear feedback during execution:

```
======================================================================
Creating 3 recurring meeting(s)...
======================================================================

[1/3] Processing: Weekly Team Standup
  Host: user1@yourorganization.com
  ✓ Meeting created successfully!
    - Meeting ID: 87654321098
    - Join URL: https://zoom.us/j/87654321098
    - Registration URL: https://zoom.us/meeting/register/tJ...

[2/3] Processing: Monthly Leadership Meeting
  Host: user2@yourorganization.com
  ✓ Meeting created successfully!
    - Meeting ID: 98765432101
    - Join URL: https://zoom.us/j/98765432101
    - Registration URL: https://zoom.us/meeting/register/tZ...

======================================================================
✓ Complete! Meeting details saved to: zoom_meetings_output.csv
======================================================================
```

### CSV Output File

All meeting details are saved to a persistent CSV file (default: `zoom_meetings_output.csv`):

| Column | Description |
|--------|-------------|
| `created_at` | Timestamp when meeting was created |
| `host_email` | Email of the meeting host |
| `meeting_id` | Unique Zoom meeting ID |
| `meeting_topic` | Meeting title |
| `start_time` | First occurrence start time |
| `timezone` | Meeting timezone |
| `duration` | Meeting duration in minutes |
| `join_url` | Join URL for the meeting |
| `registration_url` | Registration URL (if registration is enabled) |
| `recurrence_type` | Type of recurrence (1=daily, 2=weekly, 3=monthly) |
| `occurrences` | Number of occurrences |

**Example CSV content:**

```csv
created_at,host_email,meeting_id,meeting_topic,start_time,timezone,duration,join_url,registration_url,recurrence_type,occurrences
2026-02-10T14:30:00,user1@org.com,87654321098,Weekly Team Standup,2026-03-03T09:00:00,America/New_York,30,https://zoom.us/j/87654321098,https://zoom.us/meeting/register/tJ...,2,44
```

## Examples

### Example 1: Weekly Meeting, Single User

```json
{
  "zoom_api": {
    "account_id": "abc123xyz",
    "client_id": "client_id_here",
    "client_secret": "client_secret_here"
  },
  "output_file": "team_meetings.csv",
  "meetings": [
    {
      "host_email": "manager@company.com",
      "topic": "Monday Team Sync",
      "agenda": "Weekly team synchronization meeting",
      "start_date": "2026-03-03",
      "start_time": "09:00:00",
      "duration": 45,
      "timezone": "America/New_York",
      "recurrence_type": "weekly",
      "weekly_days": "2",
      "end_date": "2026-12-31",
      "enable_registration": true
    }
  ]
}
```

### Example 2: Multiple Users, Different Schedules

```json
{
  "zoom_api": {
    "account_id": "abc123xyz",
    "client_id": "client_id_here",
    "client_secret": "client_secret_here"
  },
  "meetings": [
    {
      "host_email": "sales@company.com",
      "topic": "Sales Pipeline Review",
      "start_date": "2026-03-04",
      "start_time": "10:00:00",
      "duration": 60,
      "timezone": "America/Los_Angeles",
      "recurrence_type": "weekly",
      "weekly_days": "3",
      "end_date": "2026-12-31",
      "enable_registration": false
    },
    {
      "host_email": "engineering@company.com",
      "topic": "Engineering Sprint Planning",
      "start_date": "2026-03-04",
      "start_time": "14:00:00",
      "duration": 120,
      "timezone": "America/New_York",
      "recurrence_type": "weekly",
      "weekly_days": "3",
      "repeat_interval": 2,
      "end_date": "2026-12-31",
      "enable_registration": true
    }
  ]
}
```

### Example 3: Monthly Meeting with Fixed Day

```json
{
  "zoom_api": {
    "account_id": "abc123xyz",
    "client_id": "client_id_here",
    "client_secret": "client_secret_here"
  },
  "meetings": [
    {
      "host_email": "hr@company.com",
      "topic": "Monthly All-Hands",
      "agenda": "Company-wide monthly meeting",
      "start_date": "2026-03-15",
      "start_time": "15:00:00",
      "duration": 90,
      "timezone": "America/Chicago",
      "recurrence_type": "monthly",
      "monthly_day": 15,
      "occurrences": 10,
      "enable_registration": true,
      "waiting_room": false,
      "auto_recording": "cloud"
    }
  ]
}
```

## Troubleshooting

### Common Issues

#### 1. Authentication Error

**Error:** `Error getting access token: 401 Unauthorized`

**Solution:**
- Verify your Account ID, Client ID, and Client Secret are correct
- Ensure your OAuth app is activated in the Zoom Marketplace
- Check that you haven't accidentally added extra spaces in credentials

#### 2. Insufficient Permissions

**Error:** `User does not have permission to create meeting`

**Solution:**
- Ensure your OAuth app has the `meeting:write:admin` scope
- Verify you have admin permissions in your Zoom account
- Re-activate your OAuth app after adding scopes

#### 2a. Verbose Mode Scope Warning

**Warning:** `Skipping user verification: token missing user read scope(s).`

**What it means:**
- Meeting creation can still succeed if meeting write scopes are present
- Only the verbose pre-check (`GET /users/{email}`) is skipped

**To enable full verbose user verification:**
- Add `user:read:user:admin` and `user:read:user` scopes to your Zoom app
- Re-activate the app and generate a fresh token

#### 3. Invalid User Email

**Error:** `User not found`

**Solution:**
- Verify the email address exists in your Zoom account
- Check for typos in the email address
- Ensure the user is active (not deactivated)

#### 4. Invalid Date/Time Format

**Error:** `Invalid start_date format`

**Solution:**
- Use ISO format for dates: YYYY-MM-DD
- Use 24-hour format for times: HH:MM:SS
- Example: "2026-03-15" and "14:30:00"

#### 5. Rate Limiting

**Error:** `Too many requests`

**Solution:**
- The script automatically adds 1-second delays between API calls
- If you have many meetings, consider splitting into multiple configuration files
- Wait a few minutes before retrying

### Validation

Before running, validate your configuration with dry-run:

```bash
python scripts/create_zoom_recurring_meetings.py --config config.json --dry-run --verbose
```

This will:
- ✓ Validate JSON syntax
- ✓ Check required fields
- ✓ Verify date/time formats
- ✓ Show what would be created
- ✗ NOT make any API calls or create meetings

### Getting Help

If you encounter issues:

1. **Check the logs** - Run with `--verbose` flag for detailed output
2. **Validate your config** - Use `--dry-run` to test configuration
3. **Review Zoom API docs** - https://developers.zoom.us/docs/api/
4. **Check the output CSV** - See what meetings were successfully created

## Security Best Practices

### 1. Protect Your Credentials

- ⚠️ **Never** commit your configuration file with real credentials to version control
- Store credentials in environment variables or a secure secrets manager
- Add `*-config.json` to your `.gitignore` file

### 2. Use Strong Passwords

- If setting meeting passwords, use strong, unique passwords
- Consider using a password manager to generate passwords

### 3. Configure Security Settings

```json
{
  "waiting_room": false,
  "password": "strong-password-here",
  "meeting_authentication": true,
  "watermark": true
}
```

### 4. Limit Permissions

- Only grant necessary OAuth scopes
- Review and audit app permissions regularly
- Deactivate OAuth apps when no longer needed

## Additional Resources

- **Zoom API Documentation:** https://developers.zoom.us/docs/api/
- **Zoom App Marketplace:** https://marketplace.zoom.us/
- **Meeting API Reference:** https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Meetings
- **OAuth Documentation:** https://developers.zoom.us/docs/internal-apps/s2s-oauth/

## Support

For issues specific to this script:
- Check the [troubleshooting section](#troubleshooting)
- Review example configurations in `examples/zoom-config.json`
- Run with `--verbose` flag for detailed debugging

For Zoom API issues:
- Consult Zoom API documentation
- Contact Zoom Developer Support
- Check Zoom API status page

---

**Last Updated:** February 2026  
**Script Version:** 1.0.0
