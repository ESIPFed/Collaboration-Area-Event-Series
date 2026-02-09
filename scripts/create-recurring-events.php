<?php
/**
 * Create Recurring Events using The Events Calendar Pro API
 * 
 * This script creates recurring events in WordPress using The Events Calendar Pro REST API.
 * Each event in the series has a unique name and recurs monthly on a specific day pattern
 * (e.g., first Monday of each month).
 * 
 * Requirements:
 * - WordPress with The Events Calendar Pro plugin installed
 * - REST API enabled
 * - Application password or authentication credentials
 * 
 * Usage:
 *   php create-recurring-events.php --config=config.json
 * 
 * @package Collaboration-Area-Event-Series
 * @version 1.0.0
 */

// Parse command line arguments
$options = getopt('', ['config:', 'help']);

if (isset($options['help']) || !isset($options['config'])) {
    showHelp();
    exit(0);
}

$configFile = $options['config'];

if (!file_exists($configFile)) {
    echo "Error: Config file not found: $configFile\n";
    exit(1);
}

// Load configuration
$config = json_decode(file_get_contents($configFile), true);

if (json_last_error() !== JSON_ERROR_NONE) {
    echo "Error: Invalid JSON in config file: " . json_last_error_msg() . "\n";
    exit(1);
}

// Validate configuration
validateConfig($config);

// Create events
createRecurringEventSeries($config);

/**
 * Display help message
 */
function showHelp() {
    echo <<<HELP

Create Recurring Events for The Events Calendar Pro

Usage:
  php create-recurring-events.php --config=<config-file>
  php create-recurring-events.php --help

Options:
  --config    Path to JSON configuration file
  --help      Display this help message

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

HELP;
}

/**
 * Validate configuration structure
 * 
 * @param array $config Configuration array
 */
function validateConfig($config) {
    $required = ['wordpress_url', 'username', 'app_password', 'events'];
    
    foreach ($required as $field) {
        if (!isset($config[$field])) {
            echo "Error: Missing required field '$field' in config\n";
            exit(1);
        }
    }
    
    if (!is_array($config['events']) || empty($config['events'])) {
        echo "Error: 'events' must be a non-empty array\n";
        exit(1);
    }
    
    foreach ($config['events'] as $index => $event) {
        $eventRequired = ['title', 'start_date', 'end_date', 'start_time', 'end_time'];
        foreach ($eventRequired as $field) {
            if (!isset($event[$field])) {
                echo "Error: Event $index missing required field '$field'\n";
                exit(1);
            }
        }
    }
}

/**
 * Create recurring event series
 * 
 * @param array $config Configuration array
 */
function createRecurringEventSeries($config) {
    $wpUrl = rtrim($config['wordpress_url'], '/');
    $apiUrl = "$wpUrl/wp-json/tribe/events/v1/events";
    
    $auth = base64_encode($config['username'] . ':' . $config['app_password']);
    
    echo "Creating recurring event series...\n";
    echo "WordPress URL: $wpUrl\n";
    echo "Number of events to create: " . count($config['events']) . "\n\n";
    
    $successCount = 0;
    $failureCount = 0;
    
    foreach ($config['events'] as $index => $eventData) {
        echo "Processing event " . ($index + 1) . ": {$eventData['title']}\n";
        
        try {
            $eventId = createRecurringEvent($apiUrl, $auth, $eventData);
            if ($eventId) {
                echo "  ✓ Successfully created event ID: $eventId\n";
                $successCount++;
            } else {
                echo "  ✗ Failed to create event\n";
                $failureCount++;
            }
        } catch (Exception $e) {
            echo "  ✗ Error: " . $e->getMessage() . "\n";
            $failureCount++;
        }
        
        echo "\n";
        
        // Small delay to avoid overwhelming the server
        usleep(500000); // 0.5 seconds
    }
    
    echo "Summary:\n";
    echo "  Successfully created: $successCount\n";
    echo "  Failed: $failureCount\n";
}

/**
 * Create a single recurring event
 * 
 * @param string $apiUrl API endpoint URL
 * @param string $auth Base64 encoded authentication
 * @param array $eventData Event data
 * @return int|false Event ID on success, false on failure
 */
function createRecurringEvent($apiUrl, $auth, $eventData) {
    // Prepare recurrence rules
    $recurrenceRules = buildRecurrenceRules($eventData);
    
    // Prepare event payload
    $payload = [
        'title' => $eventData['title'],
        'description' => $eventData['description'] ?? '',
        'status' => 'publish',
        'start_date' => $eventData['start_date'] . ' ' . $eventData['start_time'],
        'end_date' => $eventData['start_date'] . ' ' . $eventData['end_time'],
        'all_day' => false,
        'recurrence' => $recurrenceRules,
    ];
    
    // Add optional fields
    if (isset($eventData['venue'])) {
        $payload['venue'] = ['venue' => $eventData['venue']];
    }
    
    if (isset($eventData['organizer'])) {
        $payload['organizer'] = ['organizer' => $eventData['organizer']];
    }
    
    if (isset($eventData['categories'])) {
        $payload['categories'] = $eventData['categories'];
    }
    
    // Make API request
    $ch = curl_init($apiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Basic ' . $auth,
        'Content-Type: application/json',
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode >= 200 && $httpCode < 300) {
        $result = json_decode($response, true);
        return $result['id'] ?? false;
    } else {
        echo "  HTTP Error $httpCode: $response\n";
        return false;
    }
}

/**
 * Build recurrence rules for the event
 * 
 * @param array $eventData Event data
 * @return array Recurrence rules
 */
function buildRecurrenceRules($eventData) {
    $pattern = strtoupper($eventData['recurrence_pattern'] ?? 'MONTHLY');
    $recurrenceDay = $eventData['recurrence_day'] ?? 'first Monday';
    
    // Parse recurrence day (e.g., "first Monday", "second Tuesday", "third Wednesday")
    preg_match('/^(first|second|third|fourth|last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$/i', 
               $recurrenceDay, $matches);
    
    if (!$matches) {
        throw new Exception("Invalid recurrence_day format: $recurrenceDay");
    }
    
    $position = strtolower($matches[1]);
    $dayOfWeek = strtoupper($matches[2]);
    
    // Map position to number (1-5, -1 for last)
    $positionMap = [
        'first' => 1,
        'second' => 2,
        'third' => 3,
        'fourth' => 4,
        'last' => -1,
    ];
    
    $positionNum = $positionMap[$position];
    
    // Build recurrence rule string (RFC 5545 format)
    $rules = [
        'rules' => [
            [
                'type' => 'Custom',
                'custom' => [
                    'type' => 'Monthly',
                    'interval' => 1,
                    'same-time' => 'yes',
                    'month' => [
                        'same-day' => 'no',
                        'number' => $positionNum,
                        'day' => $dayOfWeek,
                    ],
                ],
            ],
        ],
        'end-type' => 'On',
        'end-count' => null,
        'end' => $eventData['end_date'],
    ];
    
    return $rules;
}
