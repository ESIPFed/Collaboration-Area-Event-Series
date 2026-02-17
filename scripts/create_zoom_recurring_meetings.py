#!/usr/bin/env python3
"""
Create Recurring Zoom Meetings using Zoom API

This script creates recurring meetings in Zoom for multiple users within your organization.
Each meeting can have unique configurations for start date, time, recurrence pattern, and end date.
Registration is enabled by default, and meeting details with registration links are saved to a
persistent CSV file.

Requirements:
- Python 3.6+
- requests library (install with: pip install requests)
- Zoom Server-to-Server OAuth App credentials
- Admin or appropriate permissions to create meetings for users

Usage:
    python create_zoom_recurring_meetings.py --config config.json
    python create_zoom_recurring_meetings.py --config config.json --dry-run
    python create_zoom_recurring_meetings.py --help

@package Collaboration-Area-Event-Series
@version 1.0.0
"""

import argparse
import json
import sys
import time
import csv
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import base64

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


class ZoomAPIClient:
    """Client for interacting with Zoom API"""
    
    def __init__(self, account_id: str, client_id: str, client_secret: str):
        """
        Initialize Zoom API client with Server-to-Server OAuth credentials
        
        Args:
            account_id: Zoom Account ID
            client_id: OAuth Client ID
            client_secret: OAuth Client Secret
        """
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.zoom.us/v2"
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self) -> str:
        """
        Get OAuth access token using Server-to-Server OAuth
        
        Returns:
            Access token string
        """
        # Check if we have a valid token
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        # Request new token
        token_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={self.account_id}"
        
        # Create Basic Auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            response = requests.post(token_url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data["access_token"]
            # Token expires in data["expires_in"] seconds, set expiry with buffer
            self.token_expiry = datetime.now() + timedelta(seconds=data["expires_in"] - 300)
            
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting access token: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            sys.exit(1)
    
    def create_meeting(self, user_email: str, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a meeting for a specific user
        
        Args:
            user_email: Email of the Zoom user who will host the meeting
            meeting_data: Dictionary containing meeting configuration
            
        Returns:
            Dictionary with meeting details including registration link
        """
        token = self.get_access_token()
        
        url = f"{self.base_url}/users/{user_email}/meetings"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=meeting_data)
        response.raise_for_status()
        
        return response.json()
    
    def get_user_info(self, user_email: str) -> Dict[str, Any]:
        """
        Get information about a Zoom user
        
        Args:
            user_email: Email of the Zoom user
            
        Returns:
            Dictionary with user information
        """
        token = self.get_access_token()
        
        url = f"{self.base_url}/users/{user_email}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()


def parse_recurrence_config(meeting_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse meeting configuration and build Zoom recurrence object
    
    Args:
        meeting_config: Meeting configuration dictionary
        
    Returns:
        Zoom API recurrence configuration
    """
    recurrence = {
        "type": 1,  # Default to daily, will be overridden
        "repeat_interval": meeting_config.get("repeat_interval", 1)
    }
    
    # Parse recurrence type
    recurrence_type = meeting_config.get("recurrence_type", "weekly").lower()
    
    if recurrence_type == "daily":
        recurrence["type"] = 1
    elif recurrence_type == "weekly":
        recurrence["type"] = 2
        # weekly_days: 1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday
        # Can be comma-separated for multiple days: "1,3,5"
        if "weekly_days" in meeting_config:
            recurrence["weekly_days"] = meeting_config["weekly_days"]
        else:
            # Default to the day of the start date
            start_date = datetime.fromisoformat(meeting_config["start_date"])
            # Python weekday: 0=Monday to 6=Sunday, Zoom: 1=Sunday to 7=Saturday
            python_weekday = start_date.weekday()
            zoom_weekday = python_weekday + 2 if python_weekday < 6 else 1
            recurrence["weekly_days"] = str(zoom_weekday)
    elif recurrence_type == "monthly":
        recurrence["type"] = 3
        # Option 1: Specific day of month (monthly_day: 1-31)
        # Option 2: Nth weekday of month (monthly_week + monthly_week_day)
        if "monthly_week" in meeting_config and "monthly_week_day" in meeting_config:
            recurrence["monthly_week"] = meeting_config["monthly_week"]
            recurrence["monthly_week_day"] = meeting_config["monthly_week_day"]
            # monthly_day and monthly_week[_day] are mutually exclusive in Zoom API
            recurrence.pop("monthly_day", None)
        elif "monthly_day" in meeting_config:
            recurrence["monthly_day"] = meeting_config["monthly_day"]
        else:
            # Default to the day of the start date
            start_date = datetime.fromisoformat(meeting_config["start_date"])
            recurrence["monthly_day"] = start_date.day
    
    # Set end date/occurrences
    if "end_date" in meeting_config:
        end_date = datetime.fromisoformat(meeting_config["end_date"])
        recurrence["end_date_time"] = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    elif "occurrences" in meeting_config:
        recurrence["end_times"] = meeting_config["occurrences"]
    
    return recurrence


def build_meeting_payload(meeting_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build the Zoom API meeting payload from configuration
    
    Args:
        meeting_config: Meeting configuration dictionary
        
    Returns:
        Zoom API meeting payload
    """
    # Parse start date and time
    start_date = meeting_config["start_date"]
    start_time = meeting_config["start_time"]
    
    # Combine date and time
    start_datetime = f"{start_date}T{start_time}"
    
    # Build base payload
    payload = {
        "topic": meeting_config["topic"],
        "type": 8,  # 8 = Recurring meeting with fixed time
        "start_time": start_datetime,
        "duration": meeting_config.get("duration", 60),
        "timezone": meeting_config.get("timezone", "UTC"),
        "agenda": meeting_config.get("agenda", ""),
        "recurrence": parse_recurrence_config(meeting_config),
        "settings": {
            "host_video": meeting_config.get("host_video", True),
            "participant_video": meeting_config.get("participant_video", True),
            "join_before_host": meeting_config.get("join_before_host", False),
            "mute_upon_entry": meeting_config.get("mute_upon_entry", True),
            "watermark": meeting_config.get("watermark", False),
            "use_pmi": False,
            "approval_type": meeting_config.get("approval_type", 2),  # 0=auto, 1=manual, 2=no registration required
            "registration_type": meeting_config.get("registration_type", 1),  # 1=Attendees register once and can attend any occurrence
            "audio": meeting_config.get("audio", "both"),  # both, telephony, voip
            "auto_recording": meeting_config.get("auto_recording", "none"),  # none, local, cloud
            "waiting_room": meeting_config.get("waiting_room", True),
            "meeting_authentication": meeting_config.get("meeting_authentication", False)
        }
    }
    
    # Enable registration by default (as required)
    enable_registration = meeting_config.get("enable_registration", True)
    if enable_registration:
        payload["settings"]["approval_type"] = meeting_config.get("approval_type", 0)  # 0=auto approve
    
    # Add password if specified
    if "password" in meeting_config:
        payload["password"] = meeting_config["password"]
    
    return payload


def save_meeting_to_file(meeting_info: Dict[str, Any], user_email: str, output_file: str, verbose: bool = False):
    """
    Save meeting information to a persistent CSV file
    
    Args:
        meeting_info: Meeting information from Zoom API
        user_email: Email of the meeting host
        output_file: Path to output CSV file
        verbose: Enable verbose output
    """
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(output_file)
    
    # Prepare row data
    row = {
        "created_at": datetime.now().isoformat(),
        "host_email": user_email,
        "meeting_id": meeting_info.get("id", ""),
        "meeting_topic": meeting_info.get("topic", ""),
        "start_time": meeting_info.get("start_time", ""),
        "timezone": meeting_info.get("timezone", ""),
        "duration": meeting_info.get("duration", ""),
        "join_url": meeting_info.get("join_url", ""),
        "registration_url": meeting_info.get("registration_url", ""),
        "recurrence_type": meeting_info.get("recurrence", {}).get("type", ""),
        "occurrences": meeting_info.get("occurrences", 0)
    }
    
    # Write to CSV
    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        
        # Write header if new file
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row)
    
    if verbose:
        print(f"✓ Saved meeting details to {output_file}")


def create_meetings_from_config(config: Dict[str, Any], dry_run: bool = False, verbose: bool = False):
    """
    Create Zoom meetings from configuration file
    
    Args:
        config: Configuration dictionary
        dry_run: If True, show what would be created without creating
        verbose: Enable verbose output
    """
    # Extract Zoom API credentials
    zoom_config = config.get("zoom_api", {})
    account_id = zoom_config.get("account_id")
    client_id = zoom_config.get("client_id")
    client_secret = zoom_config.get("client_secret")
    
    if not all([account_id, client_id, client_secret]):
        print("Error: Missing Zoom API credentials in configuration")
        print("Required: zoom_api.account_id, zoom_api.client_id, zoom_api.client_secret")
        sys.exit(1)
    
    # Initialize Zoom API client
    if not dry_run:
        zoom_client = ZoomAPIClient(account_id, client_id, client_secret)
        print("✓ Connected to Zoom API")
    
    # Get output file path
    output_file = config.get("output_file", "zoom_meetings.csv")
    default_password = config.get("default_password")
    
    # Process each meeting configuration
    meetings = config.get("meetings", [])
    
    if not meetings:
        print("Warning: No meetings defined in configuration")
        return
    
    print(f"\n{'=' * 70}")
    print(f"Creating {len(meetings)} recurring meeting(s)...")
    print(f"{'=' * 70}\n")
    
    for idx, meeting_config in enumerate(meetings, 1):
        user_email = meeting_config.get("host_email")
        topic = meeting_config.get("topic", "Untitled Meeting")
        
        if not user_email:
            print(f"⚠ Skipping meeting #{idx}: Missing host_email")
            continue
        
        print(f"[{idx}/{len(meetings)}] Processing: {topic}")
        print(f"  Host: {user_email}")
        
        if dry_run:
            print("  [DRY RUN] Would create meeting with:")
            meeting_config_with_defaults = dict(meeting_config)
            if default_password and "password" not in meeting_config_with_defaults:
                meeting_config_with_defaults["password"] = default_password

            payload = build_meeting_payload(meeting_config_with_defaults)
            print("  [DRY RUN] JSON payload:")
            print(json.dumps(payload, indent=2))
            print(f"    - Topic: {payload['topic']}")
            print(f"    - Start: {payload['start_time']}")
            print(f"    - Duration: {payload['duration']} minutes")
            print(f"    - Timezone: {payload['timezone']}")
            print(f"    - Recurrence: Type {payload['recurrence']['type']}")
            print(f"    - Registration: {'Enabled' if meeting_config.get('enable_registration', True) else 'Disabled'}")
            print()
            continue
        
        try:
            # Verify user exists
            if verbose:
                try:
                    user_info = zoom_client.get_user_info(user_email)
                    print(f"  ✓ User verified: {user_info.get('first_name', '')} {user_info.get('last_name', '')}")
                except requests.exceptions.HTTPError as e:
                    error_message = ""
                    if hasattr(e, 'response') and e.response is not None:
                        try:
                            error_message = e.response.json().get("message", "")
                        except Exception:
                            error_message = e.response.text

                    if "does not contain scopes" in error_message and (
                        "user:read:user:admin" in error_message or "user:read:user" in error_message
                    ):
                        print("  ⚠ Skipping user verification: token missing user read scope(s).")
                        print("    Add scopes 'user:read:user:admin' and 'user:read:user' to enable this verbose check.")
                    else:
                        raise
            
            # Build meeting payload
            meeting_config_with_defaults = dict(meeting_config)
            if default_password and "password" not in meeting_config_with_defaults:
                meeting_config_with_defaults["password"] = default_password

            payload = build_meeting_payload(meeting_config_with_defaults)
            
            # Create meeting
            meeting_info = zoom_client.create_meeting(user_email, payload)
            
            print(f"  ✓ Meeting created successfully!")
            print(f"    - Meeting ID: {meeting_info.get('id')}")
            print(f"    - Join URL: {meeting_info.get('join_url')}")
            
            if meeting_config.get("enable_registration", True):
                reg_url = meeting_info.get("registration_url", "N/A")
                print(f"    - Registration URL: {reg_url}")
            
            # Save to persistent file
            save_meeting_to_file(meeting_info, user_email, output_file, verbose)
            
            print()
            
            # Rate limiting - be nice to the API
            if idx < len(meetings):
                time.sleep(1)
                
        except requests.exceptions.HTTPError as e:
            print(f"  ✗ Error creating meeting: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"    Error details: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"    Response: {e.response.text}")
            print()
            continue
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            print()
            continue
    
    if not dry_run:
        print(f"{'=' * 70}")
        print(f"✓ Complete! Meeting details saved to: {output_file}")
        print(f"{'=' * 70}")


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration file
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    # Check for Zoom API credentials
    if "zoom_api" not in config:
        print("Error: Missing 'zoom_api' section in configuration")
        return False
    
    zoom_config = config["zoom_api"]
    required_zoom_fields = ["account_id", "client_id", "client_secret"]
    
    for field in required_zoom_fields:
        if field not in zoom_config:
            print(f"Error: Missing required field 'zoom_api.{field}'")
            return False
    
    # Check for meetings
    if "meetings" not in config or not config["meetings"]:
        print("Error: No meetings defined in configuration")
        return False
    
    # Validate each meeting
    for idx, meeting in enumerate(config["meetings"], 1):
        required_meeting_fields = ["host_email", "topic", "start_date", "start_time"]
        
        for field in required_meeting_fields:
            if field not in meeting:
                print(f"Error: Meeting #{idx} missing required field '{field}'")
                return False
        
        # Validate date format
        try:
            datetime.fromisoformat(meeting["start_date"])
        except ValueError:
            print(f"Error: Meeting #{idx} has invalid start_date format. Use YYYY-MM-DD")
            return False
        
        # Validate time format
        try:
            datetime.strptime(meeting["start_time"], "%H:%M:%S")
        except ValueError:
            print(f"Error: Meeting #{idx} has invalid start_time format. Use HH:MM:SS")
            return False
        
        # Validate end_date if provided
        if "end_date" in meeting:
            try:
                datetime.fromisoformat(meeting["end_date"])
            except ValueError:
                print(f"Error: Meeting #{idx} has invalid end_date format. Use YYYY-MM-DD")
                return False
    
    return True


def get_help_epilog() -> str:
    """Get help epilog text"""
    return """
Configuration File Format:
{
  "zoom_api": {
    "account_id": "your-account-id",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  },
  "output_file": "zoom_meetings.csv",
    "default_password": "collab26",
  "meetings": [
    {
      "host_email": "user@example.com",
      "topic": "Weekly Team Meeting",
      "agenda": "Discuss project updates and blockers",
      "start_date": "2026-03-01",
      "start_time": "10:00:00",
      "duration": 60,
      "timezone": "America/New_York",
      "recurrence_type": "weekly",
      "weekly_days": "2",
      "end_date": "2026-12-31",
      "enable_registration": true,
      "host_video": true,
      "participant_video": true,
    "waiting_room": false
    }
  ]
}

Recurrence Types:
- daily: Repeats every day or every N days (use repeat_interval)
- weekly: Repeats on specific days of the week
  * weekly_days: "1" (Sunday), "2" (Monday), ..., "7" (Saturday)
  * Multiple days: "1,3,5" (Sunday, Tuesday, Thursday)
- monthly: Repeats on a specific day of the month
    * monthly_day: 1-31 (day of month)
    * OR monthly_week + monthly_week_day for nth weekday patterns:
        - monthly_week: 1 (first), 2 (second), 3 (third), 4 (fourth), -1 (last)
        - monthly_week_day: 1 (Sunday) ... 7 (Saturday)

End Date Options:
- end_date: ISO format date (YYYY-MM-DD)
- occurrences: Number of times to repeat (alternative to end_date)

Registration Settings:
- enable_registration: true/false (default: true)
- approval_type: 0 (auto), 1 (manual), 2 (no registration)
- registration_type: 1 (register once for all), 2 (register for each), 3 (register for one)

For more information, see: https://developers.zoom.us/docs/api/
"""


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description='Create recurring Zoom meetings using Zoom API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_help_epilog()
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Path to JSON configuration file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without actually creating'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    # Create meetings
    create_meetings_from_config(config, dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()
