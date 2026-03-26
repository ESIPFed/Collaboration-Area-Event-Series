# Manual Setup Guide: Zoom Meetings and WordPress Events

This guide walks you through creating a Zoom meeting and a WordPress event by hand — using the same settings that the scripts use automatically. If you have ever used the script to set things up, this will feel familiar. If you haven't, no problem — just follow the steps in order.

---

## Part 1: Creating a Zoom Meeting by Hand

The script creates what Zoom calls a **recurring meeting with a fixed time** — a meeting that repeats on a schedule (weekly, monthly, etc.) and lets people register in advance. Here is how to do the same thing through the Zoom website.

### Step 1: Sign in to Zoom

1. Go to [zoom.us](https://zoom.us) and click **Sign In**.
2. Enter your email and password.
3. Once you are in, look at the left side of the screen and click **Meetings**.

---

### Step 2: Start a New Meeting

1. Click the **Schedule a Meeting** button (usually in the upper right area).
2. You will see a form with a lot of options. Don't worry — you only need to fill in the important ones.

---

### Step 3: Fill In the Basic Info

| Field | What to Enter |
|---|---|
| **Topic** | The name of your meeting (e.g., "Data Stewardship - 2026") |
| **Description** | A short summary of what the meeting is about (optional but helpful) |
| **When** | The date and time of the **first** occurrence |
| **Duration** | How long each meeting will last (e.g., 1 hour) |
| **Time Zone** | Pick the correct time zone for your group |

> **Tip:** The script uses 24-hour time (e.g., 14:00 means 2:00 PM). On the Zoom website, you can just pick AM or PM like normal.

---

### Step 4: Turn On Recurring Meeting

1. Check the box that says **Recurring meeting**.
2. A new section will appear with recurrence options.

**For a monthly meeting (most common for ESIP collaboration areas):**

| Setting | What to Choose |
|---|---|
| **Recurrence** | Monthly |
| **Repeat every** | 1 month |
| **On day** | Pick the day of the month (e.g., the 15th) — OR — pick a pattern like "the third Tuesday" |
| **End date** | Set a date when the series should stop, OR set a number of occurrences |

**For a weekly meeting:**

| Setting | What to Choose |
|---|---|
| **Recurrence** | Weekly |
| **Repeat every** | 1 week (or 2 for bi-weekly) |
| **Day(s)** | Check the day(s) of the week (e.g., Monday) |
| **End date** | Set an end date or number of occurrences |

---

### Step 5: Meeting Security Settings

These match what the script uses:

| Setting | What to Choose |
|---|---|
| **Passcode** | You can add one if you want, or leave it off |
| **Waiting Room** | Turn this **off** (the script turns it off by default) |
| **Require authentication** | Leave this **off** unless your group needs it |

---

### Step 6: Video and Audio Settings

| Setting | What to Choose |
|---|---|
| **Host video** | On |
| **Participant video** | On |
| **Audio** | Both (telephone and computer audio) |

---

### Step 7: Meeting Options

| Setting | What to Choose |
|---|---|
| **Allow participants to join before host** | Off |
| **Mute participants upon entry** | On |
| **Automatically record** | No recording (leave as "None") |

---

### Step 8: Turn On Registration

This is one of the most important settings. The script turns on registration for every meeting so that people get a personal join link when they sign up.

1. Scroll down and find the **Registration** section.
2. Check the box that says **Required**.
3. After you check it, two more options will appear:
   - **Approval**: Choose **Automatic** — this means anyone who registers gets approved right away without you having to do anything.
   - **Registration closes**: You can leave this blank to allow registration at any time.
4. For **Registration Type**, choose: **Attendees register once and can attend any of the occurrences** — this way people only have to sign up one time for the whole series.

> **Why does this matter?** When registration is on, Zoom gives each person their own unique join link. This lets Zoom track attendance and lets you send reminders automatically.

---

### Step 9: Save the Meeting

1. Click **Save** at the bottom of the page.
2. Zoom will show you the meeting details, including:
   - **Meeting ID** — a long number that identifies your meeting
   - **Join URL** — the link people use to join (after registering)
   - **Registration URL** — the link you share so people can sign up

> **Write down the Registration URL.** You will need it when setting up the WordPress event.

---

### Step 10: Copy Your Links

After saving, click on the meeting name to open its detail page. From here you can:

- Copy the **Registration Link** to share in emails, on your website, etc.
- View the list of people who have registered
- Edit the meeting if anything needs to change

---

## Part 2: Creating a WordPress Event by Hand (and Setting Up the Series)

The script creates a **single event** in WordPress — just one date and time, not a repeating series. This is because the WordPress plugin (The Events Calendar Pro) does not support creating recurring series through its API.

So the workflow is:
1. The script (or you, manually) creates one event.
2. You then go into WordPress and turn it into a recurring series by hand.

This section shows you how to do both steps.

---

### Step 1: Log In to WordPress

1. Go to your WordPress site and add `/wp-admin` to the end of the address (e.g., `https://yoursite.org/wp-admin`).
2. Enter your username and password.

---

### Step 2: Create a New Event

1. In the left menu, look for **Events** and click on it.
2. Click **Add New** to start a new event.

---

### Step 3: Fill In the Event Details

**Title**
- Type the name of your event at the top (e.g., "Data Stewardship Working Group").
- Do not include the year in the title if you plan to reuse the event series each year.

**Description**

The description must be entered as **HTML** using the code/text editor in WordPress (not the visual editor). The script uses a standard HTML block for every event. You should use the same block so that all events look the same on the website.

#### How to switch to the HTML editor in WordPress

In the WordPress event editor, look for a tab or button near the description area that says **Text** or **HTML** (as opposed to **Visual**). Click it to switch to the plain-text/code view. That is where you will paste the HTML below.

#### The HTML template

Copy the block below and paste it into the HTML editor. Then make the two changes listed underneath it.

```html
<div class="registration-container">
<h2 class="headline">CLUSTER NAME 2026 Registration</h2>
<p class="registration-note"><strong>ESIP meetings are open to all</strong> who wish to participate and contribute. To ensure a secure and collaborative environment for all attendees, <strong>registration is required</strong> for each meeting series. Once registered, you will have immediate access to the join links for all upcoming sessions.</p>
<a class="my-custom-button" href="REGISTRATION LINK FROM ZOOM">Click to register for the series</a>
<p class="footer-note">After registering, Zoom will email you a confirmation with a calendar invitation for the entire series. Use the <strong>"Add to Calendar"</strong> link to save the dates and your unique join link. <strong>Note:</strong> If a meeting time changes, you will receive an updated email. Because Zoom cannot auto-update your private calendar, please delete the old entry and use the new link to refresh your schedule.</p>
<p class="annual-reset-note"><strong>Note on Annual Registration:</strong> Your registration is valid for all meetings within the <strong>current calendar year</strong>. To maintain a secure environment and ensure our community lists are up-to-date, we perform an annual reset each January. You will be invited to re-register for your preferred Collaboration Areas at the start of the new year.</p>

</div>
```

#### What to change

There are exactly **two** things to update in the HTML above:

**1. Replace `CLUSTER NAME` with the name of your collaboration area.**

Find this line:
```html
<h2 class="headline">CLUSTER NAME 2026 Registration</h2>
```

Change `CLUSTER NAME` to the actual name. For example:
```html
<h2 class="headline">Data Stewardship 2026 Registration</h2>
```

**2. Replace `REGISTRATION LINK FROM ZOOM` with the registration URL you copied from Zoom.**

Find this line:
```html
<a class="my-custom-button" href="REGISTRATION LINK FROM ZOOM">Click to register for the series</a>
```

Paste your Zoom registration URL inside the quotes after `href=`. For example:
```html
<a class="my-custom-button" href="https://zoom.us/meeting/register/tJcpd-xxxxxxxxxxxxxx">Click to register for the series</a>
```

> **Do not change anything else in the HTML.** The class names (like `registration-container`, `my-custom-button`, `footer-note`) are used by the website's stylesheet to control how the description looks. Changing them will break the formatting.

#### What it looks like when rendered

Once saved, the description will display as:

- A heading with the collaboration area name and year
- A paragraph explaining that registration is required
- A button that takes people to the Zoom registration page
- A note about the calendar invitation and what to do if meeting times change
- A note explaining that registration resets each January

---

### Step 4: Set the Date and Time

Look for the **Event Date & Time** section (usually on the right side or below the description).

| Field | What to Enter |
|---|---|
| **Start Date** | The date of the first meeting in the series |
| **Start Time** | The time the meeting begins |
| **End Date** | Same as the start date (most meetings end the same day) |
| **End Time** | The time the meeting ends (add the duration to the start time) |
| **Time Zone** | Pick the correct time zone |

---

### Step 5: Add the Venue

1. Find the **Venue** section.
2. Type `Virtual - Zoom` as the venue name.
3. If a venue named "Virtual - Zoom" already exists in the system, select it from the dropdown.

---

### Step 6: Add the Organizer

1. Find the **Organizer** section.
2. Enter the name of the person or group running the meeting.
3. If the organizer already exists in the system, select them from the dropdown.

---

### Step 7: Add Categories

1. Look for the **Event Categories** section (usually on the right side).
2. Check (or add) the category **Collaboration Area**.
3. You can also add other relevant categories for your group.

---

### Step 8: Save as Draft First

Before publishing, save the event as a **Draft** so you can check everything before it goes live.

1. In the top right, find the **Publish** box.
2. Change the status to **Draft**.
3. Click **Save Draft**.

---

### Step 9: Turn It Into a Recurring Series

This is the step that the script cannot do for you — you must do it by hand in WordPress.

1. Look for the **Recurring Event** section. It is usually in the right sidebar or below the event details. It is part of The Events Calendar Pro plugin.

2. Check the box or toggle that says something like **Make this event recurring** or **Recurrence**.

3. A new set of options will appear. Fill them in to match your Zoom meeting schedule:

**For a monthly meeting:**

| Setting | What to Choose |
|---|---|
| **Recurrence** | Monthly |
| **Repeat every** | 1 month |
| **On** | The specific day (e.g., "the 15th") or a pattern (e.g., "the third Tuesday") — match this exactly to your Zoom meeting |
| **End** | Set an end date that matches your Zoom meeting's end date |

**For a weekly meeting:**

| Setting | What to Choose |
|---|---|
| **Recurrence** | Weekly |
| **Repeat every** | 1 week |
| **On** | The day of the week (e.g., Monday) |
| **End** | Set an end date that matches your Zoom meeting |

> **Important:** Make sure the recurrence pattern here matches what you set up in Zoom. If the Zoom meeting is on the third Tuesday of each month, this event should also be set to the third Tuesday of each month.

---

### Step 10: Publish the Event

1. Once you are happy with everything, go back to the **Publish** box.
2. Change the status from **Draft** to **Published** (or **Pending** if someone else needs to review it first).
3. Click **Publish** (or **Update** if you already saved it).

The event will now appear on your WordPress events calendar and repeat on the schedule you set.

---

## Quick Reference: Script Settings vs. Manual Settings

This table shows how the settings in the script map to what you do by hand.

### Zoom

| Script Setting | Manual Equivalent |
|---|---|
| `type: 8` (recurring fixed time) | Check "Recurring meeting" |
| `enable_registration: true` | Check "Registration: Required" |
| `approval_type: 0` (auto approve) | Set approval to "Automatic" |
| `registration_type: 1` (register once for all) | "Register once for any occurrence" |
| `waiting_room: false` | Turn off Waiting Room |
| `mute_upon_entry: true` | Check "Mute participants upon entry" |
| `join_before_host: false` | Leave "Join before host" unchecked |
| `auto_recording: none` | Set recording to "None" |
| `recurrence_type: monthly` | Set recurrence to Monthly |
| `recurrence_type: weekly` | Set recurrence to Weekly |
| `monthly_day: 15` | "On the 15th of every month" |
| `end_date: 2026-12-31` | Set end date in recurrence settings |

### WordPress

| Script Setting | Manual Equivalent |
|---|---|
| `title` | Event title at the top |
| `description` | Text in the main content area |
| `start_date` + `start_time` | Start Date and Start Time fields |
| `end_date` + `end_time` | End Date and End Time fields |
| `venue: "Virtual - Zoom"` | Venue field: "Virtual - Zoom" |
| `organizer` | Organizer field |
| `categories: ["Collaboration Area"]` | Event Categories checkbox |
| `status: "draft"` | Save as Draft before publishing |
| *(not in script — must be done manually)* | Recurring Event settings in Events Calendar Pro |

---

## Common Questions

**Why does the script only create one WordPress event instead of the whole series?**

The Events Calendar Pro plugin does not support creating a recurring series through its programming interface (API). The script can only create one event at a time this way. That is why you need to go into WordPress and set up the recurrence yourself after the script runs (or after you create the first event by hand).

**Do I need to create a new Zoom meeting every year?**

Yes. Zoom recurring meetings eventually expire. When a new program year starts, you will need to create a new Zoom meeting with the new dates. Once you have the new registration URL, you will also need to update the WordPress event description with the new link.

**What if the meeting time changes?**

In Zoom, you can edit the meeting from the Meetings page and update the time. In WordPress, you can edit the event and update the start and end time there too. Remember to update both places so they stay in sync.

**How do I find the registration URL after creating the Zoom meeting?**

Go to zoom.us, click **Meetings**, click on the name of your meeting, and look for the **Registration** section. The registration link will be listed there. You can also click **Copy** to copy it to your clipboard.
