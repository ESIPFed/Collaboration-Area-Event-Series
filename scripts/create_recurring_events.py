#!/usr/bin/env python3
"""
Create Recurring Events using The Events Calendar Pro API

This script creates recurring events in WordPress using The Events Calendar Pro REST API.
Each event in the series has a unique name and recurs monthly on a specific day pattern
(e.g., first Monday of each month).

Requirements:
- Python 3.6+
- requests library (install with: pip install requests)
- WordPress with The Events Calendar Pro plugin installed
- REST API enabled
- Application password or authentication credentials

Usage:
    python create_recurring_events.py --config config.json
    python create_recurring_events.py --help

@package Collaboration-Area-Event-Series
@version 1.0.0
"""

import argparse
import json
import sys
import time
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description='Create recurring events for The Events Calendar Pro',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_help_epilog()
    )
    parser.add_argument('--config', required=True, help='Path to JSON configuration file')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without actually creating')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
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
    
    # Create events
    create_recurring_event_series(config, dry_run=args.dry_run, verbose=args.verbose)


def get_help_epilog() -> str:
    """Get help epilog text"""
    return """
Configuration File Format:
{
  "wordpress_url": "https://your-site.com",
  "username": "your-username",
  "app_password": "your-app-password",
  "events": [
    {
      "title": "Event Name",
      "description": "Event description",
      "start_date": "2024-01-01",
      "end_date": "2024-12-31",
      "start_time": "14:00:00",
      "end_time": "15:00:00",
      "recurrence_pattern": "MONTHLY",
      "recurrence_day": "first Monday",
      "venue": "Virtual",
      "organizer": "Organization Name",
      "categories": ["Category1", "Category2"]
    }
  ]
}

Recurrence Day Format:
  - "first Monday" - First Monday of each month
  - "second Tuesday" - Second Tuesday of each month
  - "third Wednesday" - Third Wednesday of each month
  - "fourth Thursday" - Fourth Thursday of each month
  - "last Friday" - Last Friday of each month
"""


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['wordpress_url', 'username', 'app_password', 'events']
    
    for field in required_fields:
        if field not in config:
            print(f"Error: Missing required field '{field}' in config")
            return False
    
    if not isinstance(config['events'], list) or not config['events']:
        print("Error: 'events' must be a non-empty array")
        return False
    
    for index, event in enumerate(config['events']):
        event_required = ['title', 'start_date', 'end_date', 'start_time', 'end_time']
        for field in event_required:
            if field not in event:
                print(f"Error: Event {index} missing required field '{field}'")
                return False
        
        # Validate date format
        try:
            datetime.strptime(event['start_date'], '%Y-%m-%d')
            datetime.strptime(event['end_date'], '%Y-%m-%d')
        except ValueError as e:
            print(f"Error: Invalid date format in event {index}: {e}")
            return False
        
        # Validate time format
        try:
            datetime.strptime(event['start_time'], '%H:%M:%S')
            datetime.strptime(event['end_time'], '%H:%M:%S')
        except ValueError as e:
            print(f"Error: Invalid time format in event {index}: {e}")
            return False
    
    return True


def create_recurring_event_series(config: Dict[str, Any], dry_run: bool = False, verbose: bool = False):
    """
    Create recurring event series
    
    Args:
        config: Configuration dictionary
        dry_run: If True, show what would be created without actually creating
        verbose: Enable verbose output
    """
    wp_url = config['wordpress_url'].rstrip('/')
    api_url = f"{wp_url}/wp-json/tribe/events/v1/events"
    
    auth = (config['username'], config['app_password'])
    
    print("Creating recurring event series...")
    print(f"WordPress URL: {wp_url}")
    print(f"Number of events to create: {len(config['events'])}")
    
    if dry_run:
        print("\n*** DRY RUN MODE - No events will be created ***\n")
    
    print()
    
    success_count = 0
    failure_count = 0
    
    for index, event_data in enumerate(config['events']):
        print(f"Processing event {index + 1}: {event_data['title']}")
        
        try:
            if dry_run:
                print(f"  [DRY RUN] Would create recurring event")
                if verbose:
                    print(f"  Event data: {json.dumps(event_data, indent=2)}")
                success_count += 1
            else:
                event_id = create_recurring_event(api_url, auth, event_data, verbose)
                if event_id:
                    print(f"  ✓ Successfully created event ID: {event_id}")
                    success_count += 1
                else:
                    print(f"  ✗ Failed to create event")
                    failure_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failure_count += 1
        
        print()
        
        # Small delay to avoid overwhelming the server
        if not dry_run:
            time.sleep(0.5)
    
    print("Summary:")
    print(f"  Successfully created: {success_count}")
    print(f"  Failed: {failure_count}")


def create_recurring_event(api_url: str, auth: tuple, event_data: Dict[str, Any], verbose: bool = False) -> Optional[int]:
    """
    Create a single recurring event
    
    Args:
        api_url: API endpoint URL
        auth: Tuple of (username, password)
        event_data: Event data dictionary
        verbose: Enable verbose output
    
    Returns:
        Event ID on success, None on failure
    """
    # Prepare recurrence rules
    recurrence_rules = build_recurrence_rules(event_data)
    
    # Prepare event payload
    payload = {
        'title': event_data['title'],
        'description': event_data.get('description', ''),
        'status': 'publish',
        'start_date': f"{event_data['start_date']} {event_data['start_time']}",
        'end_date': f"{event_data['start_date']} {event_data['end_time']}",
        'all_day': False,
        'recurrence': recurrence_rules,
    }
    
    # Add optional fields
    if 'venue' in event_data:
        payload['venue'] = {'venue': event_data['venue']}
    
    if 'organizer' in event_data:
        payload['organizer'] = {'organizer': event_data['organizer']}
    
    if 'categories' in event_data:
        payload['categories'] = event_data['categories']
    
    if verbose:
        print(f"  Payload: {json.dumps(payload, indent=2)}")
    
    # Make API request
    try:
        response = requests.post(
            api_url,
            json=payload,
            auth=auth,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if verbose:
            print(f"  Response status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            return result.get('id')
        else:
            print(f"  HTTP Error {response.status_code}: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"  Request error: {e}")
        return None


def build_recurrence_rules(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build recurrence rules for the event
    
    Args:
        event_data: Event data dictionary
    
    Returns:
        Recurrence rules dictionary
    
    Raises:
        ValueError: If recurrence day format is invalid
    """
    pattern = event_data.get('recurrence_pattern', 'MONTHLY').upper()
    recurrence_day = event_data.get('recurrence_day', 'first Monday')
    
    # Parse recurrence day (e.g., "first Monday", "second Tuesday")
    match = re.match(
        r'^(first|second|third|fourth|last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$',
        recurrence_day,
        re.IGNORECASE
    )
    
    if not match:
        raise ValueError(f"Invalid recurrence_day format: {recurrence_day}")
    
    position = match.group(1).lower()
    day_of_week = match.group(2).upper()
    
    # Map position to number (1-5, -1 for last)
    position_map = {
        'first': 1,
        'second': 2,
        'third': 3,
        'fourth': 4,
        'last': -1,
    }
    
    position_num = position_map[position]
    
    # Build recurrence rule (RFC 5545 format adapted for The Events Calendar Pro)
    rules = {
        'rules': [
            {
                'type': 'Custom',
                'custom': {
                    'type': 'Monthly',
                    'interval': 1,
                    'same-time': 'yes',
                    'month': {
                        'same-day': 'no',
                        'number': position_num,
                        'day': day_of_week,
                    },
                },
            },
        ],
        'end-type': 'On',
        'end': event_data['end_date'],
    }
    
    return rules


if __name__ == '__main__':
    main()
